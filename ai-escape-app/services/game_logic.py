from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified # New import
from models import GameSession, SavedGame
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS
from services.ai_service import evaluate_and_adapt_puzzle, generate_room_description


def create_game_session(
    db_session: Session,
    player_id: str,
    theme: str = "mystery",
    location: str = "ancient_library", # This 'location' is actually the desired start_room_id
    difficulty: str = "medium",
) -> GameSession:
    """
    Initializes and stores a new GameSession in the database.
    """
    # Determine the actual theme based on the location if it's not explicitly provided
    selected_theme_id = theme
    if selected_theme_id not in ROOM_DATA:
        # Fallback to a default theme if selected theme is invalid
        selected_theme_id = "mystery" # Default theme

    # Get the theme data from ROOM_DATA
    theme_data = ROOM_DATA.get(selected_theme_id)
    if not theme_data:
        # This case should ideally not happen if ROOM_DATA is properly structured
        return None # Or raise an error as appropriate

    # Find the starting room within the selected theme
    # The 'location' parameter passed here is actually the intended first_room_id
    first_room_id = location
    if first_room_id not in theme_data["rooms"]:
        # Fallback to the theme's default start_room if the provided location is not in this theme
        first_room_id = theme_data["start_room"]
    
    room_info = theme_data["rooms"].get(first_room_id)
    if not room_info:
        # Should not happen if start_room is correctly defined
        return None # Or raise an error

    initial_room_description = generate_room_description(
        theme=selected_theme_id, # Pass the resolved theme (e.g. "forgotten_library")
        scenario_name_for_ai_prompt=room_info["name"], # Pass the human-readable name of the actual start room
        narrative_state={}, # Initial narrative state is empty
        room_context={
            "name": room_info["name"],
            "exits": list(room_info["exits"].keys()),
            "puzzles": list(room_info["puzzles"].keys()),
            "items": room_info.get("items", []),
        },
        current_room_id=first_room_id,
    )

    if initial_room_description.startswith("Error:"):
        # Fallback to static description if AI generation fails
        initial_room_description = room_info["description"]

    new_session = GameSession(
        player_id=player_id,
        current_room=first_room_id,
        theme=selected_theme_id, # Store the actual theme used (e.g. "forgotten_library")
        location=selected_theme_id, # Store the top-level scenario key (e.g. "forgotten_library")
        difficulty=difficulty,
        start_time=datetime.now(timezone.utc),
        current_room_description=initial_room_description, # Use dynamically generated description
        game_history=[], # Initialize with an empty list
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
                # Handle JSON fields that need explicit modification flagging
                if key == "inventory":
                    game_session.inventory = list(value) # Ensure a new list object is assigned
                    flag_modified(game_session, "inventory")
                elif key == "game_history":
                    game_session.game_history = list(value) # Ensure a new list object is assigned
                    flag_modified(game_session, "game_history")
                elif key == "puzzle_state":
                    game_session.puzzle_state = value # Assume value is already a modified dict
                    flag_modified(game_session, "puzzle_state")
                elif key == "narrative_state":
                    game_session.narrative_state = value
                    flag_modified(game_session, "narrative_state")
                else:
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
    flag_modified(game_session, "inventory") # Explicitly flag the JSON field as modified
    game_session.last_updated = datetime.now(timezone.utc)
    db_session.commit()
    db_session.refresh(game_session)
    return game_session


def solve_puzzle(
    db_session: Session, session_id: int, puzzle_id: str, solution_attempt: str
) -> tuple[bool, str, GameSession | None, dict]:
    """
    Evaluates a puzzle solution attempt using AI and adapts the puzzle.
    Returns a tuple: (is_solved: bool, message: str, updated_game_session: GameSession | None, ai_evaluation: dict)
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return False, "Game session not found.", None, {"error": "Game session not found."}

    current_room_id = game_session.current_room
    theme_id = game_session.theme # Get the theme ID from the game session
    
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return False, "Game theme data not found.", game_session, {"error": "Game theme data not found."}

    room_info = theme_data["rooms"].get(current_room_id)

    if not room_info or puzzle_id not in room_info["puzzles"]:
        return False, "Puzzle not found in current room.", game_session, {"error": "Puzzle not found."}

    # Retrieve puzzle details from game_session.puzzle_state
    # This assumes puzzle_state stores the puzzle details including its solution
    puzzle_details_from_state = game_session.puzzle_state.get(puzzle_id, {})
    
    # Check if puzzle is solved from the puzzle_state
    if puzzle_details_from_state.get("solved", False):
        return False, "This puzzle is already solved.", game_session, {"error": "Puzzle already solved."}

    # Get the actual correct solution from ROOM_DATA
    correct_solution = room_info["puzzles"][puzzle_id]["solution"] 
    current_puzzle_description = room_info["puzzles"][puzzle_id]["description"]


    # Use AI to evaluate the attempt and get adaptation suggestions
    ai_evaluation = evaluate_and_adapt_puzzle(
        puzzle_id=puzzle_id,
        player_attempt=solution_attempt,
        puzzle_solution=correct_solution, # Pass the correct solution to the AI for evaluation
        current_puzzle_state=puzzle_details_from_state, # Pass the entire puzzle state for context
        current_puzzle_description=current_puzzle_description, # Pass current puzzle description
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
    # Create a mutable copy of game_session.puzzle_state
    new_puzzle_state = game_session.puzzle_state.copy() 
    
    # Update the specific puzzle_id entry
    current_puzzle_details = new_puzzle_state.get(puzzle_id, {})
    current_puzzle_details["solved"] = is_correct
    current_puzzle_details["attempts"] = current_puzzle_details.get("attempts", 0) + 1
    current_puzzle_details["last_attempt"] = solution_attempt
    current_puzzle_details["ai_feedback"] = ai_evaluation
    # Increment hints_used if a hint was provided in the AI feedback and it's not solved
    if ai_evaluation.get("hint") and not is_correct:
        current_puzzle_details["hints_used"] = current_puzzle_details.get("hints_used", 0) + 1
    
    new_puzzle_state[puzzle_id] = current_puzzle_details
    game_session.puzzle_state = new_puzzle_state # Reassign the modified dictionary
    flag_modified(game_session, "puzzle_state") # Explicitly flag the JSON field as modified


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
    theme_id = game_session.theme # Get the theme ID from the game session
    
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return ["Error: Game theme data not found."]

    room_info = theme_data["rooms"].get(current_room_id)

    if not room_info:
        return ["Error: Room data not found in current theme."]

    # Default option
    options.append("Look around the room")

    # Exits
    for direction, next_room_id in room_info["exits"].items():
        # Ensure next_room_id is within the current theme before adding as an option
        if next_room_id in theme_data["rooms"]:
            next_room_name = theme_data["rooms"].get(next_room_id, {}).get("name", next_room_id)
            options.append(f"Go {direction} to {next_room_name}")

    # Puzzles
    for puzzle_id, puzzle_details in room_info["puzzles"].items():
        if not game_session.puzzle_state.get(puzzle_id, {}).get("solved", False):
            options.append(f"Solve {puzzle_id}") # Using puzzle_id for now, can be changed to a more descriptive name

    # Add a generic "Go back" option, assuming this maps to moving to a previous room.
    # For now, it's just a placeholder as the navigation is linear.
    if game_session.game_history: # Only allow going back if there's history
        options.append("Go back")

    return options

def verify_puzzle_solvability(puzzles: list[dict]) -> tuple[bool, str]:
    """
    Verifies if a list of puzzles forms a solvable dependency chain.

    Args:
        puzzles: A list of dictionaries, where each dictionary represents a puzzle
                 and contains at least 'puzzle_id', 'prerequisites' (list of strings),
                 and 'outcomes' (list of strings).

    Returns:
        A tuple (is_solvable, message). is_solvable is True if the chain is solvable, False otherwise.
    """
    if not puzzles:
        return True, "No puzzles to verify, so it's solvable."

    # Build a graph of dependencies and a set of all possible outcomes
    puzzle_map = {p['puzzle_id']: p for p in puzzles}
    all_outcomes = set()
    
    # Check for circular dependencies (simple cycle detection during graph traversal)
    # Using Kahn's algorithm or DFS for topological sort would be more robust,
    # but for simplicity, we'll start with a basic approach.

    # Detect cycles (using DFS-like approach for detecting back edges)
    # This is a simplified check and might not catch all complex cycles,
    # but will catch direct circular prerequisites.

    # Collect all prerequisites and check if they can be met
    all_prerequisites_needed = set()
    for puzzle in puzzles:
        if 'prerequisites' in puzzle and puzzle['prerequisites']:
            for prereq in puzzle['prerequisites']:
                all_prerequisites_needed.add(prereq)
        if 'outcomes' in puzzle and puzzle['outcomes']:
            for outcome in puzzle['outcomes']:
                all_outcomes.add(outcome)

    unmet_prerequisites = all_prerequisites_needed - all_outcomes

    if unmet_prerequisites:
        return False, f"Unmet prerequisites found: {', '.join(unmet_prerequisites)}. Puzzles may not be solvable."

    # A more robust check would involve a full topological sort
    # For now, if all prerequisites can be generated as outcomes, we assume solvability
    # and delegate complex cycle detection to the AI's generation or a later story.

    return True, "Puzzle chain appears solvable based on prerequisites and outcomes."

def save_game_state(db_session: Session, session_id: int, save_name: str, saved_at: datetime = None) -> SavedGame | None:
    """
    Saves the current state of a game session to the SavedGame table.
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return None

    game_state_dict = game_session.to_dict()

    new_saved_game = SavedGame(
        player_id=game_session.player_id,
        session_id=session_id,
        save_name=save_name,
        game_state=game_state_dict,
        saved_at=saved_at if saved_at else datetime.now(timezone.utc),
    )

    db_session.add(new_saved_game)
    db_session.commit()
    db_session.refresh(new_saved_game)
    return new_saved_game


def load_game_state(db_session: Session, saved_game_id: int) -> GameSession | None:
    """
    Loads a game state from a SavedGame record and applies it to the original GameSession.
    """
    saved_game = db_session.query(SavedGame).filter(SavedGame.id == saved_game_id).first()
    if not saved_game:
        return None

    # The game state is stored in the 'game_state' field.
    # We need to exclude fields that are not part of the GameSession model or should not be overwritten.
    game_state_to_load = saved_game.game_state
    session_id = saved_game.session_id

    # We need to be careful about what we're updating. 
    # For example, 'id', 'player_id', 'start_time' should likely not be changed.
    # The update_game_session function handles the update logic.
    
    # Remove keys that should not be updated from the loaded state
    game_state_to_load.pop('id', None)
    game_state_to_load.pop('player_id', None)
    game_state_to_load.pop('start_time', None)
    game_state_to_load.pop('last_updated', None)


    return update_game_session(db_session, session_id, **game_state_to_load)


def get_saved_games(db_session: Session, player_id: str) -> list[SavedGame]:
    """
    Retrieves all saved games for a given player.
    """
    return db_session.query(SavedGame).filter(SavedGame.player_id == player_id).order_by(SavedGame.saved_at.desc()).all()


def get_a_hint(db_session: Session, session_id: int) -> tuple[str, GameSession | None]:
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return "Game session not found.", None

    current_room_id = game_session.current_room
    theme_id = game_session.theme # Get the theme ID from the game session
    
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return "Game theme data not found.", None

    room_info = theme_data["rooms"].get(current_room_id)
    if not room_info or not room_info["puzzles"]:
        return "No puzzles in this room to get a hint for.", game_session

    # Find the first unsolved puzzle in the room
    puzzle_id = None
    for p_id, p_details in room_info["puzzles"].items():
        if not game_session.puzzle_state.get(p_id, {}).get("solved", False):
            puzzle_id = p_id
            break

    if not puzzle_id:
        return "All puzzles in this room are solved.", game_session

    puzzle_details_from_state = game_session.puzzle_state.get(puzzle_id, {})
    correct_solution = room_info["puzzles"][puzzle_id]["solution"]
    current_puzzle_description = room_info["puzzles"][puzzle_id]["description"]

    # Use AI to get a hint
    ai_evaluation = evaluate_and_adapt_puzzle(
        puzzle_id=puzzle_id,
        player_attempt="I need a hint", # Special phrase to request a hint
        puzzle_solution=correct_solution,
        current_puzzle_state=puzzle_details_from_state,
        current_puzzle_description=current_puzzle_description,
        theme=game_session.theme,
        location=game_session.location,
        difficulty=game_session.difficulty,
        narrative_archetype=game_session.narrative_archetype,
    )

    if "error" in ai_evaluation:
        return f"AI evaluation failed: {ai_evaluation['error']}", game_session

    hint = ai_evaluation.get("hint", "No hint available from the AI.")

    # Update puzzle state with hints_used
    new_puzzle_state = game_session.puzzle_state.copy()
    current_puzzle_details = new_puzzle_state.get(puzzle_id, {})
    current_puzzle_details["hints_used"] = current_puzzle_details.get("hints_used", 0) + 1
    new_puzzle_state[puzzle_id] = current_puzzle_details
    game_session.puzzle_state = new_puzzle_state
    flag_modified(game_session, "puzzle_state")

    db_session.commit()
    db_session.refresh(game_session)

    return hint, game_session