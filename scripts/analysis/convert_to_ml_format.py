#!/usr/bin/env python
"""Convert evaluation results to ML-ready format (pandas/sklearn compatible)."""

import json
import sys
from pathlib import Path


def convert_to_records(json_file: str) -> list[dict]:
    """Convert evaluation JSON to list of flat dictionaries (records).

    Returns list of dicts where each dict is one document with:
    - All criterion scores as float features
    - Target variable (is_rd: 0 or 1)
    - Metadata (file, model)
    """
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    records = []

    for result in data["results"]:
        if not result["evaluation"]:
            continue

        eval_data = result["evaluation"]

        # Create flat record
        record = {}

        # Metadata
        file_path = result["file"]
        record["file"] = Path(file_path).name
        record["model"] = result["model"]

        # Target variable (1 = GOOD R&D, 0 = NOT R&D)
        # Based on folder: ok/ = 1, not_ok/ = 0
        record["is_rd"] = 1 if "/ok/" in file_path.lower() else 0

        # Extract all scores
        for key, value in eval_data.items():
            if isinstance(value, dict) and "score" in value:
                # Convert string scores to float
                try:
                    record[key] = float(value["score"])
                except (ValueError, TypeError):
                    record[key] = None
            elif key == "score":
                # Overall score
                try:
                    record["overall_score"] = float(value)
                except (ValueError, TypeError):
                    record["overall_score"] = None

        records.append(record)

    return records


def save_csv(records: list[dict], output_file: str):
    """Save records to CSV file."""
    import csv

    if not records:
        return

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def save_pickle(records: list[dict], output_file: str):
    """Save records to pickle file (for pandas)."""
    import pickle

    with open(output_file, "wb") as f:
        pickle.dump(records, f)


def print_summary(records: list[dict]):
    """Print summary statistics."""
    print("=" * 80)
    print("CONVERSION SUMMARY")
    print("=" * 80)
    print(f"Total records: {len(records)}")

    if records:
        print(f"\nFeatures: {len(records[0]) - 3} (excluding file, model, is_rd)")
        print("\nFeature names:")
        features = [k for k in records[0] if k not in ["file", "model", "is_rd"]]
        for i, feat in enumerate(features, 1):
            print(f"  {i:2d}. {feat}")

        # Target distribution
        rd_count = sum(r["is_rd"] for r in records)
        not_rd_count = len(records) - rd_count
        print("\nTarget distribution:")
        print(f"  is_rd=1 (GOOD R&D): {rd_count}")
        print(f"  is_rd=0 (NOT R&D):  {not_rd_count}")

        # Example record
        print("\nExample record (first document):")
        for key, value in list(records[0].items())[:10]:
            print(f"  {key:20s}: {value}")
        if len(records[0]) > 10:
            print(f"  ... and {len(records[0]) - 10} more features")


def demo_sklearn_usage():
    """Print example sklearn usage code."""
    print("\n" + "=" * 80)
    print("SKLEARN USAGE EXAMPLE")
    print("=" * 80)
    print("""
# Load the data
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Option 1: Load from CSV
df = pd.read_csv('evaluation_ml_format.csv')

# Option 2: Load from pickle
import pickle
with open('evaluation_ml_format.pkl', 'rb') as f:
    records = pickle.load(f)
df = pd.DataFrame(records)

# Prepare features and target
feature_cols = [c for c in df.columns if c not in ['file', 'model', 'is_rd', 'overall_score']]
X = df[feature_cols]
y = df['is_rd']

# Handle missing values if any
X = X.fillna(0)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': clf.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance.head(10))
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_to_ml_format.py <evaluation_file.json> [output_base_name]")
        print("\nExample:")
        print("  python convert_to_ml_format.py evaluation.json")
        print("  python convert_to_ml_format.py evaluation.json my_data")
        sys.exit(1)

    input_file = sys.argv[1]

    # Determine output base name
    if len(sys.argv) > 2:
        output_base = sys.argv[2]
    else:
        # Use input filename without extension
        output_base = Path(input_file).stem + "_ml_format"

    # Convert
    print(f"Converting {input_file}...")
    records = convert_to_records(input_file)

    # Save in multiple formats (timestamped + latest)
    csv_file = f"{output_base}.csv"
    pkl_file = f"{output_base}.pkl"
    csv_latest = "agent_evaluation_latest_ml_format.csv"
    pkl_latest = "agent_evaluation_latest_ml_format.pkl"

    save_csv(records, csv_file)
    save_pickle(records, pkl_file)
    save_csv(records, csv_latest)
    save_pickle(records, pkl_latest)

    print("\n✓ Saved:")
    print(f"  {csv_file}")
    print(f"  {pkl_file}")
    print(f"  {csv_latest}")
    print(f"  {pkl_latest}")

    # Print summary
    print_summary(records)

    # Print usage example
    demo_sklearn_usage()
