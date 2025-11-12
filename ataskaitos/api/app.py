"""FastAPI application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ataskaitos.evaluators import get_registry, initialize_default_evaluators

from .routes import evaluate_router, health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup and shutdown."""
    # Startup: Initialize evaluators
    registry = get_registry()
    initialize_default_evaluators(registry)

    print(f"✓ Loaded evaluators:")
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
        version="0.2.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000",  # Common React dev port
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health_router)
    app.include_router(evaluate_router)

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
