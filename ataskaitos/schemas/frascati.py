from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, computed_field, field_validator


class RDType(str, Enum):
    BASIC_RESEARCH = "basic_research"
    APPLIED_RESEARCH = "applied_research"
    EXPERIMENTAL_DEVELOPMENT = "experimental_development"
    NOT_RD = "not_rd"


class RDClassification(str, Enum):
    STRONG_RD = "strong_rd"  # 0.80-1.00
    MODERATE_RD = "moderate_rd"  # 0.65-0.79
    BORDERLINE = "borderline"  # 0.50-0.64
    WEAK_RD = "weak_rd"  # 0.30-0.49
    NOT_RD = "not_rd"  # 0.00-0.29


class NoveltyLevel(str, Enum):
    GROUNDBREAKING = "groundbreaking"
    SIGNIFICANT = "significant"
    INCREMENTAL = "incremental"
    MINOR = "minor"
    ADAPTATION = "adaptation"
    ROUTINE = "routine"


class UncertaintySource(str, Enum):
    SCIENTIFIC_TECHNICAL = "scientific_technical"  # Valid R&D
    TEAM_INEXPERIENCE = "team_inexperience"  # Not R&D
    MARKET_BUSINESS = "market_business"  # Not R&D
    PREDICTABLE = "predictable"  # Not R&D


class PersonnelLevel(str, Enum):
    PHD_RESEARCHERS = "phd_researchers"
    EXPERIENCED_ENGINEERS = "experienced_engineers"
    TECHNICAL_SPECIALISTS = "technical_specialists"
    GENERAL_STAFF = "general_staff"
    NOT_SPECIFIED = "not_specified"


# ═══════════════════════════════════════════════════════════════
# CORE CRITERIA MODELS
# ═══════════════════════════════════════════════════════════════


class NoveltyAssessment(BaseModel):
    """Frascati Criterion 1: Novel"""

    score: float = Field(ge=0.0, le=0.1, description="Novelty score (0.0-0.1)")
    level: NoveltyLevel = Field(description="Novelty classification")
    beyond_state_of_art: bool = Field(description="Exceeds current knowledge")
    evidence: str = Field(description="Specific evidence of novelty")
    knowledge_gap: str | None = Field(None, description="What knowledge gap is addressed")


class CreativityAssessment(BaseModel):
    """Frascati Criterion 2: Creative"""

    score: float = Field(ge=0.0, le=0.1, description="Creativity score (0.0-0.1)")
    non_obvious_approach: bool = Field(description="Requires creative problem-solving")
    new_methods_developed: bool = Field(description="Novel methodology created")
    evidence: str = Field(description="Specific creative elements")
    innovation_type: str | None = Field(None, description="Type of creative innovation")


class UncertaintyAssessment(BaseModel):
    """Frascati Criterion 3: Uncertain"""

    score: float = Field(ge=0.0, le=0.1, description="Uncertainty score (0.0-0.1)")
    outcome_unpredictable: bool = Field(description="Genuine unpredictability")
    uncertainty_source: UncertaintySource = Field(description="Source of uncertainty")
    failure_risk: Literal["high", "moderate", "low", "none"] = Field(description="Risk level")
    evidence: str = Field(description="Specific uncertainty factors")

    @field_validator("score")
    @classmethod
    def validate_uncertainty_score(cls, v, info):
        # If uncertainty source is not scientific/technical, score should be low
        if "uncertainty_source" in info.data:
            source = info.data["uncertainty_source"]
            if source != UncertaintySource.SCIENTIFIC_TECHNICAL and v > 0.05:
                raise ValueError("High uncertainty score only valid for scientific/technical uncertainty")
        return v


class SystematicAssessment(BaseModel):
    """Frascati Criterion 4: Systematic"""

    score: float = Field(ge=0.0, le=0.1, description="Systematic score (0.0-0.1)")
    has_hypothesis: bool = Field(description="Defined research questions/hypothesis")
    has_methodology: bool = Field(description="Planned methodology documented")
    has_budget: bool = Field(description="Resources formally allocated")
    evidence: str = Field(description="Evidence of systematic approach")


