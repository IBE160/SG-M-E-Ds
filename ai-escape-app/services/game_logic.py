from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import GameSession
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS


def create_game_session(
    db_session: Session,
    player_id: str,
    theme: str = "mystery",
    location: str = "mansion",
    difficulty: str = "medium",
) -> GameSession:
    """
    Initializes and stores a new GameSession in the database.
    """
    first_room_id = next(iter(ROOM_DATA))  # Get the first room ID from ROOM_DATA
    new_session = GameSession(
        player_id=player_id,
        current_room=first_room_id, # Set default to the first room in ROOM_DATA
        theme=theme,
        location=location,
        difficulty=difficulty,
        start_time=datetime.now(timezone.utc),
        last_updated=datetime.now(timezone.utc),
    )
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)
    return new_session


def get_game_session(db_session: Session, session_id: int) -> GameSession | None:
    """
    Retrieves a GameSession by its ID.
    """
    return db_session.query(GameSession).filter(GameSession.id == session_id).first()


def update_game_session(
    db_session: Session, session_id: int, **kwargs
) -> GameSession | None:
    """
    Updates an existing GameSession with the given keyword arguments.
    """
    game_session = get_game_session(db_session, session_id)
    if game_session:
        for key, value in kwargs.items():
            if hasattr(game_session, key):
                setattr(game_session, key, value)
        game_session.last_updated = datetime.now(timezone.utc)
        db_session.commit()
        db_session.refresh(game_session)
    return game_session


def delete_game_session(db_session: Session, session_id: int) -> bool:
    """
    Deletes a GameSession by its ID.
    """
    game_session = get_game_session(db_session, session_id)
    if game_session:
        db_session.delete(game_session)
        db_session.commit()
        return True
    return False


def update_player_inventory(
    db_session: Session, session_id: int, item: str, action: str
) -> GameSession | None:
    """
    Adds or removes an item from the player's inventory.
    Action can be 'add' or 'remove'.
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return None

    inventory = list(game_session.inventory)  # Create a mutable copy

    if action == "add":
        if item not in inventory:
            inventory.append(item)
    elif action == "remove":
        if item in inventory:
            inventory.remove(item)
    else:
        # Invalid action, return the session without updating
        return game_session

    game_session.inventory = inventory  # Reassign the modified list
    game_session.last_updated = datetime.now(timezone.utc)
    db_session.commit()
    db_session.refresh(game_session)
    return game_session


def solve_puzzle(
    db_session: Session, session_id: int, puzzle_id: str, solution_attempt: str
) -> tuple[bool, str, GameSession | None]:
    """
    Evaluates a puzzle solution attempt.
    Returns a tuple: (is_solved: bool, message: str, updated_game_session: GameSession | None)
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return False, "Game session not found.", None

    current_room_id = game_session.current_room
    room_info = ROOM_DATA.get(current_room_id)

    if not room_info or puzzle_id not in room_info["puzzles"]:
        return False, "Puzzle not found in current room.", game_session

    puzzle_info = room_info["puzzles"][puzzle_id]
    correct_solution = PUZZLE_SOLUTIONS.get(puzzle_id)

    if game_session.puzzle_state.get(puzzle_id, False): # Check if puzzle is solved in game_session.puzzle_state
        return False, "This puzzle is already solved.", game_session

    if solution_attempt.lower() == correct_solution.lower():
        game_session.puzzle_state = {**game_session.puzzle_state, puzzle_id: True} # Mark puzzle as solved in game state
        
        # Directly update the narrative_state
        current_narrative_state = game_session.narrative_state.copy() # Work on a copy
        
        if current_room_id not in current_narrative_state:
            current_narrative_state[current_room_id] = {"puzzles": {}}
        
        if "puzzles" not in current_narrative_state[current_room_id]:
            current_narrative_state[current_room_id]["puzzles"] = {}
            
        current_narrative_state[current_room_id]["puzzles"][puzzle_id] = {"solved": True} # Only store the solved status
        
        game_session.narrative_state = current_narrative_state # Reassign to trigger SQLAlchemy change detection
        
        # Important: Mark the JSON column as modified
        db_session.add(game_session)
        db_session.commit()
        db_session.refresh(game_session)
        return True, "Puzzle solved!", game_session
    else:
        return False, "Incorrect solution.", game_session


def get_contextual_options(game_session: GameSession) -> list[str]:
    """
    Dynamically generates a list of possible interactions based on the current room and game state.
    """
    options = []
    current_room_id = game_session.current_room
    room_info = ROOM_DATA.get(current_room_id)

    if not room_info:
        return ["Error: Room data not found."]

    # Default option
    options.append("Look around the room")

    # Exits
    for direction, next_room_id in room_info["exits"].items():
        next_room_name = ROOM_DATA.get(next_room_id, {}).get("name", next_room_id)
        options.append(f"Go {direction} to {next_room_name}")

    # Puzzles
    for puzzle_id, puzzle_details in room_info["puzzles"].items():
        if not game_session.puzzle_state.get(puzzle_id, False):
            options.append(f"Solve {puzzle_id}") # Using puzzle_id for now, can be changed to a more descriptive name

    # Add a generic "Go back" option, assuming this maps to moving to a previous room.
    # For now, it's just a placeholder as the navigation is linear.
    options.append("Go back")

    return options

