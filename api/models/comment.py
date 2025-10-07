import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.post import Post
    from api.models.user import User


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    body: str = Field()
    is_published: bool = Field(default=False)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)
    post_id: int | None = Field(default=None, foreign_key="post.id", index=True)

    # Relationships
    author: Optional["User"] = Relationship(back_populates="comments")
    post: Optional["Post"] = Relationship(back_populates="comments")
