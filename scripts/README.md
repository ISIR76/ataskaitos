# Development Scripts

Utilities for batch evaluation, analysis, and ML experimentation.

## Directory Structure

### analysis/
ML and statistical analysis tools:
- `analyze_classification.py` - Classification accuracy (OK vs NOT_OK)
- `analyze_evaluation.py` - Agent evaluation statistics
- `analyze_results.py` - Model performance comparison
- `convert_to_ml_format.py` - Convert evaluations to pandas/sklearn format
- `demo_sklearn.py` - Feature importance (Random Forest, Decision Trees)

### evaluation/
Batch evaluation runners:
- `run_agent.py` - Parallel agent evaluation on multiple documents

### utils/
Helper utilities:
- `combine_results.py` - Convert JSON evaluation results to CSV
- `show_predictions.py` - Display predictions in tabular format

### conversion/
Document format conversion:
- `convert_docx_to_md.py` - DOCX to Markdown converter

## Usage Examples

See main [Makefile](../Makefile) for convenient targets:
```bash
make eval-agent          # Run batch agent evaluation
make convert-latest      # Convert to ML format
make analyze-latest      # Run sklearn analysis
make pipeline            # Full workflow
```

## Development Workflow

### 1. Batch Evaluation
Run evaluations on multiple documents:
```bash
# Using Makefile
make eval-reports        # Evaluate reports (Frascati)
make eval-articles       # Evaluate articles (SMSM subset)
make eval-agent          # Run agent evaluation

# Direct script execution
uv run python scripts/evaluation/run_agent.py "docs/**/*.docx" 5
```

### 2. Convert to ML Format
Convert evaluation JSON to pandas/sklearn format:
```bash
make convert-latest
# or
uv run python scripts/analysis/convert_to_ml_format.py evaluation.json
```

### 3. Run Analysis
Analyze evaluation results:
```bash
make analyze-latest
# or
uv run python scripts/analysis/demo_sklearn.py evaluation_ml_format.csv
```

### 4. View Results
Display predictions in tabular format:
```bash
make show-latest
# or
uv run python scripts/utils/show_predictions.py evaluation.json
```

## Full Pipeline
Run the complete workflow (evaluate → convert → analyze):
```bash
make pipeline
```
