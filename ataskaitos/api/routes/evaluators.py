"""CRUD endpoints for user-editable evaluator definitions."""

import json
import logging
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ataskaitos.api.dependencies import current_active_user
from ataskaitos.database import get_session
from ataskaitos.models.database import Evaluator, User
from ataskaitos.repositories.evaluator_repository import EvaluatorRepository

router = APIRouter(prefix="/api/v1/evaluators-admin", tags=["evaluators-admin"])
logger = logging.getLogger(__name__)


class EvaluatorRecord(BaseModel):
    """Public representation of a stored evaluator."""

    id: int
    name: str
    document_type: Literal["article", "report"]
    rubric: str
    has_assertion: bool
    is_active: bool
    source: Literal["default", "custom"]
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluatorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    document_type: Literal["article", "report"]
    rubric: str = Field(min_length=1)
    has_assertion: bool = False


class EvaluatorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    rubric: str | None = Field(default=None, min_length=1)
    has_assertion: bool | None = None
    is_active: bool | None = None


class EvaluatorActiveToggle(BaseModel):
    is_active: bool


def _to_record(evaluator: Evaluator) -> EvaluatorRecord:
    try:
        meta = json.loads(evaluator.extra_metadata or "{}")
    except json.JSONDecodeError:
        meta = {}
    return EvaluatorRecord(
        id=evaluator.id,
        name=evaluator.name,
        document_type=evaluator.document_type,  # type: ignore[arg-type]
        rubric=evaluator.rubric,
        has_assertion=bool(evaluator.has_assertion),
        is_active=bool(evaluator.is_active),
        source=evaluator.source,  # type: ignore[arg-type]
        metadata=meta,
    )


@router.get("", response_model=list[EvaluatorRecord])
async def list_evaluators(
    document_type: Literal["article", "report"] | None = None,
    only_active: bool = False,
    _: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """List all evaluators, optionally filtered by document type / active flag."""
    repo = EvaluatorRepository(session)
    if document_type is not None:
        rows = await repo.list_by_type(document_type, only_active=only_active)
    else:
        rows = await repo.list_all()
        if only_active:
            rows = [r for r in rows if r.is_active]
    return [_to_record(r) for r in rows]


@router.post("", response_model=EvaluatorRecord, status_code=201)
async def create_evaluator(
    payload: EvaluatorCreate,
    _: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a new custom evaluator."""
    repo = EvaluatorRepository(session)
    existing = await repo.get_by_name(payload.document_type, payload.name)
    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Evaluator '{payload.name}' already exists for {payload.document_type}",
        )
    try:
        evaluator = await repo.create(
            name=payload.name,
            document_type=payload.document_type,
            rubric=payload.rubric,
            has_assertion=payload.has_assertion,
            is_active=True,
            source="custom",
        )
        await session.commit()
        await session.refresh(evaluator)
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Evaluator name conflict") from exc
    return _to_record(evaluator)


@router.patch("/{evaluator_id}", response_model=EvaluatorRecord)
async def update_evaluator(
    evaluator_id: int,
    payload: EvaluatorUpdate,
    _: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Update an evaluator. Renaming is only allowed for ``source='custom'`` rows."""
    repo = EvaluatorRepository(session)
    evaluator = await repo.get_by_id(evaluator_id)
    if evaluator is None:
        raise HTTPException(status_code=404, detail=f"Evaluator {evaluator_id} not found")

    if payload.name is not None and evaluator.source == "default" and payload.name != evaluator.name:
        raise HTTPException(status_code=400, detail="Cannot rename a default evaluator")

    try:
        updated = await repo.update(
            evaluator_id,
            rubric=payload.rubric,
            has_assertion=payload.has_assertion,
            is_active=payload.is_active,
            name=payload.name,
        )
        await session.commit()
        await session.refresh(updated)
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Evaluator name conflict") from exc
    return _to_record(updated)


@router.patch("/{evaluator_id}/active", response_model=EvaluatorRecord)
async def toggle_active(
    evaluator_id: int,
    payload: EvaluatorActiveToggle,
    _: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Enable or disable an evaluator. Works for both default and custom rows."""
    repo = EvaluatorRepository(session)
    evaluator = await repo.get_by_id(evaluator_id)
    if evaluator is None:
        raise HTTPException(status_code=404, detail=f"Evaluator {evaluator_id} not found")

    updated = await repo.update(evaluator_id, is_active=payload.is_active)
    await session.commit()
    await session.refresh(updated)
    return _to_record(updated)


@router.delete("/{evaluator_id}", status_code=204)
async def delete_evaluator(
    evaluator_id: int,
    _: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Delete a custom evaluator. Defaults can only be deactivated, not removed."""
    repo = EvaluatorRepository(session)
    evaluator = await repo.get_by_id(evaluator_id)
    if evaluator is None:
        raise HTTPException(status_code=404, detail=f"Evaluator {evaluator_id} not found")
    if evaluator.source == "default":
        raise HTTPException(
            status_code=400,
            detail="Default evaluators cannot be deleted; deactivate them instead.",
        )

    await repo.delete(evaluator_id)
    await session.commit()
