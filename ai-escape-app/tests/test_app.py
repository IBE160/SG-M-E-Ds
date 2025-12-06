import pytest
import json
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


def test_get_game_session(client):
    # First create a session
    start_response = client.post("/start_game", json={"player_id": "test_player_get"})
    session_id = json.loads(start_response.data)["id"]

    response = client.get(f"/game_session/{session_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == session_id
    assert data["player_id"] == "test_player_get"

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


def test_solve_puzzle_route_correct_solution(client):
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

    # Verify puzzle state updated
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["puzzle_state"].get("observation_puzzle") is True


def test_solve_puzzle_route_incorrect_solution(client):
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
    assert data["message"] == "Incorrect solution."

    # Verify puzzle state not updated
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["puzzle_state"].get("observation_puzzle") is not True


def test_solve_puzzle_route_puzzle_already_solved(client):
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


def test_game_escape(client):
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

