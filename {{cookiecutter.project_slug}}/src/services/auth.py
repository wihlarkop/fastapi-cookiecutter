import uuid
from datetime import datetime

{% if cookiecutter.use_async_database == "yes" -%}
from sqlalchemy.ext.asyncio import AsyncConnection
{% else -%}
from sqlalchemy import Connection
{% endif -%}

from src.entities.user import UserEntity
from src.repositories.interface import UserInterface
from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    AccessTokenPayload,
    RefreshTokenPayload,
    UserResponse,
)
from src.helper.jwt_token import JWTHelper
from src.helper.password import hash_password, verify_password
from src.exceptions.auth import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class AuthService:
    """Authentication service for user operations."""

    def __init__(self, user_repo: UserInterface, jwt_helper: JWTHelper):
        self.user_repo = user_repo
        self.jwt_helper = jwt_helper

{% if cookiecutter.use_async_database == "yes" -%}
    async def register(self, conn: AsyncConnection, request: RegisterRequest) -> UserResponse:
{% else -%}
    def register(self, conn: Connection, request: RegisterRequest) -> UserResponse:
{% endif -%}
        """Register a new user."""
        # Check if user already exists
{% if cookiecutter.use_async_database == "yes" -%}
        existing_user = await self.user_repo.get_by_email(conn, request.email)
{% else -%}
        existing_user = self.user_repo.get_by_email(conn, request.email)
{% endif -%}
        if existing_user:
            raise UserAlreadyExistsError("User with this email already exists")

{% if cookiecutter.use_async_database == "yes" -%}
        existing_username = await self.user_repo.get_by_username(conn, request.username)
{% else -%}
        existing_username = self.user_repo.get_by_username(conn, request.username)
{% endif -%}
        if existing_username:
            raise UserAlreadyExistsError("User with this username already exists")

        # Create new user
        user = UserEntity(
            id=str(uuid.uuid4()),
            email=request.email,
            username=request.username,
            hashed_password=hash_password(request.password),
            full_name=request.full_name,
            is_active=True,
            is_superuser=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

{% if cookiecutter.use_async_database == "yes" -%}
        await self.user_repo.create(conn, user)
{% else -%}
        self.user_repo.create(conn, user)
{% endif -%}

        return UserResponse.model_validate(user, from_attributes=True)

{% if cookiecutter.use_async_database == "yes" -%}
    async def login(self, conn: AsyncConnection, request: LoginRequest) -> TokenResponse:
{% else -%}
    def login(self, conn: Connection, request: LoginRequest) -> TokenResponse:
{% endif -%}
        """Authenticate user and return tokens."""
        # Get user by email
{% if cookiecutter.use_async_database == "yes" -%}
        user = await self.user_repo.get_by_email(conn, request.email)
{% else -%}
        user = self.user_repo.get_by_email(conn, request.email)
{% endif -%}
        if not user:
            raise InvalidCredentialsError()

        # Verify password
        if not verify_password(request.password, user["hashed_password"]):
            raise InvalidCredentialsError()

        # Check if user is active
        if not user["is_active"]:
            raise InvalidCredentialsError("User account is disabled")

        # Generate tokens
        access_token_payload = AccessTokenPayload(
            sub=user["id"],
            email=user["email"],
            username=user["username"],
        )
        refresh_token_payload = RefreshTokenPayload(sub=user["id"])

        access_token = self.jwt_helper.create_access_token(access_token_payload.model_dump())
        refresh_token = self.jwt_helper.create_refresh_token(refresh_token_payload.model_dump())

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Generate new access token from refresh token."""
        # Verify refresh token
        payload = self.jwt_helper.verify_token(refresh_token, token_type="refresh")

        # Generate new tokens
        access_token_payload = {"sub": payload["sub"]}
        refresh_token_payload = {"sub": payload["sub"]}

        new_access_token = self.jwt_helper.create_access_token(access_token_payload)
        new_refresh_token = self.jwt_helper.create_refresh_token(refresh_token_payload)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

{% if cookiecutter.use_async_database == "yes" -%}
    async def get_current_user(self, conn: AsyncConnection, token: str) -> UserResponse:
{% else -%}
    def get_current_user(self, conn: Connection, token: str) -> UserResponse:
{% endif -%}
        """Get current user from access token."""
        # Verify token
        payload = self.jwt_helper.verify_token(token, token_type="access")

        # Get user
{% if cookiecutter.use_async_database == "yes" -%}
        user = await self.user_repo.get_by_id(conn, payload["sub"])
{% else -%}
        user = self.user_repo.get_by_id(conn, payload["sub"])
{% endif -%}
        if not user:
            raise UserNotFoundError()

        return UserResponse.model_validate(**user)
