"""Health check and information endpoints."""

from fastapi import APIRouter, Depends, Request

from ataskaitos.api.dependencies import ENV, get_evaluator_registry
from ataskaitos.api.models import (
    EvaluatorInfo,
    EvaluatorsListResponse,
    HealthCheckResponse,
    RootResponse,
)
from ataskaitos.evaluators import EvaluatorRegistry
from ataskaitos.settings import settings

router = APIRouter(prefix="/api", tags=["Health & Info"])


@router.get("/", response_model=RootResponse)
async def root():
    """Root endpoint with basic service information."""
    return RootResponse(
        message="Ataskaitos API - AI-powered evaluation platform",
        status="healthy",
        version=settings.api_version,
        docs_url="/api/docs",
    )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Detailed health check endpoint with service configuration."""
    return HealthCheckResponse(
        status="healthy",
        service=settings.service_name,
        version=settings.api_version,
        evaluation_methods=["agent", "scoring"],
        document_types=["report", "article"],
        environment=ENV,
        authentication_required=True,  # FastAPI-Users authentication is always required
    )


@router.get("/cors-test")
async def cors_test(request: Request):
    """Test endpoint to verify CORS is working correctly."""
    return {
        "message": "CORS is working!",
        "origin": request.headers.get("origin"),
        "method": request.method,
        "cors_enabled": True,
    }


@router.get("/v1/evaluators", response_model=EvaluatorsListResponse)
async def list_evaluators(
    registry: EvaluatorRegistry = Depends(get_evaluator_registry),
):
    """List all available evaluators grouped by document type.

    Returns information about each evaluator including:
    - Name
    - Source file/module
    - Whether it has assertions
    - Additional metadata

    Useful for discovering what evaluators are available and how to use them.
    """
    # Get all evaluators from registry
    available = registry.list_available()

    # Convert to EvaluatorInfo models
    evaluators_by_type = {}
    total_count = 0

    for doc_type, evaluators_list in available.items():
        evaluators_info = [
            EvaluatorInfo(
                name=eval_dict["name"],
                source=eval_dict.get("source"),
                has_assertion=eval_dict.get("has_assertion", False),
                rubric=eval_dict.get("rubric"),
                metadata={k: v for k, v in eval_dict.items() if k not in ["name", "source", "has_assertion", "rubric"]},
            )
            for eval_dict in evaluators_list
        ]
        evaluators_by_type[doc_type] = evaluators_info
        total_count += len(evaluators_info)

    return EvaluatorsListResponse(
        evaluators=evaluators_by_type,
        total_evaluators=total_count,
        document_types=list(evaluators_by_type.keys()),
    )


@router.get("/v1/agents")
async def list_agents():
    """List all available agents grouped by document type.

    Returns information about each agent including:
    - Name
    - Description
    - Output schema type
    - Additional metadata

    Useful for discovering what agents are available for agent-based evaluation.
    """
    try:
        from ataskaitos.agents import get_agent_registry

        agent_registry = get_agent_registry()
        available = agent_registry.list_available()

        return {"agents": available, "total_count": sum(len(agents) for agents in available.values())}
    except ImportError:
        return {"agents": {"report": [], "article": []}, "total_count": 0}
