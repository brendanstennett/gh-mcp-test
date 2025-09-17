import pytest
from sqlmodel import Session, SQLModel, create_engine
from api.services.repositories.posts_repository import PostsRepository
from api.models.post import Post


@pytest.fixture
def test_session():
    """Create a test database session"""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def posts_repository(test_session: Session):
    """Create a PostsRepository instance with test session"""
    return PostsRepository(test_session)


@pytest.mark.asyncio
async def test_create_and_find_post(posts_repository: PostsRepository):
    """Test creating and finding a post"""
    # Create a new post
    new_post = Post(name="Test Post")
    created_post = await posts_repository.create_post(new_post)

    assert created_post.id is not None
    assert created_post.name == "Test Post"

    # Find the created post
    found_post = await posts_repository.find_post(created_post.id)
    assert found_post is not None
    assert found_post.name == "Test Post"


@pytest.mark.asyncio
async def test_all_posts(posts_repository: PostsRepository):
    """Test retrieving all posts"""
    # Create some test posts
    post1 = Post(name="First Post")
    post2 = Post(name="Second Post")

    await posts_repository.create_post(post1)
    await posts_repository.create_post(post2)

    # Get all posts
    all_posts = await posts_repository.all_posts()

    assert len(all_posts) == 2
    assert any(post.name == "First Post" for post in all_posts)
    assert any(post.name == "Second Post" for post in all_posts)


@pytest.mark.asyncio
async def test_update_post(posts_repository: PostsRepository):
    """Test updating a post"""
    # Create a post
    new_post = Post(name="Original Name")
    created_post = await posts_repository.create_post(new_post)

    # Ensure the post was updated successfully
    assert created_post is not None
    assert created_post.id is not None

    # Update the post
    updated_post = await posts_repository.update_post(
        created_post.id,
        {"name": "Updated Name"}
    )

    assert updated_post is not None
    assert updated_post.name == "Updated Name"
    assert updated_post.id == created_post.id


@pytest.mark.asyncio
async def test_delete_post(posts_repository: PostsRepository):
    """Test deleting a post"""
    # Create a post
    new_post = Post(name="To Delete")
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
async def test_find_nonexistent_post(posts_repository: PostsRepository):
    """Test finding a post that doesn't exist"""
    result = await posts_repository.find_post(999)
    assert result is None


@pytest.mark.asyncio
async def test_delete_nonexistent_post(posts_repository: PostsRepository):
    """Test deleting a post that doesn't exist"""
    success = await posts_repository.delete_post(999)
    assert success is False
