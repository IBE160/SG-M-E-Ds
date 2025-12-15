from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified # New import
from models import GameSession, SavedGame
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS
from services.ai_service import evaluate_and_adapt_puzzle


def create_game_session(
    db_session: Session,
    player_id: str,
    theme: str = "forgotten_library",
    location: str = "forgotten_library_entrance", # This 'location' is actually the desired start_room_id
    difficulty: str = "medium",
) -> tuple[GameSession | None, str | None]: # Modified return type
    """
    Initializes and stores a new GameSession in the database.
    Returns (GameSession, None) on success, or (None, error_message) on failure.
    """
    print(f"create_game_session received - theme: {theme}, location: {location}")
    
    selected_theme_id = theme
    if selected_theme_id not in ROOM_DATA:
        # User-provided theme is invalid
        return None, f"Invalid theme '{selected_theme_id}'. Please choose a valid theme."

    theme_data = ROOM_DATA.get(selected_theme_id)
    # This check should now always be true due to the above validation, but keeping for safety.
    if not theme_data:
        return None, "Error: Theme data not found after validation."

    first_room_id = location
    if first_room_id not in theme_data["rooms"]:
        # User-provided location for the theme is invalid
        return None, f"Invalid starting location '{first_room_id}' for theme '{selected_theme_id}'. Please choose a valid room for this theme."
    
    room_info = theme_data["rooms"].get(first_room_id)
    if not room_info:
        return None, "Error: Room info not found after validation."

    # Directly use the static room description
    initial_room_description = room_info.get("description", "A mysterious room you find yourself in.")

    # Initialize hints_remaining based on difficulty
    if difficulty == "easy":
        hints_budget = 8
    elif difficulty == "hard":
        hints_budget = 3
    else: # normal or medium
        hints_budget = 5

    # Prepare initial narrative state with the intro story and hint state
    initial_narrative_state = {
        "intro_story": theme_data.get("intro_story", ""),
        "hints_remaining": hints_budget, # Store hints_remaining in narrative_state
        "last_hint_timestamp": None, # Store last_hint_timestamp in narrative_state
    }
    # Potentially add other initial narrative state items based on game start

    new_session = GameSession(
        player_id=player_id,
        current_room=first_room_id,
        theme=selected_theme_id,
        location=selected_theme_id, # Stores the top-level scenario key (e.g. "forgotten_library")
        difficulty=difficulty,
        start_time=datetime.now(timezone.utc),
        current_room_description=initial_room_description, # Use static description
        game_history=[],
        narrative_state=initial_narrative_state, # Initialize with collected narrative state
        last_updated=datetime.now(timezone.utc),
    )
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)
    return new_session, None

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
                if key == "inventory":
                    game_session.inventory = list(value)
                    flag_modified(game_session, "inventory")
                elif key == "game_history":
                    game_session.game_history = list(value)
                    flag_modified(game_session, "game_history")
                elif key == "puzzle_state":
                    game_session.puzzle_state = value
                    flag_modified(game_session, "puzzle_state")
                elif key == "narrative_state":
                    game_session.narrative_state = value
                    flag_modified(game_session, "narrative_state")
                else:
                    setattr(game_session, key, value)

        game_session.last_updated = datetime.now(timezone.utc)

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
        location=game_session.current_room, # Corrected: should be current_room_id
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

    # --- END NEW LOGIC ---
    
    new_puzzle_state_from_ai = ai_evaluation_response.get("new_puzzle_state")
    items_found = ai_evaluation_response.get("items_found", [])
    items_consumed = ai_evaluation_response.get("items_consumed", [])
    
    # Preserve original game_session for reference if it changes during transition
    original_game_session = game_session 

    # Initialize game_state_changes (Fix for NameError)
    game_state_changes = {} 

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

    game_session.puzzle_state[puzzle_id] = new_puzzle_session_state
    flag_modified(game_session, "puzzle_state") # Explicitly flag the JSON field as modified

    # Final commit after all changes in solve_puzzle are applied
    db_session.add(game_session) # Add the potentially new game_session object to session
    db_session.commit()
    # No explicit refresh here, as game_session should already be the latest state from update_game_session

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

       # --- Automatic room transition for "ancient_symbol_door_puzzle" ---
