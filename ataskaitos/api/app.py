"""FastAPI application factory."""

from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path

import logfire
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ataskaitos.evaluators import get_registry, initialize_default_evaluators
from ataskaitos.settings import settings

from .routes import auth_router, evaluate_router, health_router, projects_router

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic()
logfire.instrument_pydantic_ai()
logger = getLogger(None)
logger.addHandler(logfire.LogfireLoggingHandler(level="DEBUG"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup and shutdown."""
    # Startup
    # 1. Initialize databases (sync and async)
    from ataskaitos.database import init_db, init_db_async

    init_db()
    await init_db_async()

    # 2. Initialize evaluators
    registry = get_registry()
    initialize_default_evaluators(registry)

    print("✓ Loaded evaluators:")
    counts = registry.count()
    for doc_type, count in counts.items():
        print(f"  - {doc_type}: {count} evaluators")

    yield

    # Shutdown: Cleanup if needed
    print("Shutting down API...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Ataskaitos API",
        description="""
        # AI-Powered Evaluation Platform

        Automated evaluation system for scientific documents using AI agents and LLM judges.

        ## Document Types

        - **Reports**: R&D activity reports evaluated against Frascati Manual standards
        - **Articles**: Scientific articles evaluated against SMSM publication standards

        ## Evaluation Methods

        - **Scoring**: Multiple LLM judges score documents on standardized criteria (0.0-1.0 scale)
        - **Agent**: Single AI agent provides comprehensive qualitative analysis

        ## Features

        - Multi-format support (DOCX, PDF, MD, TXT)
        - Configurable evaluators per document type
        - Detailed scoring with reasoning
        - Lithuanian and English support
        - Production-ready with authentication
        """,
        version=settings.api_version,
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    logfire.instrument_fastapi(app)

    # Configure CORS for authentication and API access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "X-Requested-With",
        ],
        expose_headers=["Content-Type", "Authorization"],
        max_age=settings.cors_max_age_seconds,
    )

    # Register routers
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(evaluate_router)
    app.include_router(projects_router)

    # Serve frontend static files (only if frontend/dist exists)
    frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
    if frontend_dist.exists():
        # Mount static assets (JS, CSS, images, etc.)
        app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

        # Catch-all route for SPA routing - must be last
        @app.get("/{full_path:path}")
        async def serve_spa(request: Request, full_path: str):
            """Serve the React SPA for all non-API routes."""
            # If path starts with /api, let it 404 naturally
            if full_path.startswith("api/"):
                return None

            # Check if requested file exists in dist directory
            requested_file = frontend_dist / full_path
            if requested_file.is_file():
                return FileResponse(requested_file)

            # Otherwise, serve index.html (SPA routing)
            return FileResponse(frontend_dist / "index.html")

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
