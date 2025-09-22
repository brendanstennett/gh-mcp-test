import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from api.models.post import Post
from api.models.user import User
from api.services.repositories.posts_repository import PostsRepository


@pytest_asyncio.fixture
async def test_session():
    """Create a test database session with both User and Post tables"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # Manually create tables to avoid foreign key issues during testing
    async with engine.begin() as conn:
        from sqlalchemy import text

        await conn.execute(text("""
            CREATE TABLE user (
                id CHAR(36) NOT NULL,
                email VARCHAR(320) NOT NULL,
                hashed_password VARCHAR(1024) NOT NULL,
                is_active BOOLEAN NOT NULL,
                is_superuser BOOLEAN NOT NULL,
                is_verified BOOLEAN NOT NULL,
                PRIMARY KEY (id)
            )
        """))

        await conn.execute(text("""
            CREATE TABLE post (
                id INTEGER NOT NULL,
                title VARCHAR NOT NULL,
                body VARCHAR NOT NULL,
                is_published BOOLEAN NOT NULL,
                user_id CHAR(36),
                PRIMARY KEY (id)
            )
        """))

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def posts_repository(test_session):
    """Create a PostsRepository instance with test session"""
    return PostsRepository(test_session)


@pytest.mark.asyncio
async def test_create_post_with_user_id(posts_repository):
    """Test creating a post with a user_id"""
    # Create a test user ID
    test_user_id = uuid.uuid4()

    # Create a post with user_id
    new_post = Post(
        title="Test Post",
        body="Test content",
        is_published=False,
        user_id=test_user_id
    )
    created_post = await posts_repository.create_post(new_post)

    assert created_post.id is not None
    assert created_post.title == "Test Post"
    assert created_post.user_id == test_user_id

    # Find the created post
    found_post = await posts_repository.find_post(created_post.id)
    assert found_post is not None
    assert found_post.title == "Test Post"
    assert found_post.user_id == test_user_id


@pytest.mark.asyncio
async def test_create_post_without_user_id(posts_repository):
    """Test creating a post without a user_id (should be None)"""
    # Create a post without user_id
    new_post = Post(
        title="Test Post No User",
        body="Test content",
        is_published=False
    )
    created_post = await posts_repository.create_post(new_post)

    assert created_post.id is not None
    assert created_post.title == "Test Post No User"
    assert created_post.user_id is None


@pytest.mark.asyncio
async def test_find_posts_by_user_id(posts_repository, test_session):
    """Test finding posts by user_id"""
    # Create test user IDs
    user1_id = uuid.uuid4()
    user2_id = uuid.uuid4()

    # Create posts for different users
    post1 = Post(title="User 1 Post 1", body="Content 1", is_published=True, user_id=user1_id)
    post2 = Post(title="User 1 Post 2", body="Content 2", is_published=False, user_id=user1_id)
    post3 = Post(title="User 2 Post 1", body="Content 3", is_published=True, user_id=user2_id)

    await posts_repository.create_post(post1)
    await posts_repository.create_post(post2)
    await posts_repository.create_post(post3)

    # Query posts for user1 directly with SQLAlchemy
    from sqlmodel import select
    result = await test_session.execute(select(Post).where(Post.user_id == user1_id))
    user1_posts = result.scalars().all()

    assert len(user1_posts) == 2
    assert all(post.user_id == user1_id for post in user1_posts)

    # Query posts for user2
    result = await test_session.execute(select(Post).where(Post.user_id == user2_id))
    user2_posts = result.scalars().all()

    assert len(user2_posts) == 1
    assert user2_posts[0].user_id == user2_id