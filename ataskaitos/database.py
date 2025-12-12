"""Database connection and session management."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ataskaitos.models.database import Base

DATABASE_URL = "sqlite:///:memory:"

# # Use in-memory database in production, file-based locally
# if os.getenv("ENV") == "production":
#     DATABASE_URL = "sqlite:///:memory:"
#     print("Using in-memory SQLite database")
# else:
#     # Create data directory if it doesn't exist
#     DATA_DIR = Path("data/database")
#     DATA_DIR.mkdir(parents=True, exist_ok=True)
#     DATABASE_URL = "sqlite:///data/database/ataskaitos.db"
#     print(f"Using file-based SQLite database: {DATABASE_URL}")

# Create engine with SQLite
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False},  # Needed for SQLite with FastAPI
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")


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
