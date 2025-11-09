{% if cookiecutter.use_database == "yes" -%}
from typing import Annotated, AsyncIterator

from fastapi import Depends
{% if cookiecutter.use_async_database == "yes" -%}
from sqlalchemy.ext.asyncio import AsyncConnection
{% else -%}
from sqlalchemy import Connection
{% endif -%}

from src.database.client import engine


{% if cookiecutter.use_async_database == "yes" -%}
async def get_connection() -> AsyncIterator[AsyncConnection]:
    async with engine.connect() as connection:
        yield connection


DBConnection: type[AsyncConnection] = Annotated[AsyncConnection, Depends(get_connection)]
{% else -%}
def get_connection() -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


DBConnection: type[Connection] = Annotated[Connection, Depends(get_connection)]
{% endif -%}
{% endif -%}
