import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Assuming 'app' is the Flask application instance where session is attached
# For unit tests, we'll mock the session and GameSession model interaction
# We need to import the functions from game_logic
from ai-escape-app.services.game_logic import (
    create_game_session, get_game_session, update_game_session, 
    update_player_inventory, solve_puzzle, player_action, get_contextual_options,
    use_item
)
from ai-escape-app.models import GameSession, Base
from ai-escape-app.data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS
from ai-escape-app.services.ai_service import evaluate_and_adapt_puzzle, generate_room_description

# Mock SQLAlchemy Session and GameSession for testing
@pytest.fixture
def mock_db_session():
    session = MagicMock(spec=Session)
    # Configure mock session to return specific GameSession objects for queries
    session.query.return_value.filter.return_value.first.return_value = None
    yield session

@pytest.fixture
def mock_game_session():
    # A realistic mock of GameSession with JSON fields initialized
    gs = GameSession(
        id=1,
        player_id="test_player",
        current_room="forgotten_library_entrance",
        current_room_description="A test room.",
        inventory=[],
        game_history=[],
        narrative_state={},
        puzzle_state={},
        theme="forgotten_library",
        location="forgotten_library_entrance",
        difficulty="medium",
        start_time=datetime.now(timezone.utc),
        last_updated=datetime.now(timezone.utc)
    )
    # Ensure JSON fields are mutable during test
    gs.inventory = []
    gs.game_history = []
    gs.narrative_state = {}
    gs.puzzle_state = {}
    return gs


@pytest.fixture(autouse=True)
def mock_ai_service():
    """Mocks the AI service functions to return predictable results."""
    with patch('ai-escape-app.services.game_logic.evaluate_and_adapt_puzzle') as mock_eval_puzzle, \
         patch('ai-escape-app.services.game_logic.generate_room_description') as mock_gen_room_desc:
        
        # Default mock for generate_room_description
        mock_gen_room_desc.return_value = "A dynamically generated room description."

        # Default mock for evaluate_and_adapt_puzzle
        # This can be overridden in specific tests
        mock_eval_puzzle.return_value = {
            "is_correct": False,
            "feedback": "That didn't seem to work.",
            "puzzle_status": "unsolved",
            "items_found": [],
            "game_state_changes": {},
            "puzzle_progress": {}
        }
        yield mock_eval_puzzle, mock_gen_room_desc


