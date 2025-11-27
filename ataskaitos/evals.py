"""
Frascati Manual R&D Evaluation System for Lithuanian Research Council

This module implements evaluators for determining whether activities qualify as R&D
according to the OECD Frascati Manual 2015 standard. Used by the Lithuanian Research
Council to assess R&D project applications.

KEY FINDINGS FROM EVALUATION ANALYSIS
=====================================

The Lithuanian Research Council rejects documents that are "engineering optimization/
consulting services" rather than "R&D creating generalizable knowledge", even when
they appear to meet basic Frascati criteria on surface.

CRITICAL DISTINCTION (Frascati Manual §2.28-2.35):
--------------------------------------------------
❌ REJECTED (Engineering Services):
   - Project-specific optimization for particular client/application
   - Results like: "Using 15% dolomite with THIS concrete mix..."
   - Findings limited to tested materials/conditions
   - Applies existing knowledge to solve specific problem
   - Example: "Replace BMW stabilizer with 20mm bar to reduce understeer"

✅ ACCEPTED (True R&D):
   - Creates generalizable principles, methods, or relationships
   - Results like: "Ratio X systematically affects property Y..."
   - Findings applicable to different contexts/materials
   - Advances scientific/technical understanding of phenomena
   - Example: "Polyurethane ratio 100/65 provides 3x greater flexibility..."

ADDITIONAL RED FLAGS FOR NON-R&D:
---------------------------------
1. Explicit "MTEP veikla" self-justification sections claiming R&D status
2. Conclusions recommend specific product changes rather than knowledge contribution
3. Client-commissioned work optimizing specific system
4. Results heavily qualified as "for this composition/configuration"
5. Missing literature contribution or field advancement discussion

EVALUATOR DESIGN:
----------------
This module implements 10 evaluators with continuous 0.00-1.00 scoring:
1. short_evaluator - Quick 3-criteria R&D check
2. combined_score - Holistic 5-criteria Frascati assessment
3. novelty_score - Advancement beyond state-of-the-art
4. creativity_score - Non-obvious approaches and methods
5. uncertainty_score - Scientific/technical unpredictability
6. systematic_score - Planned and organized approach
7. transferable_score - Codified and reproducible knowledge
8. generalizability_score - ⚠️ CRITICAL: Generalizable knowledge vs project-specific
9. rd_vs_innovation_boundary - ⚠️ CRITICAL: Creates vs applies knowledge
10. comprehensive_rd_score - Full detailed Frascati evaluation

The two CRITICAL evaluators (8-9) are essential for catching engineering services that
superficially appear to meet basic R&D criteria but don't create transferable knowledge.

RECOMMENDED USAGE:
-----------------
Primary decision criteria should weight:
- generalizability_score (0.00-0.39 = likely NOT R&D)
- rd_vs_innovation_boundary (0.00-0.39 = likely NOT R&D)
- combined_score (overall Frascati compliance)

A document scoring HIGH on novelty/systematic/transferable but LOW on generalizability
is likely engineering services, NOT R&D.
"""

from dataclasses import dataclass
from typing import Any

from pydantic_evals import Dataset
from pydantic_evals.evaluators import LLMJudge
from pydantic_evals.evaluators.llm_as_a_judge import set_default_judge_model

from combine_results import combine_evaluation_results

DEFAULT_JUDGE_MODEL = "gemini-2.5-pro"
set_default_judge_model(DEFAULT_JUDGE_MODEL)


@dataclass
class RDActivity:
    """R&D activity description for Frascati Manual evaluation."""

    description: str


