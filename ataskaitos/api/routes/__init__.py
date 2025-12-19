"""API route modules."""

from .auth import router as auth_router
from .evaluate import router as evaluate_router
from .health import router as health_router
from .projects import router as projects_router

__all__ = [
    "health_router",
    "evaluate_router",
    "projects_router",
    "auth_router",
]
