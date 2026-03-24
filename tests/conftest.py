import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provides a TestClient instance for testing FastAPI endpoints."""
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Provides a sample email for testing."""
    return "student@test.edu"