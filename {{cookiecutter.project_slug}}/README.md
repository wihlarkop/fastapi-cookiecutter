# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Features

- ✅ FastAPI framework with async support
- ✅ Clean architecture (Controllers → Services → Repositories)
- ✅ Pydantic for configuration and validation
{% if cookiecutter.use_database == "yes" -%}
- ✅ {{ cookiecutter.database_type }} database with SQLAlchemy {% if cookiecutter.use_async_database == "yes" %}(async){% endif %}
{% endif -%}
{% if cookiecutter.use_alembic == "yes" -%}
- ✅ Alembic for database migrations
{% endif -%}
{% if cookiecutter.use_structured_logging == "yes" -%}
- ✅ Structured logging with structlog
{% endif -%}
{% if cookiecutter.include_middleware_logging == "yes" -%}
- ✅ ASGI request/response logging middleware
{% endif -%}
{% if cookiecutter.include_cors == "yes" -%}
- ✅ CORS middleware configured
{% endif -%}
{% if cookiecutter.use_jwt == "yes" -%}
- ✅ JWT authentication support
{% endif -%}
{% if cookiecutter.include_testing == "yes" -%}
- ✅ Testing with pytest
{% endif -%}
{% if cookiecutter.use_docker == "yes" -%}
- ✅ Docker multi-stage build
{% endif -%}
{% if cookiecutter.use_ruff == "yes" -%}
- ✅ Code linting and formatting with Ruff
{% endif -%}

## Prerequisites

- Python {{ cookiecutter.python_version }}+
- uv (recommended) or pip
{% if cookiecutter.database_type == "PostgreSQL" -%}
- PostgreSQL
{% elif cookiecutter.database_type == "MySQL" -%}
- MySQL
{% endif -%}

## Setup

### 1. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Using `pip`:
```bash
pip install -e .
```

### 2. Environment Configuration

Copy the example environment file and update values:
```bash
cp .env-example .env
```

Edit `.env` with your configuration:
- Update `SECRET_KEY` with a secure random key (min 32 characters)
{% if cookiecutter.use_database == "yes" -%}
- Configure database connection settings
{% endif -%}
- Adjust other settings as needed

{% if cookiecutter.use_alembic == "yes" -%}
### 3. Database Migration

Run Alembic migrations:
```bash
alembic upgrade head
```

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```
{% endif -%}

## Running the Application

### Development

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port {{ cookiecutter.default_port }}
```

{% if cookiecutter.use_docker == "yes" -%}
### Docker

Build and run with Docker:
```bash
docker build -t {{ cookiecutter.project_slug }} .
docker run -p {{ cookiecutter.default_port }}:{{ cookiecutter.default_port }} --env-file .env {{ cookiecutter.project_slug }}
```
{% endif -%}

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:{{ cookiecutter.default_port }}/docs
- ReDoc: http://localhost:{{ cookiecutter.default_port }}/redoc

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── main.py                 # Application entry point
├── src/
│   ├── config.py          # Configuration management
│   ├── version.py         # Application version
│   ├── controllers/       # API route handlers
│   ├── services/          # Business logic layer
│   ├── repositories/      # Data access layer
│   ├── entities/          # Domain models
│   ├── schemas/           # Request/response schemas
│   ├── models/            # Database table definitions
{% if cookiecutter.use_database == "yes" -%}
│   ├── database/          # Database client
{% endif -%}
│   ├── dependencies/      # Dependency injection
│   ├── exceptions/        # Custom exceptions
│   ├── middleware/        # ASGI middleware
│   ├── helper/            # Utility functions
{% if cookiecutter.include_external_integrations == "yes" -%}
│   └── integrations/      # External service integrations
{% endif -%}
{% if cookiecutter.use_alembic == "yes" -%}
├── migrations/            # Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini            # Alembic configuration
{% endif -%}
{% if cookiecutter.include_testing == "yes" -%}
├── test/                  # Test files
{% endif -%}
{% if cookiecutter.use_docker == "yes" -%}
├── Dockerfile             # Docker configuration
├── .dockerignore
{% endif -%}
├── pyproject.toml         # Project dependencies
└── .env-example           # Environment variables template
```

## Development

{% if cookiecutter.use_ruff == "yes" -%}
### Code Quality

Format code:
```bash
ruff format .
```

Lint code:
```bash
ruff check .
```

Auto-fix issues:
```bash
ruff check --fix .
```
{% endif -%}

{% if cookiecutter.include_testing == "yes" -%}
### Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=src --cov-report=html
```
{% endif -%}

## License

This project is licensed under the terms specified by {{ cookiecutter.author_name }}.

## Author

{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
