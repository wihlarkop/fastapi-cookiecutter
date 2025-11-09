from typing import Generic, TypeVar

from fastapi import status
from pydantic import BaseModel

T = TypeVar("T")


class MetaResponse(BaseModel):
    page: int | None = None
    limit: int | None = None
    total_data: int | None = 0
    execution_time_seconds: float | None = None


class JsonResponse(BaseModel, Generic[T]):
    data: T | None = None
    message: str | list[str] | None = None
    success: bool = True
    meta: MetaResponse | None = None
    status_code: int = status.HTTP_200_OK
    timestamp: str | None = None
    error_code: str | None = None
