"""Authentication exceptions."""

from src.exceptions.base import BaseCustomException
from fastapi import status


class InvalidCredentialsError(BaseCustomException):
    """Raised when credentials are invalid."""
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_CREDENTIALS"
        )


class UserAlreadyExistsError(BaseCustomException):
    """Raised when user already exists."""
    def __init__(self, message: str = "User already exists"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="USER_ALREADY_EXISTS"
        )


class UserNotFoundError(BaseCustomException):
    """Raised when user is not found."""
    def __init__(self, message: str = "User not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="USER_NOT_FOUND"
        )


class UnauthorizedError(BaseCustomException):
    """Raised when user is unauthorized."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )
