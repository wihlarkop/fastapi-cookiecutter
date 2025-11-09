"""JWT token exceptions."""


class TokenExpiredError(Exception):
    """Raised when a token has expired."""
    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(Exception):
    """Raised when a token is invalid."""
    def __init__(self, message: str = "Invalid token"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenTypeError(Exception):
    """Raised when token type doesn't match expected type."""
    def __init__(self, expected: str, received: str):
        self.message = f"Expected token type '{expected}', received '{received}'"
        super().__init__(self.message)
