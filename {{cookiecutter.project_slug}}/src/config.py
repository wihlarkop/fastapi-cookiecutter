from functools import lru_cache
from typing import Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache()
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables with fallback to .env file.

    This class uses Pydantic's BaseSettings to handle configuration from environment
    variables and .env files. It includes validation and type conversion.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        enable_decoding=False
    )

    # Application Settings
    APP_NAME: str = Field(default="{{ cookiecutter.project_name }}")
    APP_ENV: str = Field(default="local", description="Environment: local, development, staging, production")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default={{ cookiecutter.default_port }}, ge=1, le=65535)
    DEBUG: bool = Field(default=False)

    # Security Settings
    SECRET_KEY: str = Field(default=..., min_length=32, description="Secret key for JWT tokens")
    ALLOWED_HOSTS: list[str] = Field(default=["localhost", "127.0.0.1"], description="Allowed host headers")
{% if cookiecutter.include_cors == "yes" -%}
    ALLOWED_ORIGINS: list[str] = Field(default=["http://localhost:3000"], description="CORS allowed origins")
{% endif -%}

{% if cookiecutter.use_database == "yes" -%}
    # Database Settings
{%- if cookiecutter.database_type == "PostgreSQL" %}
    POSTGRES_USER: str = Field(default=..., description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(default=..., description="PostgreSQL password")
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, ge=1, le=65535, description="PostgreSQL port")
    POSTGRES_DB: str = Field(default=..., description="PostgreSQL database name")
{%- elif cookiecutter.database_type == "MySQL" %}
    MYSQL_USER: str = Field(default=..., description="MySQL username")
    MYSQL_PASSWORD: str = Field(default=..., description="MySQL password")
    MYSQL_HOST: str = Field(default="localhost", description="MySQL host")
    MYSQL_PORT: int = Field(default=3306, ge=1, le=65535, description="MySQL port")
    MYSQL_DB: str = Field(default=..., description="MySQL database name")
{%- elif cookiecutter.database_type == "SQLite" %}
    SQLITE_DB_PATH: str = Field(default="./app.db", description="SQLite database file path")
{%- endif %}

{% if cookiecutter.use_cloud_sql == "yes" -%}
    # Cloud SQL Settings (optional - only needed for Cloud SQL)
    USE_CLOUD_SQL: bool = Field(default=False, description="Use Cloud SQL instead of direct connection")
    CLOUD_SQL_INSTANCE_CONNECTION_NAME: str = Field(
        "",
        description="Cloud SQL instance connection name (project:region:instance)"
    )

{% endif -%}
    # Database Connection Pool Settings
    DB_POOL_SIZE: int = Field(default=20, ge=1, le=100, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=30, ge=0, le=100, description="Max overflow connections")
    DB_POOL_RECYCLE: int = Field(default=3600, ge=300, description="Connection recycle time in seconds")
    DB_POOL_TIMEOUT: int = Field(default=30, ge=5, description="Connection timeout in seconds")
    DB_POOL_PRE_PING: bool = Field(default=True, description="Enable connection pool pre-ping")

{% endif -%}
    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
{% if cookiecutter.use_structured_logging == "yes" -%}
    LOG_FORMAT: str = Field(default="{{ cookiecutter.log_format[0] }}", description="Log format: json or text")
{% endif -%}

{% if cookiecutter.use_jwt == "yes" -%}
    # JWT Settings
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        ge=1,
        description="Access token expiration time in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, description="Refresh token expiration time in days")

{% endif -%}
    # File Upload Settings
    MAX_FILE_SIZE: int = Field(default=50, description="Max file size in megabytes")

    @field_validator('ALLOWED_HOSTS', mode='before')
    @classmethod
    def decode_allowed_host(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            v = v.split(',')
        return [x.strip() for x in v]

{% if cookiecutter.include_cors == "yes" -%}
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def decode_allowed_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            v = v.split(',')
        return [x.strip() for x in v]

{% endif -%}
    @field_validator('APP_ENV', mode='before')
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed_envs = ['local', 'development', 'staging', 'production']
        if v not in allowed_envs:
            raise ValueError(f'Invalid environment. Must be one of: {allowed_envs}')
        return v

    @field_validator('LOG_LEVEL', mode='before')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed_levels:
            raise ValueError(f'Invalid log level. Must be one of: {allowed_levels}')
        return v.upper()

{% if cookiecutter.use_structured_logging == "yes" -%}
    @field_validator('LOG_FORMAT', mode='before')
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        allowed_formats = ['json', 'text']
        if v not in allowed_formats:
            raise ValueError(f'Invalid log format. Must be one of: {allowed_formats}')
        return v

{% endif -%}
    @model_validator(mode='after')
    def validate_production_settings(self) -> Self:
        if self.APP_ENV == 'production' and self.DEBUG:
            raise ValueError('DEBUG must be False in production')
        return self

    @property
    def is_production(self) -> bool:
        """Check if the application is running in production environment."""
        return self.APP_ENV == 'production'

    @property
    def is_development(self) -> bool:
        """Check if the application is running in development environment."""
        return self.APP_ENV in ['local', 'development']


settings = Settings()
