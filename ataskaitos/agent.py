"""
DEPRECATED: Legacy agent implementation (kept for reference)

This file contains the original simple agent implementation before refactoring.

Current production implementation:
- ataskaitos/agents/factory.py (agent creation)
- ataskaitos/agents/registry.py (agent management)
- ataskaitos/agents/schemas/ (output schemas)

This file is kept for:
- Historical reference
- Understanding original design
- Comparison with refactored architecture

DO NOT USE for new development.
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIModel


# Simple MVP structured output for report evaluation
class SimpleReportEvaluation(BaseModel):
    """Simple structured evaluation result for R&D reports."""

    overall_score: float = Field(ge=0.0, le=1.0, description="Overall R&D qualification score (0.0-1.0)")
    qualifies_as_rd: bool = Field(description="Does this qualify as R&D per Frascati Manual?")
    novelty_score: float = Field(ge=0.0, le=1.0, description="Novelty/innovation level (0.0-1.0)")
    systematic_score: float = Field(ge=0.0, le=1.0, description="Systematic planning and organization (0.0-1.0)")
    uncertainty_score: float = Field(ge=0.0, le=1.0, description="Scientific/technical uncertainty (0.0-1.0)")
    summary: str = Field(description="Brief summary of the evaluation (2-3 sentences)")
    strengths: list[str] = Field(description="2-3 key strengths of the R&D activity")
    weaknesses: list[str] = Field(description="2-3 areas for improvement")


settings = ModelSettings(temperature=0)

base_instructions = """
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


class AgentFactory:
    @staticmethod
    def create_simple_report_agent(model_name: str = "gpt-4o") -> Agent[None, SimpleReportEvaluation]:
        """Create a simple agent for R&D report evaluation."""
        model = OpenAIModel(model_name, settings=settings)
        return Agent(
            model=model,
            output_type=SimpleReportEvaluation,
            system_prompt=base_instructions,
        )


# Create default agent instance
agent = AgentFactory.create_simple_report_agent()

if __name__ == "__main__":
    with open("./docs/reference_documents/energus-ataskaita.md", "r", encoding="utf-8") as f:
        doc_text = f.read()

    # Run evaluation
    result = agent.run_sync(
        f"""
        Evaluate the following document

        {doc_text}
        """
    )

    with open("frascati_evaluation_str.md", "w", encoding="utf-8") as f:
        f.write(result.output)

# # Access structured data
# evaluation: FrascatiEvaluation = result.output

# print(f"Total Score: {evaluation.total_score:.2f}")
# print(f"Classification: {evaluation.classification.value}")
# print(f"Qualifies as R&D: {evaluation.qualifies_as_rd}")
# print(f"R&D Type: {evaluation.rd_type.value}")
# print(f"\nNovelty Level: {evaluation.novelty.level.value}")
# print(f"Novelty Score: {evaluation.novelty.score}")
# print(f"Evidence: {evaluation.novelty.evidence}")
# print(f"\nUncertainty Source: {evaluation.uncertainty.uncertainty_source.value}")
# print(f"R&D Content: {evaluation.rd_content.rd_percentage}%")
# print(f"\nRecommendations:")
# for rec in evaluation.recommendations:
#     print(f"  - {rec}")

# # dump structured output as JSON
# with open("frascati_evaluation.json", "w", encoding="utf-8") as f:
#     f.write(evaluation.model_dump_json(indent=2))
