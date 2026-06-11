# pylint: disable=redefined-outer-name
"""Fixtures for testing."""

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class AuthActions:
    """A helper class to log in and out in tests."""
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        """Make a POST request to /auth/login with the given username and password."""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        """Make a GET request to /auth/logout."""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """A helper to log in and out in tests."""
    return AuthActions(client)