# Define evaluators separately for reuse
evaluators = [
    # 1. Basic Frascati R&D check
    LLMJudge(
        rubric="""
            Evaluate according to Frascati Manual definition of R&D using a continuous scale from 0.00 to 1.00:

            Consider three core criteria:
            1. NOVELTY: Does it aim to create NEW knowledge (not just apply existing)?
            2. UNCERTAINTY: Does it have UNCERTAIN outcomes (not predictable with current knowledge)?
            3. SYSTEMATIC: Is it SYSTEMATIC (planned and documented)?

            Provide a score from 0.00 to 1.00 (two decimal places) that reflects how well the activity satisfies these criteria:
            - Score close to 1.00: Activity strongly demonstrates all three criteria with clear evidence
            - Score around 0.70-0.90: Activity demonstrates most criteria well with some gaps
            - Score around 0.40-0.70: Activity shows some R&D characteristics but with notable limitations
            - Score below 0.40: Activity lacks several key R&D characteristics

            Consider the strength of evidence and degree to which each criterion is satisfied.
            Cite specific evidence from the activity description.
            """,
        include_input=False,
        score={"evaluation_name": "short_evaluator", "include_reason": True},
    ),
    # 2. All Frascati criteria combined
    LLMJudge(
        rubric="""
            Evaluate against all 5 core Frascati Manual criteria for R&D using a continuous scale from 0.00 to 1.00:

            Consider these five criteria holistically:
            1. NOVEL: Activity aims to advance beyond current state-of-the-art or knowledge frontier
            2. CREATIVE: Uses non-obvious concepts, methodologies, or approaches
            3. UNCERTAIN: Outcome cannot be determined in advance using existing knowledge
            4. SYSTEMATIC: Planned, budgeted, and documented in advance
            5. TRANSFERABLE: Results can be codified, documented, and reproduced by others

            Provide a score from 0.00 to 1.00 (two decimal places) that reflects the overall strength across all criteria:
            - Score 0.80-1.00: Strong R&D - clearly qualifies per Frascati Manual (most/all criteria strongly satisfied)
            - Score 0.65-0.79: Moderate R&D - likely qualifies with good evidence for most criteria
            - Score 0.50-0.64: Borderline - R&D elements present but some criteria weakly satisfied
            - Score 0.30-0.49: Weak - primarily innovation/application, limited R&D characteristics
            - Score 0.00-0.29: Not R&D - routine work or insufficient evidence of R&D criteria

            Assess each criterion's strength and provide an overall score reflecting the combined evidence.
            Provide specific evidence for your assessment from the activity description.
            """,
        include_input=False,
        score={"evaluation_name": "combined_score", "include_reason": True},
    ),
    # 3-7. Individual Frascati criteria
    LLMJudge(
        rubric="""
            NOVELTY according to Frascati Manual - does activity advance knowledge/technology beyond current state-of-the-art?

            Provide a continuous score from 0.00 to 1.00 (two decimal places) reflecting the degree of novelty:

            Consider:
            - How significantly does this advance beyond existing knowledge/methods?
            - Is it groundbreaking, incremental, or routine application?
            - What is the gap between current state-of-the-art and this work?

            Higher scores (0.80-1.00): Groundbreaking or highly significant advancement in the field
            Moderate scores (0.50-0.79): Notable advancement or creative adaptation beyond existing approaches
            Lower scores (0.20-0.49): Minor improvements or adaptation of known methods
            Minimal scores (0.00-0.19): Routine application of established knowledge

            Evidence required: Cite what existing knowledge/methods are being advanced beyond and the degree of advancement.
            """,
        include_input=False,
        score={"evaluation_name": "novelty_score", "include_reason": True},
    ),
    LLMJudge(
        rubric="""
            CREATIVITY according to Frascati Manual - does activity use non-obvious concepts, approaches, or methodologies?

            Provide a continuous score from 0.00 to 1.00 (two decimal places) reflecting the degree of creativity:

            Consider:
            - How novel or non-obvious are the approaches/methodologies used?
            - Does it require creative problem-solving or innovative thinking?
            - Is it a new methodology, novel combination, or standard application?

            Higher scores (0.80-1.00): Entirely new methodology invented or highly innovative approaches developed
            Moderate scores (0.50-0.79): Novel combinations or creative adaptations requiring significant problem-solving
            Lower scores (0.20-0.49): Some creative elements mixed with mostly standard approaches
            Minimal scores (0.00-0.19): Straightforward application of standard methods

            Evidence required: Describe what creative problem-solving or non-obvious thinking was required.
            """,
        include_input=False,
        score={"evaluation_name": "creativity_score", "include_reason": True},
    ),
    LLMJudge(
        rubric="""
            UNCERTAINTY according to Frascati Manual - is the outcome genuinely unpredictable using current knowledge?

            Provide a continuous score from 0.00 to 1.00 (two decimal places) reflecting the degree of R&D uncertainty:

            CRITICAL: Only scientific/technical uncertainty qualifies - distinguish from other types:

            R&D uncertainty (score appropriately based on degree):
            - Higher scores (0.80-1.00): Fundamental unknowns in science/technology; multiple failure paths despite expertise
            - Moderate scores (0.50-0.79): Significant technical risk or unpredictability in how to achieve result
            - Lower scores (0.20-0.49): Some technical uncertainty but largely predictable with current knowledge
            - Minimal scores (0.00-0.19): Outcome mostly predictable using existing knowledge

            NOT R&D uncertainty (always score 0.00):
            - Team inexperience or learning curve
            - Market/business/commercial risk
            - Implementation challenges with known solutions
            - Resource or timing uncertainty

            Evidence required: Specify what scientific/technical unknowns exist and assess the degree of unpredictability.
            """,
        include_input=False,
        score={"evaluation_name": "uncertainty_score", "include_reason": True},
    ),
    LLMJudge(
        rubric="""
            SYSTEMATIC according to Frascati Manual - is the activity formally organized with clear planning?

            Provide a continuous score from 0.00 to 1.00 (two decimal places) reflecting the degree of systematic organization:

            Consider the presence and quality of:
            - Defined hypothesis, research questions, or clear objectives
            - Planned methodology and documented procedures
            - Budget, timeline, and resource allocation

            Higher scores (0.80-1.00): Comprehensive systematic planning with all elements well-documented
            Moderate scores (0.50-0.79): Good planning with most elements present and reasonably detailed
            Lower scores (0.20-0.49): Some planning evident but lacks detail or missing key elements
            Minimal scores (0.00-0.19): Little to no systematic planning evident (ad-hoc work)

            Assess not just presence but also the quality and completeness of systematic organization.
            Evidence required: Cite specific mentions of planning, methodology, or resource allocation.
            """,
        include_input=False,
        score={"evaluation_name": "systematic_score", "include_reason": True},
    ),
    LLMJudge(
        rubric="""
            TRANSFERABLE/REPRODUCIBLE according to Frascati Manual - can knowledge be codified and reproduced?

            Provide a continuous score from 0.00 to 1.00 (two decimal places) reflecting the degree of transferability:

            Consider the presence and quality of:
            - Results documented in reproducible format
            - Process/methodology that can be followed by other qualified researchers
            - Knowledge communicable through publications, patents, or reports

            Higher scores (0.80-1.00): Excellent documentation with comprehensive reproducible methods and clear knowledge transfer
            Moderate scores (0.50-0.79): Good documentation with most elements present and transferable
            Lower scores (0.20-0.49): Some documentation but lacks detail or completeness for full reproducibility
            Minimal scores (0.00-0.19): Little to no evidence of documentation or reproducibility

            Assess not just presence but also the quality and completeness of documentation and transferability.
            Evidence required: Cite how results will be/were documented and made reproducible.
            """,
        include_input=False,
        score={"evaluation_name": "transferable_score", "include_reason": True},
    ),
    # 8. CRITICAL: Generalizability vs Project-Specificity
    LLMJudge(
        rubric="""
            GENERALIZABILITY - Does this create generalizable knowledge or solve a specific problem?

            CRITICAL DISTINCTION per Frascati Manual §2.28-2.35:
            This evaluator distinguishes TRUE R&D from engineering services/consulting.

            Provide a continuous score from 0.00 to 1.00 (two decimal places):

            HIGH SCORES (0.80-1.00) - GENERALIZABLE R&D:
            - Creates principles, relationships, or methods applicable to MANY contexts
            - Results stated as: "Ratio X affects property Y..." or "Method Z enables..."
            - Findings advance field understanding beyond the specific case
            - Conclusions discuss theoretical/scientific implications
            - Example: "Polyurethane 100/65 ratio provides 3x flexibility compared to 100/85"
            - Can be applied to different materials, products, or situations

            MODERATE SCORES (0.40-0.79) - SOME GENERALIZABILITY:
            - Mix of general principles and specific recommendations
            - Some findings transferable, others context-specific
            - Partial contribution to broader knowledge

            LOW SCORES (0.00-0.39) - PROJECT-SPECIFIC ENGINEERING:
            - Optimizes/solves problem for ONE specific client/product/application
            - Results stated as: "For THIS mix..." or "This BMW needs..."
            - Conclusions recommend specific product changes (e.g., "use 20mm stabilizer bar")
            - Findings heavily qualified: "with this composition", "for this vehicle"
            - Missing discussion of broader applicability or field contribution
            - Applies existing knowledge to solve client's specific problem

            RED FLAGS for non-R&D (should score LOW):
            - Client-commissioned optimization of specific system
            - Conclusions focus on "what to do" for this case, not "what we learned"
            - Results don't establish relationships or advance understanding
            - Explicit "MTEP veikla" self-justification sections

            Evidence required: Cite specific conclusions and assess their generalizability.
            """,
        include_input=False,
        score={"evaluation_name": "generalizability_score", "include_reason": True},
    ),
    # 9. CRITICAL: R&D vs Innovation/Engineering Boundary
    LLMJudge(
        rubric="""
            R&D vs INNOVATION BOUNDARY - Does it CREATE or APPLY knowledge?

            CRITICAL per Frascati Manual §2.28-2.35:
            The fundamental distinction between R&D and innovation/engineering services.

            Provide a continuous score from 0.00 to 1.00 (two decimal places):

            PRIMARY OBJECTIVE ASSESSMENT:

            HIGH SCORES (0.80-1.00) - CREATES NEW KNOWLEDGE (R&D):
            - Discovers new phenomena, principles, or relationships
            - Develops new methods, techniques, or theoretical frameworks
            - Establishes systematic understanding of how/why things work
            - Advances scientific or technical knowledge frontier
            - Example: "We discovered that parameter X influences outcome Y through mechanism Z"
            - Focus on understanding and knowledge creation

            MODERATE SCORES (0.40-0.79) - MIXED:
            - Some knowledge creation mixed with application
            - Validates or extends existing knowledge in new contexts
            - Incremental contributions to understanding

            LOW SCORES (0.00-0.39) - APPLIES EXISTING KNOWLEDGE (NOT R&D):
            - Uses well-established methods to solve specific problem
            - Optimizes, adapts, or configures known solutions
            - Engineering troubleshooting or technical consulting
            - Example: "We applied method X to achieve better performance for client Y"
            - Focus on problem-solving using existing knowledge
            - Even if systematic and documented, it's application not research

            KEY QUESTIONS:
            1. What NEW knowledge was created that didn't exist before?
            2. Can you point to specific discoveries, principles, or relationships established?
            3. Does this advance understanding, or apply existing understanding?
            4. Would other researchers cite this for its knowledge contribution?

            IMPORTANT: An activity can be systematic, uncertain, novel application,
            and well-documented but STILL not be R&D if it doesn't CREATE new knowledge.

            Evidence required: Identify what specific new knowledge was created vs what was applied.
            """,
        include_input=False,
        score={"evaluation_name": "rd_vs_innovation_boundary", "include_reason": True},
    ),
    # 10. Comprehensive evaluation
    LLMJudge(
        rubric="""
    COMPREHENSIVE FRASCATI MANUAL R&D EVALUATION

    Based on OECD Frascati Manual 2015 - Standard for R&D Statistics

    Provide a continuous score from 0.00 to 1.00 (two decimal places) based on comprehensive analysis of the following dimensions:

    ═══════════════════════════════════════════════════════════════
    CORE FRASCATI CRITERIA (Primary evaluation focus)
    ═══════════════════════════════════════════════════════════════

    1. NOVELTY (Frascati §2.7): Does it aim to achieve NEW knowledge?
       Consider the degree of advancement from routine application to groundbreaking discovery

    2. CREATIVITY (Frascati §2.7): Does it use non-obvious creative concepts?
       Consider the degree of innovation from standard procedures to entirely new methodologies

    3. UNCERTAINTY (Frascati §2.7, §2.24-2.27): Is the outcome uncertain?
       CRITICAL: Only scientific/technical uncertainty counts (NOT team inexperience, market risk, or predictable implementation)
       Consider the degree of unpredictability in the scientific/technical outcome

    4. SYSTEMATIC (Frascati §2.7): Is it planned and organized?
       Consider quality and completeness of hypothesis, methodology, and resource planning

    5. TRANSFERABLE (Frascati §2.7, 2.11): Will it produce codified knowledge?
       Consider quality of documentation, reproducibility, and knowledge communication

    ═══════════════════════════════════════════════════════════════
    FRASCATI EXCLUSIONS - Check for disqualifying activities (§2.64-2.91)
    ═══════════════════════════════════════════════════════════════

    Activities that REDUCE the score significantly if they dominate:
    - Routine testing/quality control (§2.85)
    - Market research/consumer surveys (§2.90)
    - Feasibility studies without R&D (§2.89)
    - Production/pre-production (§2.84)
    - Software maintenance/routine debugging (§2.71)
    - Routine data collection (§2.88)
    - Legal/administrative work (§2.91)
    - Installation of existing systems (§2.86)

    If primary activity is excluded, score should be very low (<0.30)

    ═══════════════════════════════════════════════════════════════
    R&D CONTENT RATIO (Frascati §2.19-2.23)
    ═══════════════════════════════════════════════════════════════

    What percentage is ACTUAL R&D vs supporting/ancillary activities?
    Key question: Is this "R&D project with supporting work" or "routine project with some R&D elements"?
    Higher R&D content should result in higher scores

    ═══════════════════════════════════════════════════════════════
    R&D VS INNOVATION BOUNDARY (Frascati §2.28-2.35)
    ═══════════════════════════════════════════════════════════════

    CRITICAL distinction: Does it CREATE new knowledge (R&D) or APPLY existing knowledge (Innovation, NOT R&D)?
    - Creating fundamentally new knowledge → Higher scores
    - Applying existing knowledge innovatively → Lower scores
    - Implementing known solutions → Very low scores

    ═══════════════════════════════════════════════════════════════
    SUPPORTING FACTORS
    ═══════════════════════════════════════════════════════════════

    Personnel Qualification (Frascati §5.2-5.19):
    Consider if qualified researchers (PhD/Master's level) are leading the work

    Documentation & Rigor (Frascati §2.7, 2.11):
    Consider presence of research objectives, methodology, literature review, outcome tracking

    ═══════════════════════════════════════════════════════════════
    SCORING INTERPRETATION
    ═══════════════════════════════════════════════════════════════

    0.80-1.00: STRONG R&D - Clearly qualifies per Frascati (PASS)
    0.65-0.79: MODERATE R&D - Likely qualifies with proper documentation (PASS)
    0.50-0.64: BORDERLINE - R&D elements but mixed activities (Review needed)
    0.30-0.49: WEAK - Primarily innovation/application, not R&D (FAIL)
    0.00-0.29: NOT R&D - Routine work or excluded per Frascati (FAIL)

    ═══════════════════════════════════════════════════════════════
    R&D TYPE CLASSIFICATION (Frascati §2.5-2.9)
    ═══════════════════════════════════════════════════════════════

    If score ≥0.65 (PASS), classify as:
    - BASIC RESEARCH (§2.5): New knowledge with no particular application in view
    - APPLIED RESEARCH (§2.6): New knowledge directed towards specific practical aim
    - EXPERIMENTAL DEVELOPMENT (§2.7): Using existing knowledge to produce new/improved materials, products, processes

    ═══════════════════════════════════════════════════════════════
    REQUIRED EVALUATION OUTPUT
    ═══════════════════════════════════════════════════════════════

    Your response MUST include:
    1. Overall score (0.00-1.00) with justification
    2. Analysis of each core criterion strength/weakness
    3. Exclusions check - any disqualifying activities identified
    4. R&D content ratio estimate (what % is genuine R&D)
    5. R&D vs Innovation classification with reasoning
    6. Personnel and documentation assessment
    7. PASS/FAIL determination (≥0.65 = PASS)
    8. R&D type classification if PASS
    9. Key gaps or missing information
    10. Recommendations to strengthen R&D qualification
    11. Evidence citations from activity description
    12. Relevant Frascati Manual section references
    """,
        include_input=False,
        score={"evaluation_name": "comprehensive_rd_score", "include_reason": True},
        assertion={
            "evaluation_name": "comprehensive_rd_qualified",
            "include_reason": True,
        },
    ),
]

