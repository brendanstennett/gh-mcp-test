from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from api.models.post import Post
from typing import Sequence

class PostsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def all_posts(self) -> Sequence[Post]:
        """Retrieve all posts from the database"""
        result = await self.session.execute(select(Post))
        return result.scalars().all()

    async def find_post(self, post_id: int) -> Post | None:
        """Find a specific post by ID"""
        statement = select(Post).where(Post.id == post_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def create_post(self, post: Post) -> Post:
        """Create a new post"""
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def update_post(self, post_id: int, post_data: dict) -> Post | None:
        """Update an existing post"""
        statement = select(Post).where(Post.id == post_id)
        result = await self.session.execute(statement)
        post = result.scalars().first()

        if post:
            for key, value in post_data.items():
                if hasattr(post, key):
                    setattr(post, key, value)

            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post)
            return post

        return None

    async def delete_post(self, post_id: int) -> bool:
        """Delete a post by ID"""
        statement = select(Post).where(Post.id == post_id)
        result = await self.session.execute(statement)
        post = result.scalars().first()

        if post:
            await self.session.delete(post)
            await self.session.commit()
            return True

        return False
