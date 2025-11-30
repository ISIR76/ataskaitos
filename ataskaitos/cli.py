"""CLI for Ataskaitos - Scientific Document Evaluation Platform."""

from pathlib import Path
from typing import Optional

import click
import markitdown
from pypdf import PdfReader, PdfWriter


@click.group()
@click.version_option()
def cli():
    """AI-powered platform for evaluating scientific documents (R&D reports and articles)."""
    pass


# ============================================================================
# Document Evaluation Commands (Hierarchical)
# ============================================================================


@cli.group()
def ataskaitos():
    """Evaluate R&D reports against Frascati Manual standards."""
    pass


@ataskaitos.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path), required=False)
@click.option("--batch", type=str, help="Glob pattern for batch evaluation (e.g., 'docs/**/*.docx')")
@click.option("--agents", "-a", multiple=True, help="Specific agents to run (default: all)")
@click.option("--concurrency", "-c", type=int, default=5, help="Number of concurrent evaluations")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
def agent(file: Optional[Path], batch: Optional[str], agents: tuple, concurrency: int, output: Optional[Path]):
    """Run agent-based evaluation for R&D reports.

    Examples:
        ataskaitos agent report.docx
        ataskaitos agent --batch "docs/reports/**/*.docx" -c 3
        ataskaitos agent report.docx -a simple_report_agent -o result.json
    """
    if not file and not batch:
        raise click.UsageError("Provide either FILE argument or --batch option")

    if file and batch:
        raise click.UsageError("Provide either FILE or --batch, not both")

    if file:
        _run_single_agent_evaluation(file, "report", agents, output)
    else:
        _run_batch_agent_evaluation(batch, "report", agents, concurrency, output)


@ataskaitos.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path), required=False)
@click.option("--batch", type=str, help="Glob pattern for batch evaluation")
@click.option("--evaluators", "-e", multiple=True, help="Specific evaluators to run (default: all)")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
def evals(file: Optional[Path], batch: Optional[str], evaluators: tuple, output: Optional[Path]):
    """Run evals-based (scoring) evaluation for R&D reports.

    Examples:
        ataskaitos evals report.docx
        ataskaitos evals --batch "docs/reports/{ok,not_ok}/*.docx"
        ataskaitos evals report.docx -e novelty_score -e systematic_score
    """
    if not file and not batch:
        raise click.UsageError("Provide either FILE argument or --batch option")

    if file and batch:
        raise click.UsageError("Provide either FILE or --batch, not both")

    if file:
        _run_single_evals_evaluation(file, "report", evaluators, output)
    else:
        _run_batch_evals_evaluation(batch, "report", evaluators, output)


@cli.group()
def straipsniai():
    """Evaluate scientific articles against SMSM standards."""
    pass


@straipsniai.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path), required=False)
@click.option("--batch", type=str, help="Glob pattern for batch evaluation")
@click.option("--agents", "-a", multiple=True, help="Specific agents to run (default: all)")
@click.option("--concurrency", "-c", type=int, default=5, help="Number of concurrent evaluations")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
def agent(file: Optional[Path], batch: Optional[str], agents: tuple, concurrency: int, output: Optional[Path]):
    """Run agent-based evaluation for scientific articles.

    Examples:
        straipsniai agent article.pdf
        straipsniai agent --batch "docs/articles/**/*.md" -c 3
        straipsniai agent article.pdf -a detailed_article_agent
    """
    if not file and not batch:
        raise click.UsageError("Provide either FILE argument or --batch option")

    if file and batch:
        raise click.UsageError("Provide either FILE or --batch, not both")

    if file:
        _run_single_agent_evaluation(file, "article", agents, output)
    else:
        _run_batch_agent_evaluation(batch, "article", agents, concurrency, output)


