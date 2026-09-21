"""Pydantic schemas for User model."""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data."""



class UserCreate(schemas.BaseUserCreate):
    """Schema for user registration."""



class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user data."""

