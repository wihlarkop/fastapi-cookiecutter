"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def app():
    """Create application instance for testing."""
    from main import app
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    from fastapi.testclient import TestClient
    return TestClient(app)
