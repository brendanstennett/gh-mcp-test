from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from api.setup.database import get_async_session
from api.models.user import User
from api.setup.auth import UserManager
from api.services.repositories.posts_repository import PostsRepository

# Database Dependencies
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# User Database Dependencies
async def get_user_db(session: AsyncSessionDep):
    yield SQLAlchemyUserDatabase(session, User)

UserDBDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]

# User Manager Dependencies
async def get_user_manager(user_db: UserDBDep):
    yield UserManager(user_db)

UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]

# Repository Dependencies
def get_posts_repository(session: AsyncSessionDep):
    return PostsRepository(session)

PostsRepositoryDep = Annotated[PostsRepository, Depends(get_posts_repository)]

# Authentication Dependencies
# These import at runtime to avoid circular imports
def _get_current_user():
    from api.setup.auth import current_user
    return current_user

def _get_current_superuser():
    from api.setup.auth import current_superuser
    return current_superuser

CurrentUserDep = Annotated[User, Depends(_get_current_user)]
CurrentSuperuserDep = Annotated[User, Depends(_get_current_superuser)]
