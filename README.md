# FastAPI Cookiecutter Template

A production-ready FastAPI project template following clean architecture principles, inspired by the ezdocs-service architecture.

## Features

- **Clean Architecture**: Layered separation (Controllers → Services → Repositories → Database)
- **Multiple Database Support**: PostgreSQL, MySQL, SQLite with async/sync options
- **Authentication System**: JWT-based auth with Argon2 password hashing
- **Database Migrations**: Alembic with async support
- **Structured Logging**: structlog with JSON formatting
- **ASGI Middleware**: Optimized pure ASGI logging middleware
- **Type Safety**: Protocol-based repository interfaces
- **Docker Support**: Multi-stage builds with uv package manager
- **Testing**: pytest setup with fixtures
- **Configuration**: Pydantic Settings with validation

## Prerequisites

- Python 3.10+
- [cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Quick Start

### 1. Install Cookiecutter

```bash
pip install cookiecutter
```

### 2. Generate Project

```bash
cookiecutter https://github.com/yourusername/fastapi-cookiecutter
```

Or from local path:

```bash
cookiecutter /path/to/fastapi-cookiecutter
```

### 3. Answer the Prompts

You'll be asked to configure your project:

```
project_name [My FastAPI Project]:
project_slug [my-fastapi-project]:
description [A FastAPI project]:
author [Your Name]:
python_version [3.12]:
version [0.1.0]:
use_database [yes]:
database_type [PostgreSQL]:
use_async_database [yes]:
use_alembic [yes]:
include_authentication [yes]:
use_jwt [yes]:
include_testing [yes]:
use_docker [yes]:
include_cors [yes]:
...
```

### 4. Navigate to Project and Install Dependencies

```bash
cd my-fastapi-project

# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 5. Configure Environment

```bash
cp .env-example .env
# Edit .env with your configuration
```

### 6. Run Database Migrations (if using database)

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

### 7. Run the Application

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration Options

### Database

- **use_database**: Enable/disable database support
- **database_type**: Choose PostgreSQL, MySQL, or SQLite
- **use_async_database**: Enable async database operations
- **use_alembic**: Include Alembic for migrations
- **use_cloud_sql**: Enable Google Cloud SQL connector

### Authentication

- **include_authentication**: Full JWT-based authentication system
- **use_jwt**: JWT token helper utilities

When authentication is enabled, you get:
- User registration endpoint: `POST /api/v1/auth/register`
- Login endpoint: `POST /api/v1/auth/login`
- Token refresh: `POST /api/v1/auth/refresh`
- Get current user: `GET /api/v1/auth/me`
- Argon2 password hashing
- Protocol-based user repository

### Features

- **include_health_check**: Health and version endpoint
- **include_testing**: pytest setup with fixtures
- **include_cors**: CORS middleware configuration
- **include_middleware_logging**: ASGI logging middleware
- **include_external_integrations**: Folder for external service integrations
- **use_structured_logging**: structlog with JSON formatting

### Docker

- **use_docker**: Include Dockerfile and .dockerignore
- Multi-stage builds for optimized image size
- Database-specific runtime dependencies

## Project Structure

```
my-fastapi-project/
├── main.py                      # Application entry point
├── src/
│   ├── config.py               # Pydantic settings
│   ├── version.py              # Version constant
│   ├── controllers/            # API endpoints (routes)
│   │   ├── health.py
│   │   └── auth.py            # If authentication enabled
│   ├── services/              # Business logic
│   │   └── auth.py            # If authentication enabled
│   ├── repositories/          # Data access layer
│   │   ├── interface.py       # Protocol interfaces
│   │   └── user.py            # If authentication enabled
│   ├── models/                # SQLAlchemy table definitions
│   │   └── user.py            # If authentication enabled
│   ├── entities/              # Pydantic entities
│   │   └── user.py            # If authentication enabled
│   ├── schemas/               # Request/Response schemas
│   │   ├── health.py
│   │   └── auth.py            # If authentication enabled
│   ├── dependencies/          # FastAPI dependencies
│   │   ├── database.py
│   │   ├── http_client.py
│   │   └── auth.py            # If authentication enabled
│   ├── database/              # Database client
│   │   └── client.py
│   ├── helper/                # Utility functions
│   │   ├── generator.py
│   │   ├── logger.py
│   │   ├── response.py
│   │   ├── jwt_token.py       # If JWT enabled
│   │   └── password.py        # If authentication enabled
│   ├── middleware/            # Custom middleware
│   │   └── asgi_logging.py
│   ├── exceptions/            # Custom exceptions
│   │   ├── base.py
│   │   ├── exception_registration.py
│   │   ├── jwt_token.py       # If JWT enabled
│   │   └── auth.py            # If authentication enabled
│   └── integrations/          # External service integrations (optional)
├── migrations/                # Alembic migrations (if enabled)
│   └── env.py
├── test/                      # Tests (if enabled)
│   ├── conftest.py
│   └── test_health.py
├── .env-example               # Environment variables template
├── pyproject.toml             # Project dependencies
├── Dockerfile                 # Docker configuration (if enabled)
└── alembic.ini                # Alembic configuration (if enabled)
```

## Architecture

The template follows **Clean Architecture** principles:

### Layers

1. **Controllers** (`src/controllers/`): Handle HTTP requests/responses, validate input
2. **Services** (`src/services/`): Contain business logic, orchestrate operations
3. **Repositories** (`src/repositories/`): Data access layer, database operations
4. **Models** (`src/models/`): SQLAlchemy table definitions
5. **Entities** (`src/entities/`): Pydantic models representing domain objects

### Dependency Flow

```
Controllers → Services → Repositories → Database
     ↓           ↓            ↓
  Schemas    Entities    Models (Tables)
```

### Key Patterns

- **Protocol Interfaces**: Repositories use Python's `Protocol` for structural typing
- **Dependency Injection**: Services receive repositories via constructor injection
- **Repository Pattern**: All database access goes through repository layer
- **SQLAlchemy Core**: Uses Table API instead of ORM for better control

## Authentication System

When `include_authentication=yes`, you get a complete JWT-based authentication system:

### Features

- User registration with email/username validation
- Login with email and password
- JWT access and refresh tokens
- Token refresh endpoint
- Get current user endpoint
- Argon2 password hashing (more secure than bcrypt)
- Protocol-based repository interface

### Usage Example

```python
# Register a new user
POST /api/v1/auth/register
{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
}

# Login
POST /api/v1/auth/login
{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}

# Response
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}

