dev:
	uv run uvicorn ataskaitos.api:app --host=localhost --port=8000 --reload

# Evaluation workflows
eval-agent:
	uv run python scripts/evaluation/run_agent.py

eval-reports:
	uv run python ataskaitos/evals.py

eval-articles:
	uv run python straipsniai/evals.py

# Analysis pipeline
convert-latest:
	uv run python scripts/analysis/convert_to_ml_format.py docs/out/reports/agent_evaluations/agent_evaluation_latest.json

analyze-latest:
	uv run python scripts/analysis/demo_sklearn.py agent_evaluation_latest_ml_format.csv

show-latest:
	uv run python scripts/utils/show_predictions.py docs/out/reports/agent_evaluations/agent_evaluation_latest.json

pdf-latest:
	uv run python scripts/analysis/generate_pdf_report.py docs/out/reports/agent_evaluations/agent_evaluation_latest.json

# Utilities
combine-results:
	uv run python scripts/utils/combine_results.py

# Linting
lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

# Full workflow: evaluate → convert → analyze
pipeline: eval-agent convert-latest analyze-latest

# Cleanup development outputs
clean:
	rm -f *_evaluation_results*.json *_evaluation_results*.csv
	rm -f *_ml_format.csv *_ml_format.pkl
	rm -f temp_fresh_results.json
	rm -rf docs/out/reports/agent_evaluations/*.json

# Restore from backup if needed
restore-backup:
	@echo "Backup files are in backup/ directory"
	@echo "Manually copy files back if needed"

.PHONY: dev eval-agent eval-reports eval-articles convert-latest analyze-latest show-latest pdf-latest combine-results lint lint-fix pipeline clean restore-backup