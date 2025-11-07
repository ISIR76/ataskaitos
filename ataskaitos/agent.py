from email.mime import base
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models import Model
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.toolsets import combined
from ataskaitos.schemas import FrascatiEvaluation

settings = ModelSettings(temperature=0)

base_instructions = """
You are a Frascati Manual expert evaluator. Analyze activities against 
all R&D criteria and return structured evaluation data.

Score each component carefully:
- Core criteria: 0.1 each (0.5 total)
- R&D content: 0.15 max
- Innovation vs R&D: 0.1 max
- Personnel: 0.075 max
- Documentation: 0.075 max
- Exclusions: subtract penalties

Be precise with evidence and rationale.
"""

with open(
    "./prompts/ekspertai/ekspertas-komercializacijos.md", "r", encoding="utf-8"
) as f:
    commercialization_instructions = f.read()

with open("./prompts/uzduotys/greitas-perziura.md", "r", encoding="utf-8") as f:
    quick_review_instructions = f.read()

combined_instructions = (
    base_instructions
    + "\n"
    + commercialization_instructions
    + "\n"
    + quick_review_instructions
)


class AgentFactory:
    @staticmethod
    def create_frascati_agent(
        model: Model, instructions: str
    ) -> Agent[None, FrascatiEvaluation]:
        return Agent(
            model=model,
            output_type=FrascatiEvaluation,
            instructions=instructions,
        )

    @staticmethod
    def create_generic_agent(model: Model, instructions: str) -> Agent[None, str]:
        return Agent(
            model=model,
            output_type=str,
            instructions=instructions,
        )


models = [
    OpenAIResponsesModel("gpt-5", settings=settings),
    # AnthropicModel("claude-sonnet-4-5-20250929", settings=settings),
    # GoogleModel("gemini-pro-20240925", settings=settings),
]

agents = [
    AgentFactory.create_generic_agent(model, combined_instructions) for model in models
]
agent = agents[0]

if __name__ == "__main__":
    with open(
        "./docs/reference_documents/energus-ataskaita.md", "r", encoding="utf-8"
    ) as f:
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
