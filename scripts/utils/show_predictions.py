#!/usr/bin/env python
"""Show evaluation scores in tabular format."""

import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python show_predictions.py <evaluation_file.json>")
    sys.exit(1)

with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)

# Collect all files and their scores
rows = []

for result in data["results"]:
    if not result["evaluation"]:
        continue

    eval_data = result["evaluation"]
    row = {"file": Path(result["file"]).name}

    # Collect all scores
    for key, value in eval_data.items():
        if isinstance(value, dict) and "score" in value:
            row[key] = float(value["score"])
        elif key == "score":
            row["OVERALL"] = float(value)

    rows.append(row)

# Get all criteria (excluding file)
criteria = [k for k in rows[0].keys() if k != "file"]

# Print header
print(f"{'File':<15}", end="")
for c in criteria:
    print(f"{c:<8}", end="")
print()
print("=" * (15 + len(criteria) * 8))

# Print rows
for row in rows:
    print(f"{row['file']:<15}", end="")
    for c in criteria:
        val = row.get(c, "")
        if isinstance(val, float):
            print(f"{val:<8.2f}", end="")
        else:
            print(f"{val:<8}", end="")
    print()
