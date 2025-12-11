"""Projects API router for project-based document management."""

import json
import logging
import time
from pathlib import Path

import logfire
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse

from ataskaitos.api.dependencies import get_document_service, get_evaluation_service

logger = logging.getLogger(__name__)
from ataskaitos.api.models import (
    CreateProjectRequest,
    ProjectListResponse,
    ProjectResponse,
    DocumentVersionResponse,
    DocumentVersionDetailResponse,
    EvaluationHistoryItem,
    EvaluationDetailResponse,
    UnifiedEvaluationResponse,
)
from ataskaitos.database import get_session
from ataskaitos.repositories.project_repository import ProjectRepository
from ataskaitos.repositories.document_repository import DocumentVersionRepository
from ataskaitos.repositories.evaluation_repository import EvaluationRepository
from ataskaitos.services.document_service import DocumentService
from ataskaitos.services.evaluation_service import EvaluationService
from ataskaitos.services.storage_service import storage_service

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


# Helper functions


def _build_project_response(project, doc_repo: DocumentVersionRepository) -> ProjectResponse:
    """Build ProjectResponse from database model."""
    active_version = None
    if project.active_version_id:
        active_version = doc_repo.get_by_id(project.active_version_id)

    return ProjectResponse(
        id=project.id,
        name=project.name,
        project_type=project.project_type,
        active_version_id=project.active_version_id,
        active_version_number=active_version.version_number if active_version else None,
        total_versions=len(project.versions),
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def _build_version_response(
    version, project, eval_repo: EvaluationRepository
) -> DocumentVersionResponse:
    """Build DocumentVersionResponse from database model."""
    evaluations = eval_repo.list_by_version(version.id)

    return DocumentVersionResponse(
        id=version.id,
        project_id=version.project_id,
        version_number=version.version_number,
        original_filename=version.original_filename,
        character_count=version.character_count,
        evaluation_count=len(evaluations),
        is_active=(version.id == project.active_version_id),
        created_at=version.created_at,
    )


def _build_evaluation_history_item(evaluation) -> EvaluationHistoryItem:
    """Build EvaluationHistoryItem from database model."""
    return EvaluationHistoryItem(
        id=evaluation.id,
        evaluation_id=evaluation.evaluation_id,
        evaluation_type=evaluation.evaluation_type,
        evaluators_used=json.loads(evaluation.evaluators_used),
        status=evaluation.status,
        duration_seconds=evaluation.duration_seconds,
        created_at=evaluation.created_at,
    )


# Project endpoints


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(request: CreateProjectRequest):
    """Create a new project.

    Args:
        request: Project creation request with name and type

    Returns:
        Created project details

    Raises:
        HTTPException: If project name already exists
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)

        # Check if name already exists
        existing = project_repo.get_by_name(request.name)
        if existing:
            raise HTTPException(status_code=400, detail=f"Project with name '{request.name}' already exists")

        # Create project
        project = project_repo.create(name=request.name, project_type=request.project_type)

        return _build_project_response(project, doc_repo)


@router.get("", response_model=ProjectListResponse)
async def list_projects(skip: int = 0, limit: int = 100):
    """List all projects with pagination.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)

    Returns:
        List of projects with total count
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)

        projects = project_repo.list_all(skip=skip, limit=limit)
        total = project_repo.count()

        project_responses = [_build_project_response(p, doc_repo) for p in projects]

        return ProjectListResponse(projects=project_responses, total=total)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """Get project details by ID.

    Args:
        project_id: Project ID

    Returns:
        Project details

    Raises:
        HTTPException: If project not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)

        project = project_repo.get_by_id(project_id, load_versions=True)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        return _build_project_response(project, doc_repo)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int):
    """Delete a project and all its versions.

    Args:
        project_id: Project ID

    Raises:
        HTTPException: If project not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        # Delete all files for this project
        storage_service.delete_project_files(project_id)

        # Delete project from database (cascade will delete versions and evaluations)
        project_repo.delete(project_id)


# Document version endpoints


@router.post("/{project_id}/versions", response_model=DocumentVersionResponse, status_code=201)
async def upload_version(
    project_id: int,
    file: UploadFile = File(...),
    doc_service: DocumentService = Depends(get_document_service),
):
    """Upload a new document version to a project.

    Args:
        project_id: Project ID
        file: Document file to upload
        doc_service: Document service (injected)

    Returns:
        Created document version details

    Raises:
        HTTPException: If project not found or file processing fails
    """
    print(f"Upload endpoint called: project_id={project_id}, file={file.filename if file else 'None'}")

    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)
        eval_repo = EvaluationRepository(session)

        # Verify project exists
        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        # Convert document to markdown
        try:
            markdown_content = await doc_service.convert_to_markdown(file)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to convert document: {str(e)}")

        # Get next version number
        version_number = doc_repo.get_next_version_number(project_id)

        # Save files to storage
        file.file.seek(0)  # Reset file pointer after reading
        original_path, markdown_path = await storage_service.save_document_files(
            project_id, version_number, file, markdown_content
        )

        # Create document version record
        file_extension = Path(file.filename or "").suffix
        version = doc_repo.create(
            project_id=project_id,
            version_number=version_number,
            original_filename=file.filename or "document",
            file_extension=file_extension,
            original_file_path=original_path,
            markdown_file_path=markdown_path,
            character_count=len(markdown_content),
        )

        # If this is the first version, set it as active
        if version_number == 1:
            project_repo.update_active_version(project_id, version.id)

        return _build_version_response(version, project, eval_repo)


