"""Simple CLI for Ataskaitos using Click."""

from pathlib import Path

import click
import markitdown
from pypdf import PdfReader, PdfWriter


@click.group()
@click.version_option()
def cli():
    """AI-powered platform for scientific research report writing."""
    pass


@cli.command()
@click.argument("report_file", type=click.Path(exists=True))
def literature(report_file):
    """Run Literature Review Agent."""
    click.echo(f"Running Literature Review Agent on: {report_file}")


@cli.command()
@click.argument("report_file", type=click.Path(exists=True))
def validity(report_file):
    """Run Scientific Validity Agent."""
    click.echo(f"Running Scientific Validity Agent on: {report_file}")


@cli.command()
@click.argument("report_file", type=click.Path(exists=True))
def evaluation(report_file):
    """Run Report Evaluation Agent."""
    click.echo(f"Running Report Evaluation Agent on: {report_file}")


@cli.command()
def ui():
    """Start interactive UI."""
    click.echo("Starting interactive UI...")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host, port, reload):
    """Start FastAPI server for document evaluation."""
    import uvicorn
    click.echo(f"Starting API server on http://{host}:{port}")
    click.echo("API documentation available at http://localhost:8000/docs")
    uvicorn.run(
        "ataskaitos.api:app",
        host=host,
        port=port,
        reload=reload,
    )


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def extract(path):
    """Extract all PDFs in PATH to markdown. Supports page ranges like file-5-10.pdf"""
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
        match = re.match(r"(.+) (\d+)-(\d+)\.pdf$", pdf_file.name)

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
    """Split PDF pages. Usage: split input.pdf 5-10 output.pdf"""
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


if __name__ == "__main__":
    cli()
