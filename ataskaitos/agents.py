"""Multiple agents for document evaluation with different output schemas."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIModel


# ============================================================================
# OUTPUT SCHEMAS
# ============================================================================

class SimpleArticleEvaluation(BaseModel):
    """Simple article evaluation - quick overview."""

    overall_quality: float = Field(
        ge=0.0, le=1.0,
        description="Overall publication quality (0.0-1.0)"
    )
    meets_standards: bool = Field(
        description="Does this meet academic publication standards?"
    )
    summary: str = Field(
        description="Brief 2-3 sentence summary of evaluation"
    )
    key_issues: list[str] = Field(
        max_length=3,
        description="Top 3 issues or concerns (if any)"
    )


class DetailedArticleEvaluation(BaseModel):
    """Detailed article evaluation - comprehensive analysis."""

    overall_score: float = Field(
        ge=0.0, le=1.0,
        description="Overall publication quality score (0.0-1.0)"
    )
    meets_standards: bool = Field(
        description="Meets academic publication standards?"
    )

    # Component scores
    scientific_apparatus_score: float = Field(
        ge=0.0, le=1.0,
        description="Quality of references, methodology, data, technical content"
    )
    novelty_score: float = Field(
        ge=0.0, le=1.0,
        description="Level of scientific novelty and contribution"
    )
    rigor_score: float = Field(
        ge=0.0, le=1.0,
        description="Methodological rigor and argumentation quality"
    )

    # Qualitative assessment
    summary: str = Field(
        description="Comprehensive evaluation summary (3-5 sentences)"
    )
    strengths: list[str] = Field(
        min_length=2,
        max_length=4,
        description="2-4 key strengths"
    )
    weaknesses: list[str] = Field(
        min_length=2,
        max_length=4,
        description="2-4 key weaknesses or areas for improvement"
    )
    publication_type: str = Field(
        description="Most likely publication type (journal article, conference, monograph, etc.)"
    )


class SimpleReportEvaluation(BaseModel):
    """Simple R&D report evaluation."""

    overall_score: float = Field(
        ge=0.0, le=1.0,
        description="Overall R&D qualification score (0.0-1.0)"
    )
    qualifies_as_rd: bool = Field(
        description="Does this qualify as R&D per Frascati Manual?"
    )
    novelty_score: float = Field(
        ge=0.0, le=1.0,
        description="Novelty/innovation level (0.0-1.0)"
    )
    systematic_score: float = Field(
        ge=0.0, le=1.0,
        description="Systematic planning and organization (0.0-1.0)"
    )
    uncertainty_score: float = Field(
        ge=0.0, le=1.0,
        description="Scientific/technical uncertainty (0.0-1.0)"
    )
    summary: str = Field(
        description="Brief summary of the evaluation (2-3 sentences)"
    )
    strengths: list[str] = Field(
        description="2-3 key strengths of the R&D activity"
    )
    weaknesses: list[str] = Field(
        description="2-3 areas for improvement"
    )


# ============================================================================
# AGENT FACTORY
# ============================================================================

class AgentFactory:
    """Factory for creating evaluation agents."""

    _settings = ModelSettings(temperature=0)

    @classmethod
    def create_simple_article_agent(cls) -> Agent[None, SimpleArticleEvaluation]:
        """Create simple article evaluation agent - quick assessment."""
        instructions = """
You are a scientific publication evaluator. Provide quick, actionable assessments.

Evaluate academic publications focusing on:
1. **Overall Quality**: Does this meet publication standards?
2. **Key Issues**: What are the most critical problems (if any)?

Score 0.0-1.0:
- 0.8-1.0: Excellent, publication-ready
- 0.6-0.7: Good, minor revisions needed
- 0.4-0.5: Acceptable, moderate issues
- 0.2-0.3: Weak, major problems
- 0.0-0.1: Does not meet standards