@straipsniai.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path), required=False)
@click.option("--batch", type=str, help="Glob pattern for batch evaluation")
@click.option("--evaluators", "-e", multiple=True, help="Specific evaluators to run (default: all)")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
def evals(file: Optional[Path], batch: Optional[str], evaluators: tuple, output: Optional[Path]):
    """Run evals-based (scoring) evaluation for scientific articles.

    Examples:
        straipsniai evals article.md
        straipsniai evals --batch "docs/articles/**/*.md"
        straipsniai evals article.md -e novelty_score -e rigor_score
    """
    if not file and not batch:
        raise click.UsageError("Provide either FILE argument or --batch option")

    if file and batch:
        raise click.UsageError("Provide either FILE or --batch, not both")

    if file:
        _run_single_evals_evaluation(file, "article", evaluators, output)
    else:
        _run_batch_evals_evaluation(batch, "article", evaluators, output)


# ============================================================================
# Utility Commands
# ============================================================================


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host, port, reload):
    """Start FastAPI server for document evaluation API.

    API documentation will be available at http://localhost:8000/docs
    """
    import uvicorn

    click.echo(f"Starting API server on http://{host}:{port}")
    click.echo(f"API documentation: http://localhost:{port}/docs")
    uvicorn.run(
        "ataskaitos.api:app",
        host=host,
        port=port,
        reload=reload,
    )


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def extract(path):
    """Extract PDF files to markdown format.

    Supports page range pattern: file-5-10.pdf extracts pages 5-10

    Examples:
        extract docs/pdfs/
        extract report.pdf
    """
    import re
    import tempfile

    folder = path if path.is_dir() else path.parent
    pdf_files = list(folder.glob("*.pdf"))

    if not pdf_files:
        click.echo(f"No PDF files found in {folder}")
        return

    click.echo(f"Found {len(pdf_files)} PDF file(s) in {folder}")

    md = markitdown.MarkItDown()

    for pdf_file in pdf_files:
        # Check if filename has page range pattern: name-5-10.pdf
        match = re.match(r"(.+)-(\d+)-(\d+)\.pdf$", pdf_file.name)

        if match:
            _, start, end = match.groups()
            start, end = int(start), int(end)
            click.echo(f"Extracting pages {start}-{end} from {pdf_file.name}")

            # Split pages to temporary file
            try:
                reader = PdfReader(pdf_file)
                writer = PdfWriter()

                for page_num in range(start - 1, end):
                    if page_num < len(reader.pages):
                        writer.add_page(reader.pages[page_num])

                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    writer.write(tmp)
                    temp_pdf = Path(tmp.name)

                # Convert the split PDF
                result = md.convert(str(temp_pdf))
                temp_pdf.unlink()  # Delete temp file

                output_file = pdf_file.with_suffix(".md")
                output_file.write_text(result.text_content)
                click.echo(f"  ✓ Saved to {output_file.name}")

            except Exception as e:
                click.echo(f"  ✗ Error: {e}", err=True)
        else:
            # No page range, convert entire PDF
            output_file = pdf_file.with_suffix(".md")
            click.echo(f"Converting {pdf_file.name} -> {output_file.name}")

            try:
                result = md.convert(str(pdf_file))
                output_file.write_text(result.text_content)
                click.echo(f"  ✓ Saved to {output_file.name}")
            except Exception as e:
                click.echo(f"  ✗ Error: {e}", err=True)

    click.echo(f"\nCompleted: {len(pdf_files)} file(s) processed")


