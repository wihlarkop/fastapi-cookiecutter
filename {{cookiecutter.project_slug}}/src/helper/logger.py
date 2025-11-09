{% if cookiecutter.use_structured_logging == "yes" -%}
import logging
import logging.config
import sys
from typing import Any, Dict

import structlog
from pythonjsonlogger.json import JsonFormatter

from src.config import settings
from src.version import VERSION


def setup_logging() -> None:
    """Configure logging with JSON format using structlog and python-json-logger."""

    # Configure standard library logging
    _configure_stdlib_logging()

    # Configure structlog
    _configure_structlog()


def _configure_stdlib_logging() -> None:
    """Configure standard library logging with JSON formatter."""

    # Create custom JSON formatter
    class CustomJsonFormatter(JsonFormatter):
        def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord,
                       message_dict: Dict[str, Any]) -> None:
            super().add_fields(log_record, record, message_dict)

            # Add standard fields
            log_record['timestamp'] = record.created
            log_record['level'] = record.levelname
            log_record['logger'] = record.name
            log_record['module'] = record.module
            log_record['function'] = record.funcName
            log_record['line'] = record.lineno
            log_record['app_name'] = settings.APP_NAME
            log_record['app_env'] = settings.APP_ENV
            log_record['app_version'] = VERSION

            # Extract structured data from JSON message
            if isinstance(log_record.get('message'), str):
                try:
                    import json
                    message_data = json.loads(log_record['message'])
                    if isinstance(message_data, dict):
                        # Extract event_type to root level
                        if 'event_type' in message_data:
                            log_record['event_type'] = message_data.pop('event_type')

                        # Use the human-readable 'event' as the message
                        if 'event' in message_data:
                            log_record['message'] = message_data.pop('event')

                        # Add remaining structured fields to log record
                        for key, value in message_data.items():
                            if key not in ['logger', 'level', 'timestamp']:  # Skip duplicates
                                log_record[key] = value
                except (json.JSONDecodeError, TypeError):
                    # If it's not JSON, leave as is
                    pass

    # Configure handler
    handler = logging.StreamHandler(sys.stdout)

    if settings.LOG_FORMAT == "json":
        formatter = CustomJsonFormatter(
            fmt='%(timestamp)s %(level)s %(logger)s %(module)s %(function)s %(line)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.LOG_LEVEL)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
{% if cookiecutter.use_database == "yes" -%}
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
{% endif -%}


def _configure_structlog() -> None:
    """Configure structlog for structured logging."""

    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.LOG_FORMAT == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


# Create application logger instance
logger = get_logger(__name__)
{% else -%}
import logging
import sys

from src.config import settings


def setup_logging() -> None:
    """Configure basic logging."""

    # Configure handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.LOG_LEVEL)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str = None):
    """Get a logger instance."""
    return logging.getLogger(name)


# Create application logger instance
logger = get_logger(__name__)
{% endif -%}
