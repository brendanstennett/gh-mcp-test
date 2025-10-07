# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportAny=false
# pyright: reportUnknownMemberType=false

import uuid
from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from api.models.comment import Comment
from api.models.user import User
from api.services.repositories.comments_repository import CommentsRepository
from api.setup.app import app
from api.setup.auth import current_user
from api.setup.dependencies import get_comments_repository


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
def mock_comments_repository() -> CommentsRepository:
    mock: CommentsRepository = create_autospec(CommentsRepository, spec_set=True, instance=True)
    return mock


@pytest.fixture
def mock_current_user():
    """Create a mock current user"""
    user = User(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    return user


@pytest.fixture
def client_with_mocks(mock_comments_repository, mock_current_user):
    """Create a test client with mocked dependencies"""

    def override_get_comments_repository():
        return mock_comments_repository

    def override_current_user():
        return mock_current_user

    app.dependency_overrides[get_comments_repository] = override_get_comments_repository
    app.dependency_overrides[current_user] = override_current_user

    with TestClient(app) as client:
        yield client, mock_comments_repository, mock_current_user

    app.dependency_overrides.clear()


@pytest.fixture
def sample_comment():
    """Create a sample comment for testing"""
    return Comment(id=1, body="Test comment", is_published=True, post_id=1)


@pytest.fixture
def sample_comments():
    """Create a list of sample comments for testing"""
    return [
        Comment(id=1, body="First comment", is_published=True, post_id=1),
        Comment(id=2, body="Second comment", is_published=True, post_id=1),
        Comment(id=3, body="Third comment", is_published=True, post_id=2),
    ]


class TestListComments:
    """Test cases for GET /api/v1/comments endpoint"""

    @pytest.mark.asyncio
    async def test_list_comments_success(self, client_with_mocks, sample_comments):
        """Test successful retrieval of all comments"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.all_comments.return_value = sample_comments

        response = client.get("/api/v1/comments")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["body"] == "First comment"
        assert data[1]["body"] == "Second comment"
        assert data[2]["body"] == "Third comment"
        mock_repo.all_comments.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_comments_empty(self, client_with_mocks):
        """Test retrieval when no comments exist"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.all_comments.return_value = []

        response = client.get("/api/v1/comments")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        mock_repo.all_comments.assert_called_once()


class TestFindComment:
    """Test cases for GET /api/v1/comments/{comment_id} endpoint"""

    @pytest.mark.asyncio
    async def test_find_comment_success(self, client_with_mocks, sample_comment):
        """Test successful retrieval of a specific comment"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.find_comment.return_value = sample_comment

        response = client.get("/api/v1/comments/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["body"] == "Test comment"
        mock_repo.find_comment.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_find_comment_not_found(self, client_with_mocks):
        """Test retrieval of non-existent comment"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.find_comment.return_value = None

        response = client.get("/api/v1/comments/999")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Comment not found"
        mock_repo.find_comment.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_find_comment_invalid_id(self, client_with_mocks):
        """Test retrieval with invalid comment ID format"""
        client, _, _ = client_with_mocks

        response = client.get("/api/v1/comments/invalid")

        assert response.status_code == 422  # Validation error


class TestCreateComment:
    """Test cases for POST /api/v1/comments endpoint"""

    @pytest.mark.asyncio
    async def test_create_comment_success(self, client_with_mocks, sample_comment):
        """Test successful comment creation"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.create_comment.return_value = sample_comment

        comment_data = {"body": "Test comment", "is_published": True, "post_id": 1}
        response = client.post("/api/v1/comments", json=comment_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["body"] == "Test comment"
        # Verify the call was made with a Comment object
        mock_repo.create_comment.assert_called_once()
        call_args = mock_repo.create_comment.call_args[0][0]
        assert call_args.body == "Test comment"

    @pytest.mark.asyncio
    async def test_create_comment_with_id_specified(self, client_with_mocks):
        """Test comment creation when ID is specified (should be ignored)"""
        client, mock_repo, _ = client_with_mocks

        created_comment = Comment(id=1, body="Test comment", is_published=True, post_id=1)
        mock_repo.create_comment.return_value = created_comment

        comment_data = {"id": 999, "body": "Test comment", "is_published": True, "post_id": 1}  # ID should be ignored
        response = client.post("/api/v1/comments", json=comment_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1  # Uses the ID from mock, not from request
        assert data["body"] == "Test comment"
        mock_repo.create_comment.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_comment_empty_body(self, client_with_mocks):
        """Test comment creation with empty body"""
        client, mock_repo, _ = client_with_mocks

        created_comment = Comment(id=1, body="", is_published=False, post_id=1)
        mock_repo.create_comment.return_value = created_comment

        comment_data = {"body": "", "is_published": False, "post_id": 1}
        response = client.post("/api/v1/comments", json=comment_data)

        assert response.status_code == 201
        data = response.json()
        assert data["body"] == ""
        mock_repo.create_comment.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_comment_without_auth(self):
        """Test comment creation without authentication"""
        with TestClient(app) as client:
            comment_data = {"body": "Test comment", "is_published": True, "post_id": 1}
            response = client.post("/api/v1/comments", json=comment_data)

            assert response.status_code == 401


class TestUpdateComment:
    """Test cases for PUT /api/v1/comments/{comment_id} endpoint"""

    @pytest.mark.asyncio
    async def test_update_comment_success(self, client_with_mocks):
        """Test successful comment update"""
        client, mock_repo, _ = client_with_mocks
        updated_comment = Comment(id=1, body="Updated comment", is_published=True, post_id=1)
        mock_repo.update_comment.return_value = updated_comment

        comment_data = {"body": "Updated comment", "is_published": True, "post_id": 1}
        response = client.put("/api/v1/comments/1", json=comment_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["body"] == "Updated comment"
        # Verify the call was made correctly
        mock_repo.update_comment.assert_called_once()
        call_args = mock_repo.update_comment.call_args
        assert call_args[0][0] == 1  # comment_id
        assert call_args[0][1].body == "Updated comment"  # updated comment data

    @pytest.mark.asyncio
    async def test_update_comment_not_found(self, client_with_mocks):
        """Test update of non-existent comment"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.update_comment.return_value = None

        comment_data = {"body": "Updated comment", "is_published": True, "post_id": 1}
        response = client.put("/api/v1/comments/999", json=comment_data)

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Comment not found"
        mock_repo.update_comment.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_comment_with_same_body(self, client_with_mocks):
        """Test update with same body"""
        client, mock_repo, _ = client_with_mocks

        updated_comment = Comment(id=1, body="Same body", is_published=True, post_id=1)
        mock_repo.update_comment.return_value = updated_comment

        comment_data = {"body": "Same body", "is_published": True, "post_id": 1}
        response = client.put("/api/v1/comments/1", json=comment_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["body"] == "Same body"
        mock_repo.update_comment.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_comment_without_auth(self):
        """Test comment update without authentication"""
        with TestClient(app) as client:
            comment_data = {"body": "Updated comment", "is_published": True, "post_id": 1}
            response = client.put("/api/v1/comments/1", json=comment_data)

            assert response.status_code == 401


class TestDeleteComment:
    """Test cases for DELETE /api/v1/comments/{comment_id} endpoint"""

    @pytest.mark.asyncio
    async def test_delete_comment_success(self, client_with_mocks):
        """Test successful comment deletion"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.delete_comment.return_value = True

        response = client.delete("/api/v1/comments/1")

        assert response.status_code == 204
        assert response.text == ""
        mock_repo.delete_comment.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_comment_not_found(self, client_with_mocks):
        """Test deletion of non-existent comment"""
        client, mock_repo, _ = client_with_mocks
        mock_repo.delete_comment.return_value = False

        response = client.delete("/api/v1/comments/999")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Comment not found"
        mock_repo.delete_comment.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_delete_comment_invalid_id(self, client_with_mocks):
        """Test deletion with invalid comment ID format"""
        client, _, _ = client_with_mocks

        response = client.delete("/api/v1/comments/invalid")

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_comment_without_auth(self):
        """Test comment deletion without authentication"""
        with TestClient(app) as client:
            response = client.delete("/api/v1/comments/1")

            assert response.status_code == 401


class TestCommentsControllerIntegration:
    """Integration test cases for comments controller"""

    @pytest.mark.asyncio
    async def test_full_comment_lifecycle(self, client_with_mocks):
        """Test complete CRUD lifecycle of a comment"""
        client, mock_repo, _ = client_with_mocks

        # Create
        created_comment = Comment(id=1, body="Test comment", is_published=True, post_id=1)
        mock_repo.create_comment.return_value = created_comment

        create_response = client.post(
            "/api/v1/comments", json={"body": "Test comment", "is_published": True, "post_id": 1}
        )
        assert create_response.status_code == 201

        # Read
        mock_repo.find_comment.return_value = created_comment
        get_response = client.get("/api/v1/comments/1")
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["body"] == "Test comment"

        # Update
        updated_comment = Comment(id=1, body="Updated comment", is_published=True, post_id=1)
        mock_repo.update_comment.return_value = updated_comment

        update_response = client.put(
            "/api/v1/comments/1", json={"body": "Updated comment", "is_published": True, "post_id": 1}
        )
        assert update_response.status_code == 200
        update_data = update_response.json()
        assert update_data["body"] == "Updated comment"

        # Delete
        mock_repo.delete_comment.return_value = True
        delete_response = client.delete("/api/v1/comments/1")
        assert delete_response.status_code == 204

    @pytest.mark.asyncio
    async def test_comments_controller_with_multiple_comments(self, client_with_mocks, sample_comments):
        """Test controller with multiple comments in different scenarios"""
        client, mock_repo, _ = client_with_mocks

        # Test listing multiple comments
        mock_repo.all_comments.return_value = sample_comments
        response = client.get("/api/v1/comments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        # Test finding specific comments
        mock_repo.find_comment.return_value = sample_comments[0]
        response = client.get("/api/v1/comments/1")
        assert response.status_code == 200
        data = response.json()
        assert data["body"] == "First comment"