@cli.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.argument("pages")
@click.argument("output", type=click.Path(path_type=Path))
def split(source, pages, output):
    """Split PDF pages to a new file.

    Examples:
        split input.pdf 5-10 output.pdf
        split input.pdf 5 page5.pdf
    """
    try:
        # Parse page range
        if "-" in pages:
            start, end = map(int, pages.split("-"))
        else:
            start = end = int(pages)

        reader = PdfReader(source)
        writer = PdfWriter()

        # PDF pages are 0-indexed, user provides 1-indexed
        for page_num in range(start - 1, end):
            if page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])

        with open(output, "wb") as f:
            writer.write(f)

        click.echo(f"✓ Extracted pages {start}-{end} from {source.name} to {output}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)


# ============================================================================
# Helper Functions for Evaluation
# ============================================================================


def _run_single_agent_evaluation(file: Path, doc_type: str, agents: tuple, output: Optional[Path]):
    """Run agent-based evaluation on a single file."""
    from ataskaitos.services.document_service import DocumentService
    from ataskaitos.services.evaluation_service import get_evaluation_service
    import asyncio
    import json

    click.echo(f"Evaluating {file.name} with agent mode...")

    # Convert document to markdown
    doc_service = DocumentService()
    try:
        markdown = doc_service.convert_file_to_markdown_sync(str(file))
    except Exception as e:
        click.echo(f"✗ Error converting document: {e}", err=True)
        raise click.Abort()

    # Run evaluation
    eval_service = get_evaluation_service()

    async def run_eval():
        return await eval_service.evaluate_document(
            document_text=markdown,
            document_type=doc_type,
            evaluation_type="agent",
            agent_names=list(agents) if agents else None,
        )

    try:
        result = asyncio.run(run_eval())

        # Output results
        if output:
            output.write_text(json.dumps(result.model_dump(), indent=2))
            click.echo(f"✓ Results saved to {output}")
        else:
            click.echo("\nResults:")
            click.echo(json.dumps(result.model_dump(), indent=2))

    except Exception as e:
        click.echo(f"✗ Evaluation error: {e}", err=True)
        raise click.Abort()


def _run_batch_agent_evaluation(pattern: str, doc_type: str, agents: tuple, concurrency: int, output: Optional[Path]):
    """Run agent-based evaluation on multiple files."""
    click.echo(f"Batch evaluation with pattern: {pattern}")
    click.echo(f"Document type: {doc_type}, Concurrency: {concurrency}")

    if agents:
        click.echo(f"Agents: {', '.join(agents)}")

    # This would call the batch evaluation service
    click.echo("\n⚠ Batch evaluation not yet implemented - use scripts/evaluation/run_agent.py")
    click.echo(f'  Run: uv run python scripts/evaluation/run_agent.py "{pattern}" {concurrency}')


def _run_single_evals_evaluation(file: Path, doc_type: str, evaluators: tuple, output: Optional[Path]):
    """Run evals-based evaluation on a single file."""
    from ataskaitos.services.document_service import DocumentService
    from ataskaitos.services.evaluation_service import get_evaluation_service
    import asyncio
    import json

    click.echo(f"Evaluating {file.name} with scoring mode...")

    # Convert document to markdown
    doc_service = DocumentService()
    try:
        markdown = doc_service.convert_file_to_markdown_sync(str(file))
    except Exception as e:
        click.echo(f"✗ Error converting document: {e}", err=True)
        raise click.Abort()

    # Run evaluation
    eval_service = get_evaluation_service()

    async def run_eval():
        return await eval_service.evaluate_document(
            document_text=markdown,
            document_type=doc_type,
            evaluation_type="scoring",
            evaluator_names=list(evaluators) if evaluators else None,
        )

    try:
        result = asyncio.run(run_eval())

        # Output results
        if output:
            output.write_text(json.dumps(result.model_dump(), indent=2))
            click.echo(f"✓ Results saved to {output}")
        else:
            click.echo("\nResults:")
            click.echo(json.dumps(result.model_dump(), indent=2))

    except Exception as e:
        click.echo(f"✗ Evaluation error: {e}", err=True)
        raise click.Abort()


def _run_batch_evals_evaluation(pattern: str, doc_type: str, evaluators: tuple, output: Optional[Path]):
    """Run evals-based evaluation on multiple files."""
    click.echo(f"Batch evals evaluation with pattern: {pattern}")
    click.echo(f"Document type: {doc_type}")

    if evaluators:
        click.echo(f"Evaluators: {', '.join(evaluators)}")

    # This would use the existing evals.py for batch processing
    if doc_type == "report":
        click.echo("\n⚠ Batch evaluation not yet fully integrated - use:")
        click.echo("  Run: uv run python ataskaitos/evals.py")
    else:
        click.echo("\n⚠ Batch evaluation not yet fully integrated - use:")
        click.echo("  Run: uv run python straipsniai/evals.py")


if __name__ == "__main__":
    cli()
