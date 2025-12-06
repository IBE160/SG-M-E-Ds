import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, GameSession
from services.game_logic import (
    create_game_session,
    get_game_session,
    update_game_session,
    delete_game_session,
    update_player_inventory,
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
    assert new_session.current_room == "start_room"
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
    assert retrieved_session.current_room == "start_room"

    assert get_game_session(db_session, 999) is None  # Test non-existent session


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
