"""FastAPI server for document evaluation.

Two evaluation approaches:
1. Agent-based evaluation - Flexible, can return different structured outputs
2. Scoring-based evaluation - Standardized LLM judge scores across multiple criteria
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated, Any, Dict, Optional

from fastapi import Depends, FastAPI, File, HTTPException, Query, Security, UploadFile
from fastapi.security import APIKeyHeader
from markitdown import MarkItDown
from pydantic import BaseModel, Field
from pydantic_evals import Dataset

from ataskaitos.agent import agent
from ataskaitos.evals import RDActivity, convert_results, do, evaluators

# Environment and security configuration
ENV = os.getenv("ENV", "development")
API_KEY = os.getenv("API_KEY", "")
REQUIRE_AUTH = ENV != "development"

# API Key security scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    """
    Verify API key for protected endpoints.

    In development (ENV=development): Authentication is disabled
    In production (ENV=production): X-API-Key header is required
    """
    if not REQUIRE_AUTH:
        # Development mode - no authentication required
        return True

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not configured on server")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="X-API-Key header required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return True


app = FastAPI(
    title="Ataskaitos API",
    description="AI-powered platform for scientific research report writing",
    version="0.1.0",
)

md_converter = MarkItDown()


# Response models for different evaluation types


class BaseEvaluationResponse(BaseModel):
    """Base response model for all evaluations."""

    markdown_content: str = Field(description="Converted markdown text from document")
    evaluation_type: str = Field(description="Type of evaluation performed")
    status: str = Field(default="success", description="Response status")


class AgentEvaluationResponse(BaseEvaluationResponse):
    """Response from agent-based evaluation - flexible structured output."""

    agent_output: str = Field(description="Agent evaluation output (can be structured or text)")
    evaluation_type: str = Field(default="agent")


class ScoringEvaluationResponse(BaseEvaluationResponse):
    """Response from scoring-based evaluation - standardized scores."""

    evaluation_results: Dict[str, Any] = Field(
        description="Standardized evaluation scores and reasons from multiple evaluators"
    )
    evaluation_type: str = Field(default="scoring")


class EvaluatorsListResponse(BaseModel):
    """Response from /evaluators/list endpoint."""

    total_evaluators: int = Field(description="Total number of evaluators")
    evaluators: list[Dict[str, Any]] = Field(description="List of evaluator specifications")
    framework: str = Field(description="Evaluation framework used")
    source: str = Field(description="Source of evaluators")
    filter: Optional[Dict[str, str]] = Field(None, description="Applied filters")


class HealthCheckResponse(BaseModel):
    """Response from /health endpoint."""

    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
    version: str = Field(description="API version")
    evaluation_methods: list[str] = Field(description="Available evaluation methods")
    environment: str = Field(description="Current environment")
    authentication_required: bool = Field(description="Whether authentication is required")


class RootResponse(BaseModel):
    """Response from root endpoint."""

    message: str = Field(description="Welcome message")
    status: str = Field(description="Service status")


@app.get("/", response_model=RootResponse)
async def root():
    """Root endpoint with basic service information."""
    return RootResponse(message="Ataskaitos API is running", status="healthy")


@app.post("/evaluate/agent", response_model=AgentEvaluationResponse)
async def evaluate_with_agent(
    file: Annotated[UploadFile, File(description="Document file to evaluate (DOCX, PDF, etc.)")],
    authenticated: bool = Depends(verify_api_key),
):
    """
    Agent-based evaluation: Single AI agent analyzes the document.

    **Approach**: Uses PydanticAI agent that can return flexible structured outputs.
    The agent can be configured to return different schemas (e.g., FrascatiEvaluation
    with specific fields, or plain text analysis).

    **Use case**: When you need comprehensive qualitative analysis with flexible output format.

    **Returns**:
    - markdown_content: The converted markdown text
    - agent_output: The agent's evaluation (format depends on agent configuration)
    - evaluation_type: "agent"
    """
    markdown_content = await _convert_file_to_markdown(file)

    try:
        # Pass to evaluation agent
        evaluation_result = agent.run_sync(
            f"""
            Evaluate the following document according to Frascati Manual criteria.

            {markdown_content}
            """
        )

        return AgentEvaluationResponse(
            markdown_content=markdown_content,
            agent_output=evaluation_result.output,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during agent evaluation: {str(e)}")


@app.post("/evaluate/scoring", response_model=ScoringEvaluationResponse)
async def evaluate_with_scoring(
    file: Annotated[UploadFile, File(description="Document file to evaluate (DOCX, PDF, etc.)")],
    authenticated: bool = Depends(verify_api_key),
):
    """
    Scoring-based evaluation: Multiple LLM judges score against standardized criteria.

    **Approach**: Uses pydantic-evals framework with multiple LLMJudge evaluators.
    Each evaluator scores the document on a 0.0-1.0 scale with detailed reasoning.

    **Evaluators included** (from evals.py):
    - short_evaluator: Basic Frascati R&D check (3 core conditions)
    - combined_score: All 5 Frascati criteria combined (0.2 per criterion)
    - novelty_score: Individual novelty assessment (0.0-1.0)
    - creativity_score: Individual creativity assessment (0.0-1.0)
    - uncertainty_score: Individual uncertainty assessment (0.0-1.0)
    - systematic_score: Individual systematic planning assessment (0.0-1.0)
    - transferable_score: Individual transferability assessment (0.0-1.0)
    - comprehensive_rd_score: Full Frascati Manual evaluation with all 6 parts

    **Use case**: When you need quantitative scores for comparison, benchmarking,
    or consistent evaluation across multiple documents.

    **Returns**:
    - markdown_content: The converted markdown text
    - evaluation_results: Standardized scores with reasons, metrics, and durations
    - evaluation_type: "scoring"
    """
    markdown_content = await _convert_file_to_markdown(file)

    try:
        # Create a temporary dataset with this document
        # Pass the LLMJudge evaluators directly (Dataset accepts Evaluator instances)
        temp_dataset = Dataset(
            cases=[],
            evaluators=evaluators,  # Use evaluators from evals.py
        )

        # Add the document as a case
        temp_dataset.add_case(
            name=file.filename or "uploaded_file",
            inputs=RDActivity(description=markdown_content),
            metadata={
                "source_file": file.filename,
                "character_count": len(markdown_content),
            },
        )

        # Run comprehensive evaluation (use async version)
        eval_results = await temp_dataset.evaluate(do)

        # Convert results to JSON-serializable format
        results_data = convert_results(eval_results)

        return ScoringEvaluationResponse(markdown_content=markdown_content, evaluation_results=results_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during scoring evaluation: {str(e)}")


@app.get("/evaluators/list", response_model=EvaluatorsListResponse)
async def list_evaluators(
    evaluation_name: Optional[str] = Query(None, description="Filter by evaluation_name (unique identifier)"),
):
    """
    List all available evaluators in the scoring system.

    Dynamically reads from the actual evaluators configured in evals.py.
    Returns information about each evaluator including their specifications.

    **Filter by evaluation_name**: Pass `?evaluation_name=short_evaluator` to get a specific evaluator.
    """
    evaluators_info = []

    for evaluator in evaluators:
        print(f"Checking evaluator: {getattr(evaluator, 'score', None)}")
        # Use the built-in as_spec method for clean serialization
        spec = evaluator.as_spec()

        # Filter by evaluation_name if provided
        if evaluation_name:
            # Extract evaluation_name from score config
            score_config = getattr(evaluator, "score", None)
            if score_config and isinstance(score_config, dict):
                eval_name = score_config.get("evaluation_name")
                if eval_name != evaluation_name:
                    continue  # Skip this evaluator
            else:
                continue  # Skip if no score config

        # Convert EvaluatorSpec to dict for JSON serialization
        evaluators_info.append(spec.model_dump() if hasattr(spec, "model_dump") else dict(spec))

    return EvaluatorsListResponse(
        total_evaluators=len(evaluators_info),
        evaluators=evaluators_info,
        framework="pydantic-evals with LLMJudge",
        source="ataskaitos.evals.evaluators",
        filter={"evaluation_name": evaluation_name} if evaluation_name else None,
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Detailed health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        service="ataskaitos-api",
        version="0.1.0",
        evaluation_methods=["agent", "scoring"],
        environment=ENV,
        authentication_required=REQUIRE_AUTH,
    )


# Helper functions


async def _convert_file_to_markdown(file: UploadFile) -> str:
    """Convert uploaded file to markdown text."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    supported_formats = {".docx", ".pdf", ".doc", ".txt", ".md"}

    if file_ext not in supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_ext}. Supported formats: {', '.join(supported_formats)}",
        )

    try:
        # Save uploaded file to temporary location
        with NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = Path(tmp_file.name)

        # Convert to markdown
        try:
            result = md_converter.convert(str(tmp_path))
            return result.text_content
        finally:
            # Clean up temp file
            tmp_path.unlink(missing_ok=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file to markdown: {str(e)}") from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
