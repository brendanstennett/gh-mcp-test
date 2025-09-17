from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from api.boot.database import get_async_session
from api.boot.auth import get_user_db
from api.services.repositories.posts_repository import PostsRepository


# Session dependency
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# User database dependency
UserDbDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]

# Posts repository dependency
def get_posts_repository(session: SessionDep) -> PostsRepository:
    return PostsRepository(session)

PostRepositoryDep = Annotated[PostsRepository, Depends(get_posts_repository)]
