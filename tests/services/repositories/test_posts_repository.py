# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportAny=false
# pyright: reportUnknownMemberType=false

import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from api.services.repositories.posts_repository import PostsRepository
from api.models.post import Post
from api.models.user import User


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
async def posts_repository(test_session):
    """Create a PostsRepository instance with test session"""
    return PostsRepository(test_session)


@pytest.mark.asyncio
async def test_create_and_find_post(posts_repository):
    """Test creating and finding a post"""
    # Create a new post
    new_post = Post(title="Test Post", body="Test content", is_published=False)
    created_post = await posts_repository.create_post(new_post)

    assert created_post.id is not None
    assert created_post.title == "Test Post"

    # Find the created post
    found_post = await posts_repository.find_post(created_post.id)
    assert found_post is not None
    assert found_post.title == "Test Post"


@pytest.mark.asyncio
async def test_all_posts(posts_repository):
    """Test retrieving all posts"""
    # Create some test posts
    post1 = Post(title="First Post", body="First content", is_published=True)
    post2 = Post(title="Second Post", body="Second content", is_published=False)

    _ = await posts_repository.create_post(post1)
    _ = await posts_repository.create_post(post2)

    # Get all posts
    all_posts = await posts_repository.all_posts()

    # Assert we have at least the posts we created
    assert len(all_posts) >= 2
    assert any(post.title == "First Post" for post in all_posts)
    assert any(post.title == "Second Post" for post in all_posts)


@pytest.mark.asyncio
async def test_update_post(posts_repository):
    """Test updating a post"""
    # Create a post
    new_post = Post(title="Original Title", body="Original content", is_published=False)
    created_post = await posts_repository.create_post(new_post)

    # Ensure the post was created successfully
    assert created_post is not None
    assert created_post.id is not None

    # Update the post
    update_data = Post(title="Updated Title", body="Updated content", is_published=True)
    updated_post = await posts_repository.update_post(
        created_post.id,
        update_data
    )

    assert updated_post is not None
    assert updated_post.title == "Updated Title"
    assert updated_post.body == "Updated content"
    assert updated_post.is_published == True
    assert updated_post.id == created_post.id


@pytest.mark.asyncio
async def test_delete_post(posts_repository):
    """Test deleting a post"""
    # Create a post
    new_post = Post(title="To Delete", body="Will be deleted", is_published=True)
    created_post = await posts_repository.create_post(new_post)

    # Ensure the post was created successfully
    assert created_post is not None
    assert created_post.id is not None

    # Delete the post
    success = await posts_repository.delete_post(created_post.id)
    assert success is True

    # Verify the post is deleted
    deleted_post = await posts_repository.find_post(created_post.id)
    assert deleted_post is None


@pytest.mark.asyncio
async def test_find_nonexistent_post(posts_repository):
    """Test finding a post that doesn't exist"""
    result = await posts_repository.find_post(999)
    assert result is None


@pytest.mark.asyncio
async def test_delete_nonexistent_post(posts_repository):
    """Test deleting a post that doesn't exist"""
    success = await posts_repository.delete_post(999)
    assert success is False
