import pytest
from unittest.mock import patch, MagicMock
from app import create_app, TestConfig

@pytest.fixture
def client():
    app = create_app(config_object=TestConfig)
    with app.test_client() as client:
        yield client

@patch('routes.generate_room_description')
def test_generate_room_description_success(mock_generate_room_description, client):
    mock_generate_room_description.return_value = "A dynamically generated room description."

    response = client.post(
        '/generate_room_description',
        json={
            "theme": "fantasy",
            "location": "castle",
            "narrative_state": "The player is looking for a lost artifact.",
            "room_context": {"name": "Throne Room"}
        }
    )

    assert response.status_code == 200
    assert response.json == {'description': 'A dynamically generated room description.'}
    mock_generate_room_description.assert_called_once()

@patch('routes.generate_room_description')
def test_generate_room_description_missing_data(mock_generate_room_description, client):
    response = client.post(
        '/generate_room_description',
        json={"theme": "fantasy"} # Missing other required fields
    )

    assert response.status_code == 400
    assert response.json == {'error': 'Theme, location, narrative_state, and room_context are required'}
    mock_generate_room_description.assert_not_called()

@patch('routes.generate_room_description')
def test_generate_room_description_ai_service_error(mock_generate_room_description, client):
    mock_generate_room_description.return_value = "Error: AI service is down."

    response = client.post(
        '/generate_room_description',
        json={
            "theme": "sci-fi",
            "location": "space station",
            "narrative_state": "The AI is malfunctioning.",
            "room_context": {"name": "Bridge"}
        }
    )

    assert response.status_code == 500
    assert response.json == {'error': 'Error: AI service is down.'}
    mock_generate_room_description.assert_called_once()
