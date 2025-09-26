from fastapi import APIRouter

from api.schemas.user import UserCreate, UserRead, UserUpdate
from api.setup.auth import auth_backend, fastapi_users

# Create the auth router
router = APIRouter()

# Include fastapi-users authentication routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["auth"],
)

# Include user registration routes
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)

# Include user management routes (requires authentication)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Optional: Include password reset routes
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
    tags=["auth"],
)

# Optional: Include email verification routes
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/verify",
    tags=["auth"],
)
