import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.comment import Comment
    from api.models.post import Post


class User(SQLModel, table=True):
    # Replicate fastapi-users fields for compatibility
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, sa_column_kwargs={"unique": True})
    hashed_password: str = Field()
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

    # Relationships
    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(
        back_populates="author", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
