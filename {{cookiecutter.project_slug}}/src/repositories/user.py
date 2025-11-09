from sqlalchemy import select, insert, update
{% if cookiecutter.use_async_database == "yes" -%}
from sqlalchemy.ext.asyncio import AsyncConnection
{% else -%}
from sqlalchemy import Connection
{% endif -%}
from sqlalchemy.engine.row import RowMapping

from src.models.user import users
from src.entities.user import UserEntity
from src.repositories.interface import UserInterface


class UserRepositories(UserInterface):
    """User repository for database operations."""

{% if cookiecutter.use_async_database == "yes" -%}
    async def get_by_email(self, conn: AsyncConnection, email: str) -> RowMapping | None:
{% else -%}
    def get_by_email(self, conn: Connection, email: str) -> RowMapping | None:
{% endif -%}
        """Get user by email."""
        query = select(users).where(users.c.email == email, users.c.deleted_at.is_(None))
{% if cookiecutter.use_async_database == "yes" -%}
        result = await conn.execute(query)
{% else -%}
        result = conn.execute(query)
{% endif -%}
        return result.mappings().first()

{% if cookiecutter.use_async_database == "yes" -%}
    async def get_by_username(self, conn: AsyncConnection, username: str) -> RowMapping | None:
{% else -%}
    def get_by_username(self, conn: Connection, username: str) -> RowMapping | None:
{% endif -%}
        """Get user by username."""
        query = select(users).where(users.c.username == username, users.c.deleted_at.is_(None))
{% if cookiecutter.use_async_database == "yes" -%}
        result = await conn.execute(query)
{% else -%}
        result = conn.execute(query)
{% endif -%}
        return result.mappings().first()

{% if cookiecutter.use_async_database == "yes" -%}
    async def get_by_id(self, conn: AsyncConnection, user_id: str) -> RowMapping | None:
{% else -%}
    def get_by_id(self, conn: Connection, user_id: str) -> RowMapping | None:
{% endif -%}
        """Get user by ID."""
        query = select(users).where(users.c.id == user_id, users.c.deleted_at.is_(None))
{% if cookiecutter.use_async_database == "yes" -%}
        result = await conn.execute(query)
{% else -%}
        result = conn.execute(query)
{% endif -%}
        return result.mappings().first()

{% if cookiecutter.use_async_database == "yes" -%}
    async def create(self, conn: AsyncConnection, user: UserEntity) -> None:
{% else -%}
    def create(self, conn: Connection, user: UserEntity) -> None:
{% endif -%}
        """Create a new user."""
        query = insert(users).values(**user.model_dump())
{% if cookiecutter.use_async_database == "yes" -%}
        await conn.execute(query)
        await conn.commit()
{% else -%}
        conn.execute(query)
        conn.commit()
{% endif -%}

{% if cookiecutter.use_async_database == "yes" -%}
    async def update_password(self, conn: AsyncConnection, user_id: str, hashed_password: str) -> None:
{% else -%}
    def update_password(self, conn: Connection, user_id: str, hashed_password: str) -> None:
{% endif -%}
        """Update user password."""
        query = update(users).where(users.c.id == user_id).values(hashed_password=hashed_password)
{% if cookiecutter.use_async_database == "yes" -%}
        await conn.execute(query)
        await conn.commit()
{% else -%}
        conn.execute(query)
        conn.commit()
{% endif -%}
