import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.user import User


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    body: str = Field()
    is_published: bool = Field()
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")

    # Relationship to user/author
    author: Optional["User"] = Relationship(back_populates="posts")

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
