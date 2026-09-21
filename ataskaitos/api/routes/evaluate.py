"""Unified evaluation endpoints for all document types."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from ataskaitos.api.dependencies import (
    current_active_user,
    get_document_service,
    get_evaluation_service,
)
from ataskaitos.api.models import UnifiedEvaluationResponse
from ataskaitos.models.database import User
from ataskaitos.services import DocumentService, EvaluationService

router = APIRouter(prefix="/api/v1", tags=["Evaluation"])


@router.post("/evaluate", response_model=UnifiedEvaluationResponse)
async def evaluate_document(
    file: Annotated[UploadFile, File(description="Document file to evaluate (DOCX, PDF, MD, TXT)")],
    document_type: Annotated[
        Literal["report", "article"],
        Form(description="Type of document: 'report' or 'article'"),
    ],
    evaluation_type: Annotated[
        Literal["agent", "scoring"],
        Form(description="Evaluation method: 'agent' or 'scoring' (default)"),
    ] = "scoring",
    evaluators: str | None = Form(
        None,
        description="Comma-separated list of specific evaluators to run (for scoring mode)",
    ),
    agents: str | None = Form(
        None,
        description="Comma-separated list of specific agents to run (for agent mode)",
    ),
    user: User = Depends(current_active_user),
    doc_service: DocumentService = Depends(get_document_service),
    eval_service: EvaluationService = Depends(get_evaluation_service),
):
    """Unified evaluation endpoint for both reports and articles.

    **Document Types:**
    - `report`: R&D activity reports evaluated against Frascati Manual standards
    - `article`: Scientific articles evaluated against SMSM publication standards

    **Evaluation Methods:**
    - `scoring`: Multiple LLM judges score against standardized criteria (0.0-1.0 scale)
    - `agent`: Single AI agent provides comprehensive qualitative analysis

    **Evaluators:**
    - Leave empty to run all evaluators for the document type
    - Provide comma-separated list to run specific evaluators (e.g., "novelty_score,rigor_fluid")
    - Use `/api/v1/evaluators` endpoint to see available evaluators

    **Supported File Formats:**
    - `.docx` - Microsoft Word documents
    - `.pdf` - PDF documents
    - `.doc` - Legacy Word documents
    - `.txt` - Plain text files
    - `.md` - Markdown files

    **Returns:**
    - Converted markdown content
    - Evaluation results (format depends on evaluation_type)
    - Metadata (filename, character count, duration, etc.)
    - Unique evaluation ID for reference
    """
    try:
        # Convert file to markdown
        markdown_content = await doc_service.convert_to_markdown(file)

        # Parse evaluator names if provided (for scoring mode)
        evaluator_names = None
        if evaluators:
            evaluator_names = [name.strip() for name in evaluators.split(",")]

        # Parse agent names if provided (for agent mode)
        agent_names = None
        if agents:
            agent_names = [name.strip() for name in agents.split(",")]

        # Run evaluation
        result = await eval_service.evaluate_document(
            content=markdown_content,
            document_type=document_type,
            evaluation_type=evaluation_type,
            evaluator_names=evaluator_names,
            agent_names=agent_names,
            metadata={},
            filename=file.filename or "uploaded_file",
        )

        # Return unified response
        return UnifiedEvaluationResponse(
            evaluation_id=result.evaluation_id,
            document_type=result.document_type,
            evaluation_type=result.evaluation_type,
            status=result.status,
            markdown_content=result.markdown_content,
            results=result.results,
            metadata=result.metadata,
        )

    except ValueError as e:
        # Handle validation errors (e.g., unknown evaluators)
        raise HTTPException(status_code=400, detail="Unknown evaluator or agent specified.") from e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail="An error occurred during document evaluation.",
        ) from e


# Convenience endpoints for specific document types


@router.post("/reports/evaluate", response_model=UnifiedEvaluationResponse)
async def evaluate_report(
    file: Annotated[UploadFile, File(description="Report document to evaluate (DOCX, PDF, etc.)")],
    evaluation_type: Annotated[
        Literal["agent", "scoring"],
        Form(description="Evaluation method: 'agent' or 'scoring'"),
    ] = "scoring",
    evaluators: Annotated[
        str | None,
        Form(description="Comma-separated list of evaluators (optional)"),
    ] = None,
    user: User = Depends(current_active_user),
    doc_service: DocumentService = Depends(get_document_service),
    eval_service: EvaluationService = Depends(get_evaluation_service),
):
    """Evaluate R&D activity report against Frascati Manual standards.

    Convenience endpoint equivalent to `/api/v1/evaluate` with `document_type=report`.

    See `/api/v1/evaluate` for full documentation.
    """
    return await evaluate_document(
        file=file,
        document_type="report",
        evaluation_type=evaluation_type,
        evaluators=evaluators,
        user=user,
        doc_service=doc_service,
        eval_service=eval_service,
    )


@router.post("/articles/evaluate", response_model=UnifiedEvaluationResponse)
async def evaluate_article(
    file: Annotated[UploadFile, File(description="Article document to evaluate (DOCX, PDF, etc.)")],
    evaluation_type: Annotated[
        Literal["agent", "scoring"],
        Form(description="Evaluation method: 'agent' or 'scoring'"),
    ] = "scoring",
    evaluators: Annotated[
        str | None,
        Form(description="Comma-separated list of evaluators (optional)"),
    ] = None,
    user: User = Depends(current_active_user),
    doc_service: DocumentService = Depends(get_document_service),
    eval_service: EvaluationService = Depends(get_evaluation_service),
):
    """Evaluate scientific article against SMSM publication standards.

    Convenience endpoint equivalent to `/api/v1/evaluate` with `document_type=article`.

    See `/api/v1/evaluate` for full documentation.
    """
    return await evaluate_document(
        file=file,
        document_type="article",
        evaluation_type=evaluation_type,
        evaluators=evaluators,
        user=user,
        doc_service=doc_service,
        eval_service=eval_service,
    )
