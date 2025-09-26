import uuid
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from api.services.repositories.posts_repository import PostsRepository
from api.setup.auth import UserManager, current_superuser, current_user
from api.setup.database import get_async_session

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
