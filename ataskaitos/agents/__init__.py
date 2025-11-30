"""Multiple agents for document evaluation with different output schemas.

This module maintains backward compatibility while the implementation
has been refactored into separate modules for better maintainability.

Prompts are now in ataskaitos/prompts/ directory.
Schemas are organized in ataskaitos/agents/schemas/ module.
Factory and registry logic is in ataskaitos/agents/ module.
"""

# Re-export all schemas for backward compatibility
# Import MTEP agent (existing)
from ataskaitos.agent_from_human import create_mtep_agent

# Re-export core classes and functions
from .factory import AgentFactory
from .registry import (
    AgentRegistry,
    get_agent_registry,
    get_default_agent,
)
from .schemas import (
    DetailedArticleEvaluation,
    DetailedReportEvaluation,
    FrascatiClassifierEvaluation,
    ReportBreakdown,
    # Article schemas
    SimpleArticleEvaluation,
    # Report schemas
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
    # Core functionality
    "AgentFactory",
    "AgentRegistry",
    "get_agent_registry",
    "get_default_agent",
    "create_mtep_agent",
]
