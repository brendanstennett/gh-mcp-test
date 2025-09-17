from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from api.boot.database import engine
from api.services.repositories.posts_repository import PostsRepository

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def get_posts_repository(session: SessionDep) -> PostsRepository:
    return PostsRepository(session)

PostRepositoryDep = Annotated[PostsRepository, Depends(get_posts_repository)]
