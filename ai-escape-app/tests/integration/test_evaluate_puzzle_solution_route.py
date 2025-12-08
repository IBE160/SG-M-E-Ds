import pytest
from unittest.mock import patch, MagicMock
from app import create_app, TestConfig
from models import GameSession
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    app = create_app(config_object=TestConfig)
    with app.test_client() as client:
        # Push an application context to make app.session available
        with app.app_context():
            yield client

@patch('routes.evaluate_and_adapt_puzzle')
def test_evaluate_puzzle_solution_success(
    mock_evaluate_and_adapt_puzzle,
    client,
):
    # Setup mocks
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Excellent!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }

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
    mock_evaluate_and_adapt_puzzle.assert_called_once_with(
        puzzle_id="test_puzzle",
        player_attempt="correct",
        puzzle_solution="correct",
        current_puzzle_state={},
        theme="mystery",
        location="mansion",
        difficulty="medium",
        narrative_archetype="mystery",
    )

@patch('routes.evaluate_and_adapt_puzzle')
def test_evaluate_puzzle_solution_missing_parameters(
    mock_evaluate_and_adapt_puzzle,
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

@patch('routes.evaluate_and_adapt_puzzle')
def test_evaluate_puzzle_solution_ai_error(
    mock_evaluate_and_adapt_puzzle,
    client,
):
    mock_evaluate_and_adapt_puzzle.return_value = {"error": "AI service unavailable."}
    
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
    mock_evaluate_and_adapt_puzzle.assert_called_once()


