# Ataskaitos - Scientific Document Evaluation Platform

AI-powered evaluation platform for scientific documents (R&D reports and articles).

## Quick Start

### Installation
```bash
uv sync
```

### Run API Server
```bash
make dev
# or
uv run uvicorn ataskaitos.api:app --reload
```

API available at: http://localhost:8000
API docs: http://localhost:8000/docs

### Environment Setup
Copy `.env.example` to `.env` and configure:
```bash
OPENAI_API_KEY=sk-...  # Required for agents
```

## Architecture

See [CLAUDE.md](CLAUDE.md) for AI assistant context.
See [API.md](API.md) for API documentation.

### Document Types
- **Reports** (ataskaitos) - R&D activities evaluated against Frascati Manual
- **Articles** (straipsniai) - Scientific publications evaluated against SMSM standards

### Evaluation Modes
- **Scoring Mode** - Multiple LLM judges with 0.0-1.0 scores (pydantic_evals)
- **Agent Mode** - AI agents with structured Pydantic output schemas

### Directory Structure
```
ataskaitos/           # Main package (production)
├── agents/           # Agent definitions and schemas
├── evaluators/       # JSON evaluator configurations
│   ├── articles/     # SMSM judges for articles
│   └── reports/      # Frascati judges for reports
├── api/              # FastAPI routes and models
├── services/         # Business logic
└── evals.py          # Report evaluators (dev tool)

straipsniai/          # Article evaluation (dev tool)
└── evals.py          # Article evaluators (subset testing)

scripts/              # Development utilities
├── analysis/         # ML and statistical analysis
├── evaluation/       # Batch evaluation runners
└── utils/            # Conversion and display tools

tests/                # Test suite
```

## CLI Usage

The CLI provides hierarchical commands for document evaluation:

### Single File Evaluation

```bash
# Evaluate report with agent
uv run python -m ataskaitos.cli ataskaitos agent report.docx

# Evaluate report with specific evaluators
uv run python -m ataskaitos.cli ataskaitos evals report.docx -e novelty_score -e systematic_score

# Evaluate article with agent
uv run python -m ataskaitos.cli straipsniai agent article.pdf -o results.json

# Evaluate article with evals
uv run python -m ataskaitos.cli straipsniai evals article.md
```

### Batch Evaluation

```bash
# Batch evaluate reports with agents
uv run python -m ataskaitos.cli ataskaitos agent --batch "docs/**/*.docx" -c 5

# Batch evaluate articles with evals
uv run python -m ataskaitos.cli straipsniai evals --batch "docs/articles/**/*.md"
```

### Utility Commands

```bash
# Start API server
uv run python -m ataskaitos.cli serve --reload

# Extract PDFs to markdown
uv run python -m ataskaitos.cli extract docs/pdfs/

# Split PDF pages
uv run python -m ataskaitos.cli split input.pdf 5-10 output.pdf
```

## Development Workflows

### Makefile Shortcuts

```bash
# Evaluation
make eval-reports    # Batch evaluate reports (Frascati)
make eval-articles   # Batch evaluate articles (SMSM subset)
make eval-agent      # Run agent evaluation

# Analysis pipeline
make pipeline        # Full workflow: evaluate → convert → analyze
make convert-latest  # Convert to ML format
make analyze-latest  # Run sklearn analysis
make show-latest     # Display predictions

# Utilities
make clean           # Remove generated outputs
make lint            # Run linter
make lint-fix        # Fix linting issues
```

## API Usage

### Evaluate Document
```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "...",
    "document_type": "report",
    "evaluation_type": "scoring",
    "evaluators": ["novelty_score", "systematic_score"]
  }'
```

See [API.md](API.md) for full endpoint documentation.

## Standards
- **Frascati Manual** - OECD R&D statistics standard (for reports)
- **SMSM Regulation** - Lithuanian scientific publication standards (for articles)

## Tech Stack
- FastAPI, PydanticAI, pydantic-evals
- OpenAI API (GPT-4o for agents)
- markitdown (DOCX→Markdown conversion)
- scikit-learn (ML analysis)
- uv (package manager)
