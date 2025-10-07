import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.comment import Comment
    from api.models.user import User


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    body: str = Field()
    is_published: bool = Field()
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")

    # Relationships
    author: Optional["User"] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")
