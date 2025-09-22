import uuid
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.models.user import User

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    body: str = Field()
    is_published: bool = Field()
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    # Relationship to user/author
    author: Optional["User"] = Relationship(back_populates="posts")