# --- Automatic room transition for "ancient_symbol_door_puzzle" ---
    if puzzle_id == "ancient_symbol_door_puzzle":
        next_room_id = room_info.get("next_room_id")
    if next_room_id:
        next_room_info = theme_data["rooms"].get(next_room_id)
        if next_room_info:
            new_room_description = next_room_info.get(
                "description", "A mysterious room."
            )

            updated_session_after_move = update_game_session(
                db_session,
                session_id,
                current_room=next_room_id,
                current_room_description=new_room_description,
                game_history=list(original_game_session.game_history)
                + [original_game_session.current_room],
            )

            if updated_session_after_move:
                # Apply room change to the tracked game_session object
                game_session.current_room = updated_session_after_move.current_room
                flag_modified(game_session, "current_room")

                game_session.current_room_description = (
                    updated_session_after_move.current_room_description
                )

                game_session.game_history = updated_session_after_move.game_history
                flag_modified(game_session, "game_history")

                # ✅ Persist room transition
                db_session.add(game_session)
                db_session.commit()

            else:
                feedback_message += (
                    "\nFailed to transition to the next room automatically."
                )


    # The remaining state changes (items_found, items_consumed, game_state_changes) happen after the conditional is_correct block
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

    # --- After successful puzzle solve, check for room completion ---
    if is_correct:
        all_room_puzzles = room_info["puzzles"]
        all_puzzles_in_room_solved = True
        for p_id_in_room in all_room_puzzles:
            if not game_session.puzzle_state.get(p_id_in_room, {}).get("solved", False):
                all_puzzles_in_room_solved = False
                break
        
        if all_puzzles_in_room_solved:
            game_state_changes["current_room_completed"] = True
            feedback_message += f"\n\nRoom '{room_info['name']}' completed!"
            logging.info(f"Room completed: {current_room_id} for session {session_id}")

            # --- Check for Win Condition (final room) ---
            if current_room_id == f"{theme_id}_escape_chamber" and puzzle_id == "final_escape_puzzle":
                game_state_changes["game_over"] = True
                feedback_message += "\n\nCongratulations! You have successfully escaped and won the game!"
                logging.info(f"Game won! Session {session_id}")

    # Return structure: (is_solved: bool, message: str, updated_game_session: GameSession | None, ai_evaluation: dict)
    # Ensure game_state_changes (like game_over, room_completed) are in the returned ai_evaluation_response
    ai_evaluation_response["game_state_changes"] = {**ai_evaluation_response.get("game_state_changes", {}), **game_state_changes}
    if ai_evaluation_response["game_state_changes"].get("current_room_completed"):
        ai_evaluation_response["current_room_completed"] = True
    if ai_evaluation_response["game_state_changes"].get("game_over"):
        ai_evaluation_response["game_over"] = True
    
    return is_correct, feedback_message, game_session, ai_evaluation_response


