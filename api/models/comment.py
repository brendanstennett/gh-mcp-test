import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.post import Post
    from api.models.user import User


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    body: str = Field(max_length=10000, sa_type=String(10000))
    is_published: bool = Field(default=False)
    user_id: uuid.UUID | None = Field(
        default=None,
        sa_column=Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), index=True),
    )
    post_id: int | None = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), index=True),
    )

    # Relationships
    author: Optional["User"] = Relationship(back_populates="comments")
    post: Optional["Post"] = Relationship(back_populates="comments")
