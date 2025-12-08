import pytest
from unittest.mock import patch, MagicMock
from app import create_app, TestConfig

@pytest.fixture
def client():
    app = create_app(config_object=TestConfig)
    with app.test_client() as client:
        yield client

@patch('routes.generate_puzzle')
def test_generate_puzzle_success(mock_generate_puzzle, client):
    mock_generate_puzzle.return_value = {"description": "What has an eye but cannot see?", "solution": "A needle"}

    response = client.post(
        '/generate_puzzle',
        json={
            "puzzle_type": "Riddle",
            "difficulty": "easy",
            "theme": "fantasy",
            "location": "magical forest",
            "narrative_archetype": "mystery",
            "puzzle_context": {"item_present": "magical orb"}
        }
    )

    assert response.status_code == 200
    assert response.json == {"description": "What has an eye but cannot see?", "solution": "A needle"}
    mock_generate_puzzle.assert_called_once_with(
        puzzle_type="Riddle",
        difficulty="easy",
        theme="fantasy",
        location="magical forest",
        narrative_archetype="mystery",
        puzzle_context={"item_present": "magical orb"}
    )

@patch('routes.generate_puzzle')
def test_generate_puzzle_missing_required_data(mock_generate_puzzle, client):
    response = client.post(
        '/generate_puzzle',
        json={
            "puzzle_type": "Riddle",
            "difficulty": "easy",
            "theme": "fantasy",
            # Missing location
        }
    )

    assert response.status_code == 400
    assert response.json == {"error": "Puzzle type, difficulty, theme, and location are required"}
    mock_generate_puzzle.assert_not_called()

@patch('routes.generate_puzzle')
def test_generate_puzzle_ai_service_error(mock_generate_puzzle, client):
    mock_generate_puzzle.return_value = {"error": "AI puzzle generation failed."}

    response = client.post(
        '/generate_puzzle',
        json={
            "puzzle_type": "Observation",
            "difficulty": "medium",
            "theme": "sci-fi",
            "location": "space station",
        }
    )

    assert response.status_code == 500
    assert response.json == {"error": "AI puzzle generation failed."}
    mock_generate_puzzle.assert_called_once()
