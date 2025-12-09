import pytest
import json
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, PlayerSettings
from app import create_app
from data.game_settings import GAME_SETTINGS # To verify defaults

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
        app.session = SessionLocal()
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
    Ensures a clean database state for PlayerSettings for each test.
    """
    with app_with_db.app_context():
        app_with_db.session.query(PlayerSettings).delete()
        app_with_db.session.commit()
        yield
        app_with_db.session.rollback()

def test_get_game_settings_route(client):
    """
    Tests the GET /game_settings route to ensure it returns the global GAME_SETTINGS.
    """
    response = client.get("/game_settings")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == GAME_SETTINGS

def test_get_player_settings_route_new_player(client):
    """
    Tests GET /player_settings/<player_id> for a new player, expecting default settings.
    """
    player_id = "new_player_test"
    response = client.get(f"/player_settings/{player_id}")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data["player_id"] == player_id
    assert isinstance(data["settings"], dict)
    assert data["settings"]["sound"] == GAME_SETTINGS["sound"]["default"]
    assert data["settings"]["music"] == GAME_SETTINGS["music"]["default"]
    
    with client.application.app_context():
        settings_in_db = client.application.session.query(PlayerSettings).filter_by(player_id=player_id).first()
        assert settings_in_db is not None
        assert settings_in_db.settings["language"] == GAME_SETTINGS["language"]["default"]

def test_update_options_route(client):
    """
    Tests POST /update_options route to update player settings.
    """
    player_id = "player_for_update"
    # Ensure player has settings in DB (get_player_settings implicitly creates defaults)
    client.get(f"/player_settings/{player_id}")

    new_settings = {"sound": 10, "music": 20, "language": "es"}
    response = client.post(
        "/update_options",
        json={"player_id": player_id, "settings": new_settings}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["player_id"] == player_id
    assert data["settings"]["sound"] == 10
    assert data["settings"]["language"] == "es"

    with client.application.app_context():
        settings_in_db = client.application.session.query(PlayerSettings).filter_by(player_id=player_id).first()
        assert settings_in_db.settings["music"] == 20

def test_update_options_route_invalid_data(client):
    """
    Tests POST /update_options route with missing data.
    """
    response = client.post(
        "/update_options",
        json={"player_id": "some_player"}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "settings are required" in data["error"]

    response = client.post(
        "/update_options",
        json={"settings": {"sound": 50}}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Player ID and settings are required" in data["error"]
