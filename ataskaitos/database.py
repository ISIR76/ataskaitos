"""Database connection and session management."""

import logging
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ataskaitos.models.database import Base
from ataskaitos.settings import settings

logger = logging.getLogger(__name__)

# Idempotent column additions for tables that pre-exist before a column was added.
# create_all() never alters existing tables, so columns added after the initial
# deploy must be patched in here. Each entry: (table, column, DDL fragment).
_ADDITIVE_COLUMNS: list[tuple[str, str, str]] = [
    ("projects", "is_marked_good", "BOOLEAN NOT NULL DEFAULT FALSE"),
]

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


async def _apply_additive_migrations(conn) -> None:
    """Add new columns to pre-existing tables. SQLite-safe; ignores duplicates."""
    for table, column, ddl in _ADDITIVE_COLUMNS:
        try:
            await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))
            logger.info("Added column %s.%s", table, column)
        except Exception as exc:  # noqa: BLE001
            msg = str(exc).lower()
            if "duplicate column" in msg or "already exists" in msg:
                continue
            raise


async def init_db():
    """Create all tables in the async database."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _apply_additive_migrations(conn)
    print("✓ Async database initialized")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
