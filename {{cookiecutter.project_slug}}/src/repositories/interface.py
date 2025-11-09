{% if cookiecutter.use_database == "yes" -%}
from typing import Protocol, Sequence

from sqlalchemy.engine.row import RowMapping
{% if cookiecutter.use_async_database == "yes" -%}
from sqlalchemy.ext.asyncio.engine import AsyncConnection
{% else -%}
from sqlalchemy.engine import Connection
{% endif -%}

{% if cookiecutter.include_authentication == "yes" -%}
from src.entities.user import UserEntity


class UserInterface(Protocol):
    """User repository interface."""

{% if cookiecutter.use_async_database == "yes" -%}
    async def get_by_email(self, conn: AsyncConnection, email: str) -> RowMapping | None: ...

    async def get_by_username(self, conn: AsyncConnection, username: str) -> RowMapping | None: ...

    async def get_by_id(self, conn: AsyncConnection, user_id: str) -> RowMapping | None: ...

    async def create(self, conn: AsyncConnection, user: UserEntity) -> None: ...

    async def update_password(self, conn: AsyncConnection, user_id: str, hashed_password: str) -> None: ...
{% else -%}
    def get_by_email(self, conn: Connection, email: str) -> RowMapping | None: ...

    def get_by_username(self, conn: Connection, username: str) -> RowMapping | None: ...

    def get_by_id(self, conn: Connection, user_id: str) -> RowMapping | None: ...

    def create(self, conn: Connection, user: UserEntity) -> None: ...

    def update_password(self, conn: Connection, user_id: str, hashed_password: str) -> None: ...
{% endif -%}

{% endif -%}

# Define your repository interfaces here using Protocol
# Example:
#
# class ExampleRepositoryInterface(Protocol):
#     async def get_items(
#         self, conn: {% if cookiecutter.use_async_database == "yes" %}AsyncConnection{% else %}Connection{% endif %}, page: int, limit: int
#     ) -> tuple[Sequence[RowMapping], int]: ...
#
#     async def get_item(self, conn: {% if cookiecutter.use_async_database == "yes" %}AsyncConnection{% else %}Connection{% endif %}, item_id: str) -> RowMapping | None: ...
{% endif -%}
