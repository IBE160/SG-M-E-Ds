import pytest
from unittest.mock import patch, MagicMock
import json # Added import for json
from app import create_app, TestConfig
from models import GameSession
from sqlalchemy.orm import Session

# Global mock for evaluate_and_adapt_puzzle to be used in tests
# @pytest.fixture # Removed this as it's better to patch directly in each test
# def mock_evaluate_and_adapt_puzzle_global():
#     with patch('services.ai_service.evaluate_and_adapt_puzzle') as mock_func:
#         yield mock_func

@pytest.fixture
def client():
    app = create_app(config_object=TestConfig)
    with app.test_client() as client:
        # Push an application context to make app.session available
        with app.app_context():
            yield client

@patch('services.ai_service.genai') # Patch genai directly
def test_evaluate_puzzle_solution_success(
    mock_genai, # Use mock_genai
    client,
):
    # Setup mock response for genai
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "is_correct": True,
        "feedback": "Excellent!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    })
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    response = client.post(
        '/evaluate_puzzle_solution',
        json={
            "puzzle_id": "test_puzzle",
            "player_attempt": "correct",
            "puzzle_solution": "correct",
            "current_puzzle_state": {},
            "theme": "mystery",
            "location": "mansion",
            "difficulty": "medium",
            "narrative_archetype": "mystery",
        }
    )

    assert response.status_code == 200
    assert response.json == {
        "is_correct": True,
        "feedback": "Excellent!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    # Can also assert the prompt content if needed, but not critical for this test's pass/fail
@patch('services.ai_service.evaluate_and_adapt_puzzle') # Added patch
def test_evaluate_puzzle_solution_missing_parameters(
    mock_evaluate_and_adapt_puzzle, # Added mock argument
    client
):
    response = client.post(
        '/evaluate_puzzle_solution',
        json={
            "puzzle_id": "test_puzzle",
            "player_attempt": "wrong",
            # Missing puzzle_solution
            "current_puzzle_state": {},
            "theme": "mystery",
            "location": "mansion",
            "difficulty": "medium",
            "narrative_archetype": "mystery", # Added optional parameter
        }
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing required parameters for puzzle evaluation"}
    mock_evaluate_and_adapt_puzzle.assert_not_called()

@patch('services.ai_service.genai') # Added patch to ensure it is mocked
def test_evaluate_puzzle_solution_ai_error(
    mock_genai, # Use the local mock
    client,
):
    # Setup mock return value for the patched function
    mock_response = MagicMock()
    mock_response.text = json.dumps({"error": "AI service unavailable."}) # Mock the JSON response
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
    
    response = client.post(
        '/evaluate_puzzle_solution',
        json={
            "puzzle_id": "test_puzzle",
            "player_attempt": "wrong",
            "puzzle_solution": "correct",
            "current_puzzle_state": {},
            "theme": "mystery",
            "location": "mansion",
            "difficulty": "medium",
            "narrative_archetype": "mystery",
        }
    )

    assert response.status_code == 500
    assert "error" in response.json
    assert "AI service unavailable." in response.json["error"]
    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')