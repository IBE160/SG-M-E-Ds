import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch # Added import
from models import Base, GameSession
from data.rooms import ROOM_DATA
from services.game_logic import (
    create_game_session,
    get_game_session,
    update_game_session,
    delete_game_session,
    update_player_inventory,
    solve_puzzle,
    get_contextual_options,
    verify_puzzle_solvability, # Added for tests
)


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_game_session_model():
    session = GameSession(
        player_id="test_player_id",
        current_room="test_room",
        inventory=["item1"],
        game_history=["start"],
        narrative_state={"key": "value"},
        puzzle_state={"puzzle1": "incomplete"},
        theme="fantasy",
        location="forest",
        difficulty="hard",
    )
    assert session.player_id == "test_player_id"
    assert session.current_room == "test_room"
    assert session.inventory == ["item1"]
    assert session.game_history == ["start"]
    assert session.narrative_state == {"key": "value"}
    assert session.puzzle_state == {"puzzle1": "incomplete"}
    assert session.theme == "fantasy"
    assert session.location == "forest"
    assert session.difficulty == "hard"
    # start_time and last_updated are populated by func.now() on commit, not on instantiation
    assert session.start_time is None
    assert session.last_updated is None


def test_create_game_session(db_session):
    new_session = create_game_session(db_session, "player1")
    assert new_session.id is not None
    assert new_session.player_id == "player1"
    assert new_session.current_room == next(iter(ROOM_DATA)) # Assert the first room from ROOM_DATA
    assert new_session.inventory == []
    assert isinstance(new_session.start_time, datetime)
    assert isinstance(new_session.last_updated, datetime)
    # For SQLite, tzinfo might be None even with DateTime(timezone=True) as SQLite does not store timezone info.
    # We assert that it's a datetime object, but don't strictly enforce tzinfo for SQLite.
    # PostgreSQL would correctly set tzinfo.

    retrieved_session = get_game_session(db_session, new_session.id)
    assert retrieved_session == new_session


def test_get_game_session(db_session):


    new_session = create_game_session(db_session, "player2")


    retrieved_session = get_game_session(db_session, new_session.id)


    assert retrieved_session.player_id == "player2"


    assert retrieved_session.current_room == next(iter(ROOM_DATA)) # Assert the first room from ROOM_DATA





    assert get_game_session(db_session, 999) is None # Test non-existent session


def test_update_game_session(db_session):
    new_session = create_game_session(db_session, "player3")
    updated_session = update_game_session(
        db_session, new_session.id, current_room="middle_room", inventory=["map"]
    )
    assert updated_session.current_room == "middle_room"
    assert updated_session.inventory == ["map"]
    assert updated_session.last_updated > new_session.start_time

    assert (
        update_game_session(db_session, 999, current_room="fake_room") is None
    )  # Test non-existent session


def test_delete_game_session(db_session):
    new_session = create_game_session(db_session, "player4")
    assert delete_game_session(db_session, new_session.id) is True
    assert get_game_session(db_session, new_session.id) is None

    assert delete_game_session(db_session, 999) is False  # Test non-existent session


def test_update_player_inventory_add(db_session):
    new_session = create_game_session(db_session, "player5")
    updated_session = update_player_inventory(db_session, new_session.id, "key", "add")
    assert "key" in updated_session.inventory
    assert len(updated_session.inventory) == 1

    # Add same item again, should not duplicate
    updated_session = update_player_inventory(db_session, new_session.id, "key", "add")
    assert "key" in updated_session.inventory
    assert len(updated_session.inventory) == 1


def test_update_player_inventory_remove(db_session):
    new_session = create_game_session(db_session, "player6")
    update_player_inventory(db_session, new_session.id, "key", "add")
    updated_session = update_player_inventory(
        db_session, new_session.id, "key", "remove"
    )
    assert "key" not in updated_session.inventory
    assert len(updated_session.inventory) == 0

    # Remove non-existent item
    updated_session = update_player_inventory(
        db_session, new_session.id, "non_existent_item", "remove"
    )
    assert len(updated_session.inventory) == 0


