#!/usr/bin/env python
"""Analyze classification accuracy against folder structure."""

import json
import sys
from pathlib import Path


def analyze_classification(file_path: str, threshold: float = 0.5):
    """Analyze if agent correctly classified OK vs NOT_OK documents."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 80)
    print(f"CLASSIFICATION ANALYSIS: {Path(file_path).name}")
    print("=" * 80)
    print(f"Decision threshold: {threshold:.2f}")
    print("=" * 80 + "\n")

    results = []
    for result in data["results"]:
        if not result["evaluation"]:
            continue

        file_path = result["file"]
        score = float(result["evaluation"]["score"])
        assessment = result["evaluation"].get("assessment_overview", "")

        # Determine expected classification from folder
        is_ok_folder = "/ok/" in file_path.lower()
        expected_label = "GOOD R&D" if is_ok_folder else "NOT R&D"

        # Determine predicted classification from score
        predicted_pass = score >= threshold
        predicted_label = "GOOD R&D" if predicted_pass else "NOT R&D"

        # Check if correct
        correct = (is_ok_folder and predicted_pass) or (not is_ok_folder and not predicted_pass)

        results.append(
            {
                "file": Path(file_path).name,
                "score": score,
                "expected": expected_label,
                "predicted": predicted_label,
                "correct": correct,
                "assessment": assessment[:100] + "..." if len(assessment) > 100 else assessment,
            }
        )

    # Print results
    print("INDIVIDUAL RESULTS:")
    print("-" * 80)
    for r in results:
        status = "✓" if r["correct"] else "✗"
        print(f"{status} {r['file']:20s} | Score: {r['score']:.2f}")
        print(f"   Expected: {r['expected']:15s} | Predicted: {r['predicted']:15s}")
        if not r["correct"]:
            print(f"   Assessment: {r['assessment']}")
        print()

    # Summary statistics
    correct_count = sum(1 for r in results if r["correct"])
    total_count = len(results)
    accuracy = correct_count / total_count if total_count > 0 else 0

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Accuracy: {correct_count}/{total_count} ({accuracy:.1%})")

    # Confusion matrix
    tp = sum(1 for r in results if r["expected"] == "GOOD R&D" and r["predicted"] == "GOOD R&D")
    tn = sum(1 for r in results if r["expected"] == "NOT R&D" and r["predicted"] == "NOT R&D")
    fp = sum(1 for r in results if r["expected"] == "NOT R&D" and r["predicted"] == "GOOD R&D")
    fn = sum(1 for r in results if r["expected"] == "GOOD R&D" and r["predicted"] == "NOT R&D")

    print("\nConfusion Matrix:")
    print(f"  True Positives (OK → GOOD):  {tp}")
    print(f"  True Negatives (NOT → NOT):  {tn}")
    print(f"  False Positives (NOT → GOOD): {fp} ⚠")
    print(f"  False Negatives (OK → NOT):   {fn} ⚠")

    if tp + fn > 0:
        recall = tp / (tp + fn)
        print(f"\nRecall (sensitivity): {recall:.1%}")
    if tp + fp > 0:
        precision = tp / (tp + fp)
        print(f"Precision: {precision:.1%}")

    # Score distribution
    ok_scores = [r["score"] for r in results if r["expected"] == "GOOD R&D"]
    not_ok_scores = [r["score"] for r in results if r["expected"] == "NOT R&D"]

    if ok_scores:
        print(f"\nOK folder scores: {min(ok_scores):.2f} - {max(ok_scores):.2f}")
    if not_ok_scores:
        print(f"NOT_OK folder scores: {min(not_ok_scores):.2f} - {max(not_ok_scores):.2f}")

    # Issues
    print("\n" + "=" * 80)
    print("ISSUES & RECOMMENDATIONS")
    print("=" * 80)

    if fp > 0:
        print(f"\n⚠ {fp} FALSE POSITIVES: NOT_OK documents classified as GOOD")
        print("  These documents were in 'not_ok' folder but agent scored them high:")
        for r in results:
            if r["expected"] == "NOT R&D" and r["predicted"] == "GOOD R&D":
                print(f"    - {r['file']} (score: {r['score']:.2f})")
        print("  Action: Review these documents or adjust agent rubric")

    if fn > 0:
        print(f"\n⚠ {fn} FALSE NEGATIVES: OK documents classified as NOT GOOD")
        print("  These documents were in 'ok' folder but agent scored them low:")
        for r in results:
            if r["expected"] == "GOOD R&D" and r["predicted"] == "NOT R&D":
                print(f"    - {r['file']} (score: {r['score']:.2f})")
        print("  Action: Review these documents or adjust agent rubric")

    if accuracy == 1.0:
        print("\n✓ Perfect classification! Agent correctly identified all documents.")
    elif accuracy >= 0.8:
        print(f"\n✓ Good performance ({accuracy:.1%} accuracy)")
    else:
        print(f"\n⚠ Performance needs improvement ({accuracy:.1%} accuracy)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_classification.py <evaluation_file.json> [threshold]")
        sys.exit(1)

    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    analyze_classification(sys.argv[1], threshold)
