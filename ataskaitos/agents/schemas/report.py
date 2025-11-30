"""Report evaluation schemas."""

from pydantic import BaseModel, Field, computed_field


class SimpleReportEvaluation(BaseModel):
    """Simple R&D report evaluation."""

    overall_score: float = Field(ge=0.0, le=1.0, description="Overall R&D qualification score (0.0-1.0)")
    qualifies_as_rd: bool = Field(description="Does this qualify as R&D per Frascati Manual?")
    novelty_score: float = Field(ge=0.0, le=1.0, description="Novelty/innovation level (0.0-1.0)")
    systematic_score: float = Field(ge=0.0, le=1.0, description="Systematic planning and organization (0.0-1.0)")
    uncertainty_score: float = Field(ge=0.0, le=1.0, description="Scientific/technical uncertainty (0.0-1.0)")
    summary: str = Field(description="Brief summary of the evaluation (2-3 sentences)")
    strengths: list[str] = Field(description="2-3 key strengths of the R&D activity")
    weaknesses: list[str] = Field(description="2-3 areas for improvement")


# Sub-score models for detailed evaluation
class SystematicSubScores(BaseModel):
    """Sub-scores for systematic criterion."""

    hypothesis_score: float = Field(ge=0.0, le=1.0, description="Defined hypothesis/research questions")
    methodology_score: float = Field(ge=0.0, le=1.0, description="Planned methodology documented")
    resources_score: float = Field(ge=0.0, le=1.0, description="Budget/timeline/resources allocated")


class TransferabilitySubScores(BaseModel):
    """Sub-scores for transferability criterion."""

    documentation_score: float = Field(ge=0.0, le=1.0, description="Results documented reproducibly")
    reproducibility_score: float = Field(ge=0.0, le=1.0, description="Process reproducible by qualified researchers")
    communication_score: float = Field(
        ge=0.0, le=1.0, description="Knowledge communicable (publications/patents/reports)"
    )


class ReportBreakdown(BaseModel):
    """Initial breakdown and structure analysis of the report."""

    main_activities: list[str] = Field(description="List of main activities/tasks described in the report")
    objectives: list[str] = Field(description="Stated objectives or research questions")
    methodology_summary: str = Field(description="Summary of methodology/approach used")
    key_results: list[str] = Field(description="Key results or outcomes mentioned")
    personnel_mentioned: bool = Field(description="Are qualified personnel/researchers mentioned?")
    timeline_mentioned: bool = Field(description="Is timeline or project planning mentioned?")


