import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, GameSession, SavedGame
from services.game_logic import create_game_session, save_game_state, load_game_state, get_saved_games
import datetime

@pytest.fixture(scope="function")
def db_session():
    """
    Sets up a SQLite in-memory database for testing.
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

@pytest.fixture
def new_game_session(db_session: Session) -> GameSession:
    """
    Creates and returns a new game session.
    """
    session = create_game_session(db_session, "test_player")
    return session

def test_save_game_state(db_session: Session, new_game_session: GameSession):
    """
    Tests saving the state of a game session.
    """
    session_id = new_game_session.id
    save_name = "My First Save"

    saved_game = save_game_state(db_session, session_id, save_name)

    assert saved_game is not None
    assert saved_game.session_id == session_id
    assert saved_game.save_name == save_name
    assert saved_game.player_id == new_game_session.player_id
    assert saved_game.game_state["id"] == session_id
    assert saved_game.game_state["current_room"] == new_game_session.current_room

    # Verify that the saved game is in the database
    retrieved_saved_game = db_session.query(SavedGame).filter(SavedGame.id == saved_game.id).first()
    assert retrieved_saved_game is not None
    assert retrieved_saved_game.save_name == save_name

def test_load_game_state(db_session: Session, new_game_session: GameSession):
    """
    Tests loading a saved game state.
    """
    original_session_id = new_game_session.id
    save_name = "Load Test Save"

    # Modify the original session before saving
    new_game_session.current_room = "modified_room"
    new_game_session.inventory = ["key", "map"]
    db_session.commit()
    db_session.refresh(new_game_session)

    saved_game = save_game_state(db_session, original_session_id, save_name)
    assert saved_game is not None

    # Now, simulate changes to the live session that should be overwritten by loading
    changed_session = db_session.query(GameSession).filter(GameSession.id == original_session_id).first()
    changed_session.current_room = "another_room"
    changed_session.inventory = ["sword"]
    db_session.commit()
    db_session.refresh(changed_session)

    loaded_session = load_game_state(db_session, saved_game.id)

    assert loaded_session is not None
    assert loaded_session.id == original_session_id
    assert loaded_session.current_room == "modified_room" # Should be restored from saved state
    assert "key" in loaded_session.inventory
    assert "map" in loaded_session.inventory
    assert "sword" not in loaded_session.inventory # Should not contain the overwritten item

def test_get_saved_games(db_session: Session, new_game_session: GameSession):
    """
    Tests retrieving saved games for a specific player.
    """
    player_id = new_game_session.player_id
    
    # Save a game for the test player
    save_game_state(db_session, new_game_session.id, "Test Save 1")
    
    # Create another session and save a game for a different player
    other_player_session = create_game_session(db_session, "other_player")
    save_game_state(db_session, other_player_session.id, "Other Player Save")

    saved_games = get_saved_games(db_session, player_id)

    assert len(saved_games) == 1
    assert saved_games[0].save_name == "Test Save 1"
    assert saved_games[0].player_id == player_id

    # Test for a player with no saved games
    no_games = get_saved_games(db_session, "non_existent_player")
    assert len(no_games) == 0

def test_load_game_state_non_existent_saved_game(db_session: Session):
    """
    Tests loading a non-existent saved game.
    """
    loaded_session = load_game_state(db_session, 9999) # Non-existent ID
    assert loaded_session is None

def test_save_game_state_non_existent_session(db_session: Session):
    """
    Tests saving a non-existent game session.
    """
    saved_game = save_game_state(db_session, 9999, "Invalid Save")
    assert saved_game is None