Be direct and specific. Identify the most important issues.
"""
        model = OpenAIModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=SimpleArticleEvaluation,
            system_prompt=instructions,
        )

    @classmethod
    def create_detailed_article_agent(cls) -> Agent[None, DetailedArticleEvaluation]:
        """Create detailed article evaluation agent - comprehensive analysis."""
        instructions = """
You are an expert scientific publication evaluator specializing in SMSM standards.

Provide comprehensive evaluation covering:

1. **Scientific Apparatus** (0.0-1.0):
   - References/bibliography quality and coverage
   - Methodology description and rigor
   - Technical content (formulas, diagrams, data)
   - Results presentation

2. **Novelty & Contribution** (0.0-1.0):
   - What is genuinely new?
   - Does it advance the field?
   - Is there a clear research gap addressed?

3. **Overall Rigor** (0.0-1.0):
   - Argumentation quality
   - Literature engagement
   - Methodological soundness
   - Writing quality

**Overall Score** should reflect publication readiness:
- 0.8-1.0: Excellent, high-quality publication
- 0.6-0.7: Good, meets standards
- 0.4-0.5: Acceptable, needs improvement
- 0.2-0.3: Weak, significant issues
- 0.0-0.1: Does not qualify

**Publication Type**: Infer from structure (journal article, conference paper, monograph, technical report, etc.)

Provide specific, evidence-based feedback with actionable recommendations.
"""
        model = OpenAIModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=DetailedArticleEvaluation,
            system_prompt=instructions,
        )

    @classmethod
    def create_simple_report_agent(cls) -> Agent[None, SimpleReportEvaluation]:
        """Create simple R&D report evaluation agent."""
        instructions = """
You are a Frascati Manual expert evaluator. Analyze R&D activities and provide structured evaluations.

Focus on these core Frascati criteria:
1. NOVELTY: Does it create new knowledge beyond current state-of-the-art?
2. SYSTEMATIC: Is it formally planned with defined objectives and methodology?
3. UNCERTAINTY: Are outcomes genuinely unpredictable due to scientific/technical unknowns?

Score each criterion 0.0-1.0:
- 0.8-1.0: Excellent, clearly meets criteria
- 0.6-0.7: Good, meets most requirements
- 0.4-0.5: Acceptable, some gaps
- 0.2-0.3: Weak, significant issues
- 0.0-0.1: Does not meet criteria

Overall qualification:
- qualifies_as_rd = True if overall_score >= 0.6
- qualifies_as_rd = False if overall_score < 0.6

Provide actionable, evidence-based feedback.
"""
        model = OpenAIModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=SimpleReportEvaluation,
            system_prompt=instructions,
        )


# ============================================================================
# AGENT REGISTRY
# ============================================================================

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

    def get_agents(
        self, document_type: str, names: Optional[list[str]] = None
    ) -> Dict[str, Agent]:
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

    def list_available(
        self, document_type: Optional[str] = None
    ) -> Dict[str, list[Dict[str, Any]]]:
        """List all available agents with metadata."""
        result = {}

        types = [document_type] if document_type else ["report", "article"]

        for dtype in types:
            agents_info = []
            for name, agent in self._agents.get(dtype, {}).items():
                info = {
                    "name": name,
                    "output_schema": agent.output_type.__name__ if hasattr(agent, 'output_type') else None,
                    **self._metadata[dtype].get(name, {})
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
                "output_type": "SimpleArticleEvaluation"
            }
        )

        registry.register(
            "article",
            "detailed_article_agent",
            factory.create_detailed_article_agent(),
            metadata={
                "description": "Comprehensive article analysis - detailed breakdown",
                "output_type": "DetailedArticleEvaluation"
            }
        )

        # Register report agents
        registry.register(
            "report",
            "simple_report_agent",
            factory.create_simple_report_agent(),
            metadata={
                "description": "Basic Frascati R&D evaluation",
                "output_type": "SimpleReportEvaluation"
            }
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
