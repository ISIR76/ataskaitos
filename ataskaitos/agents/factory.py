"""Factory for creating evaluation agents."""

from pathlib import Path
from typing import Optional

from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIResponsesModel

from .schemas import (
    DetailedArticleEvaluation,
    DetailedReportEvaluation,
    FrascatiClassifierEvaluation,
    SimpleArticleEvaluation,
    SimpleReportEvaluation,
)


class AgentFactory:
    """Factory for creating evaluation agents."""

    _settings = ModelSettings(temperature=0)
    _prompts_dir = Path(__file__).parent.parent / "prompts"

    @classmethod
    def _load_prompt(cls, relative_path: str) -> str:
        """Load prompt from file."""
        prompt_path = cls._prompts_dir / relative_path
        return prompt_path.read_text().strip()

    @classmethod
    def create_simple_article_agent(cls, model: Optional[Model] = None) -> Agent[None, SimpleArticleEvaluation]:
        """Create simple article evaluation agent - quick assessment.

        Args:
            model: Optional model instance. If None, uses OpenAiResponsesModel("gpt-4o")
        """
        instructions = cls._load_prompt("articles/simple_article_agent.txt")
        if model is None:
            model = OpenAIResponsesModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=SimpleArticleEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_detailed_article_agent(cls, model: Optional[Model] = None) -> Agent[None, DetailedArticleEvaluation]:
        """Create detailed article evaluation agent - comprehensive analysis.

        Args:
            model: Optional model instance. If None, uses OpenAIResponsesModel("gpt-4o")
        """
        instructions = cls._load_prompt("articles/detailed_article_agent.txt")
        if model is None:
            model = OpenAIResponsesModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=DetailedArticleEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_simple_report_agent(cls, model: Optional[Model] = None) -> Agent[None, SimpleReportEvaluation]:
        """Create simple R&D report evaluation agent.

        Args:
            model: Optional model instance. If None, uses OpenAIResponsesModel("gpt-4o")
        """
        instructions = cls._load_prompt("reports/simple_report_agent.txt")
        if model is None:
            model = OpenAIResponsesModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=SimpleReportEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_frascati_classifier_agent(
        cls, model: Optional[Model] = None
    ) -> Agent[None, FrascatiClassifierEvaluation]:
        """Create Frascati classifier agent - focused on R&D vs non-R&D discrimination.

        Args:
            model: Optional model instance. If None, uses OpenAIResponsesModel("gpt-4o")
        """
        instructions = cls._load_prompt("reports/frascati_classifier_agent.txt")
        if model is None:
            model = OpenAIResponsesModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=FrascatiClassifierEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_detailed_report_agent(cls, model: Optional[Model] = None) -> Agent[None, DetailedReportEvaluation]:
        """Create detailed R&D report evaluation agent - comprehensive Frascati analysis.

        Args:
            model: Optional model instance. If None, uses OpenAIResponsesModel("gpt-4o")
        """
        instructions = cls._load_prompt("reports/detailed_report_agent.txt")
        if model is None:
            model = OpenAIResponsesModel("gpt-4o", settings=cls._settings)
        return Agent(
            model=model,
            output_type=DetailedReportEvaluation,
            instructions=instructions,
        )
