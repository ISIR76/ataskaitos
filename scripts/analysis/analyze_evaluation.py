#!/usr/bin/env python
"""Analyze agent evaluation results."""

import json
import sys
from pathlib import Path
from statistics import mean, stdev


def analyze_evaluation_file(file_path: str):
    """Analyze evaluation results and print summary."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 80)
    print(f"EVALUATION ANALYSIS: {Path(file_path).name}")
    print("=" * 80)
    print(f"Timestamp: {data['timestamp']}")
    print(f"Agent: {data['agent']}")
    print(f"Total files: {data['total_files']}")
    print(f"Total models: {data['total_models']}")
    print(f"Total results: {len(data['results'])}")

    # Separate successful and failed results
    successful = [r for r in data["results"] if r["evaluation"]]
    failed = [r for r in data["results"] if r["error"]]

    print(f"\n✓ Successful: {len(successful)}")
    print(f"✗ Failed: {len(failed)}")

    if failed:
        print("\nErrors:")
        for result in failed:
            print(f"  - {result['file']} ({result['model']}): {result['error']}")

    if not successful:
        print("\nNo successful evaluations to analyze.")
        return

    # Analyze scores by criterion
    print("\n" + "=" * 80)
    print("SCORE ANALYSIS (FRASCATI CRITERIA)")
    print("=" * 80)

    criteria = [
        "naujumas",
        "kurybiskumas",
        "neapibreztumas",
        "sistemingumas",
        "perduodamumas",
    ]
    structural = [
        "ivadas",
        "problemos_formulavimas",
        "uzdavinio_apibrezimas",
        "veiklos_aprasymas",
        "rezultato_pateikimas",
    ]

    def extract_scores(criterion: str) -> list[float]:
        scores = []
        for result in successful:
            eval_data = result["evaluation"]
            if criterion in eval_data and "score" in eval_data[criterion]:
                score_str = eval_data[criterion]["score"]
                try:
                    scores.append(float(score_str))
                except (ValueError, TypeError):
                    pass
        return scores

    print("\nCore R&D Criteria:")
    for criterion in criteria:
        scores = extract_scores(criterion)
        if scores:
            print(f"  {criterion:20s}: {mean(scores):.3f} ± {stdev(scores):.3f} (n={len(scores)})")

    print("\nStructural Quality:")
    for criterion in structural:
        scores = extract_scores(criterion)
        if scores:
            print(f"  {criterion:25s}: {mean(scores):.3f} ± {stdev(scores):.3f} (n={len(scores)})")

    # Overall scores
    print("\n" + "=" * 80)
    print("OVERALL SCORES")
    print("=" * 80)

    for result in successful:
        eval_data = result["evaluation"]
        file_name = Path(result["file"]).name
        model = result["model"]

        # Calculate average of core criteria
        core_scores = []
        for criterion in criteria:
            if criterion in eval_data and "score" in eval_data[criterion]:
                try:
                    core_scores.append(float(eval_data[criterion]["score"]))
                except (ValueError, TypeError):
                    pass

        # Calculate average of structural criteria
        struct_scores = []
        for criterion in structural:
            if criterion in eval_data and "score" in eval_data[criterion]:
                try:
                    struct_scores.append(float(eval_data[criterion]["score"]))
                except (ValueError, TypeError):
                    pass

        avg_core = mean(core_scores) if core_scores else 0
        avg_struct = mean(struct_scores) if struct_scores else 0

        print(f"\n{file_name} ({model}):")
        print(f"  Core R&D:  {avg_core:.3f}")
        print(f"  Structure: {avg_struct:.3f}")
        print(f"  Overall:   {mean([avg_core, avg_struct]):.3f}")

    # By model performance
    print("\n" + "=" * 80)
    print("MODEL PERFORMANCE")
    print("=" * 80)

    by_model = {}
    for result in successful:
        model = result["model"]
        if model not in by_model:
            by_model[model] = []

        eval_data = result["evaluation"]
        all_scores = []
        for criterion in criteria + structural:
            if criterion in eval_data and "score" in eval_data[criterion]:
                try:
                    all_scores.append(float(eval_data[criterion]["score"]))
                except (ValueError, TypeError):
                    pass

        if all_scores:
            by_model[model].append(mean(all_scores))

    for model, scores in by_model.items():
        print(f"\n{model}:")
        print(f"  Avg score: {mean(scores):.3f} ± {stdev(scores):.3f}")
        print(f"  Evaluations: {len(scores)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_evaluation.py <evaluation_file.json>")
        sys.exit(1)

    analyze_evaluation_file(sys.argv[1])
