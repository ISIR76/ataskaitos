"""Database connection and session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ataskaitos.models.database import Base
from ataskaitos.settings import settings

# Get database URLs from settings
DATABASE_URL = settings.database_url

if DATABASE_URL.startswith("sqlite"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
elif DATABASE_URL.startswith("postgresql"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    # connect_args={"check_same_thread": False},
)

# Create session factories
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Create all tables in the async database."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Async database initialized")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