def test_update_player_inventory_invalid_action(db_session):
    new_session = create_game_session(db_session, "player7")
    updated_session = update_player_inventory(
        db_session, new_session.id, "key", "invalid"
    )
    # Should return the session unchanged if action is invalid
    assert updated_session.id == new_session.id
    assert (
        updated_session.inventory == new_session.inventory
    )  # inventory should be unchanged


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_correct_solution(mock_evaluate_and_adapt_puzzle, db_session):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    # Create a game session and set the current room to 'ancient_library'
    game_session = create_game_session(db_session, "player8")
    update_game_session(db_session, game_session.id, current_room="ancient_library")

    # Attempt to solve the 'observation_puzzle' with the correct solution
    is_solved, message, updated_session, ai_evaluation = solve_puzzle(
        db_session, game_session.id, "observation_puzzle", "3"
    )

    mock_evaluate_and_adapt_puzzle.assert_called_once()
    assert is_solved is True
    assert message == "Puzzle solved!"
    assert updated_session.puzzle_state.get("observation_puzzle", {}).get("solved") is True
    assert ai_evaluation["is_correct"] is True
    assert updated_session.puzzle_state.get("observation_puzzle", {}).get("ai_feedback") is not None


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_incorrect_solution(mock_evaluate_and_adapt_puzzle, db_session):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": False,
        "feedback": "Try again.",
        "hint": "Look closely.",
        "difficulty_adjustment_suggestion": "none",
    }
    game_session = create_game_session(db_session, "player9")
    update_game_session(db_session, game_session.id, current_room="mysterious_observatory")

    is_solved, message, updated_session, ai_evaluation = solve_puzzle(
        db_session, game_session.id, "riddle_puzzle", "wrong_answer"
    )

    mock_evaluate_and_adapt_puzzle.assert_called_once()
    assert is_solved is False
    assert "Try again." in message # Message comes from AI feedback
    assert updated_session.puzzle_state.get("riddle_puzzle", {}).get("solved") is False
    assert ai_evaluation["is_correct"] is False
    assert updated_session.puzzle_state.get("riddle_puzzle", {}).get("ai_feedback") is not None


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_already_solved(mock_evaluate_and_adapt_puzzle, db_session):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    game_session = create_game_session(db_session, "player10")
    update_game_session(db_session, game_session.id, current_room="ancient_library")

    # Solve it once
    is_solved_first, message_first, updated_session_first, ai_evaluation_first = solve_puzzle(db_session, game_session.id, "observation_puzzle", "3")
    assert is_solved_first is True

    # Try to solve it again
    is_solved, message, updated_session, ai_evaluation = solve_puzzle(
        db_session, game_session.id, "observation_puzzle", "3"
    )

    assert is_solved is False
    assert message == "This puzzle is already solved."
    assert updated_session.puzzle_state.get("observation_puzzle", {}).get("ai_feedback") is not None # Still get AI feedback for the attempt


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_puzzle_not_found(mock_evaluate_and_adapt_puzzle, db_session):
    # Mock return value, though it shouldn't be called
    mock_evaluate_and_adapt_puzzle.return_value = {"error": "Should not be called"}

    game_session = create_game_session(db_session, "player11")
    update_game_session(db_session, game_session.id, current_room="ancient_library")

    is_solved, message, updated_session, ai_evaluation = solve_puzzle(
        db_session, game_session.id, "non_existent_puzzle", "any_solution"
    )

    mock_evaluate_and_adapt_puzzle.assert_not_called()
    assert is_solved is False
    assert message == "Puzzle not found in current room."
    assert "error" in ai_evaluation # Expect an error message from AI evaluation


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_session_not_found(mock_evaluate_and_adapt_puzzle, db_session):
    # Mock return value, though it shouldn't be called
    mock_evaluate_and_adapt_puzzle.return_value = {"error": "Should not be called"}

    is_solved, message, updated_session, ai_evaluation = solve_puzzle(
        db_session, 999, "observation_puzzle", "3"
    )

    mock_evaluate_and_adapt_puzzle.assert_not_called()
    assert is_solved is False
    assert message == "Game session not found."
    assert updated_session is None
    assert "error" in ai_evaluation # Expect an error message from AI evaluation


