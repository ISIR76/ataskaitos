"""Evaluator loading utilities."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from pydantic_evals.evaluators import LLMJudge
from sqlalchemy.ext.asyncio import AsyncSession

from .base import EvaluatorRegistry

logger = logging.getLogger(__name__)


def _build_judge(name: str, rubric: str, has_assertion: bool) -> LLMJudge:
    """Construct an ``LLMJudge`` from a name/rubric/assertion triple."""
    judge_params: Dict[str, Any] = {
        "rubric": rubric,
        "include_input": False,
        "score": {"evaluation_name": name, "include_reason": True},
    }
    if has_assertion:
        assertion_name = f"{name.replace('_score', '')}_qualified"
        judge_params["assertion"] = {
            "evaluation_name": assertion_name,
            "include_reason": True,
        }
    return LLMJudge(**judge_params)


def load_evaluators_from_json(
    json_path: str | Path,
    document_type: str,
    registry: EvaluatorRegistry,
    filter_names: List[str] | None = None,
) -> List[LLMJudge]:
    """Load evaluators from JSON configuration file.

    Args:
        json_path: Path to JSON file containing evaluator configurations
        document_type: Type of document these evaluators are for ('report' or 'article')
        registry: EvaluatorRegistry to register evaluators in
        filter_names: Optional list of evaluator names to load (loads all if None)

    Returns:
        List of loaded LLMJudge evaluators

    JSON Format:
        [
            {
                "name": "evaluator_name",
                "rubric": "Evaluation instructions...",
                "has_assertion": false,  # optional
                "metadata": {...}  # optional
            },
            ...
        ]
    """
    json_path = Path(json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"Evaluator configuration not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        judges_config = json.load(f)

    evaluators = []

    for config in judges_config:
        name = config["name"]

        # Apply filter if specified
        if filter_names and name not in filter_names:
            continue

        rubric = config["rubric"]
        has_assertion = config.get("has_assertion", False)
        metadata = config.get("metadata", {})

        # Build the LLMJudge parameters
        judge_params = {
            "rubric": rubric,
            "include_input": False,
            "score": {"evaluation_name": name, "include_reason": True},
        }

        # Add assertion if specified
        if has_assertion:
            assertion_name = f"{name.replace('_score', '')}_qualified"
            judge_params["assertion"] = {
                "evaluation_name": assertion_name,
                "include_reason": True,
            }

        evaluator = LLMJudge(**judge_params)

        # Register in registry with metadata
        registry.register(
            document_type=document_type,
            name=name,
            evaluator=evaluator,
            metadata={
                "source": str(json_path),
                "has_assertion": has_assertion,
                **metadata,
            },
        )

        evaluators.append(evaluator)

    return evaluators


def load_evaluators_from_dict(
    evaluators_dict: List[Dict[str, Any]],
    document_type: str,
    registry: EvaluatorRegistry,
) -> List[LLMJudge]:
    """Load evaluators from Python dictionary (programmatic configuration).

    Args:
        evaluators_dict: List of evaluator configuration dictionaries
        document_type: Type of document these evaluators are for
        registry: EvaluatorRegistry to register evaluators in

    Returns:
        List of loaded LLMJudge evaluators
    """
    evaluators = []

    for config in evaluators_dict:
        name = config["name"]
        rubric = config["rubric"]
        has_assertion = config.get("has_assertion", False)
        metadata = config.get("metadata", {})

        judge_params = {
            "rubric": rubric,
            "include_input": False,
            "score": {"evaluation_name": name, "include_reason": True},
        }

        if has_assertion:
            assertion_name = f"{name.replace('_score', '')}_qualified"
            judge_params["assertion"] = {
                "evaluation_name": assertion_name,
                "include_reason": True,
            }

        evaluator = LLMJudge(**judge_params)

        registry.register(
            document_type=document_type,
            name=name,
            evaluator=evaluator,
            metadata={"source": "programmatic", "has_assertion": has_assertion, **metadata},
        )

        evaluators.append(evaluator)

    return evaluators


def initialize_default_evaluators(registry: EvaluatorRegistry) -> None:
    """Initialize the registry with default evaluators from configuration files.

    Loads:
    - Article evaluators from: evaluators/articles/smsm_judges.json
    - Report evaluators from: evaluators/reports/frascati_judges.json (if exists)
    """
    print("Initializing default evaluators...")
    # Get the evaluators directory path
    evaluators_dir = Path(__file__).parent

    # Load article evaluators
    articles_json = evaluators_dir / "articles" / "smsm_judges.json"
    if articles_json.exists():
        load_evaluators_from_json(json_path=articles_json, document_type="article", registry=registry)

    # Load report evaluators
    reports_json = evaluators_dir / "reports" / "frascati_judges.json"
    if reports_json.exists():
        load_evaluators_from_json(json_path=reports_json, document_type="report", registry=registry)


def _read_default_configs() -> List[Dict[str, Any]]:
    """Return all evaluator configurations bundled with the package, tagged with type."""
    evaluators_dir = Path(__file__).parent
    sources = [
        ("article", evaluators_dir / "articles" / "smsm_judges.json"),
        ("report", evaluators_dir / "reports" / "frascati_judges.json"),
    ]
    out: List[Dict[str, Any]] = []
    for document_type, path in sources:
        if not path.exists():
            continue
        with open(path, "r", encoding="utf-8") as fh:
            for cfg in json.load(fh):
                out.append({"document_type": document_type, **cfg})
    return out


async def seed_default_evaluators(session: AsyncSession) -> int:
    """Insert any JSON-defined evaluators that are not yet in the database.

    Idempotent: existing rows (matched by ``(name, document_type)``) are not
    touched, so user edits to seeded defaults are preserved across restarts.
    Returns the number of attempted inserts (some may have been no-ops).
    """
    from ataskaitos.repositories.evaluator_repository import EvaluatorRepository

    repo = EvaluatorRepository(session)
    configs = _read_default_configs()
    for cfg in configs:
        await repo.upsert_default(
            name=cfg["name"],
            document_type=cfg["document_type"],
            rubric=cfg["rubric"],
            has_assertion=bool(cfg.get("has_assertion", False)),
            extra_metadata=json.dumps(cfg.get("metadata", {})),
        )
    await session.commit()
    return len(configs)


async def build_judges_from_db(
    session: AsyncSession,
    document_type: str,
    names: List[str] | None = None,
) -> List[LLMJudge]:
    """Build ``LLMJudge`` instances for active evaluators of a given type.

    Reads from the ``evaluators`` table at request time, so edits in the
    settings UI take effect on the very next evaluation run without any
    process restart.
    """
    from ataskaitos.repositories.evaluator_repository import EvaluatorRepository

    repo = EvaluatorRepository(session)
    rows = await repo.list_by_type(document_type, only_active=True)
    if names is not None:
        wanted = set(names)
        rows = [row for row in rows if row.name in wanted]
    return [_build_judge(row.name, row.rubric, bool(row.has_assertion)) for row in rows]
