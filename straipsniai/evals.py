"""
SMSM Article Evaluation System (Development Tool)

This module is for development/testing of article evaluators:
- Loads evaluators from straipsniai/article_judges.json
- FILTERS to only "fluid" and "dynamic" named judges (subset testing)
- Batch evaluates reference documents

Production API uses ALL evaluators from:
- ataskaitos/evaluators/articles/smsm_judges.json

For development batch evaluation:
- Run: uv run python straipsniai/evals.py
- Processes: docs/reference_documents/straipsniai*/*.md
- Outputs: straipsniai_evaluation_results.json
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic_evals import Dataset
from pydantic_evals.evaluators import LLMJudge
from pydantic_evals.reporting import EvaluationReport


@dataclass
class ScientificArticle:
    description: str
    char_count: int = 0  # Character count for length validation


# Load evaluator definitions from JSON
def load_evaluators_from_json(
    json_path: str = "straipsniai/article_judges.json",
) -> list:
    """Load evaluator rubrics from JSON and create LLMJudge instances."""
    with open(json_path, "r", encoding="utf-8") as f:
        judges_config = json.load(f)

    evaluators = []
    for config in judges_config:
        name = config["name"]
        if not ("fluid" in name or "dynamic" in name or "giedre" in name):
            continue  # Skip non-fluid/dynamic/giedre evaluators

        rubric = config["rubric"]
        has_assertion = config.get("has_assertion", False)

        # Build the LLMJudge parameters
        judge_params = {
            "rubric": rubric,
            "include_input": False,
            "score": {"evaluation_name": name, "include_reason": True},
        }

        # Add assertion if specified
        if has_assertion:
            judge_params["assertion"] = {
                "evaluation_name": f"{name.replace('_score', '')}_qualified",
                "include_reason": True,
            }

        evaluators.append(LLMJudge(**judge_params))

    return evaluators


# TEXT-BASED evaluators for Lithuanian scientific publication standards (SMSM regulation)
# These evaluators work ONLY with article text content, no external metadata required
evaluators = load_evaluators_from_json()


# Create dataset using the evaluators
dataset = Dataset(
    cases=[],
    evaluators=evaluators,
)


def do(data) -> ScientificArticle:
    return data


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
                "expected_output": case.expected_output if case.expected_output else None,
                "scores": {k: {"value": v.value, "reason": v.reason} for k, v in case.scores.items()},
                "metrics": case.metrics,
                "task_duration": case.task_duration,
                "total_duration": case.total_duration,
            }
            for case in result.cases
        ],
        "failures": [
            {
                "name": failure.name,
                "expected_output": failure.expected_output if failure.expected_output else None,
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
                inputs=ScientificArticle(description=doc_text),
                metadata={
                    "source_file": str(md_file),
                    "character_count": len(doc_text),
                },
            )

    dataset.to_file("straipsniai_dataset.json")
    print(dataset)
    # results = dataset.evaluate_sync(do)
    # print(results.print(include_reasons=True))
    # dataset.evaluators = dataset.evaluators[0:-1]
    # dataset.cases = dataset.cases[0:2]
    print(len(dataset.evaluators))
    print(len(dataset.cases))

    results = dataset.evaluate_sync(do, max_concurrency=1)
    results.print(include_reasons=True, include_averages=True, include_metadata=True)

    data = convert_results(results)
    with open("straipsniai_evaluation_results.json", "w", encoding="utf-8") as f:
        import json

        f.write(json.dumps(data, indent=2))
