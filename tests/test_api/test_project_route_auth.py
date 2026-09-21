"""Tests that project routes are unreachable without authentication.

Every route under /api/v1/projects exposes project-scoped data: documents a
user uploaded, their converted markdown, and their evaluation results. None of
it may be readable, mutable or destroyable by an anonymous caller.

The app is wired to a throwaway in-memory database and stubbed services, so an
unauthenticated request that *does* reach a handler fails fast instead of
touching a real database or calling a model provider.
"""

from unittest.mock import MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic_ai import models
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from ataskaitos.api.app import create_app
from ataskaitos.api.dependencies import get_document_service, get_evaluation_service
from ataskaitos.database import get_session
from ataskaitos.models.database import Base

pytestmark = pytest.mark.anyio

# Belt and braces: no test here may reach a model provider.
models.ALLOW_MODEL_REQUESTS = False

# Built once at import: create_app() loads the evaluator registry, which is far
# too slow to repeat per test case.
app = create_app()

# No request bodies are sent. FastAPI resolves security dependencies before it
# validates the body, so a protected route answers 401 rather than 422 even when
# required fields are missing -- confirmed by the already-protected routes below.

# Routes that read or mutate project-scoped data.
PROJECT_DATA_ROUTES = [
    ("GET", "/api/v1/projects/1", {}),
    ("DELETE", "/api/v1/projects/1", {}),
    ("POST", "/api/v1/projects/1/versions", {}),
    ("GET", "/api/v1/projects/1/versions", {}),
    ("GET", "/api/v1/projects/1/versions/1", {}),
    ("GET", "/api/v1/projects/1/versions/1/markdown", {}),
    ("POST", "/api/v1/projects/1/versions/1/set-active", {}),
    ("DELETE", "/api/v1/projects/1/versions/1", {}),
    ("POST", "/api/v1/projects/1/versions/1/evaluate", {}),
    ("GET", "/api/v1/projects/1/versions/1/evaluations", {}),
    ("GET", "/api/v1/projects/1/evaluations/some-evaluation-id", {}),
]

# Routes that already required an authenticated caller. Listed so that a
# refactor cannot silently drop the dependency again.
ALREADY_PROTECTED_ROUTES = [
    ("POST", "/api/v1/projects", {}),
    ("GET", "/api/v1/projects", {}),
    ("GET", "/api/v1/projects/scores-grid", {}),
    ("PATCH", "/api/v1/projects/1/marked-good", {}),
    ("POST", "/api/v1/projects/1/versions/1/llm-detect", {}),
]


@pytest.fixture
async def anonymous_client():
    """Client that sends no Authorization header, against an isolated app."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_evaluation_service] = MagicMock
    app.dependency_overrides[get_document_service] = MagicMock

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test", timeout=30) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        await engine.dispose()


class TestProjectRoutesRequireAuthentication:
    """An anonymous caller must never reach project data."""

    @pytest.mark.parametrize(("method", "path", "kwargs"), PROJECT_DATA_ROUTES)
    async def test_rejects_anonymous_caller(self, anonymous_client, method, path, kwargs):
        """Each project-scoped route answers 401 when no credentials are sent."""
        response = await anonymous_client.request(method, path, **kwargs)

        assert response.status_code == 401, (
            f"{method} {path} answered {response.status_code} without credentials. "
            "Project documents and evaluations must not be reachable anonymously."
        )

    @pytest.mark.parametrize(("method", "path", "kwargs"), ALREADY_PROTECTED_ROUTES)
    async def test_protected_route_stays_protected(self, anonymous_client, method, path, kwargs):
        """Routes that already required a caller must keep requiring one."""
        response = await anonymous_client.request(method, path, **kwargs)

        assert response.status_code == 401, f"{method} {path} lost its authentication requirement"

    async def test_malformed_token_is_rejected(self, anonymous_client):
        """A malformed bearer token must not be accepted as a session."""
        response = await anonymous_client.get(
            "/api/v1/projects/1",
            headers={"Authorization": "Bearer not-a-real-jwt"},
        )

        assert response.status_code == 401
