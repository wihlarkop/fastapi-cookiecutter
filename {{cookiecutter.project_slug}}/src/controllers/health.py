from fastapi import APIRouter, Request
{% if cookiecutter.use_database == "yes" -%}
from sqlalchemy import select

from src.dependencies.database import DBConnection
{% endif -%}
from src.config import settings
from src.helper.response import JsonResponse
from src.schemas.health import HealthResponse{% if cookiecutter.use_database == "yes" %}, Status{% endif %}
from src.version import VERSION

health_router = APIRouter(tags=["Health"])


@health_router.get(path="/health")
async def health_check(
    request: Request
{% if cookiecutter.use_database == "yes" -%}
    , conn: DBConnection
{% endif -%}
) -> JsonResponse[HealthResponse]:
{% if cookiecutter.use_database == "yes" -%}
    db_health = await conn.execute(select(1))
    health_result = db_health.scalar()

    status = Status(database=(health_result == 1))

    result = HealthResponse(
        name=settings.APP_NAME,
        version=VERSION,
        status=status
    )
{% else -%}
    result = HealthResponse(
        name=settings.APP_NAME,
        version=VERSION
    )
{% endif -%}

    return JsonResponse(
        data=result,
        message="Ok",
    )
