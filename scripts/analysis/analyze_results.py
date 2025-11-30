#!/usr/bin/env python
"""
Example script demonstrating evaluation results analysis.

Usage:
    uv run python analyze_results.py <path_to_evaluation_json>

    # Or with specific comparisons:
    uv run python analyze_results.py <path> --compare-document OK_2.docx --models gpt-5.1 gemini-3-pro-preview
"""

import sys
from pathlib import Path

from ataskaitos.analysis import (
    analyze_document_failures,
    analyze_failure_patterns,
    compare_models,
    load_evaluation_results,
    print_performance_report,
)
from ataskaitos.analysis.evaluation_analysis import compare_model_reasoning


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    # Load results using Pydantic models
    results = load_evaluation_results(filepath)

    # Print comprehensive report
    print_performance_report(results)

    # Get best model and analyze failures
    performances = compare_models(results)
    if performances:
        best_model = performances[0].model
        print("\n")
        analyze_failure_patterns(results, best_model)

    # Example: Analyze specific document across all models
    print("\n\n")
    print("=" * 100)
    print("DOCUMENT-SPECIFIC ANALYSIS: OK_2.docx")
    print("=" * 100)

    ok2_analysis = analyze_document_failures(results, "OK_2.docx")
    if ok2_analysis:
        print(f"\nFilename: {ok2_analysis['filename']}")
        print(f"Expected: {'OK (R&D)' if ok2_analysis['expected_ok'] else 'NOT OK'}")
        print(f"Models correct: {ok2_analysis['correct_count']}/{ok2_analysis['total_models']}")
        print()

        for model_name, model_data in ok2_analysis["models"].items():
            status = "✓" if model_data["correct"] else "✗"
            print(f"{model_name:25} {status} | K:{model_data['knowledge_score']:.2f} | {model_data['purpose'][:40]}")

    # Example: Compare reasoning between correct and incorrect models
    if performances and len(performances) > 1:
        print("\n\n")
        best = performances[0].model
        # Find a model that got OK_2 wrong
        ok2_results = [r for r in results.results if r.filename == "OK_2.docx"]
        wrong_model = next((r.model for r in ok2_results if not r.is_correct and r.model != best), None)

        if wrong_model:
            compare_model_reasoning(results, "OK_2.docx", best, wrong_model)


if __name__ == "__main__":
    main()
