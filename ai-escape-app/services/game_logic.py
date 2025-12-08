from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import GameSession
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS
from services.ai_service import evaluate_and_adapt_puzzle


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
) -> tuple[bool, str, GameSession | None, dict]: # Added dict for AI evaluation
    """
    Evaluates a puzzle solution attempt using AI and adapts the puzzle.
    Returns a tuple: (is_solved: bool, message: str, updated_game_session: GameSession | None, ai_evaluation: dict)
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return False, "Game session not found.", None, {"error": "Game session not found."}

    current_room_id = game_session.current_room
    room_info = ROOM_DATA.get(current_room_id)

    if not room_info or puzzle_id not in room_info["puzzles"]:
        return False, "Puzzle not found in current room.", game_session, {"error": "Puzzle not found."}

    puzzle_info = room_info["puzzles"][puzzle_id]
    correct_solution = PUZZLE_SOLUTIONS.get(puzzle_id)

    if game_session.puzzle_state.get(puzzle_id, {}).get("solved", False): # Check if puzzle is solved
        return False, "This puzzle is already solved.", game_session, {"error": "Puzzle already solved."}

    # Use AI to evaluate the attempt and get adaptation suggestions
    ai_evaluation = evaluate_and_adapt_puzzle(
        puzzle_id=puzzle_id,
        player_attempt=solution_attempt,
        puzzle_solution=correct_solution,
        current_puzzle_state=game_session.puzzle_state.get(puzzle_id, {}),
        theme=game_session.theme,
        location=game_session.location,
        difficulty=game_session.difficulty,
        narrative_archetype=game_session.narrative_archetype,
    )

    if "error" in ai_evaluation:
        return False, f"AI evaluation failed: {ai_evaluation['error']}", game_session, ai_evaluation

    is_correct = ai_evaluation.get("is_correct", False)
    feedback_message = ai_evaluation.get("feedback", "No feedback provided by AI.")
    
    # Update puzzle_state with AI evaluation details
    current_puzzle_details = game_session.puzzle_state.get(puzzle_id, {})
    current_puzzle_details["solved"] = is_correct
    current_puzzle_details["attempts"] = current_puzzle_details.get("attempts", 0) + 1
    current_puzzle_details["last_attempt"] = solution_attempt
    current_puzzle_details["ai_feedback"] = ai_evaluation
    
    game_session.puzzle_state = {**game_session.puzzle_state, puzzle_id: current_puzzle_details}

    # Ensure SQLAlchemy detects JSON column modification
    db_session.add(game_session)
    db_session.commit()
    db_session.refresh(game_session)

    if is_correct:
        return True, "Puzzle solved!", game_session, ai_evaluation
    else:
        return False, feedback_message, game_session, ai_evaluation



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
        if not game_session.puzzle_state.get(puzzle_id, {}).get("solved", False):
            options.append(f"Solve {puzzle_id}") # Using puzzle_id for now, can be changed to a more descriptive name

    # Add a generic "Go back" option, assuming this maps to moving to a previous room.
    # For now, it's just a placeholder as the navigation is linear.
    options.append("Go back")

    return options

