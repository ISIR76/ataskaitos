# Ataskaitos API Documentation

API for evaluating scientific research reports using two different approaches.

## Authentication

The API uses X-API-Key header authentication that is **environment-dependent**:

### Development Mode (Default)
```bash
ENV=development
```
- No authentication required
- All endpoints are open
- Suitable for local development

### Production Mode
```bash
ENV=production
API_KEY=your_secure_api_key_here
```
- X-API-Key header required for evaluation endpoints
- Health and list endpoints remain public
- Generate a secure key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

**Example with authentication:**
```bash
curl -X POST "http://localhost:8000/evaluate/agent" \
  -H "X-API-Key: your_secure_api_key_here" \
  -F "file=@report.docx"
```

## Starting the Server

```bash
# Using CLI command
uv run python main.py serve --reload

# Or directly with uvicorn
uv run uvicorn ataskaitos.api:app --reload

# Default: http://localhost:8000
# API docs: http://localhost:8000/docs
```

## Two Evaluation Approaches

### 1. Agent-Based Evaluation (`/evaluate/agent`)

**What it is**: Single AI agent that provides flexible, comprehensive qualitative analysis.

**When to use**:
- Need narrative evaluation with reasoning
- Want flexible output schemas (structured or text)
- Need comprehensive analysis in natural language

**Output type**: Flexible - can be structured (FrascatiEvaluation schema) or plain text

**Example**:
```bash
curl -X POST "http://localhost:8000/evaluate/agent" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@report.docx"
```

**Response**:
```json
{
  "markdown_content": "# Research Report...",
  "agent_output": "Comprehensive analysis text or structured output...",
  "evaluation_type": "agent",
  "status": "success"
}
```

---

### 2. Scoring-Based Evaluation (`/evaluate/scoring`)

**What it is**: Multiple LLM judges score the document against standardized criteria.

**When to use**:
- Need quantitative scores (0.0-1.0 scale)
- Want to compare multiple documents
- Need consistent evaluation format
- Require benchmarking data

**Output type**: Standardized evaluation report with scores, reasons, and metrics

**Example**:
```bash
curl -X POST "http://localhost:8000/evaluate/scoring" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@report.docx"
```

**Response**:
```json
{
  "markdown_content": "# Research Report...",
  "evaluation_results": {
    "name": "report.docx",
    "total_cases": 1,
    "total_failures": 0,
    "averages": {
      "scores": {
        "short_evaluator": 0.8,
        "combined_score": 0.75,
        "novelty_score": 0.6,
        "creativity_score": 0.7,
        "uncertainty_score": 0.8,
        "systematic_score": 0.67,
        "transferable_score": 1.0,
        "comprehensive_rd_score": 0.72
      }
    },
    "cases": [
      {
        "scores": {
          "short_evaluator": {"value": 0.8, "reason": "Detailed reasoning..."},
          "novelty_score": {"value": 0.6, "reason": "Evidence from document..."}
        }
      }
    ]
  },
  "evaluation_type": "scoring",
  "status": "success"
}
```

## Evaluators in Scoring System

The scoring system uses 8 evaluators from [ataskaitos/evals.py](ataskaitos/evals.py):

1. **short_evaluator** - Basic Frascati R&D check
   - Tests 3 core conditions: NEW, UNCERTAIN, SYSTEMATIC
   - Score: 1.0 if all met, 0.0 if any missing

2. **combined_score** - All 5 Frascati criteria
   - NOVEL (0.2) + CREATIVE (0.2) + UNCERTAIN (0.2) + SYSTEMATIC (0.2) + TRANSFERABLE (0.2)
   - ≥0.8 qualifies as R&D

3. **novelty_score** - Individual novelty level
   - 0.0-1.0 scale from routine to groundbreaking

4. **creativity_score** - Individual creativity level
   - 0.0-1.0 scale from standard to entirely new methodology

5. **uncertainty_score** - Individual uncertainty assessment
   - Distinguishes R&D uncertainty from business/team uncertainty

6. **systematic_score** - Planning and organization
   - Based on hypothesis, methodology, resources

7. **transferable_score** - Reproducibility assessment
   - Documentation, reproducibility, communicability

8. **comprehensive_rd_score** - Complete Frascati evaluation
   - 6 parts: Core criteria (0.5) + Exclusions (0.1) + R&D content (0.15) + Innovation boundary (0.1) + Personnel (0.075) + Documentation (0.075)
   - ≥0.80: STRONG R&D, 0.65-0.79: MODERATE, 0.50-0.64: BORDERLINE

### List all evaluators:

```bash
curl http://localhost:8000/evaluators/list
```

## Supported File Formats

- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents
- `.doc` - Legacy Word documents
- `.txt` - Plain text
- `.md` - Markdown files

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/health` | GET | Detailed health check with available methods |
| `/evaluate/agent` | POST | Agent-based qualitative evaluation |
| `/evaluate/scoring` | POST | Scoring-based quantitative evaluation |
| `/evaluators/list` | GET | List all scoring evaluators and criteria |

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can:
- Try out endpoints directly
- See request/response schemas
- Upload files and see results

## Key Differences Summary

| Aspect | Agent-Based | Scoring-Based |
|--------|-------------|---------------|
| **Output** | Flexible (text or structured) | Standardized scores |
| **Evaluators** | Single agent | 8 LLM judges |
| **Use case** | Qualitative analysis | Quantitative comparison |
| **Format** | Narrative/structured | Scores (0.0-1.0) with reasons |
| **Framework** | PydanticAI Agent | pydantic-evals LLMJudge |
| **Best for** | Comprehensive reports | Benchmarking, metrics |

## Example: Python Client

```python
import os
import requests

# Get API key from environment (if in production)
API_KEY = os.getenv("API_KEY", "")
headers = {"X-API-Key": API_KEY} if API_KEY else {}

# Agent-based evaluation
with open("report.docx", "rb") as f:
    response = requests.post(
        "http://localhost:8000/evaluate/agent",
        files={"file": f},
        headers=headers  # Include API key in production
    )
    result = response.json()
    print(result["agent_output"])

# Scoring-based evaluation
with open("report.docx", "rb") as f:
    response = requests.post(
        "http://localhost:8000/evaluate/scoring",
        files={"file": f},
        headers=headers  # Include API key in production
    )
    result = response.json()
    scores = result["evaluation_results"]["averages"]["scores"]
    print(f"Comprehensive R&D Score: {scores['comprehensive_rd_score']}")
```

## Environment Setup

Make sure you have the required configuration in `.env`:

```bash
# LLM API Keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
ANTHROPIC_API_KEY=...

# API Server Configuration
ENV=development  # or "production" for authentication
API_KEY=your_secure_api_key_here  # Required in production

# Optional: Override models per agent
LITERATURE_MODEL=openai:gpt-4o
VALIDITY_MODEL=google:gemini-1.5-pro
EVALUATION_MODEL=openai:gpt-4o
```

**Generate a secure API key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
