"""Agent output schemas for document evaluation."""

from .article import (
    DetailedArticleEvaluation,
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
    # Report schemas
    "SimpleReportEvaluation",
    "DetailedReportEvaluation",
    "FrascatiClassifierEvaluation",
    "ReportBreakdown",
    "SystematicSubScores",
    "TransferabilitySubScores",
]
