import pytest
import json
from app import create_app
from models import Base
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
    assert data["current_room"] == "start_room"
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


def test_move_player(client):
    # First create a session
    start_response = client.post("/start_game", json={"player_id": "test_player_move"})
    session_id = json.loads(start_response.data)["id"]

    response = client.post(
        f"/game_session/{session_id}/move", json={"new_room": "middle_room"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == session_id
    assert data["current_room"] == "middle_room"

    # Verify update persisted
    get_response = client.get(f"/game_session/{session_id}")
    get_data = json.loads(get_response.data)
    assert get_data["current_room"] == "middle_room"

    # Test with non-existent session
    response = client.post("/game_session/9999/move", json={"new_room": "fake_room"})
    assert response.status_code == 404


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