class TransferableAssessment(BaseModel):
    """Frascati Criterion 5: Transferable/Reproducible"""

    score: float = Field(ge=0.0, le=0.1, description="Transferable score (0.0-0.1)")
    documented: bool = Field(description="Results documented")
    reproducible: bool = Field(description="Process can be reproduced")
    communicable: bool = Field(description="Knowledge can be shared")
    evidence: str = Field(description="Documentation quality")


class ExclusionCheck(BaseModel):
    """Activities that disqualify or reduce R&D classification"""

    has_exclusions: bool = Field(description="Any exclusions present")
    routine_testing: bool = Field(False, description="Routine testing/QC")
    market_research: bool = Field(False, description="Market research/surveys")
    feasibility_study: bool = Field(False, description="Non-R&D feasibility study")
    production: bool = Field(False, description="Production/manufacturing")
    software_maintenance: bool = Field(False, description="Software maintenance")
    routine_data_collection: bool = Field(False, description="Routine data collection")
    implementation: bool = Field(False, description="Implementation of existing solutions")
    penalty: float = Field(ge=0.0, le=1.0, description="Total penalty applied")
    details: str = Field(description="Description of exclusions found")


class RDContentRatio(BaseModel):
    """Percentage of work that is actual R&D vs supporting activities"""

    rd_percentage: int = Field(ge=0, le=100, description="Estimated R&D content %")
    score: float = Field(ge=0.0, le=0.15, description="R&D content score (0.0-0.15)")
    primary_activity: Literal["pure_rd", "mostly_rd", "mixed", "mostly_routine", "routine"] = Field(
        description="Primary nature of activity"
    )
    explanation: str = Field(description="Breakdown of R&D vs non-R&D elements")


class InnovationVsRD(BaseModel):
    """Distinguish R&D (creates knowledge) from Innovation (applies knowledge)"""

    score: float = Field(ge=0.0, le=0.1, description="R&D vs Innovation score (0.0-0.1)")
    classification: Literal["creates_knowledge", "applies_knowledge", "mixed"] = Field(description="Primary objective")
    advances_knowledge: bool = Field(description="Advances state of knowledge")
    uses_knowledge: bool = Field(description="Uses existing knowledge")
    explanation: str = Field(description="Rationale for classification")


# ═══════════════════════════════════════════════════════════════
# PERSONNEL & DOCUMENTATION
# ═══════════════════════════════════════════════════════════════


class PersonnelAssessment(BaseModel):
    """Qualification of personnel performing R&D"""

    score: float = Field(ge=0.0, le=0.075, description="Personnel score (0.0-0.075)")
    level: PersonnelLevel = Field(description="Primary personnel qualification")
    has_researchers: bool = Field(description="Research-qualified personnel")
    evidence: str = Field(description="Personnel details")


class DocumentationAssessment(BaseModel):
    """R&D process documentation and rigor"""

    score: float = Field(ge=0.0, le=0.075, description="Documentation score (0.0-0.075)")
    has_objectives: bool = Field(description="Research objectives documented")
    has_methodology: bool = Field(description="Methodology/protocols defined")
    has_literature_review: bool = Field(description="Prior art/literature reviewed")
    tracks_outcomes: bool = Field(description="Expected vs actual tracked")
    evidence: str = Field(description="Documentation quality details")


