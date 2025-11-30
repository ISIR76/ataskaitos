"""API request and response models."""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

# Request models


class EvaluationRequest(BaseModel):
    """Request for document evaluation."""

    document_type: Literal["report", "article"] = Field(description="Type of document to evaluate")
    evaluation_type: Literal["agent", "scoring"] = Field(default="scoring", description="Evaluation method to use")
    evaluators: Optional[List[str]] = Field(
        None, description="Specific evaluators to run (default: all for document type)"
    )
    store_result: bool = Field(default=False, description="Whether to persist evaluation result")


# Response models


class BaseEvaluationResponse(BaseModel):
    """Base response model for all evaluations."""

    evaluation_id: str = Field(description="Unique evaluation identifier")
    document_type: str = Field(description="Type of document evaluated")
    evaluation_type: str = Field(description="Type of evaluation performed")
    status: str = Field(default="success", description="Response status")
    markdown_content: str = Field(description="Converted markdown text from document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Evaluation metadata")


class ScoringEvaluationResponse(BaseEvaluationResponse):
    """Response from scoring-based evaluation with standardized scores."""

    evaluation_results: Dict[str, Any] = Field(
        description="Standardized evaluation scores and reasons from multiple evaluators"
    )


class AgentEvaluationResponse(BaseEvaluationResponse):
    """Response from agent-based evaluation with flexible output."""

    agent_output: Union[str, Dict[str, Any]] = Field(description="Agent evaluation output (can be structured or text)")


# Unified response that can handle both types
class UnifiedEvaluationResponse(BaseEvaluationResponse):
    """Unified response that can contain either scoring or agent results."""

    results: Dict[str, Any] = Field(description="Evaluation results (format depends on evaluation_type)")


# Info endpoints


class EvaluatorInfo(BaseModel):
    """Information about an evaluator."""

    name: str = Field(description="Evaluator name")
    source: Optional[str] = Field(None, description="Source file or module")
    has_assertion: bool = Field(False, description="Whether evaluator has assertions")
    rubric: Optional[str] = Field(None, description="Evaluation instructions/criteria")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional evaluator metadata")


class EvaluatorsListResponse(BaseModel):
    """Response from /evaluators/list endpoint."""

    evaluators: Dict[str, List[EvaluatorInfo]] = Field(description="Evaluators grouped by document type")
    total_evaluators: int = Field(description="Total number of evaluators")
    document_types: List[str] = Field(description="Available document types")


class HealthCheckResponse(BaseModel):
    """Response from /health endpoint."""

    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
    version: str = Field(description="API version")
    evaluation_methods: List[str] = Field(description="Available evaluation methods")
    document_types: List[str] = Field(description="Supported document types")
    environment: str = Field(description="Current environment")
    authentication_required: bool = Field(description="Whether authentication is required")


class RootResponse(BaseModel):
    """Response from root endpoint."""

    message: str = Field(description="Welcome message")
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    docs_url: str = Field(description="URL to API documentation")
