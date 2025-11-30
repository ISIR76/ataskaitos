"""Batch evaluation service for running multiple agents on multiple documents."""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from markitdown import MarkItDown
from pydantic import BaseModel, ConfigDict


class DocumentInput(BaseModel):
    """A document converted to markdown for evaluation."""

    file_path: str
    content: str


class AgentConfig(BaseModel):
    """Configuration for an agent with its model."""

    agent_name: str
    model: object
    model_name: str


class EvaluationTask(BaseModel):
    """Single evaluation task: one agent × one input."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    input: DocumentInput
    agent_config: AgentConfig


class ResultModel(BaseModel):
    """Result of a single evaluation."""

    file: str
    model: str
    evaluation: dict | None = None
    error: str | None = None


class OutputDataModel(BaseModel):
    """Complete output data for batch evaluation."""

    timestamp: str
    agent: str
    total_files: int
    total_models: int
    results: list[ResultModel]


class BatchEvaluator:
    """Service for batch evaluation of documents with multiple agents."""

    def __init__(self, agent_factory_fn, output_dir: Path | None = None):
        """Initialize batch evaluator.

        Args:
            agent_factory_fn: Function that creates an agent instance (e.g., create_mtep_agent)
            output_dir: Directory to save results (default: docs/out/reports/agent_evaluations)
        """
        self.agent_factory_fn = agent_factory_fn
        self.output_dir = output_dir or Path("docs/out/reports/agent_evaluations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.md_converter = MarkItDown()

    def build_inputs(self, files: list[str]) -> list[DocumentInput]:
        """Build document inputs by converting files to markdown."""
        print("\n" + "=" * 80)
        print("STEP 1: Building inputs")
        print("=" * 80)

        inputs = []
        for file_path in files:
            print(f"  Converting: {file_path}")
            try:
                md_result = self.md_converter.convert(file_path)
                content = md_result.text_content

                inputs.append(
                    DocumentInput(
                        file_path=file_path,
                        content=content,
                    )
                )
                print(f"    ✓ Converted ({len(content)} chars)")
            except Exception as e:
                print(f"    ✗ Error: {e}")

        print(f"\n✓ Built {len(inputs)} document inputs")
        return inputs

    def build_agent_configs(self, models: list, agent_name: str = "agent") -> list[AgentConfig]:
        """Build agent configurations from models.

        Args:
            models: List of model instances
            agent_name: Name of the agent (default: "agent")
        """
        return [
            AgentConfig(
                agent_name=agent_name,
                model=model,
                model_name=model.model_name,
            )
            for model in models
        ]

    def create_evaluation_matrix(
        self,
        inputs: list[DocumentInput],
        agent_configs: list[AgentConfig],
    ) -> list[EvaluationTask]:
        """Create evaluation matrix: all agents × all inputs."""
        print("\n" + "=" * 80)
        print("STEP 2: Building evaluation matrix")
        print("=" * 80)

        tasks = []
        for agent_config in agent_configs:
            for doc_input in inputs:
                tasks.append(EvaluationTask(input=doc_input, agent_config=agent_config))

        print(f"✓ Created {len(tasks)} evaluation tasks")
        print(f"  {len(agent_configs)} agents × {len(inputs)} inputs")
        return tasks

    async def _execute_single_task(
        self,
        task: EvaluationTask,
        task_id: int,
        total: int,
        semaphore: asyncio.Semaphore,
    ) -> ResultModel:
        """Execute a single evaluation task with concurrency control."""
        async with semaphore:
            file_name = Path(task.input.file_path).name
            model_name = task.agent_config.model_name

            print(f"[{task_id}/{total}] ▶ Started: {file_name} ({model_name})")

            try:
                # Create agent with specific model
                agent = self.agent_factory_fn(model=task.agent_config.model)

                result = await agent.run(task.input.content)
                result_model = ResultModel(
                    file=task.input.file_path,
                    model=task.agent_config.model_name,
                    evaluation=result.output.model_dump(),
                )

                score = result.output.score if hasattr(result.output, "score") else "N/A"
                print(f"[{task_id}/{total}] ✓ Finished: {file_name} ({model_name}) - Score: {score}")

                return result_model
            except Exception as e:
                print(f"[{task_id}/{total}] ✗ Failed: {file_name} ({model_name}) - {e}")
                return ResultModel(
                    file=task.input.file_path,
                    model=task.agent_config.model_name,
                    error=str(e),
                )

    async def execute_evaluations(
        self,
        tasks: list[EvaluationTask],
        max_concurrent: int = 5,
    ) -> list[ResultModel]:
        """Execute evaluation tasks in parallel with concurrency limit.

        Args:
            tasks: List of evaluation tasks to execute
            max_concurrent: Maximum number of concurrent tasks (default: 5)
        """
        print("\n" + "=" * 80)
        print("STEP 3: Executing evaluations (async)")
        print("=" * 80)
        print(f"Total tasks: {len(tasks)}")
        print(f"Max concurrent: {max_concurrent}")
        print("=" * 80 + "\n")

        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        # Execute all tasks concurrently with semaphore
        results = await asyncio.gather(
            *[self._execute_single_task(task, idx + 1, len(tasks), semaphore) for idx, task in enumerate(tasks)]
        )

        # Print summary by agent
        print(f"\n{'=' * 80}")
        print("Execution Summary")
        print("=" * 80)

        by_agent = {}
        for result in results:
            if result.model not in by_agent:
                by_agent[result.model] = {"success": 0, "error": 0}
            if result.error:
                by_agent[result.model]["error"] += 1
            else:
                by_agent[result.model]["success"] += 1

        for agent_name, counts in by_agent.items():
            total = counts["success"] + counts["error"]
            print(f"  {agent_name}: {counts['success']}/{total} succeeded, {counts['error']} errors")

        return list(results)

    def save_results(
        self,
        results: list[ResultModel],
        agent_name: str,
        total_files: int,
        total_models: int,
    ) -> tuple[Path, Path]:
        """Save evaluation results to JSON files.

        Args:
            results: List of evaluation results
            agent_name: Name of the agent used
            total_files: Total number of files evaluated
            total_models: Total number of models used

        Returns:
            Tuple of (timestamped_file_path, latest_file_path)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"agent_evaluation_{timestamp}.json"
        latest_file = self.output_dir / "agent_evaluation_latest.json"

        output_data = OutputDataModel(
            timestamp=datetime.now().isoformat(),
            agent=agent_name,
            total_files=total_files,
            total_models=total_models,
            results=results,
        )

        # Write timestamped file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data.model_dump(), f, indent=2, default=str, ensure_ascii=False)

        # Write latest file
        with open(latest_file, "w", encoding="utf-8") as f:
            json.dump(output_data.model_dump(), f, indent=2, default=str, ensure_ascii=False)

        return output_file, latest_file

    async def run_batch_evaluation(
        self,
        files: list[str],
        models: list,
        agent_name: str = "agent",
        max_concurrent: int = 5,
    ) -> tuple[list[ResultModel], Path, Path]:
        """Run complete batch evaluation.

        Args:
            files: List of file paths to evaluate
            models: List of model instances to use
            agent_name: Name of the agent (default: "agent")
            max_concurrent: Maximum concurrent tasks (default: 5)

        Returns:
            Tuple of (results, timestamped_file_path, latest_file_path)
        """
        print(f"Evaluating {len(files)} files with {len(models)} models...")

        # Step 1: Build document inputs
        inputs = self.build_inputs(files)

        # Step 2: Build agent configurations
        agent_configs = self.build_agent_configs(models, agent_name)

        # Step 3: Create evaluation matrix (agents × inputs)
        tasks = self.create_evaluation_matrix(inputs, agent_configs)

        # Step 4: Execute evaluations
        results = await self.execute_evaluations(tasks, max_concurrent)

        # Step 5: Save results
        output_file, latest_file = self.save_results(results, agent_name, len(files), len(models))

        print("\n" + "=" * 80)
        print("✓ Results saved to:")
        print(f"  {output_file}")
        print(f"  {latest_file}")
        print(f"  Total files: {len(files)}")
        print(f"  Total models: {len(models)}")

        return results, output_file, latest_file
