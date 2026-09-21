"""Base evaluator registry and management."""

from typing import Any

from pydantic_evals.evaluators import LLMJudge


class EvaluatorRegistry:
    """Central registry for all evaluators."""

    def __init__(self):
        self._evaluators: dict[str, dict[str, LLMJudge]] = {
            "report": {},
            "article": {},
        }
        self._metadata: dict[str, dict[str, dict[str, Any]]] = {
            "report": {},
            "article": {},
        }

    def register(
        self,
        document_type: str,
        name: str,
        evaluator: LLMJudge,
        metadata: dict[str, Any] | None = None,
    ):
        """Register an evaluator for a document type."""
        if document_type not in self._evaluators:
            raise ValueError(f"Unknown document type: {document_type}. Must be 'report' or 'article'")

        self._evaluators[document_type][name] = evaluator
        self._metadata[document_type][name] = metadata or {}

    def get_evaluator(self, document_type: str, name: str) -> LLMJudge | None:
        """Get a specific evaluator by name."""
        return self._evaluators.get(document_type, {}).get(name)

    def get_evaluators(self, document_type: str, names: list[str] | None = None) -> list[LLMJudge]:
        """Get evaluators for document type.

        Args:
            document_type: Type of document ('report' or 'article')
            names: Optional list of specific evaluator names to retrieve.
                  If None, returns all evaluators for the document type.

        Returns:
            List of LLMJudge evaluators
        """
        all_evaluators = self._evaluators.get(document_type, {})

        if names is None:
            return list(all_evaluators.values())

        return [all_evaluators[name] for name in names if name in all_evaluators]

    def list_available(self, document_type: str | None = None) -> dict[str, list[dict[str, Any]]]:
        """List all available evaluators with metadata.

        Args:
            document_type: Optional filter for specific document type

        Returns:
            Dictionary mapping document types to lists of evaluator info
        """
        result = {}

        types = [document_type] if document_type else ["report", "article"]

        for dtype in types:
            evaluators_info = []
            for name, evaluator in self._evaluators.get(dtype, {}).items():
                info = {"name": name, **self._metadata[dtype].get(name, {})}

                # Extract rubric from the LLMJudge evaluator if available
                if hasattr(evaluator, "rubric"):
                    info["rubric"] = evaluator.rubric

                evaluators_info.append(info)

            result[dtype] = evaluators_info

        return result

    def count(self, document_type: str | None = None) -> dict[str, int]:
        """Count evaluators by document type."""
        if document_type:
            return {document_type: len(self._evaluators.get(document_type, {}))}

        return {dtype: len(evaluators) for dtype, evaluators in self._evaluators.items()}


# Global registry instance
_global_registry = None


def get_registry() -> EvaluatorRegistry:
    """Get the global evaluator registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = EvaluatorRegistry()
    return _global_registry
