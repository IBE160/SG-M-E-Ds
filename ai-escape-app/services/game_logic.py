from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified # New import
from models import GameSession, SavedGame
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS
from services.ai_service import evaluate_and_adapt_puzzle, generate_room_description


def create_game_session(
    db_session: Session,
    player_id: str,
    theme: str = "forgotten_library",
    location: str = "forgotten_library_entrance", # This 'location' is actually the desired start_room_id
    difficulty: str = "medium",
) -> GameSession:
    """
    Initializes and stores a new GameSession in the database.
    """
    print(f"create_game_session received - theme: {theme}, location: {location}")
    # Determine the actual theme based on the location if it's not explicitly provided
    selected_theme_id = theme
    print(f"  selected_theme_id (after initial assignment): {selected_theme_id}")
    if selected_theme_id not in ROOM_DATA:
        # Fallback to a default theme if selected theme is invalid
        print(f"  Warning: Invalid theme '{selected_theme_id}'. Falling back to 'mystery'.")
        selected_theme_id = "mystery" # Default theme

    # Get the theme data from ROOM_DATA
    theme_data = ROOM_DATA.get(selected_theme_id)
    print(f"  theme_data (from ROOM_DATA.get): {theme_data is not None}")
    if not theme_data:
        # This case should ideally not happen if ROOM_DATA is properly structured
        return None # Or raise an error as appropriate

    # Find the starting room within the selected theme
    # The 'location' parameter passed here is actually the intended first_room_id
    first_room_id = location
    print(f"  first_room_id (after initial assignment from location): {first_room_id}")
    if first_room_id not in theme_data["rooms"]:
        # Fallback to the theme's default start_room if the provided location is not in this theme
        print(f"  Warning: Room '{first_room_id}' not found in theme's rooms. Falling back to theme's start_room: {theme_data['start_room']}.")
        first_room_id = theme_data["start_room"]
    
    room_info = theme_data["rooms"].get(first_room_id)
    if not room_info:
        # Should not happen if start_room is correctly defined
        return None # Or raise an error

    initial_room_description = generate_room_description(
        theme=selected_theme_id, # Pass the resolved theme (e.g. "forgotten_library")
        scenario_name_for_ai_prompt=room_info["name"], # Pass the human-readable name of the actual start room
        narrative_state={"intro_story": theme_data.get("intro_story", "")}, # Initialize with intro story
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
        narrative_state={"intro_story": theme_data.get("intro_story", "")}, # Ensure narrative_state is initialized with intro_story
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
    db_session: Session, session_id: int, puzzle_id: str, player_attempt: str = ""
) -> tuple[bool, str, GameSession | None, dict]:
    """
    Evaluates a puzzle solution attempt using AI and adapts the puzzle.
    Handles puzzle prerequisites, outcomes, and dynamic state updates.
    Returns a tuple: (is_successful: bool, message: str, updated_game_session: GameSession | None, ai_evaluation: dict)
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return False, "Game session not found.", None, {"error": "Game session not found."}

    current_room_id = game_session.current_room
    theme_id = game_session.theme
    
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return False, "Game theme data not found.", game_session, {"error": "Game theme data not found."}

    room_info = theme_data["rooms"].get(current_room_id)

    if not room_info or puzzle_id not in room_info["puzzles"]:
        return False, "Puzzle not found in current room.", game_session, {"error": "Puzzle not found."}

    # Get the full puzzle definition from ROOM_DATA
    puzzle_definition = room_info["puzzles"][puzzle_id]
    
    # Get the puzzle's dynamic state from game_session.puzzle_state
    current_puzzle_session_state = game_session.puzzle_state.get(puzzle_id, {})
    
    # --- Check if puzzle is already solved ---
    if current_puzzle_session_state.get("solved", False):
        return True, f"You have already solved the '{puzzle_definition['name']}' puzzle.", game_session, {"action_type": "info", "status": "solved"}

    # --- Handle initial trigger/inspection (empty player_attempt) ---
    if not player_attempt or player_attempt.strip().lower() == "inspect": # "inspect" is a generic AI trigger word, assuming here direct call
        # Return the puzzle's description and current hints/next steps from its session state
        message = puzzle_definition.get("description", "A mysterious puzzle.")
        if current_puzzle_session_state.get("next_step_description"):
            message += f"\n{current_puzzle_session_state['next_step_description']}"
        elif current_puzzle_session_state.get("ai_feedback"):
            message += f"\nAI Hint: {current_puzzle_session_state['ai_feedback'].get('hint', '')}"
        
        # This is not a solve attempt, so return its current state
        return False, message, game_session, {"action_type": "inspect_puzzle", "status": current_puzzle_session_state.get("status", "unsolved")}

    # --- Check Prerequisites ---
    prerequisites = puzzle_definition.get("prerequisites", [])
    if prerequisites:
        for prereq in prerequisites:
            # Prereq could be an item in inventory or a narrative state flag
            if prereq.startswith("item_") and prereq.replace("item_", "") not in game_session.inventory:
                return False, f"You need to find the '{prereq.replace('item_', '').replace('_', ' ')}' before attempting this.", game_session, {"error": f"Prerequisite '{prereq}' not met."}
            elif prereq not in game_session.narrative_state: # Simple check for narrative flags
                return False, f"You need to achieve '{prereq.replace('_', ' ')}' before attempting this.", game_session, {"error": f"Prerequisite '{prereq}' not met."}

    # --- Check Items Required ---
    items_required = puzzle_definition.get("items_required", [])
    if items_required:
        for required_item in items_required:
            if required_item not in game_session.inventory:
                return False, f"You need the '{required_item.replace('_', ' ')}' to solve this puzzle.", game_session, {"error": f"Item '{required_item}' not found in inventory."}

    # Get the actual correct solution from ROOM_DATA
    correct_solution = puzzle_definition["solution"] 
    current_puzzle_description_for_ai = puzzle_definition["description"]

    # Use AI to evaluate the attempt and get adaptation suggestions
    ai_evaluation_response = evaluate_and_adapt_puzzle(
        puzzle_id=puzzle_id,
        player_attempt=player_attempt,
        puzzle_solution=correct_solution,
        current_puzzle_state=current_puzzle_session_state,
        current_puzzle_description=current_puzzle_description_for_ai,
        theme=game_session.theme,
        location=game_session.location,
        difficulty=puzzle_definition.get("difficulty", "medium"), # Use puzzle's specific difficulty
        narrative_archetype=game_session.narrative_archetype,
        current_inventory=game_session.inventory # Provide inventory for context
    )

    if "error" in ai_evaluation_response:
        return False, ai_evaluation_response["error"], game_session, ai_evaluation_response

    is_correct = ai_evaluation_response.get("is_correct", False)
    feedback_message = ai_evaluation_response.get("feedback", "No feedback provided by AI.")
    hint_message = ai_evaluation_response.get("hint")
    puzzle_status = ai_evaluation_response.get("puzzle_status", "unsolved")
    
    new_puzzle_state_from_ai = ai_evaluation_response.get("new_puzzle_state")
    items_found = ai_evaluation_response.get("items_found", [])
    items_consumed = ai_evaluation_response.get("items_consumed", [])
    game_state_changes = ai_evaluation_response.get("game_state_changes", {})
    puzzle_progress = ai_evaluation_response.get("puzzle_progress", {})
    
    # --- Update puzzle_state with AI evaluation details ---
    new_puzzle_session_state = current_puzzle_session_state.copy() 
    
    # Always increment attempts for a solve attempt
    new_puzzle_session_state["attempts"] = new_puzzle_session_state.get("attempts", 0) + 1
    new_puzzle_session_state["last_attempt"] = player_attempt
    new_puzzle_session_state["ai_feedback"] = ai_evaluation_response # Store full AI feedback
    
    if is_correct:
        new_puzzle_session_state["solved"] = True
        new_puzzle_session_state["status"] = "solved"
    else:
        new_puzzle_session_state["status"] = puzzle_status # Use AI's suggested status if not solved
    
    if hint_message: # If a hint was provided by AI, track it
        new_puzzle_session_state["hints_used"] = new_puzzle_session_state.get("hints_used", 0) + 1
        new_puzzle_session_state["last_hint"] = hint_message
    
    if new_puzzle_state_from_ai:
        new_puzzle_session_state.update(new_puzzle_state_from_ai)
    if puzzle_progress:
        new_puzzle_session_state.update(puzzle_progress)

    game_session.puzzle_state[puzzle_id] = new_puzzle_session_state
    flag_modified(game_session, "puzzle_state") # Explicitly flag the JSON field as modified

    # --- Apply Game State Changes based on puzzle outcomes ---
    if is_correct:
        # Apply outcomes defined in ROOM_DATA for the solved puzzle
        for outcome in puzzle_definition.get("outcomes", []):
            game_session.narrative_state[outcome] = True # Set outcome flag in narrative_state
        
        # Add items revealed on solve
        for item_to_reveal in puzzle_definition.get("reveal_on_solve", []):
            update_player_inventory(db_session, session_id, item_to_reveal, "add")
            # Re-fetch session to ensure inventory is updated for further logic
            db_session.refresh(game_session)

        # Apply specific triggers (can be used for dynamic room description changes, unlocking exits, etc.)
        if puzzle_definition.get("triggers_event") == "unlock_door_exit":
            # Example: dynamically modify exit if the outcome is to unlock a door
            # This requires more advanced dynamic room data manipulation or flag checking in get_contextual_options
            pass # Will handle this more explicitly in get_contextual_options or a separate event handler


    # Apply any dynamic items/state changes suggested by AI regardless of solve status
    if items_found:
        for item in items_found:
            update_player_inventory(db_session, session_id, item, "add")
            db_session.refresh(game_session)

    if items_consumed:
        for item in items_consumed:
            update_player_inventory(db_session, session_id, item, "remove")
            db_session.refresh(game_session)

    if game_state_changes:
        current_narrative_state = game_session.narrative_state.copy()
        current_narrative_state.update(game_state_changes)
        game_session.narrative_state = current_narrative_state
        flag_modified(game_session, "narrative_state")

    # Ensure SQLAlchemy detects JSON column modification
    db_session.add(game_session)
    db_session.commit()
    db_session.refresh(game_session)

    # Return structure: (is_solved: bool, message: str, updated_game_session: GameSession | None, ai_evaluation: dict)
    # The message should be the feedback from AI.
    return is_correct, feedback_message, game_session, ai_evaluation_response



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

    # Add options for interacting with interactables and triggering puzzles
    for interactable_id, interactable_data in room_info.get("interactables", {}).items():
        for action in interactable_data.get("actions", []):
            effect = action.get("effect", {})
            effect_type = effect.get("type")
            puzzle_id = effect.get("puzzle_id")

            if effect_type == "trigger_puzzle":
                # Only show trigger_puzzle action if the puzzle is not yet solved
                if puzzle_id and not game_session.puzzle_state.get(puzzle_id, {}).get("solved", False):
                    options.append(action["label"])
            else:
                # Always show narrative_update, new_room effects
                options.append(action["label"])

    # Add options for solving puzzles if they are "active" (triggered) and not solved
    for puzzle_id, puzzle_definition in room_info.get("puzzles", {}).items():
        current_puzzle_session_state = game_session.puzzle_state.get(puzzle_id, {})
        
        if not current_puzzle_session_state.get("solved", False): # If puzzle is not solved
            # Check if this puzzle has been "triggered" or is inherently active
            # For simplicity, we assume if it's in room_info["puzzles"] and not solved, it's fair game
            # Or if it has a next_step_description, it's active.

            # Check prerequisites from the puzzle's definition in ROOM_DATA
            prerequisites_met = True
            for prereq in puzzle_definition.get("prerequisites", []):
                if prereq.startswith("item_"):
                    if prereq.replace("item_", "") not in game_session.inventory:
                        prerequisites_met = False
                        break
                elif prereq not in game_session.narrative_state:
                    prerequisites_met = False
                    break
            
            # Check items_required from the puzzle's definition in ROOM_DATA
            items_required_met = True
            for required_item in puzzle_definition.get("items_required", []):
                if required_item not in game_session.inventory:
                    items_required_met = False
                    break

            if prerequisites_met and items_required_met:
                if current_puzzle_session_state.get("next_step_description"):
                    options.append(current_puzzle_session_state["next_step_description"])
                else:
                    options.append(f"Solve {puzzle_definition.get('name', 'Unknown Puzzle')}")
    
    # Add options for picking up items (still relevant)
    for item_id in room_info.get("items", []):
        if item_id not in game_session.inventory:
            options.append(f"Pick up {item_id.replace('_', ' ').title()}")

    # Add options for using inventory items on interactables/puzzles (still relevant)
    for item_in_inventory in game_session.inventory:
        # Offer to use item on any interactable
        for target_id, target_data in room_info.get("interactables", {}).items():
            # Only offer if the interactable itself has an action that supports item use
            # For now, generic "Use item on object"
            options.append(f"Use {item_in_inventory.replace('_', ' ').title()} on {target_data['name']}")
        
        # Offer to use item on any unsolved puzzle that might require it
        for puzzle_id, puzzle_definition in room_info.get("puzzles", {}).items():
            current_puzzle_session_state = game_session.puzzle_state.get(puzzle_id, {})
            if not current_puzzle_session_state.get("solved", False):
                if item_in_inventory in puzzle_definition.get("items_required", []):
                    options.append(f"Use {item_in_inventory.replace('_', ' ').title()} on {puzzle_definition['name']}")

    # Add a generic "Go back" option, assuming this maps to moving to a previous room.
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


def get_saved_games(db_session: Session, player_id: str) -> list[SavedGame]:
    """
    Retrieves all saved games for a given player.
    """
    return db_session.query(SavedGame).filter(SavedGame.player_id == player_id).order_by(SavedGame.saved_at.desc()).all()


def use_item(
    db_session: Session, session_id: int, item_id: str, target_puzzle_id: str = None
) -> tuple[bool, str, GameSession | None, dict]:
    """
    Allows the player to use an item from their inventory, triggering an AI evaluation.
    Returns a tuple: (is_successful: bool, message: str, updated_game_session: GameSession | None, ai_evaluation: dict)
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return False, "Game session not found.", None, {"error": "Game session not found."}

    if item_id not in game_session.inventory:
        return False, f"You don't have '{item_id}' in your inventory.", game_session, {"error": "Item not in inventory."}

    current_room_id = game_session.current_room
    theme_id = game_session.theme
    
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return False, "Game theme data not found.", game_session, {"error": "Game theme data not found."}

    room_info = theme_data["rooms"].get(current_room_id)
    if not room_info:
        return False, "Room data not found.", game_session, {"error": "Room data not found."}

    # Construct player attempt based on whether a target puzzle is specified
    player_attempt = f"Use {item_id}"
    if target_puzzle_id:
        player_attempt = f"Use {item_id} on {target_puzzle_id}"
        # Ensure the target puzzle exists in the current room
        if target_puzzle_id not in room_info["puzzles"]:
            return False, f"Cannot use {item_id} on '{target_puzzle_id}'. It's not here.", game_session, {"error": "Target puzzle not found."}

    # Retrieve puzzle details from game_session.puzzle_state or ROOM_DATA
    # For now, we'll pass the puzzle_id and let AI interpret the "use item" attempt
    # The AI will need to understand the item's properties and the puzzle's requirements
    puzzle_details_from_state = game_session.puzzle_state.get(target_puzzle_id, {}) if target_puzzle_id else {}
    correct_solution = room_info["puzzles"][target_puzzle_id]["solution"] if target_puzzle_id and target_puzzle_id in room_info["puzzles"] else ""
    current_puzzle_description = room_info["puzzles"][target_puzzle_id]["description"] if target_puzzle_id and target_puzzle_id in room_info["puzzles"] else "N/A"

    ai_evaluation_response = evaluate_and_adapt_puzzle(
        puzzle_id=target_puzzle_id if target_puzzle_id else "item_use_action", # Use a generic ID if no specific puzzle
        player_attempt=player_attempt,
        puzzle_solution=correct_solution, # Provide solution if applicable
        current_puzzle_state=puzzle_details_from_state,
        current_puzzle_description=current_puzzle_description,
        theme=game_session.theme,
        location=game_session.location,
        difficulty=game_session.difficulty,
        narrative_archetype=game_session.narrative_archetype,
        current_inventory=game_session.inventory # Provide inventory for context
    )

    if "error" in ai_evaluation_response:
        return False, ai_evaluation_response["error"], game_session, ai_evaluation_response

    is_successful = ai_evaluation_response.get("is_correct", False) # Renamed to is_successful for item use
    feedback_message = ai_evaluation_response.get("feedback", "No feedback provided by AI.")
    items_found = ai_evaluation_response.get("items_found", [])
    items_consumed = ai_evaluation_response.get("items_consumed", []) # New: items removed from inventory
    game_state_changes = ai_evaluation_response.get("game_state_changes", {})
    puzzle_progress = ai_evaluation_response.get("puzzle_progress", {})
    
    # --- Apply Game State Changes ---
    # Update inventory (add new items, remove consumed items)
    for item_to_add in items_found:
        update_player_inventory(db_session, session_id, item_to_add, "add")
    for item_to_remove in items_consumed:
        update_player_inventory(db_session, session_id, item_to_remove, "remove")

    # Re-fetch session to get updated inventory after modification, if needed
    db_session.refresh(game_session)

    if game_state_changes:
        current_narrative_state = game_session.narrative_state.copy()
        current_narrative_state.update(game_state_changes)
        game_session.narrative_state = current_narrative_state
        flag_modified(game_session, "narrative_state")
    
    # Update puzzle state if applicable (e.g., if item use solved a puzzle step)
    if target_puzzle_id and target_puzzle_id in room_info["puzzles"]:
        new_puzzle_state_for_session = game_session.puzzle_state.copy()
        current_puzzle_details = new_puzzle_state_for_session.get(target_puzzle_id, {})

        current_puzzle_details["status"] = ai_evaluation_response.get("puzzle_status", current_puzzle_details.get("status", "unsolved"))
        current_puzzle_details["solved"] = is_successful # If item use directly solves the puzzle
        current_puzzle_details["ai_feedback"] = ai_evaluation_response
        
        if ai_evaluation_response.get("new_puzzle_state"):
            current_puzzle_details.update(ai_evaluation_response["new_puzzle_state"])
        if puzzle_progress:
            current_puzzle_details.update(puzzle_progress)

        new_puzzle_state_for_session[target_puzzle_id] = current_puzzle_details
        game_session.puzzle_state = new_puzzle_state_for_session
        flag_modified(game_session, "puzzle_state")
    # --- End Apply Game State Changes ---

    db_session.add(game_session)
    db_session.commit()
    db_session.refresh(game_session)

    return is_successful, feedback_message, game_session, ai_evaluation_response


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
    ai_evaluation_response = evaluate_and_adapt_puzzle(
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

    if "error" in ai_evaluation_response:
        return f"AI evaluation failed: {ai_evaluation_response['error']}", game_session

    hint = ai_evaluation_response.get("hint", "No hint available from the AI.")

    # Update puzzle state with hints_used
    new_puzzle_state = game_session.puzzle_state.copy()
    current_puzzle_details = new_puzzle_state.get(puzzle_id, {})
    current_puzzle_details["hints_used"] = current_puzzle_details.get("hints_used", 0) + 1
    # Update with new_puzzle_state from AI if provided, in case the AI also adapted the puzzle state
    new_puzzle_state_from_ai = ai_evaluation_response.get("new_puzzle_state")
    if new_puzzle_state_from_ai:
        current_puzzle_details.update(new_puzzle_state_from_ai)
    
    new_puzzle_state[puzzle_id] = current_puzzle_details
    game_session.puzzle_state = new_puzzle_state
    flag_modified(game_session, "puzzle_state")

    db_session.commit()
    db_session.refresh(game_session)

    return hint, game_session


def player_action(
    db_session: Session, session_id: int, action_phrase: str, player_attempt: str = ""
) -> tuple[bool, str, GameSession | None, dict]:
    """
    Processes a player's action phrase, interpreting it and triggering the appropriate game logic.
    Returns (is_successful, message, updated_game_session, ai_evaluation).
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return False, "Game session not found.", None, {"error": "Game session not found."}

    current_room_id = game_session.current_room
    theme_id = game_session.theme
    
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return False, "Game theme data not found.", game_session, {"error": "Game theme data not found."}

    room_info = theme_data["rooms"].get(current_room_id)
    if not room_info:
        return False, "Room data not found.", game_session, {"error": "Room data not found."}

    # --- Handle Structured Interactable Actions (narrative choices) ---
    for interactable_id, interactable_data in room_info.get("interactables", {}).items():
        for action in interactable_data.get("actions", []):
            if action["label"].lower() == action_phrase.lower():
                effect = action.get("effect")
                if effect:
                    effect_type = effect.get("type")
                    effect_target = effect.get("target")
                    effect_value = effect.get("value")
                    effect_message = effect.get("message", "You interact with the environment.")

                    if effect_type == "narrative_update" and effect_target == "current_room_description":
                        updated_session = update_game_session(
                            db_session, session_id, current_room_description=effect_value
                        )
                        return True, effect_message, updated_session, {"action_type": "narrative_update", "target": effect_target, "value": effect_value}
                    
                    elif effect_type == "new_room":
                        new_room_id = effect_target
                        if new_room_id not in theme_data["rooms"]:
                             return False, f"Invalid room target for new_room effect: {new_room_id}", game_session, {"error": "Invalid room target."}

                        game_history = list(game_session.game_history)
                        game_history.append(current_room_id)

                        # Generate new room description for the target room
                        new_room_info = theme_data["rooms"].get(new_room_id)
                        if not new_room_info:
                            return False, "New room not found in theme data.", game_session, {"error": "New room not found."}
                            
                        room_context = {
                            "name": new_room_info.get("name"),
                            "exits": list(new_room_info.get("exits", {}).keys()),
                            "puzzles": list(new_room_info.get("puzzles", {}).keys()),
                            "items": new_room_info.get("items", []),
                            "interactables": new_room_info.get("interactables", {}),
                        }
                        
                        new_description = generate_room_description(
                            theme=game_session.theme,
                            scenario_name_for_ai_prompt=new_room_info["name"],
                            narrative_state=game_session.narrative_state,
                            room_context=room_context,
                            current_room_id=new_room_id,
                        )

                        if new_description.startswith("Error:"):
                            new_description = new_room_info.get("description", "A mysterious room.")

                        updated_session = update_game_session(
                            db_session,
                            session_id,
                            current_room=new_room_id,
                            current_room_description=new_description,
                            game_history=game_history,
                        )
                        if updated_session:
                            return True, effect_message, updated_session, {"action_type": "new_room", "target_room": new_room_id}
                        else:
                            return False, "Failed to update game session for new room.", game_session, {"error": "Failed to update session."}
                    
                    elif effect_type == "trigger_puzzle":
                        puzzle_id = effect.get("puzzle_id")
                        if not puzzle_id:
                            return False, "Missing puzzle_id for trigger_puzzle effect.", game_session, {"error": "Missing puzzle_id."}

                        # Call solve_puzzle. An empty attempt means it's just being triggered/inspected.
                        # The solve_puzzle function will return the puzzle's description as message.
                        is_successful, message, updated_session, ai_evaluation = solve_puzzle(
                            db_session, session_id, puzzle_id, player_attempt # player_attempt might contain input if it's a direct solve action
                        )
                        return is_successful, message, updated_session, ai_evaluation
                    
                    else:
                        # For unhandled structured effects, log and return
                        return False, f"Unhandled structured effect type: {effect_type}", game_session, {"error": "Unhandled effect type."}
                else:
                    return False, "Structured action found without defined effect.", game_session, {"error": "Missing effect."}
    # --- End Structured Interactable Actions ---

    # --- Handle "Pick up" action ---
    if action_phrase.startswith("Pick up "):
        item_to_pick_up = action_phrase.replace("Pick up ", "").strip().lower().replace(' ', '_')
        current_room_info = ROOM_DATA.get(game_session.theme, {}).get("rooms", {}).get(game_session.current_room, {})
        
        if item_to_pick_up in current_room_info.get("items", []):
            updated_session = update_player_inventory(db_session, session_id, item_to_pick_up, "add")
            if updated_session:
                # Remove the item from the room's items list in ROOM_DATA temporarily for this session's context
                # This will require modifying the ROOM_DATA structure if we want persistence beyond current session state
                # For now, we'll rely on the AI not suggesting to pick up an item already picked up
                return True, f"You picked up the {item_to_pick_up.replace('_', ' ')}.", updated_session, {"action_type": "pick_up", "item_picked_up": item_to_pick_up}
            else:
                return False, "Failed to pick up item.", game_session, {"error": "Failed to update inventory."}
        else:
            return False, f"There is no {item_to_pick_up.replace('_', ' ')} to pick up here.", game_session, {"error": "Item not found in room."}

    # --- Handle "Use [item] on [target]" action ---
    if action_phrase.startswith("Use "):
        parts = action_phrase.split(" on ", 1)
        if len(parts) == 2:
            item_part = parts[0].replace("Use ", "").strip()
            target_part = parts[1].strip()
            item_to_use = item_part.lower().replace(' ', '_')
            target_name = target_part.lower().replace(' ', '_') # Convert target to ID format
            
            current_room_info = ROOM_DATA.get(game_session.theme, {}).get("rooms", {}).get(game_session.current_room, {})
            
            target_puzzle_id = None
            target_interactable_id = None

            # Check if target is a puzzle
            for p_id, p_data in current_room_info.get("puzzles", {}).items():
                if p_data.get("name", "").lower().replace(' ', '_') == target_name:
                    target_puzzle_id = p_id
                    break
            
            # Check if target is an interactable
            if not target_puzzle_id:
                for i_id, i_data in current_room_info.get("interactables", {}).items():
                    if i_data.get("name", "").lower().replace(' ', '_') == target_name:
                        target_interactable_id = i_id
                        break
            
            if target_puzzle_id:
                # If the target is a puzzle, use the existing solve_puzzle logic or a specific use_item_on_puzzle
                # For now, we'll route it through use_item which then calls evaluate_and_adapt_puzzle
                return use_item(db_session, session_id, item_to_use, target_puzzle_id)
            elif target_interactable_id:
                # If the target is an interactable, we can also route this through use_item,
                # letting the AI evaluate "Use [item] on [interactable]" as a general attempt.
                return use_item(db_session, session_id, item_to_use, target_interactable_id) # Treat interactable as a puzzle_id for AI evaluation
            else:
                return False, f"Cannot use {item_to_use.replace('_', ' ')} on {target_part}. Target not found.", game_session, {"error": "Target for item use not found."}
        else:
            return False, "Invalid 'Use' command format.", game_session, {"error": "Invalid action format."}

    # --- Handle Interactable actions (e.g., "Inspect Bookshelf", "Open Chest") ---
    # This covers actions like Inspect, Activate, Open, etc., on interactables or even puzzles
    parts = action_phrase.split(" ", 1) # Split only on the first space
    if len(parts) == 2:
        action_verb = parts[0].strip().lower()
        target_name = parts[1].strip().lower().replace(' ', '_')

        current_room_info = ROOM_DATA.get(game_session.theme, {}).get("rooms", {}).get(game_session.current_room, {})
        
        target_interactable_id = None
        target_puzzle_id = None

        # Check if target is an interactable
        for i_id, i_data in current_room_info.get("interactables", {}).items():
            if i_data.get("name", "").lower().replace(' ', '_') == target_name:
                if action_verb in i_data.get("actions", []):
                    target_interactable_id = i_id
                    break
        
        # Check if target is a puzzle
        if not target_interactable_id:
            for p_id, p_data in current_room_info.get("puzzles", {}).items():
                # We need to map generic actions like 'inspect' to a puzzle,
                # or have the AI determine if the action is relevant.
                # For now, if the action verb is 'inspect' and it's a puzzle,
                # we'll treat it as an attempt on the puzzle.
                if p_data.get("name", "").lower().replace(' ', '_') == target_name:
                    target_puzzle_id = p_id
                    break

        if target_interactable_id or target_puzzle_id:
            # Route all such interactions through evaluate_and_adapt_puzzle
            # The AI will interpret the action verb and target.
            puzzle_id_for_ai = target_puzzle_id if target_puzzle_id else target_interactable_id
            
            # Prepare player_attempt for AI
            ai_player_attempt = f"{action_verb} {target_name.replace('_', ' ')}"
            
            # Get puzzle details for AI from ROOM_DATA, if it's a puzzle
            puzzle_solution = ""
            current_puzzle_description = ""
            if target_puzzle_id:
                puzzle_data = current_room_info["puzzles"][target_puzzle_id]
                puzzle_solution = puzzle_data.get("solution", "")
                current_puzzle_description = puzzle_data.get("description", "")
            
            # If it's an interactable, the AI will use its knowledge of interactables/game state
            elif target_interactable_id:
                interactable_data = current_room_info["interactables"][target_interactable_id]
                current_puzzle_description = interactable_data.get("description", "") # Use interactable description for context


            ai_response = evaluate_and_adapt_puzzle(
                puzzle_id=puzzle_id_for_ai,
                player_attempt=ai_player_attempt,
                puzzle_solution=puzzle_solution, # Pass solution if available (for actual puzzles)
                current_puzzle_state=game_session.puzzle_state.get(puzzle_id_for_ai, {}),
                current_puzzle_description=current_puzzle_description,
                theme=game_session.theme,
                location=game_session.location,
                difficulty=game_session.difficulty,
                narrative_archetype=game_session.narrative_archetype,
                current_inventory=game_session.inventory # Provide inventory for context
            )

            if "error" in ai_response:
                return False, ai_response["error"], game_session, ai_response
            
            is_successful = ai_response.get("is_correct", False)
            feedback_message = ai_response.get("feedback", "No feedback provided by AI.")
            items_found = ai_response.get("items_found", [])
            items_consumed = ai_response.get("items_consumed", [])
            game_state_changes = ai_response.get("game_state_changes", {})
            puzzle_progress = ai_response.get("puzzle_progress", {})

            # --- Apply Game State Changes ---
            for item_to_add in items_found:
                update_player_inventory(db_session, session_id, item_to_add, "add")
            for item_to_remove in items_consumed:
                update_player_inventory(db_session, session_id, item_to_remove, "remove")

            db_session.refresh(game_session) # Refresh after inventory changes

            if game_state_changes:
                current_narrative_state = game_session.narrative_state.copy()
                current_narrative_state.update(game_state_changes)
                game_session.narrative_state = current_narrative_state
                flag_modified(game_session, "narrative_state")
            
            if puzzle_progress:
                new_puzzle_state_for_session = game_session.puzzle_state.copy()
                current_puzzle_details = new_puzzle_state_for_session.get(puzzle_id_for_ai, {})
                current_puzzle_details.update(puzzle_progress)
                if ai_response.get("new_puzzle_state"): # Also merge if AI returned full new state
                    current_puzzle_details.update(ai_response["new_puzzle_state"])
                new_puzzle_state_for_session[puzzle_id_for_ai] = current_puzzle_details
                game_session.puzzle_state = new_puzzle_state_for_session
                flag_modified(game_session, "puzzle_state")

            if ai_response.get("puzzle_status") == "solved":
                new_puzzle_state_for_session = game_session.puzzle_state.copy()
                current_puzzle_details = new_puzzle_state_for_session.get(puzzle_id_for_ai, {})
                current_puzzle_details["solved"] = True
                new_puzzle_state_for_session[puzzle_id_for_ai] = current_puzzle_details
                game_session.puzzle_state = new_puzzle_state_for_session
                flag_modified(game_session, "puzzle_state")
            # --- End Apply Game State Changes ---

            db_session.add(game_session)
            db_session.commit()
            db_session.refresh(game_session)
            
            return is_successful, feedback_message, game_session, ai_response
        else:
            return False, f"You can't {action_verb} the {target_name.replace('_', ' ')}.", game_session, {"error": "Invalid action on target."}

    # If no specific action matched, return failure
    return False, f"Unknown action: {action_phrase}", game_session, {"error": "Unknown action."}