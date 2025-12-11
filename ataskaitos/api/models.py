"""API request and response models."""

from datetime import datetime
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


# Project management models


class CreateProjectRequest(BaseModel):
    """Request to create a new project."""

    name: str = Field(description="Project name (must be unique)")
    project_type: Literal["straipsnis", "ataskaita"] = Field(description="Type of project")


class ProjectResponse(BaseModel):
    """Response for a project."""

    id: int = Field(description="Project ID")
    name: str = Field(description="Project name")
    project_type: str = Field(description="Project type")
    active_version_id: int | None = Field(description="Active version ID")
    active_version_number: int | None = Field(description="Active version number")
    total_versions: int = Field(description="Total number of versions")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class ProjectListResponse(BaseModel):
    """Response for list of projects."""

    projects: list[ProjectResponse] = Field(description="List of projects")
    total: int = Field(description="Total number of projects")


class DocumentVersionResponse(BaseModel):
    """Response for a document version."""

    id: int = Field(description="Version ID")
    project_id: int = Field(description="Project ID")
    version_number: int = Field(description="Version number")
    original_filename: str = Field(description="Original filename")
    character_count: int = Field(description="Character count")
    evaluation_count: int = Field(description="Number of evaluations")
    is_active: bool = Field(description="Whether this is the active version")
    created_at: datetime = Field(description="Creation timestamp")


class DocumentVersionDetailResponse(DocumentVersionResponse):
    """Response for a document version with markdown content."""

    markdown_content: str = Field(description="Markdown content of the document")


class EvaluationHistoryItem(BaseModel):
    """Response for an evaluation in history list."""

    id: int = Field(description="Evaluation database ID")
    evaluation_id: str = Field(description="Evaluation UUID")
    evaluation_type: str = Field(description="Type of evaluation")
    evaluators_used: list[str] = Field(description="List of evaluators used")
    status: str = Field(description="Evaluation status")
    duration_seconds: float = Field(description="Duration in seconds")
    created_at: datetime = Field(description="Creation timestamp")


class EvaluationDetailResponse(EvaluationHistoryItem):
    """Response for an evaluation with full results."""

    results: dict[str, Any] = Field(description="Full evaluation results")
