# Build stage
FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
{%- if cookiecutter.database_type == "PostgreSQL" %}
    libpq-dev \
{%- elif cookiecutter.database_type == "MySQL" %}
    default-libmysqlclient-dev \
{%- endif %}
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and source code for package installation
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
RUN uv sync --frozen --no-cache

# Runtime stage
FROM python:{{ cookiecutter.python_version }}-slim-bookworm

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
{%- if cookiecutter.database_type == "PostgreSQL" %}
    libpq5 \
{%- elif cookiecutter.database_type == "MySQL" %}
    default-mysql-client \
{%- endif %}
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Set permissions
RUN chown -R appuser:appuser /app

USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; \
        try: \
            with urllib.request.urlopen('http://localhost:{{ cookiecutter.default_port }}/health', timeout=10) as response: \
                if response.status >= 400: \
                    sys.exit(1) \
                sys.exit(0) \
        except Exception: \
            sys.exit(1)"

EXPOSE {{ cookiecutter.default_port }}

CMD ["python", "main.py"]
