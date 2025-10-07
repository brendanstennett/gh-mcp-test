from collections.abc import Sequence

from sqlmodel import select

from api.models.comment import Comment
from api.services.repositories.base_repository import BaseRepository


class CommentsRepository(BaseRepository):
    async def all_comments(self) -> Sequence[Comment]:
        """Retrieve all comments from the database"""
        result = await self.session.execute(select(Comment))
        return result.scalars().all()

    async def find_comment(self, comment_id: int) -> Comment | None:
        """Find a specific comment by ID"""
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def create_comment(self, comment: Comment) -> Comment:
        """Create a new comment"""
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def update_comment(self, comment_id: int, comment_data: Comment) -> Comment | None:
        """Update an existing comment"""
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(statement)
        existing_comment = result.scalars().first()

        if not existing_comment:
            return None

        return await self.update_model(existing_comment, comment_data, exclude={"id"})

    async def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment by ID"""
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(statement)
        comment = result.scalars().first()

        if comment:
            await self.session.delete(comment)
            await self.session.commit()
            return True

        return False
