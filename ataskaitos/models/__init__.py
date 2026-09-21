"""Domain models for evaluations."""

from .article import ScientificArticle
from .evaluation import EvaluationResult, EvaluatorScore
from .report import RDActivity

__all__ = [
    "EvaluationResult",
    "EvaluatorScore",
    "RDActivity",
    "ScientificArticle",
]
