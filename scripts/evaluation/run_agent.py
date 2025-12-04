#!/usr/bin/env python
"""Minimal CLI to run batch agent evaluation.

Configure:
- DOCUMENTS: What files to evaluate
- MODELS: What models to use
- OUTPUT_DIR: Where to save results
- MAX_CONCURRENT: Parallelism limit
"""

import asyncio
import sys
from glob import glob
from pathlib import Path

from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIResponsesModel


from ataskaitos.agent_from_human import create_mtep_agent
from ataskaitos.services.batch_evaluation import BatchEvaluator

DOCUMENTS = "docs/reference_documents/ataskaitos/**/*.docx"
MODELS = [
    GoogleModel("gemini-2.5-flash-lite"),
    GoogleModel("gemini-3-pro-preview"),
    GoogleModel("gemini-2.5-flash"),
    OpenAIResponsesModel("gpt-4o"),
    OpenAIResponsesModel("gpt-5.1"),
    OpenAIResponsesModel("gpt-5.1-mini"),
    AnthropicModel("claude-sonnet-4-5"),
    AnthropicModel("claude-opus-4-5"),
]

OUTPUT_DIR = Path("docs/out/reports/agent_evaluations")
MAX_CONCURRENT = 5
AGENT_NAME = "mtep_agent"


async def main():
    """Run batch evaluation with configured settings."""
    # Parse arguments: python run_agent.py [pattern] [max_concurrent]
    pattern = sys.argv[1] if len(sys.argv) > 1 else DOCUMENTS
    max_concurrent = int(sys.argv[2]) if len(sys.argv) > 2 else MAX_CONCURRENT

    # Find files
    files = glob(pattern, recursive=True) if "*" in pattern else [pattern]

    if not files:
        print(f"No files found: {pattern}")
        sys.exit(1)

    evaluator = BatchEvaluator(agent_factory_fn=create_mtep_agent, output_dir=OUTPUT_DIR)

    await evaluator.run_batch_evaluation(
        files=files, models=MODELS, agent_name=AGENT_NAME, max_concurrent=max_concurrent
    )


if __name__ == "__main__":
    asyncio.run(main())
