from fastapi import status
from fastapi.exceptions import RequestValidationError, HTTPException

from src.exceptions.base import BaseCustomException, create_exception_handler

# --- Exception registration dict ---
exception_handlers = {
    # Base exception handlers
    HTTPException: create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        message="Something went wrong"
    ),
    RequestValidationError: create_exception_handler(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Request validation failed"
    ),
    BaseCustomException: create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ),
    Exception: create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Unhandled internal server error"
    ),
    # Add your custom exception handlers here
    # Example:
    # CustomException: create_exception_handler(
    #     status_code=status.HTTP_404_NOT_FOUND
    # ),
}
