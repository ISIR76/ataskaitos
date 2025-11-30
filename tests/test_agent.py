"""Tests for agent module."""

import pytest
from pydantic_ai import models

pytestmark = pytest.mark.anyio
models.ALLOW_MODEL_REQUESTS = False


class TestAgent:
    """Test agent functionality."""

    def test_placeholder(self):
        """Placeholder test - TODO: Add comprehensive tests later."""
        # TODO: Test AgentFactory.create_simple_report_agent
        # TODO: Test agent evaluation with mock responses
        # TODO: Test SimpleReportEvaluation schema validation
        pass