# Get current user (with Authorization header)
GET /api/v1/auth/me
Authorization: Bearer <access_token>

# Refresh token
POST /api/v1/auth/refresh
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Protecting Routes

```python
from fastapi import Depends
from src.dependencies.auth import get_current_user
from src.schemas.auth import UserResponse

@router.get("/protected")
async def protected_route(
    current_user: UserResponse = Depends(get_current_user)
):
    return {"message": f"Hello {current_user.username}"}
```

## Development

### Running Tests

```bash
pytest
```

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality

The template includes configuration for:

- **Ruff**: Fast Python linter and formatter
- **pytest**: Testing framework

Run checks:

```bash
# Lint code
ruff check .

# Format code
ruff format .
```

### Docker

Build and run with Docker:

```bash
# Build image
docker build -t my-fastapi-project .

# Run container
docker run -p 8000:8000 --env-file .env my-fastapi-project
```

## Adding New Features

### 1. Add a New Endpoint

Create the layers in this order:

1. **Model** (if database): `src/models/item.py`
2. **Entity**: `src/entities/item.py`
3. **Schema**: `src/schemas/item.py`
4. **Repository Interface**: Add to `src/repositories/interface.py`
5. **Repository**: `src/repositories/item.py`
6. **Service**: `src/services/item.py`
7. **Controller**: `src/controllers/item.py`
8. **Register Router**: Add to `main.py`

### 2. Example: Items CRUD

```python
# 1. Model (src/models/item.py)
from sqlalchemy import Table, Column, String, Integer
from src.database.client import metadata

items = Table(
    "items",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("quantity", Integer, nullable=False),
)

# 2. Repository Interface (src/repositories/interface.py)
from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncConnection

class ItemInterface(Protocol):
    async def get_items(self, conn: AsyncConnection) -> list: ...
    async def create_item(self, conn: AsyncConnection, item) -> None: ...

# 3. Repository (src/repositories/item.py)
from src.repositories.interface import ItemInterface

class ItemRepositories(ItemInterface):
    async def get_items(self, conn, page: int = 1, limit: int = 10):
        # Implementation
        pass

# 4. Service (src/services/item.py)
class ItemService:
    def __init__(self, item_repo: ItemInterface):
        self.item_repo = item_repo

# 5. Controller (src/controllers/item.py)
from fastapi import APIRouter, Depends

item_router = APIRouter(prefix="/api/v1/items", tags=["Items"])

@item_router.get("/")
async def get_items(service: ItemService = Depends(get_item_service)):
    # Implementation
    pass
```

## Environment Variables

Key environment variables (see `.env-example` for complete list):

```bash
# Application
APP_NAME=my-fastapi-project
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Database (PostgreSQL example)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=myapp

# JWT (if authentication enabled)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Post-Generation Hooks

The template uses hooks to automatically remove unnecessary files based on your configuration:

- If `use_database=no`: Removes database client, migrations, models
- If `include_authentication=no`: Removes auth models, services, controllers
- If `use_docker=no`: Removes Dockerfile and .dockerignore
- If `include_testing=no`: Removes test directory
- If `use_jwt=no`: Removes JWT helper and exceptions

This keeps your generated project clean and minimal!

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/yourusername/fastapi-cookiecutter).
