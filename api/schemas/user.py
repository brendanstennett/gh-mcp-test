import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Schema for reading user data via API."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating users via API."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user data via API."""

    pass
