from datetime import datetime
from typing import Callable, Coroutine, Any

from fastapi import status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from src.helper.response import JsonResponse


class BaseCustomException(HTTPException):
    def __init__(
            self,
            message: str | list[str],
            status_code: int = 500,
            error_code: str = None,
            details: dict = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.error_code = error_code
        self.details = details


class NotFoundError(BaseCustomException):
    def __init__(self, resource: str, identifier: str, details: dict = None):
        msg = f"{resource} with identifier '{identifier}' not found"
        error_code = f"{resource.upper()}_NOT_FOUND"
        super().__init__(
            message=msg,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            details=details
        )


class InternalServerError(BaseCustomException):
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)


def error_response(
        message: str,
        status_code: int,
        error_code: str = None,
) -> JsonResponse:
    now = datetime.now().isoformat()

    return JsonResponse(
        data=None,
        message=message,
        status_code=status_code,
        timestamp=now,
        success=False,
        error_code=error_code,
    )


def extract_validation_errors(exc: RequestValidationError) -> list[str]:
    """
    Extract all meaningful field-level error messages from a RequestValidationError.
    Example output:
    [
      "integration_account: Input should be a valid string",
      "name: Field required"
    ]
    """
    messages = []

    for err in exc.errors():
        loc = err.get("loc", [])
        msg = err.get("msg", "Invalid input")

        # Get the most relevant field name
        field = next(
            (part for part in reversed(loc)
             if isinstance(part, str) and part not in {"body", "query", "path", "model"}),
            "field"
        )

        messages.append(f"{field}: {msg}")

    return messages


def create_exception_handler(
        status_code: int,
        message: str = None
) -> Callable[[Request, Exception], Coroutine[Any, Any, ORJSONResponse]]:
    async def handler(_: Request, exc: Exception) -> ORJSONResponse:
        code = status_code
        detail = message or str(exc)
        error_code = "InternalServerError"

        # 1. FastAPI validation
        if isinstance(exc, RequestValidationError):
            code = 422
            detail = extract_validation_errors(exc)
            error_code = "RequestValidationError"

        # 2. HTTPException (FastAPI default)
        elif isinstance(exc, HTTPException):
            code = exc.status_code
            detail = exc.detail
            error_code = type(exc).__name__

        # 3. Custom attribute check
        elif hasattr(exc, "message"):
            detail = getattr(exc, "message")
        elif hasattr(exc, "msg"):
            detail = getattr(exc, "msg")

        if hasattr(exc, "error_code"):
            error_code = getattr(exc, "error_code")

        error_result = error_response(
            message=detail,
            error_code=error_code,
            status_code=code
        ).model_dump(exclude_none=True, exclude_unset=True)

        return ORJSONResponse(error_result, status_code=code)

    return handler
