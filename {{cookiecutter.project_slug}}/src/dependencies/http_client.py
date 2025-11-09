{% if cookiecutter.include_middleware_logging == "yes" -%}
import httpx
from typing import AsyncGenerator


_http_client: httpx.AsyncClient = None


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
    try:
        yield _http_client
    finally:
        # Don't close here, let the lifespan handle cleanup
        pass


async def close_http_client():
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None
{% endif -%}
