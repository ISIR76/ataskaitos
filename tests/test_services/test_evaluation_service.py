"""Tests for EvaluationService."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic_ai import models

from ataskaitos.services.evaluation_service import EvaluationService

pytestmark = pytest.mark.anyio
models.ALLOW_MODEL_REQUESTS = False


@pytest.fixture
def mock_registry():
    """Create a mock EvaluatorRegistry."""
    registry = MagicMock()
    registry.get_evaluators.return_value = {"test_evaluator": MagicMock(name="test_evaluator")}
    registry.list_available.return_value = {"article": [{"name": "test_evaluator"}]}
    return registry


@pytest.fixture
def mock_agent_registry():
    """Create a mock AgentRegistry."""
    registry = MagicMock()
    mock_agent = MagicMock()
    registry.get_agents.return_value = {"test_agent": mock_agent}
    registry.list_available.return_value = {"article": ["test_agent"]}
    return registry


class TestEvaluationService:
    """Test EvaluationService functionality."""

    async def test_evaluate_with_scoring_mode(self, mock_registry):
        """Test evaluation using scoring mode with mock evaluators."""
        # Arrange
        service = EvaluationService(registry=mock_registry)
        content = "# Test Document\n\nSome content."

        # Mock dataset evaluation
        with patch("ataskaitos.services.evaluation_service.Dataset") as MockDataset:
            mock_dataset = MagicMock()
            mock_eval_report = MagicMock()
            mock_eval_report.averages.return_value = MagicMock(scores={}, metrics={})
            mock_eval_report.cases = []
            mock_eval_report.failures = []
            mock_eval_report.name = "test_evaluation"

            mock_dataset.evaluate = AsyncMock(return_value=mock_eval_report)
            MockDataset.return_value = mock_dataset

            # Act
            result = await service.evaluate_document(
                content=content, document_type="article", evaluation_type="scoring", evaluator_names=["test_evaluator"]
            )

            # Assert
            assert result is not None
            assert result.status == "success"
            assert result.evaluation_type == "scoring"
            mock_registry.get_evaluators.assert_called_once()

    async def test_evaluate_with_agent_mode(self, mock_registry, mock_agent_registry):
        """Test evaluation using agent mode with mock agent."""
        # Arrange
        service = EvaluationService(registry=mock_registry, agent_registry=mock_agent_registry)
        content = "# Research Article\n\nMethodology section..."

        # Mock agent result
        mock_agent = mock_agent_registry.get_agents.return_value["test_agent"]
        mock_result = MagicMock()
        mock_result.output = MagicMock()
        mock_result.output.model_dump.return_value = {"overall_score": 0.9, "summary": "Excellent research quality"}
        mock_agent.run = AsyncMock(return_value=mock_result)

        # Act
        result = await service.evaluate_document(
            content=content, document_type="article", evaluation_type="agent", agent_names=["test_agent"]
        )

        # Assert
        assert result is not None
        assert result.status == "success"
        assert result.evaluation_type == "agent"
        assert "agent_evaluations" in result.results
        mock_agent.run.assert_called_once()

    async def test_evaluate_document_no_evaluators_found(self, mock_registry):
        """Test error handling when no evaluators are found."""
        # Arrange
        service = EvaluationService(registry=mock_registry)
        mock_registry.get_evaluators.return_value = {}
        content = "# Test Document"

        # Act & Assert
        with pytest.raises(ValueError, match="No evaluators found"):
            await service.evaluate_document(
                content=content,
                document_type="article",
                evaluation_type="scoring",
                evaluator_names=["nonexistent_evaluator"],
            )
