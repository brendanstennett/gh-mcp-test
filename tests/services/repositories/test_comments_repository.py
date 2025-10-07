# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportAny=false
# pyright: reportUnknownMemberType=false

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from api.models.comment import Comment
from api.services.repositories.comments_repository import CommentsRepository


@pytest_asyncio.fixture
async def test_session():
    """Create a test database session"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        # Create tables from SQLModel metadata
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def comments_repository(test_session) -> CommentsRepository:
    """Create a CommentsRepository instance with test session"""
    return CommentsRepository(test_session)


@pytest.mark.asyncio
async def test_create_and_find_comment(comments_repository):
    """Test creating and finding a comment"""
    # Create a new comment
    new_comment = Comment(body="Test comment content", is_published=False)
    created_comment = await comments_repository.create_comment(new_comment)

    assert created_comment.id is not None
    assert created_comment.body == "Test comment content"

    # Find the created comment
    found_comment = await comments_repository.find_comment(created_comment.id)
    assert found_comment is not None
    assert found_comment.body == "Test comment content"


@pytest.mark.asyncio
async def test_all_comments(comments_repository):
    """Test retrieving all comments"""
    # Create some test comments
    comment1 = Comment(body="First comment", is_published=True)
    comment2 = Comment(body="Second comment", is_published=False)

    _ = await comments_repository.create_comment(comment1)
    _ = await comments_repository.create_comment(comment2)

    # Get all comments
    all_comments = await comments_repository.all_comments()

    # Assert we have at least the comments we created
    assert len(all_comments) >= 2
    assert any(comment.body == "First comment" for comment in all_comments)
    assert any(comment.body == "Second comment" for comment in all_comments)


@pytest.mark.asyncio
async def test_update_comment(comments_repository):
    """Test updating a comment"""
    # Create a comment
    new_comment = Comment(body="Original comment", is_published=False)
    created_comment = await comments_repository.create_comment(new_comment)

    # Ensure the comment was created successfully
    assert created_comment is not None
    assert created_comment.id is not None

    # Update the comment
    update_data = Comment(body="Updated comment", is_published=True)
    updated_comment = await comments_repository.update_comment(created_comment.id, update_data)

    assert updated_comment is not None
    assert updated_comment.body == "Updated comment"
    assert updated_comment.is_published
    assert updated_comment.id == created_comment.id


@pytest.mark.asyncio
async def test_delete_comment(comments_repository):
    """Test deleting a comment"""
    # Create a comment
    new_comment = Comment(body="To delete", is_published=True)
    created_comment = await comments_repository.create_comment(new_comment)

    # Ensure the comment was created successfully
    assert created_comment is not None
    assert created_comment.id is not None

    # Delete the comment
    success = await comments_repository.delete_comment(created_comment.id)
    assert success is True

    # Verify the comment is deleted
    deleted_comment = await comments_repository.find_comment(created_comment.id)
    assert deleted_comment is None


@pytest.mark.asyncio
async def test_find_nonexistent_comment(comments_repository):
    """Test finding a comment that doesn't exist"""
    result = await comments_repository.find_comment(999)
    assert result is None


@pytest.mark.asyncio
async def test_delete_nonexistent_comment(comments_repository):
    """Test deleting a comment that doesn't exist"""
    success = await comments_repository.delete_comment(999)
    assert success is False