class FrascatiClassifierEvaluation(BaseModel):
    """
    Focused R&D classification agent based on expert decision patterns.

    Designed to distinguish genuine R&D from high-quality engineering/testing work
    by focusing on knowledge creation vs application.
    """

    # PART 1: Knowledge Creation Assessment
    knowledge_creation_score: float = Field(
        ge=0.0, le=1.0, description="Does this CREATE new knowledge or APPLY existing knowledge?"
    )
    knowledge_creation_type: str = Field(
        description="'Discovers new relationships/principles', 'Characterizes known materials', 'Applies standard methods', 'Validates existing knowledge'"
    )
    knowledge_creation_evidence: str = Field(
        description="Specific evidence: What new knowledge is created vs what is merely applied?"
    )

    # PART 2: Result Generalizability
    generalizability_score: float = Field(
        ge=0.0, le=1.0, description="Are results GENERALIZABLE beyond this case or CASE-SPECIFIC?"
    )
    generalizability_assessment: str = Field(
        description="'Field-advancing insights', 'Validated model/method', 'Optimal parameters found', 'Case-specific characterization'"
    )
    generalizability_evidence: str = Field(
        description="Can other researchers use these findings, or are they specific to this product/application?"
    )

    # PART 3: Purpose Classification
    primary_purpose: str = Field(
        description="'Hypothesis-driven investigation', 'Feasibility testing', 'Material characterization', 'Product optimization', 'Routine testing'"
    )
    purpose_indicators: list[str] = Field(description="Key phrases/activities indicating the true purpose")

    # PART 4: Methodology Nature
    methodology_nature: str = Field(
        description="'Develops theoretical framework', 'Systematic exploration', 'Standard testing protocols', 'Software-based optimization'"
    )
    uses_standard_methods: bool = Field(description="Are standard/off-the-shelf methods used without modification?")
    methodology_evidence: str = Field(description="What methods are used and are they novel or routine?")

    # PART 5: Frascati Exclusion Check
    identified_exclusions: list[str] = Field(
        description="Frascati exclusions detected: 'Routine testing', 'Feasibility study', 'Material characterization', 'Product development', 'Engineering optimization', 'None'"
    )
    exclusion_severity: str = Field(
        description="'Disqualifying' (primary activity is excluded), 'Partial' (mixed R&D and excluded), 'Minor' (small excluded component), 'None' (no exclusions)"
    )
    exclusion_rationale: str = Field(description="Why these exclusions apply or don't apply")

    # PART 6: Results Nature Analysis
    results_type: str = Field(
        description="'Discovers correlation/relationship', 'Identifies critical technique/threshold', 'Measures material properties', 'Validates performance', 'Proves feasibility'"
    )
    results_evidence: str = Field(
        description="What was actually achieved - discovery vs characterization vs validation?"
    )

    # PART 7: Novelty Type
    novelty_type: str = Field(
        description="'Novel understanding/method', 'Novel application', 'Novel combination', 'Incremental improvement', 'Routine work'"
    )
    novelty_scope: str = Field(description="'Field-level novelty', 'Company-level novelty', 'Case-specific novelty'")

    # PART 8: Final Classification
    qualifies_as_rd: bool = Field(description="Does this qualify as R&D per Frascati Manual?")
    confidence: str = Field(description="'High', 'Medium', 'Low'")
    classification_rationale: str = Field(
        description="Clear explanation of why this qualifies or doesn't qualify, referencing specific Frascati criteria and expert patterns"
    )

    # PART 9: Summary
    one_sentence_summary: str = Field(
        description="One sentence: Is this R&D creating knowledge, or engineering/testing applying knowledge?"
    )
    key_discriminators: list[str] = Field(
        min_length=2, max_length=4, description="2-4 key factors that most strongly indicate R&D or non-R&D"
    )

    @computed_field
    @property
    def overall_score(self) -> float:
        """
        Computed overall R&D qualification score (0.0-1.0).

        Formula:
        - Base: 60% knowledge_creation + 40% generalizability
        - Penalty for exclusions:
          * Disqualifying: -0.3
          * Partial: -0.1
          * Minor/None: 0
        - Clamped to [0.0, 1.0]
        """
        base_score = 0.6 * self.knowledge_creation_score + 0.4 * self.generalizability_score

        # Apply exclusion penalty
        exclusion_penalty = {
            "Disqualifying": 0.3,
            "Partial": 0.1,
            "Minor": 0.0,
            "None": 0.0,
        }.get(self.exclusion_severity, 0.0)

        final_score = base_score - exclusion_penalty

        # Clamp to valid range
        return max(0.0, min(1.0, final_score))


