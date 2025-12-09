import pytest
import json
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, GameSession, SavedGame
from app import create_app  # Assuming create_app is in app.py
from services.game_logic import create_game_session, save_game_state
import time
from datetime import datetime, timedelta

@pytest.fixture(scope="module")
def app_with_db():
    """
    Fixture for a Flask app with an in-memory SQLite database for testing.
    """
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
    with app.app_context():
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        app.session = SessionLocal() # Attach session to app context for routes to use
        yield app
        Base.metadata.drop_all(engine)
        app.session.close()

@pytest.fixture(scope="module")
def client(app_with_db: Flask):
    """
    Fixture for a test client.
    """
    return app_with_db.test_client()

@pytest.fixture(autouse=True)
def setup_each_test(app_with_db: Flask):
    """
    Ensures a clean database state for each test by dropping and recreating tables.
    Also clears saved games.
    """
    with app_with_db.app_context():
        # Clear existing data
        app_with_db.session.query(SavedGame).delete()
        app_with_db.session.query(GameSession).delete()
        app_with_db.session.commit()
        # Ensure session is fresh for each test
        yield
        app_with_db.session.rollback() # Rollback any uncommitted changes

def test_save_game_route(client):
    """
    Tests the POST /save_game route.
    """
    with client.application.app_context():
        game_session = create_game_session(client.application.session, "test_player_save")
        session_id = game_session.id
        save_name = "My Test Save"

    response = client.post(
        "/save_game",
        json={"session_id": session_id, "save_name": save_name}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["save_name"] == save_name
    assert data["session_id"] == session_id
    assert "id" in data

    with client.application.app_context():
        saved_game = client.application.session.query(SavedGame).filter(SavedGame.id == data["id"]).first()
        assert saved_game is not None
        assert saved_game.game_state["current_room"] == game_session.current_room

def test_load_game_route(client):
    """
    Tests the GET /load_game/<int:saved_game_id> route.
    """
    with client.application.app_context():
        game_session = create_game_session(client.application.session, "test_player_load")
        game_session.current_room = "changed_room"
        game_session.inventory = ["item_a", "item_b"]
        client.application.session.commit()
        client.application.session.refresh(game_session)
        saved_game = save_game_state(client.application.session, game_session.id, "Loadable Save")
        saved_game_id = saved_game.id

    # Simulate original session being modified before load
    with client.application.app_context():
        original_session = client.application.session.query(GameSession).filter(GameSession.id == game_session.id).first()
        original_session.current_room = "original_room"
        original_session.inventory = []
        client.application.session.commit()

    response = client.get(f"/load_game/{saved_game_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == game_session.id
    assert data["current_room"] == "changed_room" # Should be loaded from saved state
    assert "item_a" in data["inventory"]

def test_list_saved_games_route(client):
    """
    Tests the GET /saved_games route.
    """
    with client.application.app_context():
        # Create a game session and save a game for player1
        game_session1 = create_game_session(client.application.session, "player1")
        
        # Explicitly set saved_at for reliable ordering
        now = datetime.now()
        save_game_state(client.application.session, game_session1.id, "Player1 Save 1", saved_at=now - timedelta(minutes=1)) # Older
        
        # Save another game for player1
        game_session1.current_room = "second_room_player1"
        client.application.session.commit()
        client.application.session.refresh(game_session1)
        save_game_state(client.application.session, game_session1.id, "Player1 Save 2", saved_at=now) # Newer

        # Create a game session and save a game for player2
        game_session2 = create_game_session(client.application.session, "player2")
        save_game_state(client.application.session, game_session2.id, "Player2 Save 1", saved_at=now - timedelta(seconds=30))

    response = client.get("/saved_games?player_id=player1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["save_name"] == "Player1 Save 2" # Newest first
    assert data[1]["save_name"] == "Player1 Save 1"

    response = client.get("/saved_games?player_id=player2")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["save_name"] == "Player2 Save 1"

    response = client.get("/saved_games?player_id=nonexistent")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0

def test_save_game_non_existent_session_route(client):
    """
    Tests the POST /save_game route with a non-existent session ID.
    """
    response = client.post(
        "/save_game",
        json={"session_id": 9999, "save_name": "Invalid Session Save"}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Game session not found" in data["error"]

def test_load_game_non_existent_saved_game_route(client):
    """
    Tests the GET /load_game/<int:saved_game_id> route with a non-existent saved game ID.
    """
    response = client.get("/load_game/9999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Saved game not found" in data["error"]

