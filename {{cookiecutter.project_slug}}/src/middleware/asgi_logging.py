{% if cookiecutter.include_middleware_logging == "yes" -%}
import json
import time
import uuid
from typing import Optional
from starlette.types import ASGIApp, Receive, Scope, Send, Message

from src.helper.logger import get_logger

logger = get_logger(__name__)


class ASGILoggingMiddleware:
    """
    Pure ASGI logging middleware with optimized performance.

    Features:
    - Preserves ContextVars (avoids BaseHTTPMiddleware limitations)
    - Request/response payload logging with sanitization
    - Configurable payload size limits
    - Selective path exclusions
    - Memory-efficient streaming handling
    """

    def __init__(
        self,
        app: ASGIApp,
        max_body_size: int = 100 * 1024,  # 100KB default
        exclude_paths: Optional[list[str]] = None
    ) -> None:
        self.app = app
        self.max_body_size = max_body_size
        self.exclude_paths = exclude_paths or ["/health", "/metrics"]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Only process HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"]

        # Skip logging for excluded paths
        if any(path.startswith(excluded) for excluded in self.exclude_paths):
            await self.app(scope, receive, send)
            return

        # Generate request ID for logging
        headers = dict(scope.get("headers", []))
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Extract request details from ASGI scope
        method = scope["method"]
        query_string = scope.get("query_string", b"").decode()

        # Extract client info
        client = scope.get("client", ("unknown", 0))
        client_ip = client[0] if client else "unknown"

        # Extract user agent
        user_agent = headers.get(b"user-agent", b"unknown").decode()

        # Check content length early to avoid buffering large payloads
        content_length = headers.get(b"content-length")
        should_buffer_request = True
        if content_length:
            try:
                if int(content_length.decode()) > self.max_body_size:
                    should_buffer_request = False
            except (ValueError, UnicodeDecodeError):
                pass

        # Capture request payload only if needed
        request_body = b"" if should_buffer_request else None

        async def receive_wrapper():
            nonlocal request_body
            message = await receive()
            if message["type"] == "http.request" and should_buffer_request:
                body = message.get("body", b"")
                # Stop buffering if exceeds limit
                if len(request_body) + len(body) <= self.max_body_size:
                    request_body += body
                else:
                    request_body = None  # Stop buffering
            return message

        # Log request start
        logger.info(
            "HTTP request started",
            request_id=request_id,
            method=method,
            path=path,
            query_string=query_string or None,
            client_ip=client_ip,
            user_agent=user_agent,
        )

        # Add request ID to scope for access in endpoints
        scope["request_id"] = request_id

        # Variables to capture response info
        status_code = None
        response_headers = {}
        response_body = b""
        should_buffer_response = True

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code, response_headers, response_body, should_buffer_response

            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_headers = dict(message.get("headers", []))

                # Check response size early
                resp_content_length = response_headers.get(b"content-length")
                if resp_content_length:
                    try:
                        if int(resp_content_length.decode()) > self.max_body_size:
                            should_buffer_response = False
                    except (ValueError, UnicodeDecodeError):
                        pass

                # Add request ID to response headers
                message["headers"] = [
                    *message.get("headers", []),
                    (b"x-request-id", request_id.encode())
                ]
            elif message["type"] == "http.response.body" and should_buffer_response:
                body = message.get("body", b"")
                # Stop buffering if exceeds limit
                if len(response_body) + len(body) <= self.max_body_size:
                    response_body += body
                else:
                    should_buffer_response = False
                    response_body = b""  # Clear to save memory

            await send(message)

        try:
            # Process the request
            await self.app(scope, receive_wrapper, send_wrapper)

            # Calculate processing time
            process_time = time.time() - start_time

            # Parse payloads for logging
            request_payload = self._safe_parse_payload(
                request_body,
                headers.get(b"content-type", b"").decode().lower(),
                "request"
            ) if request_body is not None else {"note": "Payload too large or not buffered"}

            response_payload = self._safe_parse_payload(
                response_body,
                response_headers.get(b"content-type", b"").decode().lower(),
                "response"
            ) if should_buffer_response else {"note": "Response too large or not buffered"}

            # Log successful response
            logger.info(
                "HTTP request completed",
                request_id=request_id,
                method=method,
                path=path,
                status_code=status_code,
                process_time_ms=round(process_time * 1000, 2),
                request_payload=request_payload if request_payload else None,
                response_payload=response_payload if response_payload else None,
            )

        except Exception as exc:
            # Calculate processing time for failed requests
            process_time = time.time() - start_time

            # Log error
            logger.error(
                "HTTP request failed",
                request_id=request_id,
                method=method,
                path=path,
                process_time_ms=round(process_time * 1000, 2),
                error=str(exc),
                error_type=type(exc).__name__
            )

            # Re-raise the exception
            raise exc

    def _safe_parse_payload(self, body: bytes, content_type: str, payload_type: str) -> dict | None:
        """
        Optimized payload parser with single-pass sanitization.
        """
        if not body:
            return None

        # Skip file upload content
        if "multipart/form-data" in content_type:
            return {
                "type": "multipart_form_data",
                "size_bytes": len(body),
            }

        # Parse JSON (most common case)
        if "application/json" in content_type:
            try:
                payload = json.loads(body.decode())
                # Sanitize in single pass
                return self._sanitize_payload(payload)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                return {"type": "invalid_json", "error": str(e)}

        # Handle text content
        if "text/" in content_type or "application/xml" in content_type:
            try:
                decoded = body.decode(errors='replace')
                if len(decoded) > 1000:  # Truncate long text
                    decoded = decoded[:1000] + "... [truncated]"
                return {"type": "text", "content": decoded}
            except Exception:
                pass

        # Binary or unknown content
        return {
            "type": "binary",
            "size_bytes": len(body),
            "content_type": content_type,
        }

    def _sanitize_payload(self, payload: any) -> any:
        """
        Optimized single-pass sanitization of sensitive fields.
        """
        if isinstance(payload, dict):
            return {
                key: "[REDACTED]" if self._is_sensitive_key(key)
                else self._sanitize_payload(value)
                for key, value in payload.items()
            }
        elif isinstance(payload, list):
            return [self._sanitize_payload(item) for item in payload]
        else:
            return payload

    @staticmethod
    def _is_sensitive_key(key: str) -> bool:
        """Check if key contains sensitive information."""
        key_lower = key.lower()
        sensitive_keywords = {
            'password', 'token', 'secret', 'key', 'auth',
            'credential', 'api_key', 'apikey', 'private'
        }
        return any(keyword in key_lower for keyword in sensitive_keywords)


def get_request_id_from_scope(scope: Scope) -> str:
    """Get the request ID from ASGI scope."""
    return scope.get("request_id", "unknown")
{% endif -%}