# Create dataset using the evaluators
dataset = Dataset(
    cases=[],
    evaluators=evaluators,
)


# with open(
#     "./docs/reference_documents/energus-ataskaita.md", "r", encoding="utf-8"
# ) as f:
#     doc_text = f.read()
#     Case(inputs=RDActivity(description=doc_text))


def do(data) -> RDActivity:
    return data


from pydantic_evals.reporting import EvaluationReport


def convert_results(result: EvaluationReport[Any, Any]):
    # Convert averages to JSON-serializable format
    averages = result.averages()
    averages_data = {}
    if averages:
        averages_data = {
            "scores": averages.scores,
            "metrics": averages.metrics,
            "task_duration": averages.task_duration,
            "total_duration": averages.total_duration,
        }

    results_data = {
        "name": result.name,
        "total_cases": len(result.cases),
        "total_failures": len(result.failures),
        "averages": averages_data,
        "cases": [
            {
                "name": case.name,
                # "input": case.inputs,
                "expected_output": case.expected_output
                if case.expected_output
                else None,
                # "actual_output": case.output if case.output else None,
                "scores": {
                    k: {"value": v.value, "reason": v.reason}
                    for k, v in case.scores.items()
                },
                "metrics": case.metrics,
                "task_duration": case.task_duration,
                "total_duration": case.total_duration,
            }
            for case in result.cases
        ],
        "failures": [
            {
                "name": failure.name,
                # "input": failure.inputs,
                "expected_output": failure.expected_output
                if failure.expected_output
                else None,
                "error_message": failure.error_message,
                "error_stacktrace": failure.error_stacktrace,
            }
            for failure in result.failures
        ],
    }
    return results_data


