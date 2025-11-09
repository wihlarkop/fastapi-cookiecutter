from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserEntity(BaseModel):
    id: str
    email: EmailStr
    username: str
    hashed_password: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
