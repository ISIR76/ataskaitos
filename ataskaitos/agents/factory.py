"""Factory for creating evaluation agents."""

from pathlib import Path

from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIResponsesModel

from ataskaitos.settings import settings

from .schemas import (
    DetailedArticleEvaluation,
    DetailedReportEvaluation,
    FrascatiClassifierEvaluation,
    LLMDetectionResult,
    SimpleArticleEvaluation,
    SimpleReportEvaluation,
)


class AgentFactory:
    """Factory for creating evaluation agents."""

    _settings = ModelSettings(temperature=settings.default_temperature)
    _prompts_dir = Path(__file__).parent.parent / "prompts"

    @classmethod
    def _get_model_name(cls, model_spec: str) -> str:
        """Extract model name from 'provider:model' format."""
        return model_spec.split(":")[-1]

    @classmethod
    def _load_prompt(cls, relative_path: str) -> str:
        """Load prompt from file."""
        prompt_path = cls._prompts_dir / relative_path
        return prompt_path.read_text().strip()

    @classmethod
    def create_simple_article_agent(cls, model: Model | None = None) -> Agent[None, SimpleArticleEvaluation]:
        """Create simple article evaluation agent - quick assessment.

        Args:
            model: Optional model instance. If None, uses configured default_article_model
        """
        instructions = cls._load_prompt("articles/simple_article_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_article_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(
            model=model,
            output_type=SimpleArticleEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_llm_detector_agent(cls, model: Model | None = None) -> Agent[None, LLMDetectionResult]:
        """Create an article LLM-detection agent.

        Returns a structured estimate of whether the article was AI-generated.
        """
        instructions = cls._load_prompt("articles/llm_detector_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_article_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(
            model=model,
            output_type=LLMDetectionResult,
            instructions=instructions,
        )

    @classmethod
    def create_detailed_article_agent(cls, model: Model | None = None) -> Agent[None, DetailedArticleEvaluation]:
        """Create detailed article evaluation agent - comprehensive analysis.

        Args:
            model: Optional model instance. If None, uses configured default_article_model
        """
        instructions = cls._load_prompt("articles/detailed_article_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_article_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(
            model=model,
            output_type=DetailedArticleEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_simple_report_agent(cls, model: Model | None = None) -> Agent[None, SimpleReportEvaluation]:
        """Create simple R&D report evaluation agent.

        Args:
            model: Optional model instance. If None, uses configured default_report_model
        """
        instructions = cls._load_prompt("reports/simple_report_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_report_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(
            model=model,
            output_type=SimpleReportEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_frascati_classifier_agent(
        cls, model: Model | None = None
    ) -> Agent[None, FrascatiClassifierEvaluation]:
        """Create Frascati classifier agent - focused on R&D vs non-R&D discrimination.

        Args:
            model: Optional model instance. If None, uses configured default_report_model
        """
        instructions = cls._load_prompt("reports/frascati_classifier_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_report_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(
            model=model,
            output_type=FrascatiClassifierEvaluation,
            instructions=instructions,
        )

    @classmethod
    def create_detailed_report_agent(cls, model: Model | None = None) -> Agent[None, DetailedReportEvaluation]:
        """Create detailed R&D report evaluation agent - comprehensive Frascati analysis.

        Args:
            model: Optional model instance. If None, uses configured default_report_model
        """
        instructions = cls._load_prompt("reports/detailed_report_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_report_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(
            model=model,
            output_type=DetailedReportEvaluation,
            instructions=instructions,
        )
