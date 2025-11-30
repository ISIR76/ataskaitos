"""FastAPI dependencies for authentication and shared services."""

import os
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from ataskaitos.evaluators import EvaluatorRegistry, get_registry
from ataskaitos.services import DocumentService, EvaluationService

# Environment and security configuration
ENV = os.getenv("ENV", "development")
API_KEY = os.getenv("API_KEY", "")
REQUIRE_AUTH = ENV != "development"

# API Key security scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """Verify API key for protected endpoints.

    In development (ENV=development): Authentication is disabled
    In production (ENV=production): X-API-Key header is required

    Args:
        api_key: API key from X-API-Key header

    Returns:
        True if authenticated

    Raises:
        HTTPException: If authentication fails
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


def get_evaluator_registry() -> EvaluatorRegistry:
    """Get the global evaluator registry.

    Returns:
        EvaluatorRegistry instance
    """
    return get_registry()


def get_document_service() -> DocumentService:
    """Get document service instance.

    Returns:
        DocumentService instance
    """
    return DocumentService()


def get_evaluation_service() -> EvaluationService:
    """Get evaluation service instance.

    Returns:
        EvaluationService instance
    """
    registry = get_registry()

    # Import agent registry here to avoid circular imports
    try:
        from ataskaitos.agents import get_agent_registry

        agent_registry = get_agent_registry()
    except ImportError:
        agent_registry = None

    return EvaluationService(registry=registry, agent_registry=agent_registry)
