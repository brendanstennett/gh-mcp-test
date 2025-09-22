import uuid
from typing import Optional
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    body: str = Field()
    is_published: bool = Field()
    user_id: Optional[uuid.UUID] = Field(default=None)