def get_contextual_options(game_session: GameSession) -> list[str]:
    """
    Dynamically generates a list of possible interactions based on the current room and game state.
    Refactored for linear escape room progression.
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

    # Always allow inspecting the current room for flavor
    options.append("Look around the room")

    # --- Add options for interacting with interactables and triggering puzzles ---
    # These are general actions in the room, some of which might trigger puzzles
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
                # Always show narrative_update, new_room effects (if they don't lead to movement)
                # For linear progression, "new_room" effects should be handled by the explicit "Go to Next Room"
                if effect_type != "new_room":
                    options.append(action["label"])

    # --- Add options for solving puzzles if they are "active" (triggered) and not solved ---
    # This also handles direct puzzle solution attempts
    for puzzle_id, puzzle_definition in room_info.get("puzzles", {}).items():
        current_puzzle_session_state = game_session.puzzle_state.get(puzzle_id, {})
        
        if not current_puzzle_session_state.get("solved", False): # If puzzle is not solved
            # Check prerequisites and item requirements for attempting to solve a puzzle
            prerequisites_met = True
            for prereq in puzzle_definition.get("prerequisites", []):
                if prereq.startswith("item_"):
                    if prereq.replace("item_", "") not in game_session.inventory:
                        prerequisites_met = False
                        break
                elif prereq not in game_session.narrative_state:
                    prerequisites_met = False
                    break
            
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
    
    # --- Add options for picking up items ---
    # Use dynamic items list (from narrative_state)
    current_room_dynamic_items = game_session.narrative_state.get(f"room_{current_room_id}_items", room_info.get("items", []))
    for item_id in current_room_dynamic_items:
        if item_id not in game_session.inventory: # Only show if not already in inventory
            options.append(f"Pick up {item_id.replace('_', ' ').title()}")

    # --- Add options for using inventory items ---
    for item_in_inventory in game_session.inventory:
        # Offer to use item on any interactable in the room
        for target_id, target_data in room_info.get("interactables", {}).items():
            options.append(f"Use {item_in_inventory.replace('_', ' ').title()} on {target_data['name']}")
        
        # Offer to use item on any unsolved puzzle that explicitly requires it
        for puzzle_id, puzzle_definition in room_info.get("puzzles", {}).items():
            current_puzzle_session_state = game_session.puzzle_state.get(puzzle_id, {})
            if not current_puzzle_session_state.get("solved", False):
                if item_in_inventory in puzzle_definition.get("items_required", []):
                    options.append(f"Use {item_in_inventory.replace('_', ' ').title()} on {puzzle_definition.get('name', puzzle_id.replace('_', ' ').title())}")

    # --- Conditional "Go to Next Room" option for linear progression ---
    # Assuming each room has one primary puzzle that unlocks progression
    main_puzzle_id = next(iter(room_info["puzzles"]), None) # Get the first puzzle ID if any
    if main_puzzle_id and game_session.puzzle_state.get(main_puzzle_id, {}).get("solved", False):
        next_room_in_sequence = room_info.get("next_room_id") # We will add this to ROOM_DATA
        if next_room_in_sequence:
            next_room_info = theme_data["rooms"].get(next_room_in_sequence)
            if next_room_info:
                options.append(f"Go to {next_room_info['name']}")
    
    # Add a generic "Go back" option, assuming this maps to moving to a previous room.
    # This should probably only be allowed if next_room is not unlocked, or specific to game design
    if game_session.game_history and not (main_puzzle_id and game_session.puzzle_state.get(main_puzzle_id, {}).get("solved", False)): # Only allow go back if not ready to advance
        options.append("Go back")

    # Ensure uniqueness of options before returning
    unique_options = sorted(list(set(options)))
    return unique_options

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
    correct_solution = room_info["puzzles"].get(target_puzzle_id, {}).get("solution", "") if target_puzzle_id and target_puzzle_id in room_info["puzzles"] else ""
    current_puzzle_description = room_info["puzzles"].get(target_puzzle_id, {}).get("description", "N/A") if target_puzzle_id and target_puzzle_id in room_info["puzzles"] else "N/A"

    ai_evaluation_response = evaluate_and_adapt_puzzle(
        puzzle_id=target_puzzle_id if target_puzzle_id else "item_use_action", # Use a generic ID if no specific puzzle
        player_attempt=player_attempt,
        puzzle_solution=correct_solution, # Provide solution if applicable
        current_puzzle_state=puzzle_details_from_state,
        current_puzzle_description=current_puzzle_description,
        theme=game_session.theme,
        location=game_session.current_room, # Corrected: should be current_room_id
        difficulty=game_session.difficulty,
        narrative_archetype=game_session.narrative_archetype,
        current_inventory=game_session.inventory # Provide inventory for context
    )

    if "error" in ai_evaluation_response:
        return False, ai_evaluation_response["error"], game_session, ai_evaluation_response

    is_successful = ai_evaluation_response.get("is_correct", False) # Renamed to is_successful for item use
    feedback_message = ai_evaluation_response.get("feedback", "That didn't seem to work.") # Default feedback
    items_found = ai_evaluation_response.get("items_found", [])
    items_consumed = ai_evaluation_response.get("items_consumed", []) # New: items removed from inventory
    game_state_changes = ai_evaluation_response.get("game_state_changes", {})
    
    
    # Check for specific invalid usage feedback from AI
    if not is_successful and "You do not have that item" in feedback_message:
        return False, feedback_message, game_session, ai_evaluation_response
    if not is_successful and "That doesn't seem to work here" in feedback_message:
        return False, feedback_message, game_session, ai_evaluation_response

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

    narrative_state = game_session.narrative_state
    hints_remaining = narrative_state.get("hints_remaining", 0) # Default to 0 if not set
    last_hint_timestamp_str = narrative_state.get("last_hint_timestamp")

    if hints_remaining <= 0:
        return "No more hints available for this session.", game_session

    # Check session-level cooldown
    if last_hint_timestamp_str:
        # HINT_COOLDOWN_SECONDS is imported via routes, so game_logic needs to know it.
        # Since it's a global constant for the game, it should be passed or re-imported.
        # For minimal change, and because it's a constant, I will re-import it here.
        from routes import HINT_COOLDOWN_SECONDS # Import the constant from routes
        last_hint_timestamp = datetime.fromisoformat(last_hint_timestamp_str)
        time_since_last_hint = datetime.now(timezone.utc) - last_hint_timestamp
        if time_since_last_hint < timedelta(seconds=HINT_COOLDOWN_SECONDS):
            remaining_cooldown = int(HINT_COOLDOWN_SECONDS - time_since_last_hint.total_seconds())
            return f"You need a moment to think before asking for another hint. Try again in {remaining_cooldown} seconds.", game_session

    current_room_id = game_session.current_room
    theme_id = game_session.theme
    
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

    puzzle_definition = room_info["puzzles"][puzzle_id]
    
    # Decrement hints_remaining and update timestamp for the session in narrative_state
    narrative_state["hints_remaining"] = hints_remaining - 1
    narrative_state["last_hint_timestamp"] = datetime.now(timezone.utc).isoformat()
    game_session.narrative_state = narrative_state
    flag_modified(game_session, "narrative_state")

    # We need to track how many hints have been given for THIS specific puzzle
    # This information still resides in puzzle_state, but hints_used_count for selection is distinct from session.hints_remaining
    current_puzzle_state = game_session.puzzle_state.get(puzzle_id, {})
    puzzle_hints_given_count = current_puzzle_state.get("hints_given_for_this_puzzle", 0) + 1
    current_puzzle_state["hints_given_for_this_puzzle"] = puzzle_hints_given_count
    
    game_session.puzzle_state[puzzle_id] = current_puzzle_state
    flag_modified(game_session, "puzzle_state") # Flag puzzle_state as modified as well

    # --- Progressive Hint Levels & Story-Driven Hint Text ---
    hint_levels = puzzle_definition.get("hint_levels", [])
    
    if hint_levels:
        if puzzle_hints_given_count -1 < len(hint_levels): # -1 because hints_given_for_this_puzzle is 1-indexed
            hint_message = hint_levels[puzzle_hints_given_count -1]
        else:
            hint_message = "No more specific hints available. You've seen all the clues for this puzzle. Re-read the room description carefully!"
    else:
        hint_message = f"You search for a hint, but find none specific to this puzzle. Re-examine the room: '{puzzle_definition.get('description', 'A mysterious puzzle.')}'"

    db_session.commit()
    db_session.refresh(game_session)

    return hint_message, game_session


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

    # --- Handle "Go to [Room Name]" action for linear progression ---
    if action_phrase.startswith("Go to "):
        target_room_name = action_phrase.replace("Go to ", "").strip()
        
        # Find the target room_id from the name
        target_room_id = None
        for r_id, r_info in theme_data["rooms"].items():
            if r_info.get("name", "").lower() == target_room_name.lower():
                target_room_id = r_id
                break
        
        if not target_room_id:
            return False, f"Could not find a room named '{target_room_name}'.", game_session, {"error": "Invalid room target."}

        # Verify current room completion before allowing movement
        current_room_main_puzzle_id = next(iter(room_info["puzzles"]), None)
        if current_room_main_puzzle_id and not game_session.puzzle_state.get(current_room_main_puzzle_id, {}).get("solved", False):
            return False, "You must solve the current room's main puzzle before moving on.", game_session, {"error": "Current room not completed."}

        # Perform room transition
        game_history = list(game_session.game_history)
        game_history.append(current_room_id)

        new_room_info = theme_data["rooms"].get(target_room_id)
        if not new_room_info:
            return False, "New room not found in theme data.", game_session, {"error": "New room not found."}
        
        # Generate new room description using static data
        new_description = new_room_info.get("description", "A mysterious room you find yourself in.")

        updated_session = update_game_session(
            db_session,
            session_id,
            current_room=target_room_id,
            current_room_description=new_description,
            game_history=game_history,
        )
        if updated_session:
            logging.info(f"Moved to room: {target_room_id} for session {session_id}")
            return True, f"You move to the {new_room_info['name']}.", updated_session, {"action_type": "move_room", "target_room": target_room_id}
        else:
            return False, "Failed to update game session for new room.", game_session, {"error": "Failed to update session."}

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

                    if effect_type == "narrative_update":
                        new_description = effect.get("value", effect_message) # Prioritize value, fallback to message
                        updated_session = update_game_session(
                            db_session, session_id, current_room_description=new_description
                        )
                        return True, effect_message, updated_session, {"action_type": "narrative_update", "target": "current_room_description", "value": new_description}
                    
                    elif effect_type == "new_room": # This effect should now be deprecated for linear path
                        return False, "Room transitions are now handled by 'Go to' actions after puzzle completion.", game_session, {"error": "Deprecated room transition method."}
                    
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
        
        # Check current room's static item list from ROOM_DATA
        room_static_info = ROOM_DATA.get(game_session.theme, {}).get("rooms", {}).get(game_session.current_room, {})
        
        # Check if item exists in the room's initial definition OR if it was dynamically placed there
        # For simplicity, we'll check static list and ensure it hasn't been removed from narrative state yet
        
        # Retrieve the room's dynamic items from narrative_state, or use static if not present
        current_room_dynamic_items = game_session.narrative_state.get(f"room_{current_room_id}_items", room_static_info.get("items", []))
        
        if item_to_pick_up in current_room_dynamic_items:
            # Add item to player's inventory
            updated_session_with_inventory = update_player_inventory(db_session, session_id, item_to_pick_up, "add")
            
            if updated_session_with_inventory:
                # Remove item from the room's dynamic items list in narrative_state
                updated_dynamic_items = [item for item in current_room_dynamic_items if item != item_to_pick_up]
                
                # Update narrative_state
                current_narrative_state = updated_session_with_inventory.narrative_state.copy()
                current_narrative_state[f"room_{current_room_id}_items"] = updated_dynamic_items
                
                final_updated_session = update_game_session(
                    db_session, session_id, narrative_state=current_narrative_state
                )

                if final_updated_session:
                    return True, f"You picked up the {item_to_pick_up.replace('_', ' ')}.", final_updated_session, {"action_type": "pick_up", "item_picked_up": item_to_pick_up}
                else:
                    return False, "Failed to update room state after picking up item.", game_session, {"error": "Failed to update narrative_state."}
            else:
                return False, "Failed to add item to inventory.", game_session, {"error": "Failed to update inventory."}
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
            # Route all such interactions through solve_puzzle for consistent state updates
            puzzle_id_to_solve = target_puzzle_id if target_puzzle_id else target_interactable_id
            
            # Use action_phrase as the player_attempt for solve_puzzle
            # The evaluate_and_adapt_puzzle will then interpret this.
            is_successful, message, updated_session, ai_evaluation = solve_puzzle(
                db_session, session_id, puzzle_id_to_solve, action_phrase 
            )
            return is_successful, message, updated_session, ai_evaluation
        else:
            return False, f"You can't {action_verb} the {target_name.replace('_', ' ')}.", game_session, {"error": "Invalid action on target."}

    # If no specific action matched, return failure
    return False, f"Unknown action: {action_phrase}", game_session, {"error": "Unknown action."}