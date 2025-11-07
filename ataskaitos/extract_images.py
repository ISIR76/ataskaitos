#!/usr/bin/env python3
"""Extract base64-encoded images from markdown files to separate image files."""

import re
import base64
from pathlib import Path
from typing import Counter


def extract_images(markdown_file: Path, output_dir: Path) -> int:
    """Extract all base64-encoded images from markdown file.

    Args:
        markdown_file: Path to markdown file with embedded images
        output_dir: Directory to save extracted images

    Returns:
        Number of images extracted
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    content = markdown_file.read_text(encoding="utf-8")

    # Match data URI pattern: ![alt](data:image/type;base64,DATA)
    pattern = r"!\[([^\]]*)\]\(data:image/([^;]+);base64,([^\)]+)\)"

    image_counter = Counter[str]()

    for match in re.finditer(pattern, content):
        alt_text, image_type, base64_data = match.groups()

        # Generate filename
        image_counter[image_type] += 1
        filename = f"image_{image_counter[image_type]:03d}.{image_type}"
        output_path = output_dir / filename

        # Decode and save
        image_data = base64.b64decode(base64_data)
        output_path.write_bytes(image_data)

        print(f"Extracted: {filename} ({len(image_data):,} bytes)")

    total = sum(image_counter.values())
    return total


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_images.py <markdown_file> [output_dir]")
        print("Example: python extract_images.py energus-ataskaita-full.md images/")
        sys.exit(1)

    markdown_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "images")

    if not markdown_file.exists():
        print(f"Error: {markdown_file} not found")
        sys.exit(1)

    print(f"Extracting images from: {markdown_file}")
    print(f"Output directory: {output_dir}")
    print()

    count = extract_images(markdown_file, output_dir)

    print()
    print(f"✓ Extracted {count} images to {output_dir}/")


if __name__ == "__main__":
    main()
