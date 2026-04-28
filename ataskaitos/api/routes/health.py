"""Health check and information endpoints."""

import json

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ataskaitos.api.dependencies import ENV
from ataskaitos.api.models import (
    EvaluatorInfo,
    EvaluatorsListResponse,
    HealthCheckResponse,
    RootResponse,
)
from ataskaitos.database import get_session
from ataskaitos.repositories.evaluator_repository import EvaluatorRepository
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
    session: AsyncSession = Depends(get_session),
):
    """List active evaluators grouped by document type.

    Reads from the DB-backed ``evaluators`` table so picker UIs reflect any
    runtime edits made through the settings page. Inactive evaluators are
    omitted because they are not selectable for evaluation runs.
    """
    repo = EvaluatorRepository(session)
    rows = await repo.list_all()

    evaluators_by_type: dict[str, list[EvaluatorInfo]] = {"article": [], "report": []}
    total_count = 0
    for row in rows:
        if not row.is_active:
            continue
        try:
            meta = json.loads(row.extra_metadata or "{}")
        except json.JSONDecodeError:
            meta = {}
        evaluators_by_type.setdefault(row.document_type, []).append(
            EvaluatorInfo(
                name=row.name,
                source=row.source,
                has_assertion=bool(row.has_assertion),
                rubric=row.rubric,
                metadata=meta,
            )
        )
        total_count += 1

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