class DetailedReportEvaluation(BaseModel):
    """Comprehensive R&D report evaluation with full Frascati analysis."""

    # PART 0: Report Analysis & Breakdown
    report_breakdown: ReportBreakdown = Field(description="Initial breakdown of report structure and content")

    # PART 1: Core Frascati Criteria (5 dimensions) - Primary evaluation
    # 1.1 Novelty
    novelty_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Novelty: Does activity create new knowledge beyond state-of-the-art? (Frascati §2.5-2.7)",
    )
    novelty_evidence: str = Field(description="Specific evidence from document supporting novelty score")

    # 1.2 Creativity
    creativity_score: float = Field(
        ge=0.0, le=1.0, description="Creativity: Non-obvious concepts, methodologies, or approaches (Frascati §2.7)"
    )
    creativity_evidence: str = Field(description="Specific evidence from document supporting creativity score")

    # 1.3 Uncertainty
    uncertainty_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Uncertainty: Scientific/technical unknowns with unpredictable outcomes (Frascati §2.7, §2.24-2.27)",
    )
    uncertainty_evidence: str = Field(description="Specific evidence from document supporting uncertainty score")
    uncertainty_type: str = Field(
        description="Type of uncertainty: 'Scientific/Technical (R&D)' or 'Non-R&D (team inexperience, market risk, etc.)'"
    )

    # 1.4 Systematic
    systematic_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Systematic: Formally planned with defined objectives and methodology (Frascati §2.7)",
    )
    systematic_subscores: SystematicSubScores = Field(description="Breakdown of systematic criterion components")
    systematic_evidence: str = Field(description="Specific evidence from document supporting systematic score")

    # 1.5 Transferability/Reproducibility
    transferability_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Transferability: Results produce codified, reproducible knowledge (Frascati §2.5, §2.7)",
    )
    transferability_subscores: TransferabilitySubScores = Field(
        description="Breakdown of transferability criterion components"
    )
    transferability_evidence: str = Field(
        description="Specific evidence from document supporting transferability score"
    )

    # PART 2: Additional Dimensions
    # 2.1 R&D Content Ratio
    rd_content_ratio: float = Field(
        ge=0.0,
        le=1.0,
        description="Estimated percentage of activity that is genuine R&D (vs supporting/ancillary activities)",
    )
    rd_content_breakdown: str = Field(description="Breakdown of R&D vs non-R&D activities identified in the report")

    # 2.2 R&D vs Innovation Classification
    rd_vs_innovation: str = Field(
        description="Classification: 'R&D (Creates new knowledge)' or 'Innovation (Applies existing knowledge)' or 'Mixed'"
    )
    rd_vs_innovation_rationale: str = Field(description="Rationale for R&D vs Innovation classification")

    # 2.3 Exclusions
    identified_exclusions: list[str] = Field(
        description="Frascati exclusions identified (§2.64-2.91): routine testing, market research, feasibility studies without R&D, production, maintenance, etc."
    )
    exclusion_impact: str = Field(
        description="Impact of identified exclusions on overall R&D qualification (High/Medium/Low/None)"
    )

    # 2.4 Personnel Qualification
    personnel_qualification: str = Field(
        description="Assessment of personnel qualifications per Frascati Chapter 5 (§5.2-5.19)"
    )
    personnel_evidence: str = Field(description="Evidence of qualified researchers/technicians involvement")

    # 2.5 Documentation Quality
    documentation_quality_score: float = Field(
        ge=0.0, le=1.0, description="Quality of documentation demonstrating systematic R&D approach"
    )
    documentation_assessment: str = Field(description="Assessment of documentation rigor and completeness")

    # PART 3: Overall Assessment
    overall_score: float = Field(ge=0.0, le=1.0, description="Overall R&D qualification score (0.0-1.0)")
    qualifies_as_rd: bool = Field(description="Does this qualify as R&D per Frascati Manual?")
    qualification_confidence: str = Field(
        description="Confidence in qualification: 'Strong', 'Moderate', 'Borderline', 'Weak'"
    )
    rd_type: str | None = Field(
        description="Type of R&D if qualified: 'Basic Research', 'Applied Research', 'Experimental Development', or None"
    )

    # PART 4: Qualitative Analysis
    summary: str = Field(description="Comprehensive evaluation summary (4-5 sentences covering key findings)")
    strengths: list[str] = Field(
        min_length=2, max_length=5, description="2-5 key strengths of the R&D activity with specific examples"
    )
    weaknesses: list[str] = Field(
        min_length=2, max_length=5, description="2-5 key weaknesses or concerns with specific examples"
    )
    gaps_identified: list[str] = Field(
        description="Specific missing information or weak evidence areas that should be addressed"
    )
    recommendations: list[str] = Field(
        description="Actionable recommendations to strengthen R&D qualification and documentation"
    )
