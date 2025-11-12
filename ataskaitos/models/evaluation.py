"""Shared evaluation models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Literal
from uuid import uuid4


@dataclass
class EvaluatorScore:
    """Individual evaluator score with reasoning."""

    value: float
    reason: str


@dataclass
class EvaluationResult:
    """Result of a document evaluation."""

    evaluation_id: str = field(default_factory=lambda: str(uuid4()))
    document_type: Literal["report", "article"] = "report"
    evaluation_type: Literal["agent", "scoring"] = "scoring"
    status: str = "success"
    markdown_content: str = ""
    results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "evaluation_id": self.evaluation_id,
            "document_type": self.document_type,
            "evaluation_type": self.evaluation_type,
            "status": self.status,
            "markdown_content": self.markdown_content,
            "results": self.results,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
