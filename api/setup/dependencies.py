from typing import Annotated
from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
import uuid

from api.setup.database import get_async_session
from api.models.user import User
from api.setup.auth import UserManager
from api.services.repositories.posts_repository import PostsRepository
from api.setup.auth import current_user, current_superuser

# Database Dependencies
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# User Database Dependencies
async def get_user_db(session: AsyncSessionDep) -> AsyncGenerator[SQLAlchemyUserDatabase[User, uuid.UUID], None]:
    yield SQLAlchemyUserDatabase(session, User)

UserDBDep = Annotated[SQLAlchemyUserDatabase[User, uuid.UUID], Depends(get_user_db)]

# User Manager Dependencies
async def get_user_manager(user_db: UserDBDep) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)

UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]

# Repository Dependencies
def get_posts_repository(session: AsyncSessionDep):
    return PostsRepository(session)

PostsRepositoryDep = Annotated[PostsRepository, Depends(get_posts_repository)]

# Authentication Dependencies
CurrentUserDep = Annotated[User, Depends(current_user)]
CurrentSuperuserDep = Annotated[User, Depends(current_superuser)]