@router.get("/{project_id}/versions", response_model=list[DocumentVersionResponse])
async def list_versions(project_id: int):
    """List all versions for a project.

    Args:
        project_id: Project ID

    Returns:
        List of document versions

    Raises:
        HTTPException: If project not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)
        eval_repo = EvaluationRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        versions = doc_repo.list_by_project(project_id)

        return [_build_version_response(v, project, eval_repo) for v in versions]


@router.get("/{project_id}/versions/{version_id}", response_model=DocumentVersionDetailResponse)
async def get_version(project_id: int, version_id: int):
    """Get document version details with markdown content.

    Args:
        project_id: Project ID
        version_id: Version ID

    Returns:
        Document version details with markdown content

    Raises:
        HTTPException: If project or version not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)
        eval_repo = EvaluationRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        version = doc_repo.get_by_id(version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found in project {project_id}")

        # Load markdown content from storage
        markdown_content = storage_service.get_markdown_content(project_id, version.version_number)

        evaluations = eval_repo.list_by_version(version.id)

        return DocumentVersionDetailResponse(
            id=version.id,
            project_id=version.project_id,
            version_number=version.version_number,
            original_filename=version.original_filename,
            character_count=version.character_count,
            evaluation_count=len(evaluations),
            is_active=(version.id == project.active_version_id),
            created_at=version.created_at,
            markdown_content=markdown_content,
        )


@router.get("/{project_id}/versions/{version_id}/markdown")
async def get_version_markdown(project_id: int, version_id: int):
    """Get markdown content for a version.

    Args:
        project_id: Project ID
        version_id: Version ID

    Returns:
        Plain text markdown content

    Raises:
        HTTPException: If project or version not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        version = doc_repo.get_by_id(version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found in project {project_id}")

        markdown_content = storage_service.get_markdown_content(project_id, version.version_number)

        from fastapi.responses import PlainTextResponse

        return PlainTextResponse(content=markdown_content)


@router.post("/{project_id}/versions/{version_id}/set-active", response_model=ProjectResponse)
async def set_active_version(project_id: int, version_id: int):
    """Set a version as the active version for the project.

    Args:
        project_id: Project ID
        version_id: Version ID to set as active

    Returns:
        Updated project details

    Raises:
        HTTPException: If project or version not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        version = doc_repo.get_by_id(version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found in project {project_id}")

        # Update active version
        project = project_repo.update_active_version(project_id, version_id)

        # Reload with versions
        project = project_repo.get_by_id(project_id, load_versions=True)

        return _build_project_response(project, doc_repo)


@router.delete("/{project_id}/versions/{version_id}", status_code=204)
async def delete_version(project_id: int, version_id: int):
    """Delete a document version.

    Args:
        project_id: Project ID
        version_id: Version ID

    Raises:
        HTTPException: If project or version not found, or if trying to delete the only version
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        version = doc_repo.get_by_id(version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found in project {project_id}")

        # Check if this is the only version
        version_count = doc_repo.count_by_project(project_id)
        if version_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot delete the only version of a project")

        # If this is the active version, clear it
        if project.active_version_id == version_id:
            project_repo.update_active_version(project_id, None)

        # Delete files
        storage_service.delete_version_files(project_id, version.version_number)

        # Delete from database
        doc_repo.delete(version_id)


# Evaluation endpoints


@router.post("/{project_id}/versions/{version_id}/evaluate", response_model=UnifiedEvaluationResponse)
async def evaluate_version(
    project_id: int,
    version_id: int,
    evaluation_type: str = Form("scoring"),
    evaluators: str = Form(None),
    agents: str = Form(None),
    eval_service: EvaluationService = Depends(get_evaluation_service),
):
    """Run evaluation on a document version.

    Args:
        project_id: Project ID
        version_id: Version ID
        evaluation_type: Type of evaluation ("scoring" or "agent")
        evaluators: Comma-separated list of evaluators (for scoring)
        agents: Comma-separated list of agents (for agent mode)

    Returns:
        Evaluation results

    Raises:
        HTTPException: If project or version not found, or evaluation fails
    """
    start_time = time.time()

    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)
        eval_repo = EvaluationRepository(session)

        # Verify project and version
        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        version = doc_repo.get_by_id(version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found in project {project_id}")

        # Load markdown content
        markdown_content = storage_service.get_markdown_content(project_id, version.version_number)

        # Parse evaluator/agent names
        evaluator_names = [e.strip() for e in evaluators.split(",")] if evaluators else None
        agent_names = [a.strip() for a in agents.split(",")] if agents else None

        # Map project type to document type for evaluation service
        document_type = "article" if project.project_type == "straipsnis" else "report"

        # Run evaluation
        try:
            evaluation_result = await eval_service.evaluate_document(
                content=markdown_content,
                document_type=document_type,
                evaluation_type=evaluation_type,
                evaluator_names=evaluator_names,
                agent_names=agent_names,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

        # Store evaluation in database
        duration = time.time() - start_time
        evaluators_list = evaluator_names or agent_names or []

        with logfire.span("save_evaluation_to_db",
                         project_id=project_id,
                         version_id=version_id,
                         evaluation_type=evaluation_type):
            # Extract score info for logging
            score_keys = []
            if isinstance(evaluation_result.results, dict) and 'cases' in evaluation_result.results:
                cases = evaluation_result.results.get('cases', [])
                if cases:
                    score_keys = list(cases[0].get('scores', {}).keys())

            logfire.info("Preparing to save evaluation",
                        evaluation_id=evaluation_result.evaluation_id,
                        evaluators=evaluators_list,
                        score_count=len(score_keys),
                        score_names=score_keys)

            # Log what we're about to save
            logger.info(f"💾 Saving evaluation to database:")
            logger.info(f"   Evaluation ID: {evaluation_result.evaluation_id}")
            logger.info(f"   Type: {evaluation_type}")
            logger.info(f"   Evaluators: {evaluators_list}")
            logger.info(f"   Results keys: {evaluation_result.results.keys() if isinstance(evaluation_result.results, dict) else type(evaluation_result.results)}")
            if score_keys:
                logger.info(f"   First case scores: {score_keys}")

            evaluation = eval_repo.create(
                evaluation_id=evaluation_result.evaluation_id,
                document_version_id=version_id,
                evaluation_type=evaluation_type,
                evaluators_used=json.dumps(evaluators_list),
                results_json=json.dumps(evaluation_result.results),
                status=evaluation_result.status,
                duration_seconds=duration,
            )

            logfire.info("Evaluation saved successfully", db_id=evaluation.id)
            logger.info(f"✅ Evaluation saved with ID: {evaluation.id}")

        # Return unified response
        return UnifiedEvaluationResponse(
            evaluation_id=evaluation_result.evaluation_id,
            document_type=evaluation_result.document_type,
            evaluation_type=evaluation_result.evaluation_type,
            status=evaluation_result.status,
            markdown_content=markdown_content,
            results=evaluation_result.results,
            metadata=evaluation_result.metadata,
        )


@router.get("/{project_id}/versions/{version_id}/evaluations", response_model=list[EvaluationHistoryItem])
async def list_version_evaluations(project_id: int, version_id: int):
    """List all evaluations for a document version.

    Args:
        project_id: Project ID
        version_id: Version ID

    Returns:
        List of evaluation history items

    Raises:
        HTTPException: If project or version not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        doc_repo = DocumentVersionRepository(session)
        eval_repo = EvaluationRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        version = doc_repo.get_by_id(version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found in project {project_id}")

        evaluations = eval_repo.list_by_version(version_id)

        return [_build_evaluation_history_item(e) for e in evaluations]


@router.get("/{project_id}/evaluations/{evaluation_id}", response_model=EvaluationDetailResponse)
async def get_evaluation(project_id: int, evaluation_id: str):
    """Get evaluation details by UUID.

    Args:
        project_id: Project ID
        evaluation_id: Evaluation UUID

    Returns:
        Evaluation details with full results

    Raises:
        HTTPException: If project or evaluation not found
    """
    with get_session() as session:
        project_repo = ProjectRepository(session)
        eval_repo = EvaluationRepository(session)

        project = project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        evaluation = eval_repo.get_by_uuid(evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail=f"Evaluation {evaluation_id} not found")

        # Verify evaluation belongs to this project
        doc_repo = DocumentVersionRepository(session)
        version = doc_repo.get_by_id(evaluation.document_version_id)
        if not version or version.project_id != project_id:
            raise HTTPException(status_code=404, detail=f"Evaluation {evaluation_id} not found in project {project_id}")

        return EvaluationDetailResponse(
            id=evaluation.id,
            evaluation_id=evaluation.evaluation_id,
            evaluation_type=evaluation.evaluation_type,
            evaluators_used=json.loads(evaluation.evaluators_used),
            status=evaluation.status,
            duration_seconds=evaluation.duration_seconds,
            created_at=evaluation.created_at,
            results=json.loads(evaluation.results_json),
        )
