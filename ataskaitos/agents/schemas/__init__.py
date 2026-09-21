"""Agent output schemas for document evaluation."""

from .article import (
    DetailedArticleEvaluation,
    LLMDetectionResult,
    SimpleArticleEvaluation,
)
from .report import (
    DetailedReportEvaluation,
    FrascatiClassifierEvaluation,
    ReportBreakdown,
    SimpleReportEvaluation,
    SystematicSubScores,
    TransferabilitySubScores,
)

__all__ = [
    "DetailedArticleEvaluation",
    "DetailedReportEvaluation",
    "FrascatiClassifierEvaluation",
    "LLMDetectionResult",
    "ReportBreakdown",
    "SimpleArticleEvaluation",
    "SimpleReportEvaluation",
    "SystematicSubScores",
    "TransferabilitySubScores",
]
