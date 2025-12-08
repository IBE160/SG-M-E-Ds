import pytest
import json
from unittest.mock import patch # Added import
from app import create_app
from models import Base
from data.rooms import ROOM_DATA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def client():
    # Use TestConfig for in-memory SQLite database
    app = create_app(
        config_object=type(
            "TestConfig",
            (object,),
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            },
        )
    )
    with app.test_client() as client:
        # Create tables before each test
        with app.app_context():
            engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            app.session = Session()  # Attach a new session for the test
        yield client
        # Drop tables after each test
        with app.app_context():
            Base.metadata.drop_all(engine)
            app.session.close()


def test_hello_world(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Hello, World!" in rv.data


def test_start_game(client):
    response = client.post("/start_game", json={"player_id": "test_player"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["player_id"] == "test_player"
    assert data["current_room"] == next(iter(ROOM_DATA)) # Assert the first room from ROOM_DATA
    assert data["inventory"] == []
    assert "id" in data

def test_start_game_with_theme_and_location(client):
    chosen_theme = "space"
    chosen_location = "mars colony"
    response = client.post(
        "/start_game",
        json={
            "player_id": "test_player_themed",
            "theme": chosen_theme,
            "location": chosen_location,
        }
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["player_id"] == "test_player_themed"
    assert data["id"] is not None

    # Retrieve the game session to verify theme and location
    session_id = data["id"]
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["theme"] == chosen_theme
    assert get_data["location"] == chosen_location


def test_get_game_session(client):
    # First create a session
    start_response = client.post("/start_game", json={"player_id": "test_player_get"})
    session_id = json.loads(start_response.data)["id"]
    initial_room_id = next(iter(ROOM_DATA))
    initial_room_info = ROOM_DATA[initial_room_id]

    response = client.get(f"/game_session/{session_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == session_id
    assert data["player_id"] == "test_player_get"
    assert data["current_room"] == initial_room_id
    assert data["current_room_name"] == initial_room_info["name"]
    assert data["current_room_description"] == initial_room_info["description"]
    assert data["current_room_image"] == f"/static/images/{initial_room_info['image']}"
    assert "contextual_options" in data
    assert isinstance(data["contextual_options"], list)
    assert len(data["contextual_options"]) > 0

    # Test non-existent session
    response = client.get("/game_session/9999")
    assert response.status_code == 404


def test_move_player_valid_move(client):
    start_response = client.post("/start_game", json={"player_id": "test_player_move_valid"})
    session_id = json.loads(start_response.data)["id"]

    # Assuming 'start_room' leads to 'ancient_library'
    # Need to find the first room from ROOM_DATA and set it as current_room
    first_room_id = next(iter(ROOM_DATA))
    # client.post(f"/game_session/{session_id}/move", json={"direction": "north"}) # Move from start_room to ancient_library

    # Move from ancient_library north to mysterious_observatory
    response = client.post(f"/game_session/{session_id}/move", json={"direction": "north"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == session_id
    assert data["current_room"] == "mysterious_observatory"

    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["current_room"] == "mysterious_observatory"


def test_move_player_invalid_move(client):
    start_response = client.post("/start_game", json={"player_id": "test_player_move_invalid"})
    session_id = json.loads(start_response.data)["id"]

    # Attempt to move in an invalid direction from 'start_room'
    response = client.post(f"/game_session/{session_id}/move", json={"direction": "invalid_direction"})
    assert response.status_code == 400
    assert b"Cannot move invalid_direction from Ancient Library." in response.data


def test_handle_inventory_add(client):
    # First create a session
    start_response = client.post(
        "/start_game", json={"player_id": "test_player_inventory_add"}
    )
    session_id = json.loads(start_response.data)["id"]

    response = client.post(
        f"/game_session/{session_id}/inventory", json={"item": "key", "action": "add"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == session_id
    assert "key" in data["inventory"]

    # Verify update persisted
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert "key" in get_data["inventory"]


def test_handle_inventory_remove(client):
    # First create a session and add an item
    start_response = client.post(
        "/start_game", json={"player_id": "test_player_inventory_remove"}
    )
    session_id = json.loads(start_response.data)["id"]
    client.post(
        f"/game_session/{session_id}/inventory", json={"item": "key", "action": "add"}
    )

    response = client.post(
        f"/game_session/{session_id}/inventory",
        json={"item": "key", "action": "remove"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == session_id
    assert "key" not in data["inventory"]

    # Verify update persisted
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert "key" not in get_data["inventory"]

    # Test with non-existent session
    response = client.post(
        "/game_session/9999/inventory", json={"item": "fake_item", "action": "add"}
    )
    assert response.status_code == 404


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_route_correct_solution(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_solve_puzzle_correct"})
    session_id = json.loads(start_response.data)["id"]

    # Move to a room with a puzzle (ancient_library has observation_puzzle)
    # client.post(f"/game_session/{session_id}/move", json={"direction": "north"}) # start_room to ancient_library

    response = client.post(
        f"/game_session/{session_id}/solve_puzzle",
        json={"puzzle_id": "observation_puzzle", "solution_attempt": "3"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is True
    assert data["message"] == "Puzzle solved!"
    assert "ai_evaluation" in data
    assert data["ai_evaluation"]["is_correct"] is True

    # Verify puzzle state updated
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["puzzle_state"].get("observation_puzzle", {}).get("solved") is True


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_route_incorrect_solution(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": False,
        "feedback": "Try again.",
        "hint": "Think harder.",
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_solve_puzzle_incorrect"})
    session_id = json.loads(start_response.data)["id"]

    # Move to a room with a puzzle (ancient_library has observation_puzzle)
    # client.post(f"/game_session/{session_id}/move", json={"direction": "north"}) # start_room to ancient_library

    response = client.post(
        f"/game_session/{session_id}/solve_puzzle",
        json={"puzzle_id": "observation_puzzle", "solution_attempt": "wrong"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is False
    assert "Try again." in data["message"] # Message comes from AI feedback
    assert "ai_evaluation" in data
    assert data["ai_evaluation"]["is_correct"] is False


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_solve_puzzle_route_puzzle_already_solved(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True, # The AI might still say it's correct if we re-attempt a correct solution
        "feedback": "You already solved this one!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_solve_puzzle_already"})
    session_id = json.loads(start_response.data)["id"]

    # Move to a room with a puzzle
    # client.post(f"/game_session/{session_id}/move", json={"direction": "north"}) # start_room to ancient_library

    # Solve it once
    client.post(
        f"/game_session/{session_id}/solve_puzzle",
        json={"puzzle_id": "observation_puzzle", "solution_attempt": "3"},
    )

    # Try to solve again
    response = client.post(
        f"/game_session/{session_id}/solve_puzzle",
        json={"puzzle_id": "observation_puzzle", "solution_attempt": "3"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is False
    assert data["message"] == "This puzzle is already solved."
    assert "ai_evaluation" in data
    # The AI evaluation for an already solved puzzle might still return is_correct: True
    # as it re-evaluates the attempt, but the game logic itself prevents re-solving.
    # So we only assert on the game message.


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_game_escape(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_escape"})
    session_id = json.loads(start_response.data)["id"]

    # Current room is ancient_library
    # Solve observation puzzle in ancient_library
    response = client.post(
        f"/game_session/{session_id}/solve_puzzle",
        json={"puzzle_id": "observation_puzzle", "solution_attempt": "3"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is True
    assert data["message"] == "Puzzle solved!"
    assert "game_over" not in data # Game not over yet
    assert data["ai_evaluation"]["is_correct"] is True

    # Move to mysterious_observatory
    response = client.post(f"/game_session/{session_id}/move", json={"direction": "north"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["current_room"] == "mysterious_observatory"

    # Solve riddle puzzle in mysterious_observatory
    response = client.post(
        f"/game_session/{session_id}/solve_puzzle",
        json={"puzzle_id": "riddle_puzzle", "solution_attempt": "map"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is True
    assert data["message"] == "Puzzle solved!"
    assert "game_over" not in data # Game not over yet
    assert data["ai_evaluation"]["is_correct"] is True

    # Move to escape_chamber - this should trigger the escape
    response = client.post(f"/game_session/{session_id}/move", json={"direction": "east"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["current_room"] == "escape_chamber"
    assert data["game_over"] is True
    assert data["message"] == "You escaped!"

    # Verify that the game session is marked as completed
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["current_room"] == "escape_chamber"
    # The get_session route itself doesn't return game_over,
    # it's only returned by the move_player route if the game ends.
    # So we don't assert game_over here.


def test_interact_look_around(client):
    start_response = client.post("/start_game", json={"player_id": "test_player_interact_look"})
    session_id = json.loads(start_response.data)["id"]

    # Get options for the current room
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    
    # Find "Look around the room" option index
    look_around_index = None
    for i, option in enumerate(options):
        if option == "Look around the room":
            look_around_index = i
            break
    assert look_around_index is not None

    # Interact with "Look around the room"
    response = client.post(
        f"/game_session/{session_id}/interact", json={"option_index": look_around_index}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == ROOM_DATA[next(iter(ROOM_DATA))]["description"]
    assert "contextual_options" in data


def test_interact_valid_move(client):
    start_response = client.post("/start_game", json={"player_id": "test_player_interact_move"})
    session_id = json.loads(start_response.data)["id"]

    # Get options for the current room
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    
    # Find "Go north to Mysterious Observatory" option index
    go_north_index = None
    for i, option in enumerate(options):
        if "Go north" in option:
            go_north_index = i
            break
    assert go_north_index is not None

    # Interact with "Go north"
    response = client.post(
        f"/game_session/{session_id}/interact", json={"option_index": go_north_index}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["current_room"] == "mysterious_observatory"
    assert "contextual_options" in data
    assert "Go south to Ancient Library" in data["contextual_options"]


def test_interact_invalid_move(client):
    start_response = client.post("/start_game", json={"player_id": "test_player_interact_invalid_move"})
    session_id = json.loads(start_response.data)["id"]

    # Get options for the current room (ancient_library)
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    
    # Simulate choosing an invalid move (e.g., trying to go south from ancient_library)
    # We need to construct an option index that leads to an an invalid move
    # For now, let's assume if there's no "Go south" it's invalid, or just pick a random index
    # that would lead to an invalid direction. Since options are dynamically generated,
    # an invalid direction would not be in the list of options.

    # Let's directly post an invalid option index and check for error
    response = client.post(
        f"/game_session/{session_id}/interact", json={"option_index": 999}
    )
    assert response.status_code == 400
    assert b"Invalid option index" in response.data


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_interact_solve_puzzle_correct(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_interact_solve_correct"})
    session_id = json.loads(start_response.data)["id"]

    # Get options for the current room (ancient_library)
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    
    # Find "Solve observation_puzzle" option index
    solve_puzzle_index = None
    for i, option in enumerate(options):
        if "Solve observation_puzzle" in option:
            solve_puzzle_index = i
            break
    assert solve_puzzle_index is not None

    # Interact with "Solve observation_puzzle"
    response = client.post(
        f"/game_session/{session_id}/interact", json={"option_index": solve_puzzle_index, "player_attempt": "3"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is True
    assert data["message"] == "Puzzle solved!"
    assert "contextual_options" in data
    assert "Solve observation_puzzle" not in data["contextual_options"] # Should be gone after solving
    assert "ai_evaluation" in data
    assert data["ai_evaluation"]["is_correct"] is True

    # Verify puzzle state updated
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["puzzle_state"].get("observation_puzzle", {}).get("solved") is True


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_interact_solve_puzzle_incorrect(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": False,
        "feedback": "That is not the correct answer. Try again!",
        "hint": "Consider the number of sides on a triangle.",
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_interact_solve_incorrect"})
    session_id = json.loads(start_response.data)["id"]

    # Get options for the current room (ancient_library)
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    
    # Find "Solve observation_puzzle" option index
    solve_puzzle_index = None
    for i, option in enumerate(options):
        if "Solve observation_puzzle" in option:
            solve_puzzle_index = i
            break
    assert solve_puzzle_index is not None

    # Interact with "Solve observation_puzzle" with an incorrect attempt
    response = client.post(
        f"/game_session/{session_id}/interact", json={"option_index": solve_puzzle_index, "player_attempt": "wrong_answer"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is False
    assert "That is not the correct answer. Try again!" in data["message"]
    assert "contextual_options" in data
    assert "Solve observation_puzzle" in data["contextual_options"] # Should still be there
    assert "ai_evaluation" in data
    assert data["ai_evaluation"]["is_correct"] is False
    assert data["ai_evaluation"]["hint"] == "Consider the number of sides on a triangle."

    # Verify puzzle state updated with attempt and feedback
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    puzzle_state = get_data["puzzle_state"].get("observation_puzzle", {})
    assert puzzle_state.get("solved") is False
    assert puzzle_state.get("attempts") == 1
    assert puzzle_state.get("last_attempt") == "wrong_answer"
    assert puzzle_state["ai_feedback"]["is_correct"] is False


@patch('services.game_logic.evaluate_and_adapt_puzzle')
def test_interact_game_escape(mock_evaluate_and_adapt_puzzle, client):
    mock_evaluate_and_adapt_puzzle.return_value = {
        "is_correct": True,
        "feedback": "Puzzle solved!",
        "hint": None,
        "difficulty_adjustment_suggestion": "none",
    }
    start_response = client.post("/start_game", json={"player_id": "test_player_interact_escape"})
    session_id = json.loads(start_response.data)["id"]

    # --- Solve first puzzle ---
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    solve_puzzle_index = None
    for i, option in enumerate(options):
        if "Solve observation_puzzle" in option:
            solve_puzzle_index = i
            break
    response = client.post(f"/game_session/{session_id}/interact", json={"option_index": solve_puzzle_index, "player_attempt": "3"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is True
    assert data["message"] == "Puzzle solved!"
    assert "ai_evaluation" in data
    assert data["ai_evaluation"]["is_correct"] is True

    # --- Move to second room ---
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    go_north_index = None
    for i, option in enumerate(options):
        if "Go north" in option:
            go_north_index = i
            break
    response = client.post(f"/game_session/{session_id}/interact", json={"option_index": go_north_index})
    data = json.loads(response.data)
    assert data["current_room"] == "mysterious_observatory"

    # --- Solve second puzzle ---
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    solve_riddle_index = None
    for i, option in enumerate(options):
        if "Solve riddle_puzzle" in option:
            solve_riddle_index = i
            break
    response = client.post(f"/game_session/{session_id}/interact", json={"option_index": solve_riddle_index, "player_attempt": "map"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_solved"] is True
    assert data["message"] == "Puzzle solved!"
    assert "ai_evaluation" in data
    assert data["ai_evaluation"]["is_correct"] is True

    # --- Move to escape_chamber (trigger escape) ---
    get_response = client.get(f"/game_session/{session_id}")
    options = json.loads(get_response.data)["contextual_options"]
    go_east_index = None
    for i, option in enumerate(options):
        if "Go east" in option:
            go_east_index = i
            break
    response = client.post(f"/game_session/{session_id}/interact", json={"option_index": go_east_index})
    data = json.loads(response.data)
    assert data["current_room"] == "escape_chamber"
    assert data["game_over"] is True
    assert data["message"] == "You escaped!"

    # Verify that the game session is marked as completed
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["current_room"] == "escape_chamber"
    # The get_session route itself doesn't return game_over,
    # it's only returned by the move_player route if the game ends.
    # So we don't assert game_over here.

@patch('routes.adjust_difficulty_based_on_performance')
def test_adjust_difficulty_route(mock_adjust_difficulty_based_on_performance, client):
    # Mock AI service response
    mock_adjust_difficulty_based_on_performance.return_value = {
        "difficulty_adjustment": "easier",
        "reasoning": "Player struggled.",
        "suggested_puzzle_parameters": {"complexity": "low"}
    }

    # Create a game session
    start_response = client.post("/start_game", json={"player_id": "test_player_difficulty", "difficulty": "medium"})
    session_id = json.loads(start_response.data)["id"]

    # Sample player performance metrics
    player_metrics = {"puzzle_id_1": {"attempts": 5, "hints_used": 2}}

    # Send request to adjust difficulty
    response = client.post(
        "/adjust_difficulty",
        json={
            "session_id": session_id,
            "player_performance_metrics": player_metrics
        }
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["difficulty_adjustment"] == "easier"
    assert response_data["suggested_puzzle_parameters"] == {"complexity": "low"}

    # Verify AI service was called with correct parameters
    mock_adjust_difficulty_based_on_performance.assert_called_once_with(
        puzzle_state=player_metrics,
        theme="mystery", # Default theme from create_game_session
        location="mansion", # Default location from create_game_session
        overall_difficulty="medium",
        narrative_archetype=None, # Default narrative_archetype
    )

    # Verify GameSession was updated in the database
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["difficulty"] == "easier" # Updated difficulty
    assert get_data["puzzle_state"]["difficulty_adjustment_parameters"] == {"complexity": "low"}
