import uuid
from typing import TYPE_CHECKING, Any, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.post import Post


class User(SQLModel, table=True):
    # Replicate fastapi-users fields for compatibility
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, sa_column_kwargs={"unique": True})
    hashed_password: str = Field()
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

    # Relationship to posts
    posts: List["Post"] = Relationship(back_populates="author")

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