def test_get_contextual_options_initial_room(db_session):
    game_session = create_game_session(db_session, "player_options_1")
    options = get_contextual_options(game_session)

    assert "Look around the room" in options
    assert "Go north to Mysterious Observatory" in options
    assert "Solve observation_puzzle" in options
    assert "Go back" not in options # No history yet
    assert len(options) == 3 # Look around, 1 exit, 1 puzzle


def test_get_contextual_options_after_move(db_session):
    game_session = create_game_session(db_session, "player_options_2")
    update_game_session(db_session, game_session.id, current_room="mysterious_observatory", game_history=["ancient_library"])
    options = get_contextual_options(game_session)

    assert "Look around the room" in options
    assert "Go south to Ancient Library" in options
    assert "Go east to Escape Chamber" in options
    assert "Solve riddle_puzzle" in options
    assert "Go back" in options
    assert len(options) == 5 # Look around, 2 exits, 1 puzzle, Go back


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_get_contextual_options_after_puzzle_solved(mock_evaluate_and_adapt_puzzle, db_session):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    game_session = create_game_session(db_session, "player_options_3")
    # Solve the puzzle in ancient_library
    solve_puzzle(db_session, game_session.id, "observation_puzzle", "3")
    options = get_contextual_options(game_session)

    assert "Look around the room" in options
    assert "Go north to Mysterious Observatory" in options
    assert "Solve observation_puzzle" not in options # Puzzle should not be an option after being solved
    assert "Go back" not in options # Still no history after create_game_session
    assert len(options) == 2 # Look around, 1 exit


def test_get_contextual_options_escape_chamber(db_session):
    game_session = create_game_session(db_session, "player_options_4")
    update_game_session(db_session, game_session.id, current_room="escape_chamber", game_history=["ancient_library", "mysterious_observatory"])
    options = get_contextual_options(game_session)

    assert "Look around the room" in options
    assert "Go west to Mysterious Observatory" in options
    assert "Go back" in options
    assert len(options) == 3 # Look around, 1 exit, Go back

@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_tracks_hints_used(mock_evaluate_and_adapt_puzzle, db_session):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": False,
        "feedback": "That's not quite right. Think about...",
        "hint": "Consider the shadows.",
        "difficulty_adjustment_suggestion": "none",
    }
    game_session = create_game_session(db_session, "player_hints_used")
    update_game_session(db_session, game_session.id, current_room="ancient_library")

    solve_puzzle(db_session, game_session.id, "observation_puzzle", "wrong_attempt")
    
    updated_session = get_game_session(db_session, game_session.id)
    puzzle_state = updated_session.puzzle_state.get("observation_puzzle", {})
    
    assert "hints_used" in puzzle_state
    assert puzzle_state["hints_used"] == 1 # hints_used should be 1 after AI provides a hint for an incorrect attempt

    # Test another incorrect attempt with a hint
    solve_puzzle(db_session, game_session.id, "observation_puzzle", "another_wrong_attempt")
    updated_session = get_game_session(db_session, game_session.id)
    puzzle_state = updated_session.puzzle_state.get("observation_puzzle", {})
    assert puzzle_state["hints_used"] == 2

    # Test correct attempt, hints_used should not change
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    solve_puzzle(db_session, game_session.id, "observation_puzzle", "3")
    updated_session = get_game_session(db_session, game_session.id)
    puzzle_state = updated_session.puzzle_state.get("observation_puzzle", {})
    assert puzzle_state["hints_used"] == 2 # Should remain 2, not increment for correct solve