class TestGameLogic:

    def test_create_game_session(self, mock_db_session, mock_game_session, mock_ai_service):
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.return_value = None

        # Configure the mock to return the mock_game_session when a new session is created
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session

        session = create_game_session(mock_db_session, "test_player", "forgotten_library", "forgotten_library_entrance", "medium")
        
        assert session is not None
        assert session.player_id == "test_player"
        assert session.current_room == "forgotten_library_entrance"
        assert session.theme == "forgotten_library"
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
        mock_ai_service[1].assert_called_once() # generate_room_description should be called


    def test_update_player_inventory_add(self, mock_db_session, mock_game_session):
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        updated_session = update_player_inventory(mock_db_session, 1, "old_key", "add")
        assert "old_key" in updated_session.inventory
        mock_db_session.commit.assert_called_once()

    def test_update_player_inventory_remove(self, mock_db_session, mock_game_session):
        mock_game_session.inventory = ["old_key"]
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        updated_session = update_player_inventory(mock_db_session, 1, "old_key", "remove")
        assert "old_key" not in updated_session.inventory
        mock_db_session.commit.assert_called_once()

    def test_player_action_pick_up_item(self, mock_db_session, mock_game_session, mock_ai_service):
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        
        # Ensure ROOM_DATA has the item
        ROOM_DATA["forgotten_library"]["rooms"]["forgotten_library_entrance"]["items"] = ["old_key"]

        is_successful, message, updated_session, ai_eval = player_action(mock_db_session, 1, "Pick up Old Key")
        
        assert is_successful is True
        assert "old_key" in updated_session.inventory
        assert message == "You picked up the old key."
        assert ai_eval["action_type"] == "pick_up"
        assert ai_eval["item_picked_up"] == "old_key"
        mock_db_session.commit.call_count >= 1 # Called by update_player_inventory

    def test_player_action_inspect_interactable(self, mock_db_session, mock_game_session, mock_ai_service):
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        
        # Setup interactable in ROOM_DATA
        ROOM_DATA["forgotten_library"]["rooms"]["forgotten_library_entrance"]["interactables"] = {
            "bookshelf": {"name": "Bookshelf", "description": "A bookshelf.", "actions": ["inspect"]}
        }
        
        # Configure AI mock for inspection
        mock_ai_service[0].return_value = {
            "is_correct": True,
            "feedback": "The bookshelf reveals a hidden compartment!",
            "puzzle_status": "unsolved",
            "items_found": ["hidden_note"],
            "game_state_changes": {},
            "puzzle_progress": {"bookshelf_inspected": True}
        }

        is_successful, message, updated_session, ai_eval = player_action(mock_db_session, 1, "Inspect Bookshelf")

        assert is_successful is True
        assert "The bookshelf reveals a hidden compartment!" in message
        assert "hidden_note" in updated_session.inventory
        assert updated_session.puzzle_state["bookshelf"]["puzzle_progress"]["bookshelf_inspected"] is True
        mock_ai_service[0].assert_called_once()
        mock_db_session.commit.call_count >= 1

    def test_player_action_use_item_on_interactable(self, mock_db_session, mock_game_session, mock_ai_service):
        mock_game_session.inventory = ["old_key"]
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        
        # Setup interactable in ROOM_DATA
        ROOM_DATA["forgotten_library"]["rooms"]["forgotten_library_study"]["interactables"] = {
            "desk_puzzle": {"name": "Intricate Desk", "description": "A desk.", "actions": ["unlock"]}
        }
        # Configure AI mock for using key on desk
        mock_ai_service[0].return_value = {
            "is_correct": True,
            "feedback": "The desk unlocks with a click!",
            "puzzle_status": "solved",
            "items_found": ["hidden_map"],
            "items_consumed": ["old_key"],
            "game_state_changes": {"desk_unlocked": True},
            "puzzle_progress": {}
        }

        # Need to be in the study room for this interaction
        mock_game_session.current_room = "forgotten_library_study"

        is_successful, message, updated_session, ai_eval = player_action(mock_db_session, 1, "Use Old Key on Intricate Desk")

        assert is_successful is True
        assert "The desk unlocks with a click!" in message
        assert "old_key" not in updated_session.inventory # Key consumed
        assert "hidden_map" in updated_session.inventory # New item found
        assert updated_session.narrative_state["desk_unlocked"] is True
        assert updated_session.puzzle_state["desk_puzzle"]["solved"] is True
        mock_ai_service[0].assert_called_once()
        mock_db_session.commit.call_count >= 1

    def test_solve_puzzle_with_ai_evaluation(self, mock_db_session, mock_game_session, mock_ai_service):
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        
        # Setup puzzle in ROOM_DATA
        ROOM_DATA["forgotten_library"]["rooms"]["forgotten_library_study"]["puzzles"] = {
            "desk_puzzle": {"name": "Desk Puzzle", "description": "A locked desk.", "solution": "7"}
        }

        # Configure AI mock for solving desk puzzle
        mock_ai_service[0].return_value = {
            "is_correct": True,
            "feedback": "The desk slides open, revealing a hidden compartment!",
            "puzzle_status": "solved",
            "items_found": ["ancient_scroll"],
            "game_state_changes": {"desk_open": True},
            "puzzle_progress": {"combination_entered": True}
        }

        # Need to be in the study room for this interaction
        mock_game_session.current_room = "forgotten_library_study"

        is_solved, message, updated_session, ai_eval = solve_puzzle(mock_db_session, 1, "desk_puzzle", "7")

        assert is_solved is True
        assert "The desk slides open" in message
        assert "ancient_scroll" in updated_session.inventory
        assert updated_session.narrative_state["desk_open"] is True
        assert updated_session.puzzle_state["desk_puzzle"]["solved"] is True
        assert updated_session.puzzle_state["desk_puzzle"]["puzzle_progress"]["combination_entered"] is True
        mock_ai_service[0].assert_called_once()
        mock_db_session.commit.call_count >= 1

    def test_get_contextual_options(self, mock_db_session, mock_game_session):
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_game_session
        
        # Set up room with items and interactables
        ROOM_DATA["forgotten_library"]["rooms"]["forgotten_library_entrance"]["items"] = ["old_key", "lantern"]
        ROOM_DATA["forgotten_library"]["rooms"]["forgotten_library_entrance"]["interactables"] = {
            "bookshelf": {"name": "Bookshelf", "description": "A bookshelf.", "actions": ["inspect", "push"]}
        }

        options = get_contextual_options(mock_game_session)
        
        assert "Look around the room" in options
        assert "Go North to Forgotten Library Study" in options
        assert "Pick up Old Key" in options
        assert "Pick up Lantern" in options
        assert "Inspect Bookshelf" in options
        assert "Push Bookshelf" in options
        assert "Go back" not in options # No history yet

        mock_game_session.inventory = ["old_key"]
        options_with_item = get_contextual_options(mock_game_session)
        assert "Pick up Old Key" not in options_with_item # Should not show if already picked up
        assert "Use Old Key on Bookshelf" in options_with_item # Should show use option
