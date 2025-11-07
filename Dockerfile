# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for document processing
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project files
COPY pyproject.toml ./
COPY README.md ./

# Copy source code
COPY ataskaitos ./ataskaitos
COPY main.py ./

# Install dependencies using uv
RUN uv sync --frozen

# Expose port for Cloud Run
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the FastAPI server using uvicorn
CMD ["uv", "run", "uvicorn", "ataskaitos.api:app", "--host", "0.0.0.0", "--port", "8080"]
