"""Analysis tools for evaluation results using existing Pydantic models from agents.py."""

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

# Import existing Pydantic models
from ataskaitos.agents import FrascatiClassifierEvaluation


class EvaluationResult(BaseModel):
    """Single evaluation result matching JSON structure."""

    file: str
    model: str
    evaluation: FrascatiClassifierEvaluation  # Use existing model

    @property
    def filename(self) -> str:
        """Extract just the filename."""
        return Path(self.file).name

    @property
    def is_expected_ok(self) -> bool:
        """Is this file expected to be OK (R&D)?"""
        return "/ok/" in self.file

    @property
    def is_correct(self) -> bool:
        """Is the classification correct?"""
        return self.is_expected_ok == self.evaluation.qualifies_as_rd


class EvaluationResults(BaseModel):
    """Complete evaluation results file."""

    timestamp: str
    agent: str
    total_files: int
    total_models: int
    results: list[EvaluationResult]

    def by_model(self) -> dict[str, list[EvaluationResult]]:
        """Group results by model."""
        grouped = defaultdict(list)
        for result in self.results:
            grouped[result.model].append(result)
        return dict(grouped)

    def by_file(self) -> dict[str, list[EvaluationResult]]:
        """Group results by filename."""
        grouped = defaultdict(list)
        for result in self.results:
            grouped[result.filename].append(result)
        return dict(grouped)

    def get_model_results(self, model_name: str) -> list[EvaluationResult]:
        """Get all results for a specific model."""
        return [r for r in self.results if r.model == model_name]


@dataclass
class ModelPerformance:
    """Performance metrics for a model."""

    model: str
    total_correct: int
    total_evaluations: int
    ok_correct: int
    ok_total: int
    not_ok_correct: int
    not_ok_total: int

    @property
    def accuracy(self) -> float:
        """Overall accuracy."""
        return self.total_correct / self.total_evaluations if self.total_evaluations > 0 else 0.0

    @property
    def sensitivity(self) -> float:
        """Sensitivity (true positive rate for OK documents)."""
        return self.ok_correct / self.ok_total if self.ok_total > 0 else 0.0

    @property
    def specificity(self) -> float:
        """Specificity (true negative rate for NOT OK documents)."""
        return self.not_ok_correct / self.not_ok_total if self.not_ok_total > 0 else 0.0


