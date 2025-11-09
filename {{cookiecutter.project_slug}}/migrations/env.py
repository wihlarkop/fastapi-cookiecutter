{% if cookiecutter.use_async_database == "yes" -%}
import asyncio
{% endif -%}
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
{% if cookiecutter.use_async_database == "yes" -%}
from sqlalchemy.ext.asyncio import create_async_engine
{% else -%}
from sqlalchemy import create_engine
{% endif -%}

from src.database.client import metadata
from src.config import settings
from src.helper.generator import build_connection_url
{% if cookiecutter.include_authentication == "yes" -%}
from src.models.user import users  # noqa: F401
{% endif -%}

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
{%- if cookiecutter.database_type == "PostgreSQL" %}
    url = build_connection_url(
{% if cookiecutter.use_async_database == "yes" -%}
        driver_name="postgresql+psycopg",
{% else -%}
        driver_name="postgresql+psycopg2",
{% endif -%}
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    )
{%- elif cookiecutter.database_type == "MySQL" %}
    url = build_connection_url(
{% if cookiecutter.use_async_database == "yes" -%}
        driver_name="mysql+asyncmy",
{% else -%}
        driver_name="mysql+pymysql",
{% endif -%}
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DB,
    )
{%- elif cookiecutter.database_type == "SQLite" %}
    url = f"sqlite{% if cookiecutter.use_async_database == "yes" %}+aiosqlite{% endif %}:///{settings.SQLITE_DB_PATH}"
{%- endif %}

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


{% if cookiecutter.use_async_database == "yes" -%}
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Run migrations in 'online' mode with async engine."""
{%- if cookiecutter.database_type == "PostgreSQL" %}
    url = build_connection_url(
        driver_name="postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    )
{%- elif cookiecutter.database_type == "MySQL" %}
    url = build_connection_url(
        driver_name="mysql+asyncmy",
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DB,
    )
{%- elif cookiecutter.database_type == "SQLite" %}
    url = f"sqlite+aiosqlite:///{settings.SQLITE_DB_PATH}"
{%- endif %}

    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())
{% else -%}
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
{%- if cookiecutter.database_type == "PostgreSQL" %}
    url = build_connection_url(
        driver_name="postgresql+psycopg2",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    )
{%- elif cookiecutter.database_type == "MySQL" %}
    url = build_connection_url(
        driver_name="mysql+pymysql",
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DB,
    )
{%- elif cookiecutter.database_type == "SQLite" %}
    url = f"sqlite:///{settings.SQLITE_DB_PATH}"
{%- endif %}

    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
{% endif -%}


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
