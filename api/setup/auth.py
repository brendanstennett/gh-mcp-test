from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from fastapi_users import UUIDIDMixin
from typing import override
import uuid

from api.models.user import User
from api.setup.database import get_async_session

# Secret key for JWT - in production, use environment variables
SECRET = "your-secret-key-here"  # TODO: Move to environment variables

async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[SQLAlchemyUserDatabase[User, uuid.UUID], None]:
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    User manager for fastapi-users with async support.

    This handles user registration, authentication, and user management
    operations with your async SQLAlchemy session.
    """
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    @override
    async def on_after_register(self, user: User, request: Request | None = None):
        """Called after a user registers."""
        print(f"User {user.id} has registered.")

    @override
    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        """Called after a user requests password reset."""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    @override
    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        """Called after a user requests verification."""
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = Depends(get_user_db)) -> AsyncGenerator[UserManager, None]:
    """
    Dependency to get the user manager instance.

    Args:
        user_db: The user database adapter

    Yields:
        UserManager: The user manager instance
    """
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)




# Authentication backend setup
cookie_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

# Dependencies for protecting routes
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