if __name__ == "__main__":
    from pathlib import Path
    import markitdown

    docs_dir = Path("./docs/reference_documents/")
    not_ok = list(docs_dir.glob("ataskaitos/not_ok/*.docx"))
    ok = list(docs_dir.glob("ataskaitos/ok/*.docx"))

    md_converter = markitdown.MarkItDown()
    ok_converted = []
    for pdf_file in not_ok:
        print(f"Processing: {pdf_file.name}")
        convertion_result = md_converter.convert(pdf_file)
        print(convertion_result.title)
        print(len(convertion_result.text_content))

        dataset.add_case(
            name=str(pdf_file),
            inputs=RDActivity(description=convertion_result.text_content),
            metadata={
                "source_file": str(pdf_file),
                "character_count": len(convertion_result.text_content),
                "expected_result": "NOT_OK",
            },
        )

    print("---- OK files ----")
    for ok_file in ok:
        print(f"Processing: {ok_file.name}")
        convertion_result = md_converter.convert(ok_file)
        print(convertion_result.title)
        print(len(convertion_result.text_content))

        dataset.add_case(
            name=str(ok_file),
            inputs=RDActivity(description=convertion_result.text_content),
            metadata={
                "source_file": str(ok_file),
                "character_count": len(convertion_result.text_content),
                "expected_result": "OK",
            },
        )
    # dataset.evaluators = dataset.evaluators[0:-1]
    results = dataset.evaluate_sync(do)
    results.print(include_reasons=True, include_averages=True, include_metadata=True)
    converted_results = convert_results(results)
    with open("temp_fresh_results.json", "w", encoding="utf-8") as f:
        import json

        f.write(json.dumps(converted_results, indent=2))

    # if not md_files:
    #     print(f"No markdown files found in {docs_dir}")
    # else:
    #     print(f"Found {len(md_files)} markdown file(s)")

    #     for md_file in md_files:
    #         print(f"\nProcessing: {md_file.name}")
    #         with open(md_file, "r", encoding="utf-8") as f:
    #             doc_text = f.read()
    #         print("Adding case to dataset...")
    #         print(md_file)

    #         dataset.add_case(
    #             name=str(md_file),
    #             inputs=RDActivity(description=doc_text),
    #             metadata={
    #                 "source_file": str(md_file),
    #                 "character_count": len(doc_text),
    #             },
    #         )

    # dataset.to_file("frascati_rd_dataset.json")
    # print(dataset)
    # # results = dataset.evaluate_sync(do)
    # # print(results.print(include_reasons=True))
    # # dataset.evaluators = dataset.evaluators[0:-1]
    # # dataset.cases = dataset.cases[0:2]
    # print(len(dataset.evaluators))
    # print(len(dataset.cases))

    # results = dataset.evaluate_sync(do)
    # results.print(include_reasons=True, include_averages=True, include_metadata=True)

    data = convert_results(results)
    fname = f"frascati_rd_evaluation_results_{DEFAULT_JUDGE_MODEL}.json"
    with open(fname, "w", encoding="utf-8") as f:
        import jsony

        f.write(json.dumps(data, indent=2))

    combine_evaluation_results(
        input_file=fname,
        output_file=f"frascati_rd_evaluation_results_{DEFAULT_JUDGE_MODEL}.csv",
    )
