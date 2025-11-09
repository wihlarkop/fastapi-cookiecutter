from fastapi import APIRouter, Depends

from src.dependencies.database import DBConnection
from src.dependencies.auth import get_auth_service, get_current_user
from src.services.auth import AuthService
from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
)
from src.helper.response import JsonResponse

auth_router = APIRouter(prefix="{{ cookiecutter.api_prefix }}/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=JsonResponse[UserResponse])
async def register(
    request: RegisterRequest,
    conn: DBConnection,
    auth_service: AuthService = Depends(get_auth_service),
) -> JsonResponse[UserResponse]:
    """Register a new user."""
{% if cookiecutter.use_async_database == "yes" -%}
    user = await auth_service.register(conn, request)
{% else -%}
    user = auth_service.register(conn, request)
{% endif -%}
    return JsonResponse(
        data=user,
        message="User registered successfully",
    )


@auth_router.post("/login", response_model=JsonResponse[TokenResponse])
async def login(
    request: LoginRequest,
    conn: DBConnection,
    auth_service: AuthService = Depends(get_auth_service),
) -> JsonResponse[TokenResponse]:
    """Login and get access/refresh tokens."""
{% if cookiecutter.use_async_database == "yes" -%}
    tokens = await auth_service.login(conn, request)
{% else -%}
    tokens = auth_service.login(conn, request)
{% endif -%}
    return JsonResponse(
        data=tokens,
        message="Login successful",
    )


@auth_router.post("/refresh", response_model=JsonResponse[TokenResponse])
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> JsonResponse[TokenResponse]:
    """Refresh access token using refresh token."""
    tokens = auth_service.refresh_access_token(request.refresh_token)
    return JsonResponse(
        data=tokens,
        message="Token refreshed successfully",
    )


@auth_router.get("/me", response_model=JsonResponse[UserResponse])
async def get_me(
    current_user: UserResponse = Depends(get_current_user),
) -> JsonResponse[UserResponse]:
    """Get current authenticated user."""
    return JsonResponse(
        data=current_user,
        message="User retrieved successfully",
    )
