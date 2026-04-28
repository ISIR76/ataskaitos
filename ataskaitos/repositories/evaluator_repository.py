"""Evaluator repository — DB-backed CRUD for editable evaluator definitions."""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from ataskaitos.models.database import Evaluator


class EvaluatorRepository:
    """Repository for ``Evaluator`` data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_by_type(
        self, document_type: str, only_active: bool = False
    ) -> list[Evaluator]:
        query = select(Evaluator).where(Evaluator.document_type == document_type)
        if only_active:
            query = query.where(Evaluator.is_active.is_(True))
        query = query.order_by(Evaluator.name.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_all(self) -> list[Evaluator]:
        query = select(Evaluator).order_by(
            Evaluator.document_type.asc(), Evaluator.name.asc()
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, evaluator_id: int) -> Optional[Evaluator]:
        query = select(Evaluator).where(Evaluator.id == evaluator_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, document_type: str, name: str) -> Optional[Evaluator]:
        query = select(Evaluator).where(
            Evaluator.document_type == document_type, Evaluator.name == name
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self,
        name: str,
        document_type: str,
        rubric: str,
        has_assertion: bool = False,
        is_active: bool = True,
        source: str = "custom",
        extra_metadata: str = "{}",
    ) -> Evaluator:
        evaluator = Evaluator(
            name=name,
            document_type=document_type,
            rubric=rubric,
            has_assertion=has_assertion,
            is_active=is_active,
            source=source,
            extra_metadata=extra_metadata,
        )
        self.session.add(evaluator)
        await self.session.flush()
        return evaluator

    async def update(
        self,
        evaluator_id: int,
        *,
        rubric: Optional[str] = None,
        has_assertion: Optional[bool] = None,
        is_active: Optional[bool] = None,
        name: Optional[str] = None,
    ) -> Evaluator:
        evaluator = await self.get_by_id(evaluator_id)
        if evaluator is None:
            raise ValueError(f"Evaluator {evaluator_id} not found")

        if rubric is not None:
            evaluator.rubric = rubric
        if has_assertion is not None:
            evaluator.has_assertion = has_assertion
        if is_active is not None:
            evaluator.is_active = is_active
        if name is not None and evaluator.source == "custom":
            evaluator.name = name
        evaluator.updated_at = datetime.utcnow()
        await self.session.flush()
        return evaluator

    async def delete(self, evaluator_id: int) -> bool:
        evaluator = await self.get_by_id(evaluator_id)
        if evaluator is None:
            return False
        await self.session.delete(evaluator)
        await self.session.flush()
        return True

    async def upsert_default(
        self,
        name: str,
        document_type: str,
        rubric: str,
        has_assertion: bool,
        extra_metadata: str = "{}",
    ) -> None:
        """Insert a JSON-defined default if it isn't already present.

        Idempotent on (name, document_type). Uses ``ON CONFLICT DO NOTHING`` so
        repeated startup seeding is cheap and never overwrites user edits.
        """
        dialect = self.session.bind.dialect.name if self.session.bind else "sqlite"
        values = {
            "name": name,
            "document_type": document_type,
            "rubric": rubric,
            "has_assertion": has_assertion,
            "is_active": True,
            "source": "default",
            "extra_metadata": extra_metadata,
        }
        if dialect == "postgresql":
            stmt = pg_insert(Evaluator).values(**values)
            stmt = stmt.on_conflict_do_nothing(index_elements=["name", "document_type"])
        else:
            stmt = sqlite_insert(Evaluator).values(**values)
            stmt = stmt.on_conflict_do_nothing(index_elements=["name", "document_type"])

        await self.session.execute(stmt)
