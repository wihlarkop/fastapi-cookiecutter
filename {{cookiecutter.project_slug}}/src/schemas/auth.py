from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)


class RegisterRequest(BaseModel):
    """User registration request schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    full_name: str | None = None


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: EmailStr
    username: str
    full_name: str | None = None
    is_active: bool
    is_superuser: bool


class AccessTokenPayload(BaseModel):
    """Access token payload schema."""
    sub: str  # user_id
    email: EmailStr
    username: str


class RefreshTokenPayload(BaseModel):
    """Refresh token payload schema."""
    sub: str  # user_id
