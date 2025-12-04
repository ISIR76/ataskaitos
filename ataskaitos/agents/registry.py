"""Agent registry for managing multiple agents per document type."""

from typing import Any, Dict, Optional

from pydantic_ai import Agent
from pydantic_ai.output import NativeOutput

# Import MTEP agent
from ataskaitos.agent_from_human import create_mtep_agent

from .factory import AgentFactory


class AgentRegistry:
    """Registry for managing multiple agents per document type."""

    def __init__(self):
        self._agents: Dict[str, Dict[str, Agent]] = {
            "article": {},
            "report": {},
        }
        self._metadata: Dict[str, Dict[str, Dict[str, Any]]] = {
            "article": {},
            "report": {},
        }

    def register(
        self,
        document_type: str,
        name: str,
        agent: Agent,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Register an agent for a document type."""
        if document_type not in self._agents:
            raise ValueError(f"Unknown document type: {document_type}")

        self._agents[document_type][name] = agent
        self._metadata[document_type][name] = metadata or {}

    def get_agent(self, document_type: str, name: str) -> Optional[Agent]:
        """Get a specific agent by name."""
        return self._agents.get(document_type, {}).get(name)

    def get_agents(self, document_type: str, names: Optional[list[str]] = None) -> Dict[str, Agent]:
        """Get agents for document type.

        Args:
            document_type: Type of document ('report' or 'article')
            names: Optional list of specific agent names. If None, returns all.

        Returns:
            Dictionary mapping agent names to Agent instances
        """
        all_agents = self._agents.get(document_type, {})

        if names is None:
            return all_agents

        return {name: all_agents[name] for name in names if name in all_agents}

    def list_available(self, document_type: Optional[str] = None) -> Dict[str, list[Dict[str, Any]]]:
        """List all available agents with metadata."""
        result = {}

        types = [document_type] if document_type else ["report", "article"]

        for dtype in types:
            agents_info = []
            for name, agent in self._agents.get(dtype, {}).items():
                # Safely get output schema name
                output_schema = None
                if hasattr(agent, "output_type"):
                    output_type = agent.output_type
                    if isinstance(output_type, NativeOutput):
                        # NativeOutput wraps the actual output types
                        if output_type.name:
                            output_schema = output_type.name
                        elif hasattr(output_type, "outputs"):
                            # Try to get name from the wrapped outputs
                            if hasattr(output_type.outputs, "__name__"):
                                output_schema = output_type.outputs.__name__
                    elif hasattr(output_type, "__name__"):
                        output_schema = output_type.__name__

                info = {
                    "name": name,
                    "output_schema": output_schema,
                    **self._metadata[dtype].get(name, {}),
                }
                agents_info.append(info)

            result[dtype] = agents_info

        return result


# ============================================================================
# GLOBAL REGISTRY & INITIALIZATION
# ============================================================================

_global_agent_registry = None


def get_agent_registry() -> AgentRegistry:
    """Get the global agent registry with all agents loaded."""
    global _global_agent_registry

    if _global_agent_registry is None:
        registry = AgentRegistry()
        factory = AgentFactory()

        # Register article agents
        registry.register(
            "article",
            "simple_article_agent",
            factory.create_simple_article_agent(),
            metadata={
                "description": "Quick article assessment - fast overview",
                "output_type": "SimpleArticleEvaluation",
            },
        )

        registry.register(
            "article",
            "detailed_article_agent",
            factory.create_detailed_article_agent(),
            metadata={
                "description": "Comprehensive article analysis - detailed breakdown",
                "output_type": "DetailedArticleEvaluation",
            },
        )

        # Register report agents
        registry.register(
            "report",
            "simple_report_agent",
            factory.create_simple_report_agent(),
            metadata={"description": "Basic Frascati R&D evaluation", "output_type": "SimpleReportEvaluation"},
        )

        registry.register(
            "report",
            "frascati_classifier_agent",
            factory.create_frascati_classifier_agent(),
            metadata={
                "description": "Focused R&D classifier - distinguishes knowledge creation from application based on expert patterns",
                "output_type": "FrascatiClassifierEvaluation",
            },
        )

        registry.register(
            "report",
            "detailed_report_agent",
            factory.create_detailed_report_agent(),
            metadata={
                "description": "Comprehensive Frascati analysis - full 5-criteria breakdown with evidence",
                "output_type": "DetailedReportEvaluation",
            },
        )

        registry.register(
            "report",
            "mtep_agent",
            create_mtep_agent(),
            metadata={
                "description": "MTEP evaluation agent - Lithuanian R&D standard evaluation with strict criteria",
                "output_type": "MTEPVertinimas",
            },
        )

        _global_agent_registry = registry

    return _global_agent_registry


# Convenience function for backward compatibility
def get_default_agent(document_type: str = "report") -> Agent:
    """Get default agent for a document type."""
    registry = get_agent_registry()
    agents = registry.get_agents(document_type)

    if not agents:
        raise ValueError(f"No agents configured for {document_type}")

    # Return first agent as default
    return next(iter(agents.values()))
