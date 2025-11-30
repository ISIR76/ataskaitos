#!/usr/bin/env python
"""Demo: Load evaluation data and run simple sklearn analysis."""

import sys

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


def analyze_features(csv_file: str):
    """Quick sklearn demo with the converted data."""
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} documents\n")
    print(df[["file", "is_rd", "overall_score"]].to_string(index=False))

    # Prepare features
    feature_cols = [c for c in df.columns if c not in ["file", "model", "is_rd", "overall_score"]]
    X = df[feature_cols]  # noqa: N806
    y = df["is_rd"]
    print(f"\nFeatures: {len(feature_cols)} | Target: {y.value_counts().to_dict()}\n")

    # Random Forest
    print("=" * 80)
    print("FEATURE IMPORTANCE (Random Forest)")
    print("=" * 80)
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=3)
    rf.fit(X, y)
    importance_df = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_}).sort_values(
        "importance", ascending=False
    )
    print("\nTop 10:")
    print(importance_df.head(10).to_string(index=False))

    # Logistic Regression
    print("\n" + "=" * 80)
    print("LOGISTIC REGRESSION COEFFICIENTS")
    print("=" * 80)
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X, y)
    coef_df = pd.DataFrame({"feature": feature_cols, "coefficient": lr.coef_[0]}).sort_values(
        "coefficient", key=abs, ascending=False
    )
    print("\nTop 10:")
    print(coef_df.head(10).to_string(index=False))

    # Decision Tree
    print("\n" + "=" * 80)
    print("DECISION TREE (depth=3)")
    print("=" * 80)
    dt = DecisionTreeClassifier(max_depth=3, random_state=42)
    dt.fit(X, y)
    tree_features = sorted({feature_cols[i] for i in dt.tree_.feature if i >= 0})
    print(f"\nFeatures: {', '.join(tree_features)}")

    # Predictions
    y_pred = dt.predict(X)
    results = df[["file", "is_rd"]].copy()
    results["predicted"] = y_pred
    results["correct"] = results["is_rd"] == results["predicted"]
    accuracy = results["correct"].mean()
    print(f"\n{results.to_string(index=False)}")
    print(f"\nAccuracy: {results['correct'].sum()}/{len(results)} = {accuracy:.1%}")

    # Summary
    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print("\n1. Top 3 Random Forest:")
    for _, row in importance_df.head(3).iterrows():
        print(f"   {row['feature']:30s}: {row['importance']:.3f}")
    print("\n2. Top 3 Logistic Regression:")
    for _, row in coef_df.head(3).iterrows():
        sign = "+" if row["coefficient"] > 0 else "-"
        print(f"   {row['feature']:30s}: {row['coefficient']:+.3f} ({sign})")
    print(f"\n3. Tree uses: {', '.join(tree_features)} → {accuracy:.1%}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python demo_sklearn.py <csv_file>")
        print("\nExample:")
        print("  python demo_sklearn.py agent_evaluation_20251129_113134_ml_format.csv")
        sys.exit(1)

    analyze_features(sys.argv[1])
