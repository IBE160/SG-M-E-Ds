import pytest
from app import create_app, Config
from data.game_options import GAME_SETUP_OPTIONS

@pytest.fixture
def client():
    app = create_app(Config)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_game_setup_options(client):
    """
    Test the GET /game_setup_options endpoint.
    """
    response = client.get("/game_setup_options")
    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, dict)
    
    # Assert expected keys are present
    expected_keys = ["themes", "locations", "puzzle_types", "difficulty_levels"]
    for key in expected_keys:
        assert key in data
        assert isinstance(data[key], list)
        
    # Assert the content matches the GAME_SETUP_OPTIONS
    assert data == GAME_SETUP_OPTIONS
