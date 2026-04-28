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
    # Article schemas
    "SimpleArticleEvaluation",
    "DetailedArticleEvaluation",
    "LLMDetectionResult",
    # Report schemas
    "SimpleReportEvaluation",
    "DetailedReportEvaluation",
    "FrascatiClassifierEvaluation",
    "ReportBreakdown",
    "SystematicSubScores",
    "TransferabilitySubScores",
]
