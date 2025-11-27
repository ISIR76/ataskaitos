import json
import csv
from pathlib import Path
from typing import Optional

from pydantic_ai import output


def combine_evaluation_results(
    input_file: str,
    output_file: str,
    status_keywords: Optional[dict[str, str]] = None,
    verbose: bool = True,
) -> dict:
    """
    Convert evaluation results from JSON to CSV format.

    Args:
        input_file: Path to the JSON evaluation results file
        output_file: Path to the output CSV file
        status_keywords: Dict mapping keywords to status labels.
                        Defaults to {"neiskaityti": "neiskaityti", "iskaityti": "iskaityti"}
        verbose: If True, prints progress information

    Returns:
        Dict with summary statistics:
        - total_cases: Number of cases processed
        - total_failures: Number of failures
        - score_types: List of score column names
        - output_file: Path to the generated CSV
    """
    # Default status keywords
    if status_keywords is None:
        status_keywords = {"neiskaityti": "neiskaityti", "iskaityti": "iskaityti"}

    # Read the evaluation results
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Collect all unique score types
    all_score_types = set()
    for case in data["cases"]:
        all_score_types.update(case["scores"].keys())

    # Sort score types for consistent column ordering
    score_types = sorted(all_score_types)

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        header = ["name", "status"] + score_types
        writer.writerow(header)

        # Data rows
        for case in data["cases"]:
            name = case["name"]

            # Determine status from name/path using keywords
            status = "unknown"
            for keyword, label in status_keywords.items():
                if keyword in name:
                    status = label
                    break

            # Extract score values
            row = [name, status]
            for score_type in score_types:
                if score_type in case["scores"]:
                    value = case["scores"][score_type].get("value", "")
                else:
                    value = ""
                row.append(value)

            writer.writerow(row)

    # Prepare summary
    summary = {
        "total_cases": data["total_cases"],
        "total_failures": data["total_failures"],
        "score_types": score_types,
        "output_file": output_file,
    }

    if verbose:
        print(f"Results saved to {output_file}")
        print(f"Total cases: {summary['total_cases']}")
        print(f"Total failures: {summary['total_failures']}")
        print(f"\nScore columns: {', '.join(score_types)}")

    return summary


if __name__ == "__main__":
    # Example usage for Frascati R&D results
    path = Path("frascati_rd_evaluation_results_gemini-2.5-pro.json")
    output_path = path.with_name(path.stem + "_combined.csv")
    combine_evaluation_results(input_file=path, output_file=output_path)

    # Uncomment to process straipsniai results
    # combine_evaluation_results(
    #     input_file="straipsniai_evaluation_results.json",
    #     output_file="combined_straipsniai_results.csv"
    # )
