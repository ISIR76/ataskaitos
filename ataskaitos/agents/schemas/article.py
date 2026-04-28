"""Article evaluation schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class SimpleArticleEvaluation(BaseModel):
    """Simple article evaluation - quick overview."""

    overall_quality: float = Field(ge=0.0, le=1.0, description="Overall publication quality (0.0-1.0)")
    meets_standards: bool = Field(description="Does this meet academic publication standards?")
    summary: str = Field(description="Brief 2-3 sentence summary of evaluation")
    key_issues: list[str] = Field(max_length=3, description="Top 3 issues or concerns (if any)")


class DetailedArticleEvaluation(BaseModel):
    """Detailed article evaluation - comprehensive analysis."""

    overall_score: float = Field(ge=0.0, le=1.0, description="Overall publication quality score (0.0-1.0)")
    meets_standards: bool = Field(description="Meets academic publication standards?")

    # Component scores
    scientific_apparatus_score: float = Field(
        ge=0.0, le=1.0, description="Quality of references, methodology, data, technical content"
    )
    novelty_score: float = Field(ge=0.0, le=1.0, description="Level of scientific novelty and contribution")
    rigor_score: float = Field(ge=0.0, le=1.0, description="Methodological rigor and argumentation quality")

    # Qualitative assessment
    summary: str = Field(description="Comprehensive evaluation summary (3-5 sentences)")
    strengths: list[str] = Field(min_length=2, max_length=4, description="2-4 key strengths")
    weaknesses: list[str] = Field(min_length=2, max_length=4, description="2-4 key weaknesses or areas for improvement")
    publication_type: str = Field(
        description="Most likely publication type (journal article, conference, monograph, etc.)"
    )


class LLMDetectionResult(BaseModel):
    """Result of running an LLM-authorship detector on an article."""

    ai_probability: float = Field(
        ge=0.0, le=1.0, description="Estimated probability the text is AI/LLM-generated"
    )
    verdict: Literal["likely_human", "uncertain", "likely_ai"] = Field(
        description="Coarse verdict bucket derived from ai_probability"
    )
    reasoning: str = Field(
        description="2-4 sentence justification, citing the most decisive observations"
    )
    indicators: list[str] = Field(
        min_length=1,
        max_length=8,
        description="Specific stylistic, structural, or content signals that informed the verdict",
    )
