"""Pydantic schemas for User model."""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Schema for user registration."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user data."""

    pass
