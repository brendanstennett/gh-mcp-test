# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportAny=false
# pyright: reportUnknownMemberType=false

import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import select

from api.models.comment import Comment


@pytest_asyncio.fixture
async def test_session():
    """Create a test database session with User, Post, and Comment tables"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # Create tables from model metadata
    async with engine.begin() as conn:
        from sqlmodel import SQLModel

        # Import models to ensure they're registered with SQLModel metadata
        from api.models.comment import Comment  # noqa: F401
        from api.models.post import Post  # noqa: F401
        from api.models.user import User  # noqa: F401

        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        yield session


@pytest.mark.asyncio
async def test_create_comment_with_user_and_post(test_session):
    """Test creating a comment with both user_id and post_id"""
    test_user_id = uuid.uuid4()
    test_post_id = 1

    # Create a comment with both user_id and post_id
    new_comment = Comment(
        body="Test comment", is_published=True, user_id=test_user_id, post_id=test_post_id
    )
    test_session.add(new_comment)
    await test_session.commit()
    await test_session.refresh(new_comment)

    assert new_comment.id is not None
    assert new_comment.body == "Test comment"
    assert new_comment.user_id == test_user_id
    assert new_comment.post_id == test_post_id
    assert new_comment.is_published is True


@pytest.mark.asyncio
async def test_create_comment_without_user_and_post(test_session):
    """Test creating a comment without user_id and post_id"""
    new_comment = Comment(body="Anonymous comment")
    test_session.add(new_comment)
    await test_session.commit()
    await test_session.refresh(new_comment)

    assert new_comment.id is not None
    assert new_comment.body == "Anonymous comment"
    assert new_comment.user_id is None
    assert new_comment.post_id is None
    assert new_comment.is_published is False  # Default value


@pytest.mark.asyncio
async def test_comment_default_is_published(test_session):
    """Test that is_published defaults to False"""
    new_comment = Comment(body="Test comment")
    test_session.add(new_comment)
    await test_session.commit()
    await test_session.refresh(new_comment)

    assert new_comment.is_published is False


@pytest.mark.asyncio
async def test_find_comments_by_user_id(test_session):
    """Test finding comments by user_id"""
    user1_id = uuid.uuid4()
    user2_id = uuid.uuid4()

    # Create comments for different users
    comment1 = Comment(body="User 1 Comment 1", user_id=user1_id)
    comment2 = Comment(body="User 1 Comment 2", user_id=user1_id)
    comment3 = Comment(body="User 2 Comment 1", user_id=user2_id)

    test_session.add(comment1)
    test_session.add(comment2)
    test_session.add(comment3)
    await test_session.commit()

    # Query comments for user1
    result = await test_session.execute(select(Comment).where(Comment.user_id == user1_id))
    user1_comments = result.scalars().all()

    assert len(user1_comments) == 2
    assert all(comment.user_id == user1_id for comment in user1_comments)

    # Query comments for user2
    result = await test_session.execute(select(Comment).where(Comment.user_id == user2_id))
    user2_comments = result.scalars().all()

    assert len(user2_comments) == 1
    assert user2_comments[0].user_id == user2_id


@pytest.mark.asyncio
async def test_find_comments_by_post_id(test_session):
    """Test finding comments by post_id"""
    post1_id = 1
    post2_id = 2

    # Create comments for different posts
    comment1 = Comment(body="Post 1 Comment 1", post_id=post1_id)
    comment2 = Comment(body="Post 1 Comment 2", post_id=post1_id)
    comment3 = Comment(body="Post 2 Comment 1", post_id=post2_id)

    test_session.add(comment1)
    test_session.add(comment2)
    test_session.add(comment3)
    await test_session.commit()

    # Query comments for post1
    result = await test_session.execute(select(Comment).where(Comment.post_id == post1_id))
    post1_comments = result.scalars().all()

    assert len(post1_comments) == 2
    assert all(comment.post_id == post1_id for comment in post1_comments)

    # Query comments for post2
    result = await test_session.execute(select(Comment).where(Comment.post_id == post2_id))
    post2_comments = result.scalars().all()

    assert len(post2_comments) == 1
    assert post2_comments[0].post_id == post2_id


@pytest.mark.asyncio
async def test_comment_indexes(test_session):
    """Test that user_id and post_id indexes improve query performance"""
    # This test verifies that indexes are properly created
    # by checking the table structure
    from sqlalchemy import inspect

    def get_indexes(connection):
        inspector = inspect(connection)
        return inspector.get_indexes("comment")

    connection = await test_session.connection()
    indexes = await connection.run_sync(get_indexes)

    # Check that indexes exist on user_id and post_id
    index_columns = [idx["column_names"] for idx in indexes]
    assert ["user_id"] in index_columns
    assert ["post_id"] in index_columns
