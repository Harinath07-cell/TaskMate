import pytest
from backend.app import create_app
from backend.database import db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def test_db():
    # Helper for running custom test SQL if needed
    return db
