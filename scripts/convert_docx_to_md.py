#!/usr/bin/env python3
"""Convert DOCX files to Markdown using markitdown."""

import sys
from pathlib import Path

from markitdown import MarkItDown


def convert_docx(input_path: str, output_path: str | None = None) -> None:
    """
    Convert a DOCX file to Markdown.

    Args:
        input_path: Path to input DOCX file
        output_path: Optional path to output MD file. If not provided,
                    will use same name as input with .md extension
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    if not input_file.suffix.lower() == ".docx":
        print(f"Warning: File doesn't have .docx extension: {input_file}")

    # Determine output path
    if output_path:
        output_file = Path(output_path)
    else:
        output_file = input_file.with_suffix(".md")

    # Convert
    print(f"Converting: {input_file}")
    md = MarkItDown()
    result = md.convert(str(input_file))

    # Save
    output_file.write_text(result.text_content, encoding="utf-8")

    print(f"✓ Converted to: {output_file}")
    print(f"  Length: {len(result.text_content)} characters")
    print(f"  Lines: {len(result.text_content.splitlines())}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_docx_to_md.py <input.docx> [output.md]")
        print("\nExamples:")
        print("  python convert_docx_to_md.py document.docx")
        print("  python convert_docx_to_md.py document.docx output.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    convert_docx(input_file, output_file)
