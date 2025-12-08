import pytest
from unittest.mock import patch, MagicMock
from app import create_app, TestConfig # Import your Flask app instance

@pytest.fixture
def client():
    # Use Flask's test client
    app_instance = create_app(config_object=TestConfig) # Pass TestConfig for testing
    with app_instance.test_client() as client:
        yield client

@patch('routes.generate_narrative')
def test_generate_narrative_success(mock_generate_narrative, client):
    # Mock the generate_narrative function from ai_service.py
    mock_generate_narrative.return_value = "A tale of mystery and intrigue."

    response = client.post(
        '/generate_narrative',
        json={'prompt': 'Generate a mysterious story.'}
    )

    assert response.status_code == 200
    assert response.json == {'narrative': 'A tale of mystery and intrigue.'}
    mock_generate_narrative.assert_called_once_with('Generate a mysterious story.')

@patch('routes.generate_narrative')
def test_generate_narrative_missing_prompt(mock_generate_narrative, client):
    response = client.post(
        '/generate_narrative',
        json={}
    )

    assert response.status_code == 400
    assert response.json == {'error': 'Prompt is required'}
    mock_generate_narrative.assert_not_called()

@patch('routes.generate_narrative')
def test_generate_narrative_ai_service_error(mock_generate_narrative, client):
    # Mock ai_service to return an error string
    mock_generate_narrative.return_value = "Error: Something went wrong with the AI."

    response = client.post(
        '/generate_narrative',
        json={'prompt': 'Generate a story that fails.'}
    )

    assert response.status_code == 500
    assert response.json == {'error': 'Error: Something went wrong with the AI.'}
    mock_generate_narrative.assert_called_once_with('Generate a story that fails.')

