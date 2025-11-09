import os
import signal
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
{% if cookiecutter.include_cors == "yes" -%}
from fastapi.middleware.cors import CORSMiddleware
{% endif -%}
from fastapi.responses import ORJSONResponse

from src.config import settings
{% if cookiecutter.include_health_check == "yes" -%}
from src.controllers.health import health_router
{% endif -%}
{% if cookiecutter.include_authentication == "yes" -%}
from src.controllers.auth import auth_router
{% endif -%}
{% if cookiecutter.use_database == "yes" -%}
from src.database.client import engine, client as db_client
{% endif -%}
{% if cookiecutter.include_middleware_logging == "yes" -%}
from src.dependencies.http_client import close_http_client
{% endif -%}
from src.exceptions.exception_registration import exception_handlers
from src.helper.logger import setup_logging, get_logger
{% if cookiecutter.include_middleware_logging == "yes" -%}
from src.middleware.asgi_logging import ASGILoggingMiddleware
{% endif -%}
from src.version import VERSION


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Record startup start time
    startup_start = time.time()

    # Setup logging on startup
    setup_logging()
    logger = get_logger(__name__)

    logger.info(
        "Application starting up",
        event_type="app_startup_started",
        app_name=settings.APP_NAME,
        app_version=VERSION
    )

{% if cookiecutter.use_cloud_sql == "yes" -%}
    # Initialize Cloud SQL connector in the current event loop
    if db_client.use_cloud_sql:
        await db_client.init_connector()
        logger.info(
            "Cloud SQL connector initialized",
            event_type="cloud_sql_connector_initialized"
        )

{% endif -%}
    # Calculate and log startup time
    startup_time = time.time() - startup_start
    logger.info(
        "Application startup completed",
        event_type="app_startup_completed",
        app_name=settings.APP_NAME,
        app_version=VERSION,
        startup_time_seconds=round(startup_time, 4),
        startup_time_ms=round(startup_time * 1000, 2)
    )

    yield {}

    # Cleanup on shutdown
    shutdown_start = time.time()
    logger.info(
        "Application shutting down",
        event_type="app_shutdown_started"
    )

{% if cookiecutter.use_database == "yes" -%}
    await db_client.close()
{% endif -%}
{% if cookiecutter.include_middleware_logging == "yes" -%}
    await close_http_client()
{% endif -%}

    shutdown_time = time.time() - shutdown_start
    logger.info(
        "Application shutdown completed",
        event_type="app_shutdown_completed",
        shutdown_time_seconds=round(shutdown_time, 4),
        shutdown_time_ms=round(shutdown_time * 1000, 2)
    )


app = FastAPI(
    title=settings.APP_NAME,
    version=VERSION,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
)

{% if cookiecutter.include_cors == "yes" -%}
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

{% endif -%}
{% if cookiecutter.include_middleware_logging == "yes" -%}
# Add ASGI logging middleware (avoids BaseHTTPMiddleware limitations)
app.add_middleware(ASGILoggingMiddleware)

{% endif -%}
{% if cookiecutter.include_health_check == "yes" -%}
app.include_router(health_router)
{% endif -%}
{% if cookiecutter.include_authentication == "yes" -%}
app.include_router(auth_router)
{% endif -%}

if __name__ == "__main__":
    try:
        uvicorn.run(
            app="main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
        )
    except KeyboardInterrupt:
        pass
    finally:
        os.kill(os.getpid(), signal.SIGINT)
