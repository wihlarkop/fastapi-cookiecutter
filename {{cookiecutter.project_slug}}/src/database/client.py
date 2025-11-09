{% if cookiecutter.use_database == "yes" -%}
import asyncio
from typing import Optional

{% if cookiecutter.use_cloud_sql == "yes" -%}
from google.cloud.sql.connector import Connector, create_async_connector
{% endif -%}
from sqlalchemy import MetaData
{% if cookiecutter.use_async_database == "yes" -%}
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
{% else -%}
from sqlalchemy import create_engine, Engine
{% endif -%}

from src.config import settings
from src.helper.generator import build_connection_url


class DatabaseClient:
    def __init__(self, use_cloud_sql: bool = False):
        self.use_cloud_sql = use_cloud_sql
{% if cookiecutter.use_cloud_sql == "yes" -%}
        self.connector: Optional[Connector] = None
{% endif -%}
{% if cookiecutter.use_async_database == "yes" -%}
        self._engine: Optional[AsyncEngine] = None
{% else -%}
        self._engine: Optional[Engine] = None
{% endif -%}

{% if cookiecutter.use_cloud_sql == "yes" -%}
    async def init_connector(self):
        """Initialize the Cloud SQL connector using create_async_connector"""
        if self.use_cloud_sql and self.connector is None:
            # Get the running event loop and pass it to Connector
            loop = asyncio.get_running_loop()
            self.connector = Connector(loop=loop)

    async def get_connection_callable(self):
        """
        Get connection for Cloud SQL.
        This is called by SQLAlchemy's async_creator.
        """
        if not self.connector:
            raise ValueError("Connector not initialized. Call init_connector() first.")

        connection = await self.connector.connect_async(
{%- if cookiecutter.database_type == "PostgreSQL" %}
            instance_connection_string=settings.CLOUD_SQL_INSTANCE_CONNECTION_NAME,
            driver="asyncpg",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            db=settings.POSTGRES_DB,
{%- elif cookiecutter.database_type == "MySQL" %}
            instance_connection_string=settings.CLOUD_SQL_INSTANCE_CONNECTION_NAME,
            driver="asyncmy",
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DB,
{%- endif %}
        )
        return connection

{% endif -%}
{% if cookiecutter.use_async_database == "yes" -%}
    def create_engine(self) -> AsyncEngine:
{% else -%}
    def create_engine(self) -> Engine:
{% endif -%}
        """Create SQLAlchemy {% if cookiecutter.use_async_database == "yes" %}async {% endif %}engine"""
        if self._engine is not None:
            return self._engine

{% if cookiecutter.use_cloud_sql == "yes" -%}
        if self.use_cloud_sql:
            # Use async_creator for Cloud SQL connector
            self._engine = create_async_engine(
{%- if cookiecutter.database_type == "PostgreSQL" %}
                "postgresql+asyncpg://",
{%- elif cookiecutter.database_type == "MySQL" %}
                "mysql+asyncmy://",
{%- endif %}
                async_creator=self.get_connection_callable,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_recycle=settings.DB_POOL_RECYCLE,
                pool_timeout=settings.DB_POOL_TIMEOUT,
                pool_pre_ping=settings.DB_POOL_PRE_PING,
            )
        else:
{% endif -%}
{%- if cookiecutter.database_type == "PostgreSQL" %}
            connection_url = build_connection_url(
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
            connection_url = build_connection_url(
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
            connection_url = f"sqlite{% if cookiecutter.use_async_database == "yes" %}+aiosqlite{% endif %}:///{settings.SQLITE_DB_PATH}"
{%- endif %}

{% if cookiecutter.use_async_database == "yes" -%}
            self._engine = create_async_engine(
{% else -%}
            self._engine = create_engine(
{% endif -%}
                url=connection_url,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_recycle=settings.DB_POOL_RECYCLE,
                pool_timeout=settings.DB_POOL_TIMEOUT,
                pool_pre_ping=settings.DB_POOL_PRE_PING,
            )

        return self._engine

{% if cookiecutter.use_async_database == "yes" -%}
    async def close(self):
{% else -%}
    def close(self):
{% endif -%}
        """Close the database engine and connector"""
        if self._engine:
{% if cookiecutter.use_async_database == "yes" -%}
            await self._engine.dispose()
{% else -%}
            self._engine.dispose()
{% endif -%}

{% if cookiecutter.use_cloud_sql == "yes" -%}
        if self.connector:
            await self.connector.close_async()
            self.connector = None
{% endif -%}


{% if cookiecutter.use_cloud_sql == "yes" -%}
client = DatabaseClient(use_cloud_sql=settings.USE_CLOUD_SQL)
{% else -%}
client = DatabaseClient()
{% endif -%}
engine = client.create_engine()
metadata = MetaData()
{% endif -%}
