import pytest
import json
from flask import Flask
from app import create_app
from data.help_content import HELP_CONTENT

@pytest.fixture(scope="module")
def app_with_db():
    """
    Fixture for a Flask app without a database needed for help routes.
    """
    app = create_app(
        config_object=type(
            "TestConfig",
            (object,),
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # Added dummy URI
            },
        )
    )
    # No DB setup/teardown needed
    yield app

@pytest.fixture(scope="module")
def client(app_with_db: Flask):
    """
    Fixture for a test client.
    """
    return app_with_db.test_client()

def test_get_help_content_route(client):
    """
    Tests the GET /help_content route to ensure it returns the correct structured help content.
    """
    response = client.get("/help_content")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert isinstance(data, dict)
    assert "how_to_play" in data
    assert "current_objective" in data
    assert "game_controls" in data
    assert data["how_to_play"]["title"] == HELP_CONTENT["how_to_play"]["title"]
    assert data["how_to_play"]["content"] == HELP_CONTENT["how_to_play"]["content"]
    assert data == HELP_CONTENT # Ensure the entire content matches
