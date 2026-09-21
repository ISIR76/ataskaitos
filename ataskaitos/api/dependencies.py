"""FastAPI dependencies for authentication and shared services."""

import os

from ataskaitos.auth import current_active_user
from ataskaitos.evaluators import EvaluatorRegistry, get_registry
from ataskaitos.services import DocumentService, EvaluationService

# Environment and security configuration
ENV = os.getenv("ENV", "development")

# Use FastAPI-Users authentication.
# current_active_user is a dependency that returns the authenticated User object;
# it raises 401 Unauthorized if no valid JWT token is provided. It is imported
# here purely to be re-exported, so the route modules have a single place to get
# their dependencies from. __all__ keeps linters from treating it as unused.
__all__ = [
    "ENV",
    "current_active_user",
    "get_document_service",
    "get_evaluation_service",
    "get_evaluator_registry",
]


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
