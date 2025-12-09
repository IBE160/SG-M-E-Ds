import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, PlayerSettings
from services.settings import get_player_settings, update_player_settings
from data.game_settings import GAME_SETTINGS

@pytest.fixture(scope="function")
def db_session():
    """
    Sets up a SQLite in-memory database for testing PlayerSettings.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

def test_get_player_settings_new_player(db_session: Session):
    """
    Tests that get_player_settings creates default settings for a new player.
    """
    player_id = "new_player_1"
    settings = get_player_settings(db_session, player_id)

    assert settings.player_id == player_id
    assert isinstance(settings.settings, dict)
    assert settings.settings["sound"] == GAME_SETTINGS["sound"]["default"]
    assert settings.settings["music"] == GAME_SETTINGS["music"]["default"]
    assert settings.settings["language"] == GAME_SETTINGS["language"]["default"]

    # Verify it's persisted in the database
    retrieved_settings = db_session.query(PlayerSettings).filter(PlayerSettings.player_id == player_id).first()
    assert retrieved_settings is not None
    assert retrieved_settings.settings["sound"] == GAME_SETTINGS["sound"]["default"]

def test_get_player_settings_existing_player(db_session: Session):
    """
    Tests that get_player_settings retrieves existing settings for a player.
    """
    player_id = "existing_player_1"
    initial_settings = {"sound": 50, "music": 70, "language": "fr"}
    db_session.add(PlayerSettings(player_id=player_id, settings=initial_settings))
    db_session.commit()

    settings = get_player_settings(db_session, player_id)

    assert settings.player_id == player_id
    assert settings.settings["sound"] == 50
    assert settings.settings["language"] == "fr"

def test_update_player_settings_valid_changes(db_session: Session):
    """
    Tests updating player settings with valid values.
    """
    player_id = "player_update_test"
    # Ensure player settings exist (creates defaults)
    get_player_settings(db_session, player_id)

    new_values = {"sound": 75, "music": 40, "language": "es"}
    updated_settings = update_player_settings(db_session, player_id, new_values)

    assert updated_settings is not None
    assert updated_settings.player_id == player_id
    assert updated_settings.settings["sound"] == 75
    assert updated_settings.settings["music"] == 40
    assert updated_settings.settings["language"] == "es"

    # Verify persistence
    retrieved_settings = db_session.query(PlayerSettings).filter(PlayerSettings.player_id == player_id).first()
    assert retrieved_settings.settings["sound"] == 75

def test_update_player_settings_invalid_slider_value(db_session: Session):
    """
    Tests updating player settings with an invalid slider value (out of range).
    """
    player_id = "player_invalid_slider"
    initial_settings = get_player_settings(db_session, player_id).settings # Get defaults

    new_values = {"sound": 150} # Out of range
    updated_settings = update_player_settings(db_session, player_id, new_values)

    assert updated_settings is not None
    # Should not update if invalid
    assert updated_settings.settings["sound"] == initial_settings["sound"] 

def test_update_player_settings_invalid_select_value(db_session: Session):
    """
    Tests updating player settings with an invalid select option.
    """
    player_id = "player_invalid_select"
    initial_settings = get_player_settings(db_session, player_id).settings # Get defaults

    new_values = {"language": "de"} # Not a valid option
    updated_settings = update_player_settings(db_session, player_id, new_values)

    assert updated_settings is not None
    # Should not update if invalid
    assert updated_settings.settings["language"] == initial_settings["language"]

def test_update_player_settings_unknown_setting(db_session: Session):
    """
    Tests that unknown settings are ignored during update.
    """
    player_id = "player_unknown_setting"
    initial_settings = get_player_settings(db_session, player_id).settings.copy()

    new_values = {"unknown_key": "some_value"}
    updated_settings = update_player_settings(db_session, player_id, new_values)

    assert updated_settings is not None
    # Unknown key should not be added to settings
    assert "unknown_key" not in updated_settings.settings
    assert updated_settings.settings == initial_settings # Ensure other settings are untouched
