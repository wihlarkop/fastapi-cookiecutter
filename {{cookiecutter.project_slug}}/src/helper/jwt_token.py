import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from src.config import settings
from src.exceptions.jwt_token import TokenExpiredError, InvalidTokenError, InvalidTokenTypeError


class JWTHelper:
    """JWT token helper for generating and validating tokens."""

    @staticmethod
    def create_access_token(payload: dict, expires_delta: timedelta = None) -> str:
        """
        Create a JWT access token.

        Args:
            payload: Payload data to encode in the token
            expires_delta: Custom expiration time, defaults to settings value

        Returns:
            Encoded JWT token string
        """
        to_encode = payload.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "access"})

        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(payload: dict, expires_delta: timedelta = None) -> str:
        """
        Create a JWT refresh token.

        Args:
            payload: Payload data to encode in the token
            expires_delta: Custom expiration time, defaults to settings value

        Returns:
            Encoded JWT token string
        """
        to_encode = payload.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode.update({"exp": expire, "type": "refresh", "jti": secrets.token_urlsafe(32)})

        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> dict:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string to verify
            token_type: Expected token type ("access" or "refresh")

        Returns:
            Decoded token payload

        Raises:
            TokenExpiredError: If token has expired
            InvalidTokenError: If token is malformed or invalid
            InvalidTokenTypeError: If token type doesn't match expected type
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

            # Check token type
            received_type = payload.get("type")
            if received_type != token_type:
                raise InvalidTokenTypeError(token_type, received_type)

            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.PyJWTError:
            raise InvalidTokenError()

    @staticmethod
    def hash_refresh_token(token: str) -> str:
        """
        Hash a refresh token for secure storage.

        Args:
            token: Refresh token to hash

        Returns:
            SHA256 hash of the token
        """
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def get_token_expiry(token_type: str = "access") -> datetime:
        """
        Get the expiry datetime for a token type.

        Args:
            token_type: Token type ("access" or "refresh")

        Returns:
            Expiry datetime in UTC
        """
        if token_type == "access":
            return datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        else:  # refresh
            return datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
