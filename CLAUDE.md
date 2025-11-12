# CLAUDE.md

AI-powered platform for evaluating scientific documents (R&D reports and articles).

## Architecture

### Two Evaluation Modes

**1. Scoring Mode** - Multiple LLM judges evaluate against specific criteria (0.0-1.0 scores)
- Evaluators defined in JSON files: `ataskaitos/evaluators/{articles|reports}/*.json`
- Each evaluator has a `rubric` (evaluation criteria) and returns scored results
- Example: `novelty_score`, `rigor_score`, `systematic_score`

**2. Agent Mode** - AI agents provide structured evaluation output
- Agents defined in `ataskaitos/agents.py` with Pydantic output schemas
- Multiple agents can run in parallel, each with different analysis depth
- Example: `simple_article_agent`, `detailed_article_agent`

### Document Types

- **Reports** - R&D activities evaluated against Frascati Manual (8 evaluators, 1 agent)
- **Articles** - Scientific publications evaluated against SMSM standards (18 evaluators, 2 agents)

### Tech Stack

- **Backend**: FastAPI, PydanticAI, pydantic-evals, markitdown (DOCX→Markdown)
- **Frontend**: React, TypeScript, TanStack Router, openapi-fetch, Tailwind CSS
- **Package Manager**: uv (Python)


## Key Files

- `ataskaitos/agents.py` - Agent definitions with Pydantic schemas
- `ataskaitos/evaluators/` - JSON evaluator configurations (articles/, reports/)
- `ataskaitos/api/routes/evaluate.py` - Evaluation endpoint
- `ataskaitos/services/evaluation_service.py` - Evaluation orchestration
- `frontend/src/components/DocumentUpload.tsx` - Upload UI with evaluator/agent selection
- `frontend/src/components/EvaluationResults.tsx` - Results display

## Adding New Evaluators/Agents

**Add Scoring Evaluator** (JSON):
```json
// ataskaitos/evaluators/articles/custom_judges.json
[
  {
    "name": "clarity_score",
    "rubric": "Evaluate writing clarity...",
    "has_assertion": false
  }
]
```
Automatically loaded on startup. No code changes needed.

**Add Agent** (Python):
```python
# In ataskaitos/agents.py
class CustomEvaluation(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    summary: str

agent = Agent(
    model=OpenAIModel("gpt-4o"),
    output_type=CustomEvaluation,
    system_prompt="..."
)

# Register in get_agent_registry()
registry.register("article", "custom_agent", agent, {...})
```

## Running

```bash
# Backend
cd ataskaitos && uv run python -m ataskaitos.api.app

# Frontend
cd frontend && npm run dev

# Environment
OPENAI_API_KEY=sk-... # Required for agents
```

## Standards

- **Frascati Manual** - OECD R&D statistics standard (for reports)
- **SMSM Regulation** - Lithuanian scientific publication standards (for articles)

## Document Processing Tools

### Converting DOCX to Markdown

Use `markitdown` to convert Word documents to markdown format:

```bash
# Install markitdown
uv add markitdown

# Basic conversion (images are truncated by default)
uv run python -m markitdown file.docx > output.md

# Keep full base64-encoded images (larger file size)
uv run python -m markitdown --keep-data-uris file.docx > output-with-images.md
```

**Important**: By default, markitdown truncates base64-encoded images. Use `--keep-data-uris` flag to preserve full embedded images in the output.

### Extracting Images from Markdown

Use the `extract_images.py` utility script to extract embedded base64 images:

```bash
# Extract to default 'images/' directory
uv run python extract_images.py markdown_file.md

# Extract to custom directory
uv run python extract_images.py markdown_file.md output_dir/
```

The script:
- Extracts all base64-encoded images from markdown files
- Saves them as separate files with proper extensions (PNG, JPEG, EMF, etc.)
- Names files sequentially (image_001.png, image_002.png, etc.)
- Shows extraction progress and file sizes

**EMF files**: Enhanced Metafile format (Windows vector graphics) commonly found in Office documents. These are technical diagrams and charts that can be converted to PNG if needed.
