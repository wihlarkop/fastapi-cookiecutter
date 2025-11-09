from fastapi import Depends, Header

from src.dependencies.database import DBConnection
from src.repositories.user import UserRepositories
from src.services.auth import AuthService
from src.helper.jwt_token import JWTHelper
from src.exceptions.auth import UnauthorizedError
from src.schemas.auth import UserResponse


def get_auth_service() -> AuthService:
    """Get authentication service instance."""
    jwt_helper = JWTHelper()
    user_repo = UserRepositories()
    return AuthService(user_repo=user_repo, jwt_helper=jwt_helper)


{% if cookiecutter.use_async_database == "yes" -%}
async def get_current_user(
{% else -%}
def get_current_user(
{% endif -%}
    authorization: str = Header(..., description="Bearer token"),
    conn: DBConnection = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Get current authenticated user from Bearer token."""
    # Extract token from Authorization header
    if not authorization.startswith("Bearer "):
        raise UnauthorizedError("Invalid authorization header format")

    token = authorization.replace("Bearer ", "")

    # Get user from token
{% if cookiecutter.use_async_database == "yes" -%}
    user = await auth_service.get_current_user(conn, token)
{% else -%}
    user = auth_service.get_current_user(conn, token)
{% endif -%}
    return user
