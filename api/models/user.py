from typing import TYPE_CHECKING, List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship, Mapped

if TYPE_CHECKING:
    from api.models.post import Post

Base: DeclarativeMeta = declarative_base()  # pyright: ignore[reportAny]

class User(SQLAlchemyBaseUserTableUUID, Base):  # pyright: ignore[reportUntypedBaseClass]
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