def load_evaluation_results(filepath: str | Path) -> EvaluationResults:
    """Load evaluation results from JSON file using existing Pydantic models."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return EvaluationResults(**data)


def analyze_model_performance(results: EvaluationResults, model_name: str) -> ModelPerformance:
    """Analyze performance metrics for a specific model."""
    model_results = results.get_model_results(model_name)

    total_correct = sum(1 for r in model_results if r.is_correct)
    total_evaluations = len(model_results)

    ok_results = [r for r in model_results if r.is_expected_ok]
    ok_correct = sum(1 for r in ok_results if r.evaluation.qualifies_as_rd)
    ok_total = len(ok_results)

    not_ok_results = [r for r in model_results if not r.is_expected_ok]
    not_ok_correct = sum(1 for r in not_ok_results if not r.evaluation.qualifies_as_rd)
    not_ok_total = len(not_ok_results)

    return ModelPerformance(
        model=model_name,
        total_correct=total_correct,
        total_evaluations=total_evaluations,
        ok_correct=ok_correct,
        ok_total=ok_total,
        not_ok_correct=not_ok_correct,
        not_ok_total=not_ok_total,
    )


def compare_models(results: EvaluationResults) -> list[ModelPerformance]:
    """Compare performance across all models."""
    performances = []
    for model in results.by_model():
        perf = analyze_model_performance(results, model)
        performances.append(perf)

    # Sort by accuracy (descending), then specificity, then sensitivity
    performances.sort(key=lambda p: (p.accuracy, p.specificity, p.sensitivity), reverse=True)

    return performances


def analyze_document_failures(results: EvaluationResults, filename: str) -> dict[str, Any]:
    """Analyze all model evaluations for a specific document."""
    doc_results = [r for r in results.results if r.filename == filename]

    if not doc_results:
        return {}

    expected_ok = doc_results[0].is_expected_ok

    analysis = {
        "filename": filename,
        "expected_ok": expected_ok,
        "total_models": len(doc_results),
        "correct_count": sum(1 for r in doc_results if r.is_correct),
        "models": {},
    }

    for result in doc_results:
        ev = result.evaluation
        analysis["models"][result.model] = {
            "correct": result.is_correct,
            "qualifies": ev.qualifies_as_rd,
            "knowledge_score": ev.knowledge_creation_score,
            "generalizability_score": ev.generalizability_score,
            "knowledge_type": ev.knowledge_creation_type,
            "purpose": ev.primary_purpose,
            "exclusion_severity": ev.exclusion_severity,
            "confidence": ev.confidence,
            "one_sentence_summary": ev.one_sentence_summary,
            "key_discriminators": ev.key_discriminators,
        }

    return analysis


def print_performance_report(results: EvaluationResults):
    """Print comprehensive performance report."""
    print("=" * 100)
    print("EVALUATION PERFORMANCE REPORT")
    print("=" * 100)
    print(f"Agent: {results.agent}")
    print(f"Timestamp: {results.timestamp}")
    print(f"Total files: {results.total_files}, Models: {results.total_models}")
    print()

    # Overall statistics
    all_correct = sum(1 for r in results.results if r.is_correct)
    all_total = len(results.results)
    print(f"Overall Accuracy: {all_correct}/{all_total} ({100 * all_correct / all_total:.1f}%)")
    print()

    # Model comparison
    print("=" * 100)
    print("MODEL RANKINGS")
    print("=" * 100)

    performances = compare_models(results)

    print(f"\n{'Rank':4} {'Model':25} {'Overall':12} {'Sensitivity':12} {'Specificity':12}")
    print("-" * 70)

    for i, perf in enumerate(performances, 1):
        print(
            f"{i:4} {perf.model:25} "
            f"{perf.total_correct}/{perf.total_evaluations} ({100 * perf.accuracy:.0f}%)  "
            f"{perf.ok_correct}/{perf.ok_total} ({100 * perf.sensitivity:.0f}%)  "
            f"{perf.not_ok_correct}/{perf.not_ok_total} ({100 * perf.specificity:.0f}%)"
        )

    print("\n" + "=" * 100)
    print("DETAILED MODEL ANALYSIS")
    print("=" * 100)

    for perf in performances[:3]:  # Top 3 models
        print(f"\n{perf.model}")
        print("-" * 100)

        model_results = results.get_model_results(perf.model)

        for r in sorted(model_results, key=lambda x: (not x.is_expected_ok, x.filename)):
            status = "✓" if r.is_correct else "✗"
            expected_label = "OK" if r.is_expected_ok else "NOT"
            result_label = "PASS" if r.evaluation.qualifies_as_rd else "FAIL"

            print(
                f"{r.filename:12} [{expected_label:3}] → {result_label:4} | "
                f"K:{r.evaluation.knowledge_creation_score:.2f} "
                f"G:{r.evaluation.generalizability_score:.2f} | "
                f"{r.evaluation.primary_purpose[:30]:30} | {status}"
            )

        # Score statistics
        ok_scores = [r.evaluation.knowledge_creation_score for r in model_results if r.is_expected_ok]
        not_ok_scores = [r.evaluation.knowledge_creation_score for r in model_results if not r.is_expected_ok]

        print("\nKnowledge Score Statistics:")
        if ok_scores:
            print(f"  OK avg: {sum(ok_scores) / len(ok_scores):.2f} (range: {min(ok_scores):.2f}-{max(ok_scores):.2f})")
        if not_ok_scores:
            print(
                f"  NOT OK avg: {sum(not_ok_scores) / len(not_ok_scores):.2f} "
                f"(range: {min(not_ok_scores):.2f}-{max(not_ok_scores):.2f})"
            )

        score_gap = (sum(ok_scores) / len(ok_scores) if ok_scores else 0) - (
            sum(not_ok_scores) / len(not_ok_scores) if not_ok_scores else 0
        )
        print(f"  Score discrimination: {score_gap:.2f} (higher is better)")


def analyze_failure_patterns(results: EvaluationResults, best_model: str):
    """Analyze failure patterns for the best performing model."""
    model_results = results.get_model_results(best_model)
    failures = [r for r in model_results if not r.is_correct]

    print("=" * 100)
    print(f"FAILURE ANALYSIS: {best_model}")
    print("=" * 100)

    if not failures:
        print("\nNo failures - perfect performance!")
        return

    print(f"\nTotal failures: {len(failures)}/{len(model_results)}")
    print()

    for result in failures:
        ev = result.evaluation
        expected = "OK (R&D)" if result.is_expected_ok else "NOT OK (Non-R&D)"
        got = "R&D" if ev.qualifies_as_rd else "Non-R&D"

        print("=" * 100)
        print(f"FAILURE: {result.filename}")
        print(f"Expected: {expected}, Got: {got}")
        print("=" * 100)

        print("\nScores & Classification:")
        print(f"  Knowledge Creation: {ev.knowledge_creation_score:.2f} - {ev.knowledge_creation_type}")
        print(f"  Generalizability: {ev.generalizability_score:.2f} - {ev.generalizability_assessment}")
        print(f"  Primary Purpose: {ev.primary_purpose}")
        print(f"  Methodology: {ev.methodology_nature} (Standard: {ev.uses_standard_methods})")
        print(f"  Exclusions: {ev.identified_exclusions}")
        print(f"  Exclusion Severity: {ev.exclusion_severity}")
        print(f"  Confidence: {ev.confidence}")

        print("\nOne-Sentence Summary:")
        print(f"  {ev.one_sentence_summary}")

        print("\nKey Discriminators:")
        for i, disc in enumerate(ev.key_discriminators, 1):
            print(f"  {i}. {disc[:150]}{'...' if len(disc) > 150 else ''}")

        print("\nEvidence Snippets:")
        print(f"  Knowledge: {ev.knowledge_creation_evidence[:200]}...")
        print(f"  Generalizability: {ev.generalizability_evidence[:200]}...")
        print()


def compare_model_reasoning(results: EvaluationResults, filename: str, correct_model: str, incorrect_model: str):
    """Compare reasoning between a model that got it right vs one that got it wrong."""
    doc_results = results.by_file().get(filename, [])

    if not doc_results:
        print(f"No results found for {filename}")
        return

    correct_result = next((r for r in doc_results if r.model == correct_model), None)
    incorrect_result = next((r for r in doc_results if r.model == incorrect_model), None)

    if not correct_result or not incorrect_result:
        print("Could not find both model results")
        return

    expected_ok = correct_result.is_expected_ok

    print("=" * 100)
    print(f"REASONING COMPARISON: {filename}")
    print(f"Expected: {'OK (R&D)' if expected_ok else 'NOT OK (Non-R&D)'}")
    print("=" * 100)

    print(f"\n{correct_model} (CORRECT):")
    print("-" * 100)
    ev_c = correct_result.evaluation
    print(f"Classification: {'R&D' if ev_c.qualifies_as_rd else 'Non-R&D'}")
    print(f"Knowledge: {ev_c.knowledge_creation_score:.2f} - {ev_c.knowledge_creation_type}")
    print(f"Purpose: {ev_c.primary_purpose}")
    print(f"Exclusions: {ev_c.exclusion_severity} - {ev_c.identified_exclusions}")
    print(f"\nReasoning: {ev_c.classification_rationale[:500]}...")

    print(f"\n{incorrect_model} (INCORRECT):")
    print("-" * 100)
    ev_i = incorrect_result.evaluation
    print(f"Classification: {'R&D' if ev_i.qualifies_as_rd else 'Non-R&D'}")
    print(f"Knowledge: {ev_i.knowledge_creation_score:.2f} - {ev_i.knowledge_creation_type}")
    print(f"Purpose: {ev_i.primary_purpose}")
    print(f"Exclusions: {ev_i.exclusion_severity} - {ev_i.identified_exclusions}")
    print(f"\nReasoning: {ev_i.classification_rationale[:500]}...")

    print("\n" + "=" * 100)
    print("KEY DIFFERENCES")
    print("=" * 100)
    print(
        f"Knowledge Score: {correct_model}={ev_c.knowledge_creation_score:.2f} vs {incorrect_model}={ev_i.knowledge_creation_score:.2f} (Δ={abs(ev_c.knowledge_creation_score - ev_i.knowledge_creation_score):.2f})"
    )
    print(f'Purpose: {correct_model}="{ev_c.primary_purpose}" vs {incorrect_model}="{ev_i.primary_purpose}"')
    print(
        f"Exclusion Severity: {correct_model}={ev_c.exclusion_severity} vs {incorrect_model}={ev_i.exclusion_severity}"
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python evaluation_analysis.py <path_to_evaluation_json>")
        sys.exit(1)

    filepath = sys.argv[1]
    results = load_evaluation_results(filepath)

    print_performance_report(results)

    # Analyze best model failures
    performances = compare_models(results)
    if performances:
        best_model = performances[0].model
        print("\n")
        analyze_failure_patterns(results, best_model)
