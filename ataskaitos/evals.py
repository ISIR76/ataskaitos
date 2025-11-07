from dataclasses import dataclass
from typing import Any
from xml.etree.ElementInclude import include

from pydantic_evals import Dataset
from pydantic_evals.evaluators import LLMJudge


@dataclass
class RDActivity:
    description: str


# Define evaluators separately for reuse
evaluators = [
        # 1. Basic Frascati R&D check
        LLMJudge(
            rubric="""
            Evaluate according to Frascati Manual definition of R&D:
            1. Does it aim to create NEW knowledge (not just apply existing)?
            2. Does it have UNCERTAIN outcomes (not predictable with current knowledge)?
            3. Is it SYSTEMATIC (planned and documented)?

            Score 1.0 if all three conditions are met, 0.0 if any are missing.
            Cite specific evidence from the activity description.
            """,
            include_input=False,
            score={"evaluation_name": "short_evaluator", "include_reason": True},
        ),
        # 2. All Frascati criteria combined
        LLMJudge(
            rubric="""
            Evaluate against all 5 core Frascati Manual criteria for R&D.
            Award 0.2 points for each criterion met (total 1.0 possible):

            1. NOVEL (0.2): Activity aims to advance beyond current state-of-the-art or knowledge frontier
            2. CREATIVE (0.2): Uses non-obvious concepts, methodologies, or approaches
            3. UNCERTAIN (0.2): Outcome cannot be determined in advance using existing knowledge
            4. SYSTEMATIC (0.2): Planned, budgeted, and documented in advance
            5. TRANSFERABLE (0.2): Results can be codified, documented, and reproduced by others

            Score must be ≥0.8 (4/5 criteria) to qualify as R&D according to Frascati Manual.
            Provide specific evidence for each criterion from the activity description.
            """,
            include_input=False,
            score={"evaluation_name": "combined_score", "include_reason": True},
        ),
        # 3-7. Individual Frascati criteria
        LLMJudge(
            rubric="""
            NOVELTY according to Frascati Manual - does activity advance knowledge/technology beyond current state-of-the-art?

            Score:
            - 1.0: Groundbreaking discovery or pioneering work in the field
            - 0.8: Significant advancement beyond existing knowledge
            - 0.6: Notable but incremental advancement
            - 0.4: Minor improvement over existing approaches
            - 0.2: Adaptation of known methods to new context
            - 0.0: Routine application of established knowledge

            Evidence required: Cite what existing knowledge/methods are being advanced beyond.
            """,
            include_input=False,
            score={"evaluation_name": "novelty_score", "include_reason": True},
        ),
        LLMJudge(
            rubric="""
            CREATIVITY according to Frascati Manual - does activity use non-obvious concepts, approaches, or methodologies?

            Score:
            - 1.0: Entirely new methodology or approach invented/developed
            - 0.8: Novel combination of existing methods in innovative ways
            - 0.6: Creative adaptation requiring significant problem-solving
            - 0.4: Some creative elements but mostly standard approaches
            - 0.2: Minor variations on established procedures
            - 0.0: Straightforward application of standard methods

            Evidence required: Describe what creative problem-solving or non-obvious thinking was required.
            """,
            include_input=False,
            score={"evaluation_name": "creativity_score", "include_reason": True},
        ),
        LLMJudge(
            rubric="""
            UNCERTAINTY according to Frascati Manual - is the outcome genuinely unpredictable using current knowledge?

            CRITICAL: Distinguish scientific/technical uncertainty (R&D) from other types (NOT R&D):

            R&D uncertainty (score high):
            - 1.0: Fundamental unknowns in science/technology; multiple failure paths possible
            - 0.8: Significant technical risk despite expert knowledge
            - 0.6: Some unpredictability in how to achieve result

            NOT R&D uncertainty (score 0.0):
            - Team inexperience or learning curve
            - Market/business/commercial risk
            - Implementation challenges with known solutions
            - Resource or timing uncertainty

            Evidence required: Specify what scientific/technical unknowns exist that make the outcome unpredictable.
            """,
            include_input=False,
            score={"evaluation_name": "uncertainty_score", "include_reason": True},
        ),
        LLMJudge(
            rubric="""
            SYSTEMATIC according to Frascati Manual - is the activity formally organized with clear planning?

            Award points for evidence of:
            - Defined hypothesis, research questions, or objectives (0.33 points)
            - Planned methodology and procedures documented (0.33 points)
            - Budget, timeline, and resources allocated (0.34 points)

            Score:
            - 1.0: All three elements clearly present
            - 0.67: Two elements present
            - 0.33: One element present
            - 0.0: No systematic planning evident (ad-hoc work)

            Evidence required: Cite specific mentions of planning, methodology, or resource allocation.
            """,
            include_input=False,
            score={"evaluation_name": "systematic_score", "include_reason": True},
        ),
        LLMJudge(
            rubric="""
            TRANSFERABLE/REPRODUCIBLE according to Frascati Manual - can knowledge be codified and reproduced?

            Award points for evidence of:
            - Results documented in reproducible format (0.33 points)
            - Process/methodology can be followed by other qualified researchers (0.33 points)
            - Knowledge communicable through publications, patents, or reports (0.34 points)

            Score:
            - 1.0: All three elements clearly present or planned
            - 0.67: Two elements present
            - 0.33: One element present
            - 0.0: No evidence of documentation or reproducibility

            Evidence required: Cite how results will be/were documented and made reproducible.
            """,
            include_input=False,
            score={"evaluation_name": "transferable_score", "include_reason": True},
        ),
        LLMJudge(
            rubric="""
    COMPREHENSIVE FRASCATI MANUAL R&D EVALUATION (0.0-1.0 Score)

    Based on OECD Frascati Manual 2015 - Standard for R&D Statistics

    ═══════════════════════════════════════════════════════════════
    PART 1: CORE FRASCATI CRITERIA (0.5 max - all must pass for R&D)
    ═══════════════════════════════════════════════════════════════

    1. NOVELTY (0.1): Does it aim to achieve NEW knowledge per Frascati §2.7?
       - Groundbreaking/pioneering discovery: 0.1
       - Significant advancement in field: 0.08
       - Incremental but non-trivial: 0.06
       - Minor improvement: 0.04
       - Adaptation of existing: 0.02
       - Routine/known: 0.0
       
    2. CREATIVITY (0.1): Does it use non-obvious creative concepts per Frascati §2.7?
       - Entirely new methodology invented: 0.1
       - Novel combination of approaches: 0.08
       - Creative adaptation required: 0.06
       - Some creative elements: 0.04
       - Minor variations: 0.02
       - Standard procedures: 0.0

    3. UNCERTAINTY (0.1): Is outcome uncertain per Frascati §2.7?
       CRITICAL - CHECK SOURCE OF UNCERTAINTY (Frascati §2.24-2.27):
       - Scientific/technical unknowns (QUALIFIES as R&D): 0.1
       - Multiple failure paths despite expertise (QUALIFIES as R&D): 0.08
       - Team inexperience/learning curve (DOES NOT QUALIFY): 0.0
       - Market/business/commercial risk (DOES NOT QUALIFY): 0.0
       - Outcome predictable with known methods (DOES NOT QUALIFY): 0.0
       
    4. SYSTEMATIC (0.1): Is it planned and organized per Frascati §2.7?
       - Defined hypothesis/research questions: +0.033
       - Planned methodology documented: +0.033
       - Budget/resources allocated: +0.034
       Missing any element = proportional deduction

    5. TRANSFERABLE (0.1): Will it produce codified knowledge per Frascati §2.7, 2.11?
       - Results documented in reproducible format: +0.033
       - Process reproducible by qualified researchers: +0.033
       - Knowledge communicable (publication/patent/report): +0.034
       Missing any element = proportional deduction
    
    ═══════════════════════════════════════════════════════════════
    PART 2: FRASCATI EXCLUSIONS (0.1 max penalty) - §2.64-2.91
    ═══════════════════════════════════════════════════════════════

    DEDUCT according to Frascati Manual exclusions (cumulative):
    - Routine testing/quality control (§2.85): -0.1
    - Market research/consumer surveys (§2.90): -0.1
    - Feasibility studies without R&D (§2.89): -0.1
    - Production/pre-production (§2.84): -0.1
    - Software maintenance/routine debugging (§2.71): -0.1
    - Routine data collection (§2.88): -0.1
    - Legal/administrative work (§2.91): -0.05
    - Installation of existing systems (§2.86): -0.1

    If ANY major exclusion is primary activity, cap maximum score at 0.3
    
    ═══════════════════════════════════════════════════════════════
    PART 3: R&D CONTENT RATIO (0.15 max) - Frascati §2.19-2.23
    ═══════════════════════════════════════════════════════════════

    What percentage is ACTUAL R&D vs supporting/ancillary activities?
    - 90-100% pure R&D activity: 0.15
    - 70-89% predominantly R&D: 0.12
    - 50-69% mixed R&D with other work: 0.09
    - 30-49% some R&D elements present: 0.06
    - 10-29% minimal R&D content: 0.03
    - <10% negligible R&D: 0.0

    Key question per Frascati §2.20: Is this "R&D project with supporting work"
    or "routine project with some R&D elements"?

    Cite specific evidence of what % is genuine R&D vs other activities.
    
    ═══════════════════════════════════════════════════════════════
    PART 4: R&D VS INNOVATION BOUNDARY (0.1 max) - Frascati §2.28-2.35
    ═══════════════════════════════════════════════════════════════

    Primary objective according to Frascati definitions:
    - Create fundamentally NEW knowledge (R&D per §2.5-2.9): 0.1
    - Discover/prove scientific/technical principles (R&D): 0.1
    - First practical application of new knowledge (R&D): 0.08
    - Apply existing knowledge in novel way (Innovation, NOT R&D per §2.34): 0.05
    - Implement/deploy known solutions (NOT R&D): 0.0

    CRITICAL distinction per Frascati §2.28: Does it CREATE new knowledge
    or APPLY existing knowledge (even innovatively)?

    Cite evidence of what new knowledge is being created vs. applied.
    
    ═══════════════════════════════════════════════════════════════
    PART 5: PERSONNEL QUALIFICATION (0.075 max) - Frascati §5.2-5.19
    ═══════════════════════════════════════════════════════════════

    Who performs the work (Frascati personnel classification)?
    - PhD/research scientists leading (Researchers): 0.075
    - Master's degree engineers doing research: 0.06
    - Technical specialists supporting R&D (Technicians): 0.045
    - General staff/technicians (not R&D personnel): 0.03
    - No qualified personnel mentioned: 0.0

    Cite evidence of personnel qualifications and their role in the activity.
    
    ═══════════════════════════════════════════════════════════════
    PART 6: DOCUMENTATION & RIGOR (0.075 max) - Frascati §2.7, 2.11
    ═══════════════════════════════════════════════════════════════

    Evidence of systematic R&D approach per Frascati Manual:
    - Research objectives/hypothesis documented: +0.019
    - Methodology/protocols clearly defined: +0.019
    - Literature review/state-of-art analysis: +0.019
    - Expected vs actual outcomes tracked: +0.018

    Missing any element = proportional deduction
    Cite specific evidence of documentation and systematic approach.
    
    ═══════════════════════════════════════════════════════════════
    FINAL SCORING INTERPRETATION - Frascati Manual Compliance
    ═══════════════════════════════════════════════════════════════

    0.80-1.00: STRONG R&D - Clearly qualifies per Frascati (PASS)
    0.65-0.79: MODERATE R&D - Likely qualifies with proper documentation (PASS)
    0.50-0.64: BORDERLINE - R&D elements but mixed activities (Review needed)
    0.30-0.49: WEAK R&D - Primarily innovation/application, not R&D (FAIL)
    0.00-0.29: NOT R&D - Routine work or excluded per Frascati (FAIL)
    
    ═══════════════════════════════════════════════════════════════
    R&D TYPE CLASSIFICATION - Frascati §2.5-2.9
    ═══════════════════════════════════════════════════════════════

    If score ≥0.65 (PASS), classify according to Frascati R&D types:

    - BASIC RESEARCH (§2.5): Experimental/theoretical work to acquire new
      knowledge with no particular application in view

    - APPLIED RESEARCH (§2.6): Original investigation to acquire new knowledge
      directed towards a specific practical aim or objective

    - EXPERIMENTAL DEVELOPMENT (§2.7): Systematic work using existing knowledge
      to produce new materials, products, processes, or substantially improved versions

    Cite evidence for classification choice.
    
    ═══════════════════════════════════════════════════════════════
    MANDATORY REASONING REQUIREMENTS - Evidence-Based Analysis
    ═══════════════════════════════════════════════════════════════

    Your evaluation response MUST include:

    1. OVERALL SCORE with detailed subscores for all 6 parts (0.5 + 0.1 + 0.15 + 0.1 + 0.075 + 0.075)

    2. CRITERION ANALYSIS: Which Frascati criteria are strongest/weakest with specific evidence

    3. EXCLUSIONS CHECK: Any Frascati §2.64-2.91 exclusions identified in the activity

    4. R&D CONTENT: Estimated percentage that is genuine R&D vs. supporting/other work

    5. R&D VS INNOVATION: Clear classification per Frascati §2.28-2.35 with reasoning

    6. PERSONNEL: Qualification assessment against Frascati Chapter 5 standards

    7. PASS/FAIL: Clear determination (≥0.65 = PASS, <0.65 = FAIL)

    8. R&D TYPE: If PASS, classify as Basic/Applied/Experimental per Frascati §2.5-2.9

    9. GAPS IDENTIFIED: Key missing information or weak evidence areas

    10. RECOMMENDATIONS: Specific actions to strengthen R&D qualification and Frascati compliance

    11. CITATIONS: Quote specific passages from activity description as evidence

    12. FRASCATI REFERENCES: Cite relevant Frascati Manual sections for each judgment
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

    # Read all markdown files from reference documents
    docs_dir = Path(
        "./docs/reference_documents/",
    )
    md_files = list(docs_dir.glob("straipsniai*/*.md"))
    print(md_files)

    if not md_files:
        print(f"No markdown files found in {docs_dir}")
    else:
        print(f"Found {len(md_files)} markdown file(s)")

        for md_file in md_files:
            print(f"\nProcessing: {md_file.name}")
            with open(md_file, "r", encoding="utf-8") as f:
                doc_text = f.read()
            print("Adding case to dataset...")
            print(md_file)

            dataset.add_case(
                name=str(md_file),
                inputs=RDActivity(description=doc_text),
                metadata={
                    "source_file": str(md_file),
                    "character_count": len(doc_text),
                },
            )

    dataset.to_file("frascati_rd_dataset.json")
    print(dataset)
    # results = dataset.evaluate_sync(do)
    # print(results.print(include_reasons=True))
    # dataset.evaluators = dataset.evaluators[0:-1]
    # dataset.cases = dataset.cases[0:2]
    print(len(dataset.evaluators))
    print(len(dataset.cases))

    results = dataset.evaluate_sync(do)
    results.print(include_reasons=True, include_averages=True, include_metadata=True)

    data = convert_results(results)
    with open("frascati_rd_evaluation_resultsa.json", "w", encoding="utf-8") as f:
        import json

        f.write(json.dumps(data, indent=2))
