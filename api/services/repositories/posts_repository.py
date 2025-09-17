from sqlmodel import Session, select
from api.models.post import Post
from typing import Sequence

class PostsRepository:
    def __init__(self, session: Session):
        self.session = session

    async def all_posts(self) -> Sequence[Post]:
        """Retrieve all posts from the database"""
        return self.session.scalars(select(Post)).all()

    async def find_post(self, post_id: int) -> Post | None:
        """Find a specific post by ID"""
        statement = select(Post).where(Post.id == post_id)
        result = self.session.exec(statement)
        return result.first()

    async def create_post(self, post: Post) -> Post:
        """Create a new post"""
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    async def update_post(self, post_id: int, post_data: dict) -> Post | None:
        """Update an existing post"""
        statement = select(Post).where(Post.id == post_id)
        result = self.session.exec(statement)
        post = result.first()

        if post:
            for key, value in post_data.items():
                if hasattr(post, key):
                    setattr(post, key, value)

            self.session.add(post)
            self.session.commit()
            self.session.refresh(post)
            return post

        return None

    async def delete_post(self, post_id: int) -> bool:
        """Delete a post by ID"""
        statement = select(Post).where(Post.id == post_id)
        result = self.session.exec(statement)
        post = result.first()

        if post:
            self.session.delete(post)
            self.session.commit()
            return True

        return False
