"""Database connection and session management."""

from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from ataskaitos.models.database import Base
from ataskaitos.settings import settings

# Get database URLs from settings
DATABASE_URL = settings.database_url
# Convert sync database URL to async format for SQLite
ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Create sync engine with SQLite (for existing code)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False},  # Needed for SQLite with FastAPI
)

# Create async engine with SQLite (for FastAPI-Users)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

# Create session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db_async():
    """Create all tables in the async database."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Async database initialized")


def init_db():
    """Create all tables in the sync database."""
    Base.metadata.create_all(bind=engine)
    print("✓ Sync database initialized")


@contextmanager
def get_session():
    """Get database session with automatic cleanup and transaction management.

    Usage:
        with get_session() as session:
            # Do database operations
            session.add(obj)
            # Commit happens automatically on success
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for FastAPI-Users.

    Usage:
        async with get_async_session() as session:
            # Do async database operations
    """
    async with AsyncSessionLocal() as session:
        yield session
