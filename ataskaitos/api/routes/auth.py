"""Authentication routes using FastAPI-Users."""

from fastapi import APIRouter

from ataskaitos.auth import auth_backend, fastapi_users
from ataskaitos.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Include FastAPI-Users auth routes
# POST /auth/jwt/login - Login and get JWT token
# POST /auth/jwt/logout - Logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)

# Include FastAPI-Users register routes
# POST /auth/register - Register new user
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

# Include FastAPI-Users user management routes
# GET /users/me - Get current user
# PATCH /users/me - Update current user
# GET /users/{id} - Get user by ID (superuser only)
# PATCH /users/{id} - Update user by ID (superuser only)
# DELETE /users/{id} - Delete user by ID (superuser only)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)