class FrascatiEvaluation(BaseModel):
    """Complete Frascati R&D Evaluation"""

    # Part 1: Core Criteria (0.5 max)
    novelty: NoveltyAssessment
    creativity: CreativityAssessment
    uncertainty: UncertaintyAssessment
    systematic: SystematicAssessment
    transferable: TransferableAssessment

    # Part 2: Exclusions (penalty)
    exclusions: ExclusionCheck

    # Part 3: R&D Content Ratio (0.15 max)
    rd_content: RDContentRatio

    # Part 4: Innovation vs R&D (0.1 max)
    innovation_vs_rd: InnovationVsRD

    # Part 5: Personnel (0.075 max)
    personnel: PersonnelAssessment

    # Part 6: Documentation (0.075 max)
    documentation: DocumentationAssessment

    # Overall Assessment
    total_score: float = Field(ge=0.0, le=1.0, description="Total evaluation score")
    classification: RDClassification = Field(description="Overall R&D classification")
    qualifies_as_rd: bool = Field(description="Passes R&D threshold (≥0.65)")
    rd_type: RDType = Field(description="Type of R&D if qualified")

    # Analysis & Recommendations
    strongest_criteria: list[str] = Field(description="Top 3 strongest criteria")
    weakest_criteria: list[str] = Field(description="Top 3 weakest criteria")
    missing_information: list[str] = Field(description="Gaps in provided information")
    recommendations: list[str] = Field(description="How to strengthen R&D qualification")
    overall_summary: str = Field(description="Executive summary of evaluation")

    @computed_field
    @property
    def core_criteria_score(self) -> float:
        """Sum of all 5 core criteria"""
        return sum(
            [
                self.novelty.score,
                self.creativity.score,
                self.uncertainty.score,
                self.systematic.score,
                self.transferable.score,
            ]
        )

    @computed_field
    @property
    def meets_all_criteria(self) -> bool:
        """All 5 core criteria must be present for R&D"""
        return all(
            [
                self.novelty.beyond_state_of_art,
                self.creativity.non_obvious_approach,
                self.uncertainty.outcome_unpredictable,
                self.systematic.has_methodology,
                self.transferable.reproducible,
            ]
        )

    @field_validator("total_score")
    @classmethod
    def validate_total_score(cls, v, info):
        """Verify total score matches component scores"""
        if all(
            k in info.data
            for k in [
                "novelty",
                "creativity",
                "uncertainty",
                "systematic",
                "transferable",
                "exclusions",
                "rd_content",
                "innovation_vs_rd",
                "personnel",
                "documentation",
            ]
        ):
            expected = (
                info.data["novelty"].score
                + info.data["creativity"].score
                + info.data["uncertainty"].score
                + info.data["systematic"].score
                + info.data["transferable"].score
                + info.data["rd_content"].score
                + info.data["innovation_vs_rd"].score
                + info.data["personnel"].score
                + info.data["documentation"].score
                - info.data["exclusions"].penalty
            )
            if abs(v - expected) > 0.01:  # Allow small floating point errors
                raise ValueError(f"Total score {v} doesn't match sum of components {expected}")
        return v

    @field_validator("qualifies_as_rd")
    @classmethod
    def validate_qualification(cls, v, info):
        """Qualification must match score threshold"""
        if "total_score" in info.data:
            should_qualify = info.data["total_score"] >= 0.65
            if v != should_qualify:
                raise ValueError(f"Qualification {v} doesn't match score threshold")
        return v

    @field_validator("classification")
    @classmethod
    def validate_classification(cls, v, info):
        """Classification must match score ranges"""
        if "total_score" in info.data:
            score = info.data["total_score"]
            if score >= 0.80 and v != RDClassification.STRONG_RD:
                raise ValueError("Score ≥0.80 must be STRONG_RD")
            elif 0.65 <= score < 0.80 and v != RDClassification.MODERATE_RD:
                raise ValueError("Score 0.65-0.79 must be MODERATE_RD")
            elif 0.50 <= score < 0.65 and v != RDClassification.BORDERLINE:
                raise ValueError("Score 0.50-0.64 must be BORDERLINE")
            elif 0.30 <= score < 0.50 and v != RDClassification.WEAK_RD:
                raise ValueError("Score 0.30-0.49 must be WEAK_RD")
            elif score < 0.30 and v != RDClassification.NOT_RD:
                raise ValueError("Score <0.30 must be NOT_RD")
        return v
