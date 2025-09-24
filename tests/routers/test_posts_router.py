# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportAny=false
# pyright: reportUnknownMemberType=false

import pytest
import uuid
from unittest.mock import create_autospec
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from api.setup.app import app
from api.models.post import Post
from api.models.user import User
from api.setup.dependencies import get_posts_repository
from api.setup.auth import current_user
from api.services.repositories.posts_repository import PostsRepository


@pytest.fixture
def test_engine():
    """Create a test database engine"""
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def test_session(test_engine):
    """Create a test database session"""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def mock_posts_repository() -> PostsRepository:
    mock: PostsRepository = create_autospec(PostsRepository, spec_set=True, instance=True)
    return mock


@pytest.fixture
def mock_current_user():
    """Create a mock current user"""
    user = User(id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"), email="test@example.com", is_active=True)
    return user


@pytest.fixture
def client_with_mocks(mock_posts_repository, mock_current_user):
    """Create a test client with mocked dependencies"""

    def override_get_posts_repository():
        return mock_posts_repository

    def override_current_user():
        return mock_current_user

    app.dependency_overrides[get_posts_repository] = override_get_posts_repository
    app.dependency_overrides[current_user] = override_current_user

    with TestClient(app) as client:
        yield client, mock_posts_repository, mock_current_user

    app.dependency_overrides.clear()


@pytest.fixture
def sample_post():
    """Create a sample post for testing"""
    return Post(id=1, title="Test Post", body="Test body", is_published=True)


@pytest.fixture
def sample_posts():
    """Create a list of sample posts for testing"""
    return [
        Post(id=1, title="First Post", body="First body", is_published=True),
        Post(id=2, title="Second Post", body="Second body", is_published=True),
        Post(id=3, title="Third Post", body="Third body", is_published=True),
    ]


class TestListPosts:
    """Test cases for GET /api/v1/posts endpoint"""

    @pytest.mark.asyncio
    async def test_list_posts_success(self, client_with_mocks, sample_posts):
        """Test successful retrieval of all posts"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.all_posts.return_value = sample_posts

        response = client.get("/api/v1/posts")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["title"] == "First Post"
        assert data[1]["title"] == "Second Post"
        assert data[2]["title"] == "Third Post"
        mock_repo.all_posts.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_posts_empty(self, client_with_mocks):
        """Test retrieval when no posts exist"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.all_posts.return_value = []

        response = client.get("/api/v1/posts")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        mock_repo.all_posts.assert_called_once()


class TestFindPost:
    """Test cases for GET /api/v1/posts/{post_id} endpoint"""

    @pytest.mark.asyncio
    async def test_find_post_success(self, client_with_mocks, sample_post):
        """Test successful retrieval of a specific post"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.find_post.return_value = sample_post

        response = client.get("/api/v1/posts/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test Post"
        mock_repo.find_post.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_find_post_not_found(self, client_with_mocks):
        """Test retrieval of non-existent post"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.find_post.return_value = None

        response = client.get("/api/v1/posts/999")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Post not found"
        mock_repo.find_post.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_find_post_invalid_id(self, client_with_mocks):
        """Test retrieval with invalid post ID format"""
        client, _, _ = client_with_mocks

        response = client.get("/api/v1/posts/invalid")

        assert response.status_code == 422  # Validation error


class TestCreatePost:
    """Test cases for POST /api/v1/posts endpoint"""

    @pytest.mark.asyncio
    async def test_create_post_success(self, client_with_mocks, sample_post):
        """Test successful post creation"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.create_post.return_value = sample_post

        post_data = {"title": "Test Post", "body": "Test body", "is_published": True}
        response = client.post("/api/v1/posts", json=post_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test Post"
        # Verify the call was made with a Post object
        mock_repo.create_post.assert_called_once()
        call_args = mock_repo.create_post.call_args[0][0]
        assert call_args.title == "Test Post"

    @pytest.mark.asyncio
    async def test_create_post_with_id_specified(self, client_with_mocks):
        """Test post creation when ID is specified (should be ignored)"""
        client, mock_repo, _ = client_with_mocks

        created_post = Post(id=1, title="Test Post", body="Test body", is_published=True)
        mock_repo.create_post.return_value = created_post

        post_data = {"id": 999, "title": "Test Post", "body": "Test body", "is_published": True}  # ID should be ignored
        response = client.post("/api/v1/posts", json=post_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1  # Uses the ID from mock, not from request
        assert data["title"] == "Test Post"
        mock_repo.create_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_post_empty_name(self, client_with_mocks):
        """Test post creation with empty name"""
        client, mock_repo, _ = client_with_mocks

        created_post = Post(id=1, title="", body="", is_published=False)
        mock_repo.create_post.return_value = created_post

        post_data = {"title": "", "body": "", "is_published": False}
        response = client.post("/api/v1/posts", json=post_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == ""
        mock_repo.create_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_post_without_auth(self):
        """Test post creation without authentication"""
        with TestClient(app) as client:
            post_data = {"title": "Test Post", "body": "Test body", "is_published": True}
            response = client.post("/api/v1/posts", json=post_data)

            assert response.status_code == 401


class TestUpdatePost:
    """Test cases for PUT /api/v1/posts/{post_id} endpoint"""

    @pytest.mark.asyncio
    async def test_update_post_success(self, client_with_mocks):
        """Test successful post update"""
        client, mock_repo, _ = client_with_mocks
        updated_post = Post(id=1, title="Updated Post", body="Updated body", is_published=True)
        mock_repo.update_post.return_value = updated_post

        post_data = {"title": "Updated Post", "body": "Updated body", "is_published": True}
        response = client.put("/api/v1/posts/1", json=post_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Updated Post"
        # Verify the call was made correctly
        mock_repo.update_post.assert_called_once()
        call_args = mock_repo.update_post.call_args
        assert call_args[0][0] == 1  # post_id
        assert call_args[0][1].title == "Updated Post"  # updated post data

    @pytest.mark.asyncio
    async def test_update_post_not_found(self, client_with_mocks):
        """Test update of non-existent post"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.update_post.return_value = None

        post_data = {"title": "Updated Post", "body": "Updated body", "is_published": True}
        response = client.put("/api/v1/posts/999", json=post_data)

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Post not found"
        mock_repo.update_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_post_with_same_name(self, client_with_mocks):
        """Test update with same name"""
        client, mock_repo, _ = client_with_mocks

        updated_post = Post(id=1, title="Same Name", body="Same body", is_published=True)
        mock_repo.update_post.return_value = updated_post

        post_data = {"title": "Same Name", "body": "Same body", "is_published": True}
        response = client.put("/api/v1/posts/1", json=post_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Same Name"
        mock_repo.update_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_post_without_auth(self):
        """Test post update without authentication"""
        with TestClient(app) as client:
            post_data = {"title": "Updated Post", "body": "Updated body", "is_published": True}
            response = client.put("/api/v1/posts/1", json=post_data)

            assert response.status_code == 401


class TestDeletePost:
    """Test cases for DELETE /api/v1/posts/{post_id} endpoint"""

    @pytest.mark.asyncio
    async def test_delete_post_success(self, client_with_mocks):
        """Test successful post deletion"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.delete_post.return_value = True

        response = client.delete("/api/v1/posts/1")

        assert response.status_code == 204
        assert response.text == ""
        mock_repo.delete_post.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_post_not_found(self, client_with_mocks):
        """Test deletion of non-existent post"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.delete_post.return_value = False

        response = client.delete("/api/v1/posts/999")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Post not found"
        mock_repo.delete_post.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_delete_post_invalid_id(self, client_with_mocks):
        """Test deletion with invalid post ID format"""
        client, _, _ = client_with_mocks

        response = client.delete("/api/v1/posts/invalid")

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_post_without_auth(self):
        """Test post deletion without authentication"""
        with TestClient(app) as client:
            response = client.delete("/api/v1/posts/1")

            assert response.status_code == 401


class TestPostsControllerIntegration:
    """Integration test cases for posts controller"""

    @pytest.mark.asyncio
    async def test_full_post_lifecycle(self, client_with_mocks):
        """Test complete CRUD lifecycle of a post"""
        client, mock_repo, _ = client_with_mocks

        # Create
        created_post = Post(id=1, title="Test Post", body="Test body", is_published=True)
        mock_repo.create_post.return_value = created_post

        create_response = client.post(
            "/api/v1/posts", json={"title": "Test Post", "body": "Test body", "is_published": True}
        )
        assert create_response.status_code == 201

        # Read
        mock_repo.find_post.return_value = created_post
        get_response = client.get("/api/v1/posts/1")
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["title"] == "Test Post"

        # Update
        updated_post = Post(id=1, title="Updated Post", body="Updated body", is_published=True)
        mock_repo.update_post.return_value = updated_post

        update_response = client.put(
            "/api/v1/posts/1", json={"title": "Updated Post", "body": "Updated body", "is_published": True}
        )
        assert update_response.status_code == 200
        update_data = update_response.json()
        assert update_data["title"] == "Updated Post"

        # Delete
        mock_repo.delete_post.return_value = True
        delete_response = client.delete("/api/v1/posts/1")
        assert delete_response.status_code == 204

    @pytest.mark.asyncio
    async def test_posts_controller_with_multiple_posts(self, client_with_mocks, sample_posts):
        """Test controller with multiple posts in different scenarios"""
        client, mock_repo, _ = client_with_mocks

        # Test listing multiple posts
        mock_repo.all_posts.return_value = sample_posts
        response = client.get("/api/v1/posts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        # Test finding specific posts
        mock_repo.find_post.return_value = sample_posts[0]
        response = client.get("/api/v1/posts/1")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "First Post"
