"""Evaluation orchestration service."""

import logging
from typing import Any, Dict, List, Literal, Optional

import logfire
from pydantic_evals import Dataset
from pydantic_evals.reporting import EvaluationReport

from ataskaitos.evaluators import EvaluatorRegistry
from ataskaitos.models import EvaluationResult, RDActivity, ScientificArticle

logger = logging.getLogger(__name__)


class EvaluationService:
    """Service for orchestrating document evaluations."""

    def __init__(self, registry: EvaluatorRegistry, agent_registry=None):
        """Initialize evaluation service.

        Args:
            registry: Evaluator registry with loaded evaluators
            agent_registry: Optional agent registry for agent-based evaluation
        """
        self.registry = registry
        self.agent_registry = agent_registry

    async def evaluate_document(
        self,
        content: str,
        document_type: Literal["report", "article"],
        evaluation_type: Literal["agent", "scoring"] = "scoring",
        evaluator_names: Optional[List[str]] = None,
        agent_names: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        filename: str = "document",
    ) -> EvaluationResult:
        """Evaluate document with specified method.

        Args:
            content: Markdown content of the document
            document_type: Type of document ('report' or 'article')
            evaluation_type: Evaluation method ('agent' or 'scoring')
            evaluator_names: Optional list of specific evaluators to run (for scoring)
            agent_names: Optional list of specific agents to run (for agent mode)
            metadata: Optional metadata about the document
            filename: Name of the source file

        Returns:
            EvaluationResult with scores and analysis
        """
        metadata = metadata or {}
        metadata["filename"] = filename
        metadata["character_count"] = len(content)

        if evaluation_type == "agent":
            return await self._evaluate_with_agent(content, document_type, agent_names, metadata)
        else:
            return await self._evaluate_with_scoring(content, document_type, evaluator_names, metadata, filename)

    async def _evaluate_with_agent(
        self,
        content: str,
        document_type: Literal["report", "article"],
        agent_names: Optional[List[str]],
        metadata: Dict[str, Any],
    ) -> EvaluationResult:
        """Evaluate using PydanticAI agent(s).

        Args:
            content: Markdown content
            document_type: Type of document
            agent_names: Optional list of specific agent names to run
            metadata: Document metadata

        Returns:
            EvaluationResult with agent output(s)
        """
        if not self.agent_registry:
            raise ValueError("Agent not configured for agent-based evaluation")

        # Get agents to run
        agents = self.agent_registry.get_agents(document_type, agent_names)

        if not agents:
            available = self.agent_registry.list_available(document_type)
            raise ValueError(
                f"No agents found for document type '{document_type}'. "
                f"Available: {list(available.get(document_type, []))}"
            )

        # Create evaluation prompt based on document type
        if document_type == "report":
            prompt = f"""
Evaluate the following R&D activity report according to Frascati Manual criteria.

Document:
{content}

Provide a structured evaluation covering:
- Overall R&D qualification score
- Key Frascati criteria: novelty, systematic approach, uncertainty
- Summary of findings
- Strengths and areas for improvement
"""
        else:  # article
            prompt = f"""
Evaluate the following scientific article according to SMSM publication standards.

Article:
{content}

Provide a structured evaluation covering:
- Overall publication quality
- Scientific apparatus, novelty, and rigor
- Key strengths and areas for improvement
"""

        # Run all selected agents
        agent_results = {}
        for agent_name, agent in agents.items():
            evaluation_result = await agent.run(prompt)
            agent_output = evaluation_result.output

            # Convert to dictionary
            if hasattr(agent_output, "model_dump"):
                agent_results[agent_name] = agent_output.model_dump()
            else:
                agent_results[agent_name] = str(agent_output)

        # Format results
        results_dict = {
            "agent_evaluations": agent_results,
            "agent_count": len(agent_results),
        }

        return EvaluationResult(
            document_type=document_type,
            evaluation_type="agent",
            status="success",
            markdown_content=content,
            results=results_dict,
            metadata=metadata,
        )

    async def _evaluate_with_scoring(
        self,
        content: str,
        document_type: Literal["report", "article"],
        evaluator_names: Optional[List[str]],
        metadata: Dict[str, Any],
        filename: str,
    ) -> EvaluationResult:
        """Evaluate using LLM judge scoring.

        Args:
            content: Markdown content
            document_type: Type of document
            evaluator_names: Optional specific evaluators to run
            metadata: Document metadata
            filename: Source filename

        Returns:
            EvaluationResult with scoring data
        """
        # Get evaluators from registry
        evaluators = self.registry.get_evaluators(document_type, evaluator_names)

        if not evaluators:
            available = self.registry.list_available(document_type)
            raise ValueError(
                f"No evaluators found for document type '{document_type}'. "
                f"Available: {list(available.get(document_type, {}).keys())}"
            )

        # Create appropriate input model based on document type
        if document_type == "report":
            inputs = RDActivity(description=content, metadata=metadata)
            def process_fn(x):
                return x  # Identity function for RDActivity
        else:  # article
            inputs = ScientificArticle(description=content, metadata=metadata)
            def process_fn(x):
                return x  # Identity function for ScientificArticle

        # Create temporary dataset
        temp_dataset = Dataset(cases=[], evaluators=evaluators)

        # Add document as a case
        temp_dataset.add_case(
            name=filename,
            inputs=inputs,
            metadata=metadata,
        )

        # Run evaluation
        with logfire.span("evaluate_scoring", document_type=document_type, evaluator_count=len(evaluators)):
            eval_results: EvaluationReport = await temp_dataset.evaluate(process_fn)

        # Log evaluation results
        logger.info(f"📊 Evaluation completed. Cases: {len(eval_results.cases)}")

        with logfire.span("process_eval_results", case_count=len(eval_results.cases)):
            if eval_results.cases:
                first_case = eval_results.cases[0]
                score_dict = dict(first_case.scores)
                logfire.info("Scores received from evaluation",
                            score_count=len(score_dict),
                            score_names=list(score_dict.keys()))

                logger.info(f"📈 First case scores: {score_dict}")
                logger.info(f"   Score keys: {list(first_case.scores.keys())}")
                for score_name, score_obj in first_case.scores.items():
                    logger.info(f"   - {score_name}: value={score_obj.value}, reason={score_obj.reason[:50] if score_obj.reason else 'N/A'}...")

            # Convert results to dictionary format
            results_data = self._convert_eval_results(eval_results)

            converted_scores = {}
            if results_data.get('cases'):
                converted_scores = results_data['cases'][0].get('scores', {})

            logfire.info("Results converted to dict",
                        converted_score_count=len(converted_scores),
                        converted_score_names=list(converted_scores.keys()))

            logger.info(f"🔄 Converted results_data scores: {list(converted_scores.keys())}")

        return EvaluationResult(
            document_type=document_type,
            evaluation_type="scoring",
            status="success",
            markdown_content=content,
            results=results_data,
            metadata=metadata,
        )

    def _convert_eval_results(self, result: EvaluationReport) -> Dict[str, Any]:
        """Convert EvaluationReport to JSON-serializable dictionary.

        Args:
            result: EvaluationReport from pydantic-evals

        Returns:
            Dictionary with scores, metrics, and case information
        """
        # Convert averages
        averages_data = {}
        if result.averages():
            avg = result.averages()
            averages_data = {
                "scores": avg.scores if hasattr(avg, "scores") else {},
                "metrics": avg.metrics if hasattr(avg, "metrics") else {},
                "task_duration": avg.task_duration if hasattr(avg, "task_duration") else None,
                "total_duration": avg.total_duration if hasattr(avg, "total_duration") else None,
            }

        # Convert cases
        cases_data = []
        for case in result.cases:
            case_dict = {
                "name": case.name,
                "expected_output": case.expected_output if hasattr(case, "expected_output") else None,
                "scores": {k: {"value": v.value, "reason": v.reason} for k, v in case.scores.items()},
                "metrics": case.metrics if hasattr(case, "metrics") else {},
                "task_duration": case.task_duration if hasattr(case, "task_duration") else None,
                "total_duration": case.total_duration if hasattr(case, "total_duration") else None,
            }
            cases_data.append(case_dict)

        # Convert failures
        failures_data = []
        for failure in result.failures:
            failure_dict = {
                "name": failure.name,
                "expected_output": failure.expected_output if hasattr(failure, "expected_output") else None,
                "error_message": failure.error_message if hasattr(failure, "error_message") else None,
                "error_stacktrace": failure.error_stacktrace if hasattr(failure, "error_stacktrace") else None,
            }
            failures_data.append(failure_dict)

        return {
            "name": result.name,
            "total_cases": len(result.cases),
            "total_failures": len(result.failures),
            "averages": averages_data,
            "cases": cases_data,
            "failures": failures_data,
        }
