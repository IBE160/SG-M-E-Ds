from flask import Blueprint, current_app, jsonify, request, render_template
from datetime import datetime, timezone, timedelta
from services.game_logic import (
    create_game_session,
    get_game_session,
    update_game_session,
    update_player_inventory,
    solve_puzzle,
    get_contextual_options,
    save_game_state, # New import
    load_game_state, # New import
    get_saved_games, # New import
    get_a_hint,
    player_action, # New import
)
from services.settings import get_player_settings, update_player_settings, delete_player_settings # New import
from services.ai_service import generate_narrative, generate_room_description, generate_puzzle, evaluate_and_adapt_puzzle, adjust_difficulty_based_on_performance
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS
from data.game_options import GAME_SETUP_OPTIONS
from data.help_content import HELP_CONTENT # New import
import logging
from data.game_settings import GAME_SETTINGS # New import

HINT_COOLDOWN_SECONDS = 45 # Define hint cooldown duration (e.g., 45 seconds)

bp = Blueprint("main", __name__)


@bp.route("/game_session/<int:session_id>/hint", methods=["GET"])
def get_hint_route(session_id):
    logging.info(f"Received request for a hint for session_id: {session_id}")
    hint, game_session = get_a_hint(current_app.session, session_id)
    if not game_session:
        logging.warning(f"get_hint_route: Game session {session_id} not found.")
        # If get_a_hint returned an error message, it's in 'hint'
        return jsonify({"error": hint}), 404
    
    # After a hint is successfully provided (or cooldown is active), calculate the new status
    hints_remaining = game_session.narrative_state.get("hints_remaining", 0)
    remaining_hint_cooldown = 0
    last_hint_timestamp_str = game_session.narrative_state.get("last_hint_timestamp")
    
    hint_status_display_text = "Click for a hint" # Default status

    if hints_remaining <= 0:
        hint_status_display_text = "No more hints available."
    elif last_hint_timestamp_str:
        last_hint_timestamp = datetime.fromisoformat(last_hint_timestamp_str)
        time_since_last_hint = datetime.now(timezone.utc) - last_hint_timestamp
        if time_since_last_hint < timedelta(seconds=HINT_COOLDOWN_SECONDS):
            remaining_hint_cooldown = int(HINT_COOLDOWN_SECONDS - time_since_last_hint.total_seconds())
            hint_status_display_text = f"Hint on cooldown ({remaining_hint_cooldown}s)" # Dynamic message
    
    logging.info(f"Hint provided for session {session_id}: {hint}")
    return jsonify({
        "hint": hint,
        "hints_remaining": hints_remaining,
        "remaining_hint_cooldown": remaining_hint_cooldown,
        "hint_status_display_text": hint_status_display_text
    }), 200


@bp.route("/game_setup_options", methods=["GET"])
def get_game_setup_options():
    """
    Returns the expanded list of game setup options (themes, locations, puzzle types, difficulty levels).
    """
    return jsonify(GAME_SETUP_OPTIONS), 200

@bp.route("/save_game", methods=["POST"])
def save_game():
    data = request.get_json()
    session_id = data.get("session_id")
    save_name = data.get("save_name")
    logging.info(f"Received request to save game for session_id: {session_id}, save_name: {save_name}")

    if not session_id or not save_name:
        logging.warning("save_game: Missing session_id or save_name.")
        return jsonify({"error": "Session ID and save name are required"}), 400

    saved_game = save_game_state(current_app.session, session_id, save_name)
    if not saved_game:
        logging.error(f"save_game: Game session {session_id} not found or failed to save.")
        return jsonify({"error": "Game session not found or failed to save"}), 404
    
    logging.info(f"Game session {session_id} saved successfully as '{save_name}'.")
    return jsonify(saved_game.to_dict()), 201

@bp.route("/load_game/<int:saved_game_id>", methods=["GET"])
def load_game(saved_game_id):
    logging.info(f"Received request to load game_id: {saved_game_id}")
    loaded_session = load_game_state(current_app.session, saved_game_id)
    if not loaded_session:
        logging.warning(f"load_game: Saved game {saved_game_id} not found or failed to load.")
        return jsonify({"error": "Saved game not found or failed to load"}), 404
    
    logging.info(f"Game loaded successfully for session_id: {loaded_session.id} from saved_game_id: {saved_game_id}.")
    # After loading, we return the details of the updated game session
    return jsonify(loaded_session.to_dict()), 200

@bp.route("/saved_games", methods=["GET"])
def list_saved_games():
    player_id = request.args.get("player_id")
    logging.info(f"Received request to list saved games for player_id: {player_id}")
    if not player_id:
        logging.warning("list_saved_games: Missing player_id query parameter.")
        return jsonify({"error": "Player ID is required as a query parameter"}), 400
    
    saved_games = get_saved_games(current_app.session, player_id)
    logging.info(f"Successfully retrieved {len(saved_games)} saved games for player_id: {player_id}.")
    return jsonify([sg.to_dict() for sg in saved_games]), 200

@bp.route("/help_content", methods=["GET"])
def get_help_content():
    """
    Returns the structured help content for the game.
    """
    return jsonify(HELP_CONTENT), 200

@bp.route("/game_settings", methods=["GET"])
def get_game_settings():
    """
    Returns the structured game settings for the options menu.
    """
    return jsonify(GAME_SETTINGS), 200

@bp.route("/update_options", methods=["POST"])
def update_options():
    data = request.get_json()
    player_id = data.get("player_id")
    new_settings = data.get("settings")

    if not player_id or not new_settings:
        return jsonify({"error": "Player ID and settings are required"}), 400

    updated_settings = update_player_settings(current_app.session, player_id, new_settings)
    if not updated_settings:
        return jsonify({"error": "Failed to update settings"}), 500 # This case should ideally not happen if get_player_settings creates defaults
    
    return jsonify(updated_settings.to_dict()), 200

@bp.route("/player_settings/<player_id>", methods=["GET"])
def get_player_settings_route(player_id):
    player_settings = get_player_settings(current_app.session, player_id)
    return jsonify(player_settings.to_dict()), 200

@bp.route("/player_settings/<player_id>", methods=["DELETE"])
def delete_player_settings_route(player_id):
    success = delete_player_settings(current_app.session, player_id)
    if not success:
        return jsonify({"error": "Player settings not found or failed to delete"}), 404
    return jsonify({"message": f"Settings for {player_id} deleted successfully"}), 200

@bp.route("/api/loading_messages", methods=["GET"])
def get_loading_messages():
    loading_messages = [
        "Reticulating splines...",
        "Generating narrative paradoxes...",
        "Hiding keys in obvious places...",
        "Polishing virtual dust...",
        "Teaching AI to count on its fingers...",
        "Finalizing your impending doom..."
    ]
    return jsonify(loading_messages), 200

@bp.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
    player_id = data.get("player_id")
    theme = data.get("theme")
    location = data.get("location")
    difficulty = data.get("difficulty")

    if not player_id:
        return jsonify({"error": "Player ID is required"}), 400

    new_session, error_message = create_game_session(
        current_app.session, player_id, theme, location, difficulty
    )
    
    if new_session is None:
        return jsonify({"error": error_message}), 400
        
    return jsonify({"session_id": new_session.id}), 201


@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/game/<int:session_id>")
def game_view(session_id):
    # This route now simply renders the game.html template.
    # The game logic and state will be handled by client-side JavaScript
    # interacting with the /game_session API endpoints.
    return render_template("game.html")



@bp.route("/game_session/<int:session_id>", methods=["GET"])
def get_session(session_id):
    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404
    
    contextual_options = get_contextual_options(game_session)

    theme_data = ROOM_DATA.get(game_session.theme)
    if not theme_data:
        return jsonify({"error": "Game theme data not found for session"}), 500

    current_room_info = theme_data["rooms"].get(game_session.current_room)
    room_image = None
    if current_room_info and "image" in current_room_info:
        room_image = f"/static/images/{current_room_info['image']}"

    # Calculate remaining hint cooldown
    hints_remaining = game_session.narrative_state.get("hints_remaining", 0)
    remaining_hint_cooldown = 0
    last_hint_timestamp_str = game_session.narrative_state.get("last_hint_timestamp")
    
    hint_status_display_text = "Click for a hint" # Default status

    if hints_remaining <= 0:
        hint_status_display_text = "No more hints available."
    elif last_hint_timestamp_str:
        last_hint_timestamp = datetime.fromisoformat(last_hint_timestamp_str)
        time_since_last_hint = datetime.now(timezone.utc) - last_hint_timestamp
        if time_since_last_hint < timedelta(seconds=HINT_COOLDOWN_SECONDS):
            remaining_hint_cooldown = int(HINT_COOLDOWN_SECONDS - time_since_last_hint.total_seconds())
            hint_status_display_text = f"Hint on cooldown ({remaining_hint_cooldown}s)" # Dynamic message
    
    # Objective text (hardcoded English fallback if not explicitly set in narrative_state)
    objective_display_text = game_session.narrative_state.get("objective") or "Explore and find clues."

    return jsonify(
        {
            "id": game_session.id,
            "player_id": game_session.player_id,
            "current_room": game_session.current_room,
            "current_room_name": current_room_info.get("name") if current_room_info else game_session.current_room,
            "current_room_description": game_session.current_room_description or (current_room_info.get("description") if current_room_info else ""),
            "current_room_image": room_image,
            "inventory": game_session.inventory,
            "game_history": game_session.game_history,
            "narrative_state": game_session.narrative_state,
            "puzzle_state": game_session.puzzle_state,
            "theme": game_session.theme,
            "location": game_session.location, # This 'location' now stores the specific room ID
            "difficulty": game_session.difficulty,
            "start_time": game_session.start_time.isoformat(),
            "last_updated": game_session.last_updated.isoformat(),
            "contextual_options": contextual_options,
            "hints_remaining": hints_remaining,
            "remaining_hint_cooldown": remaining_hint_cooldown,
            "hint_status_display_text": hint_status_display_text, # Add hardcoded English hint status
            "objective_display_text": objective_display_text, # Add hardcoded English objective text
        }
    )


@bp.route("/game_session/<int:session_id>/move", methods=["POST"])
def move_player(session_id):
    data = request.get_json()
    direction = data.get("direction") # Change new_room to direction

    if not direction:
        return jsonify({"error": "Direction is required"}), 400

    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404
    
    theme_id = game_session.theme
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return jsonify({"error": "Game theme data not found for session"}), 500

    current_room_id = game_session.current_room
    room_info = theme_data["rooms"].get(current_room_id)

    if not room_info:
        return jsonify({"error": "Current room not found in theme data"}), 500

    new_room_id = room_info["exits"].get(direction.lower())

    if not new_room_id:
        return jsonify({"error": f"Cannot move {direction} from {room_info['name']}."}), 400
    
    # Ensure the new_room_id is within the same theme
    if new_room_id not in theme_data["rooms"]:
        return jsonify({"error": "Cannot move to a room outside the current game's theme."}), 400


    # Generate new room description
    new_room_info = theme_data["rooms"].get(new_room_id)
    if not new_room_info:
        return jsonify({"error": "New room not found in theme data"}), 500
        
    room_context = {
        "name": new_room_info.get("name"),
        "exits": list(new_room_info.get("exits", {}).keys()),
        "puzzles": list(new_room_info.get("puzzles", {}).keys()),
        "items": new_room_info.get("items", []),
    }
    
    new_description = generate_room_description(
        theme=game_session.theme,
        location=game_session.location, # Keep this as game_session.location, which stores the current theme's starting room ID
        narrative_state=game_session.narrative_state,
        room_context=room_context,
        current_room_id=new_room_id, # Pass the ID of the new room
    )

    if new_description.startswith("Error:"):
        # Handle error in description generation, maybe fall back to static description
        new_description = new_room_info.get("description", "A mysterious room.")

    game_history = list(game_session.game_history)
    game_history.append(current_room_id) # Append current room to history BEFORE moving

    updated_session = update_game_session(
        current_app.session,
        session_id,
        current_room=new_room_id,
        current_room_description=new_description,
        game_history=game_history, # Pass updated game history
    )

    if not updated_session:
        return jsonify({"error": "Game session not found after update"}), 500 # Should not happen if game_session was found

    # Check for game completion after moving to escape_chamber (theme-specific)
    theme_escape_chamber_id = f"{theme_id}_escape_chamber"
    if updated_session.current_room == theme_escape_chamber_id:
        # Check if all puzzles before the escape chamber are solved
        # This assumes the 'escape_chamber' has no puzzles itself, and escape is triggered
        # by solving all previous puzzles and entering the final room.
        
        # Get all puzzle IDs from the current theme's rooms, excluding the escape chamber itself
        all_puzzle_ids_for_escape = []
        for r_id, r_info in theme_data["rooms"].items():
            if r_id != theme_escape_chamber_id:
                all_puzzle_ids_for_escape.extend(r_info["puzzles"].keys())
        
        all_previous_puzzles_solved = all(
            updated_session.puzzle_state.get(p_id, {}).get("solved", False) for p_id in all_puzzle_ids_for_escape
        )

        if all_previous_puzzles_solved:
            return jsonify({"id": updated_session.id, "current_room": updated_session.current_room, "message": "You escaped!", "game_over": True})


    return jsonify(
        {"id": updated_session.id, "current_room": updated_session.current_room}
    )


@bp.route("/game_session/<int:session_id>/inventory", methods=["POST"])
def handle_inventory(session_id):
    data = request.get_json()
    item = data.get("item")
    action = data.get("action")  # 'add' or 'remove'

    if not item or not action:
        return jsonify({"error": "Item and action are required"}), 400
    if action not in ["add", "remove"]:
        return jsonify({"error": "Invalid action. Must be 'add' or 'remove'"}), 400

    updated_session = update_player_inventory(
        current_app.session, session_id, item, action
    )
    if not updated_session:
        return jsonify({"error": "Game session not found"}), 404
    return jsonify({"id": updated_session.id, "inventory": updated_session.inventory})


@bp.route("/game_session/<int:session_id>/solve_puzzle", methods=["POST"])
def solve_puzzle_route(session_id):
    data = request.get_json()
    logging.info(f"Received request to /solve_puzzle/{session_id} with data: {data}")
    puzzle_id = data.get("puzzle_id")
    solution_attempt = data.get("solution_attempt") # This will now be passed directly

    if not puzzle_id or not solution_attempt:
        logging.warning(f"solve_puzzle_route: Missing puzzle_id or solution_attempt for session {session_id}")
        return jsonify({"error": "Puzzle ID and solution attempt are required"}), 400

    is_solved, message, updated_session, ai_evaluation = solve_puzzle(
        current_app.session, session_id, puzzle_id, solution_attempt # Pass solution_attempt directly
    )

    if updated_session is None: # Game session not found case
        logging.error(f"solve_puzzle_route: Game session {session_id} not found.")
        return jsonify({"error": message}), 404
    
    if "error" in ai_evaluation:
        logging.error(f"AI service failed to evaluate puzzle for session {session_id}. Error: {ai_evaluation['error']}")
    
    logging.info(f"Puzzle solution attempt for session {session_id} processed. Solved: {is_solved}")
    # The AI evaluation will now contain the actual "is_correct" and "feedback"
    return jsonify({"is_solved": is_solved, "message": message, "session_id": updated_session.id, "ai_evaluation": ai_evaluation}), 200

@bp.route("/generate_narrative", methods=["POST"])
def generate_narrative_route():
    data = request.get_json()
    logging.info(f"Received request to /generate_narrative with data: {data}")
    prompt = data.get("prompt")
    narrative_archetype = data.get("narrative_archetype")

    if not prompt:
        logging.warning("generate_narrative_route: Missing prompt.")
        return jsonify({"error": "Prompt is required"}), 400

    narrative = generate_narrative(prompt, narrative_archetype=narrative_archetype)

    if narrative.startswith("Error:"):
        logging.error(f"AI service failed to generate narrative. Error: {narrative}")
        return jsonify({"error": narrative}), 500
    
    logging.info("Successfully generated narrative.")
    return jsonify({"narrative": narrative}), 200

@bp.route("/generate_room_description", methods=["POST"])
def generate_room_description_route():
    data = request.get_json()
    logging.info(f"Received request to /generate_room_description with data: {data}")
    theme = data.get("theme")
    location = data.get("location")
    narrative_state = data.get("narrative_state")
    room_context = data.get("room_context")
    current_room_id = data.get("current_room_id") # New parameter
    narrative_archetype = data.get("narrative_archetype")

    if not all([theme, location, narrative_state, room_context, current_room_id]): # Added current_room_id to check
        logging.warning("generate_room_description_route: Missing required parameters.")
        return jsonify({"error": "Theme, location, narrative_state, room_context, and current_room_id are required"}), 400

    description = generate_room_description(
        theme, location, narrative_state, room_context, current_room_id, narrative_archetype=narrative_archetype
    )

    if description.startswith("Error:"):
        logging.error(f"AI service failed to generate room description. Error: {description}")
        return jsonify({"error": description}), 500

    logging.info(f"Successfully generated room description for room: {current_room_id}")
    return jsonify({"description": description}), 200

@bp.route("/generate_puzzle", methods=["POST"])
def generate_puzzle_route():
    data = request.get_json()
    logging.info(f"Received request to /generate_puzzle with data: {data}")
    puzzle_type = data.get("puzzle_type")
    difficulty = data.get("difficulty")
    theme = data.get("theme")
    location = data.get("location")
    narrative_archetype = data.get("narrative_archetype")
    puzzle_context = data.get("puzzle_context")

    if not all([puzzle_type, difficulty, theme, location]):
        logging.warning("generate_puzzle_route: Missing required parameters.")
        return jsonify({"error": "Puzzle type, difficulty, theme, and location are required"}), 400

    puzzle = generate_puzzle(
        puzzle_type=puzzle_type,
        difficulty=difficulty,
        theme=theme,
        location=location,
        narrative_archetype=narrative_archetype,
        puzzle_context=puzzle_context,
    )

    if "error" in puzzle:
        logging.error(f"AI service failed to generate puzzle. Error: {puzzle['error']}")
        return jsonify({"error": puzzle["error"]}), 500

    logging.info(f"Successfully generated puzzle for theme: {theme}, location: {location}")
    return jsonify(puzzle), 200

@bp.route("/evaluate_puzzle_solution", methods=["POST"])
def evaluate_puzzle_solution_route():
    data = request.get_json()
    logging.info(f"Received request to /evaluate_puzzle_solution with data: {data}")
    puzzle_id = data.get("puzzle_id")
    player_attempt = data.get("player_attempt")
    puzzle_solution = data.get("puzzle_solution")
    current_puzzle_state = data.get("current_puzzle_state")
    theme = data.get("theme") # This is the theme
    location = data.get("location") # This is the room_id
    difficulty = data.get("difficulty")
    narrative_archetype = data.get("narrative_archetype")

    required_params = [puzzle_id, player_attempt, puzzle_solution, current_puzzle_state, theme, location, difficulty]
    if not all(param is not None for param in required_params):
        logging.warning("evaluate_puzzle_solution_route: Missing required parameters.")
        return jsonify({"error": "Missing required parameters for puzzle evaluation"}), 400

    current_puzzle_description = "Unknown puzzle description."
    
    theme_data = ROOM_DATA.get(theme)
    if theme_data:
        room_info = theme_data["rooms"].get(location) # Use location as room_id
        if room_info and puzzle_id in room_info.get("puzzles", {}):
            current_puzzle_description = room_info["puzzles"][puzzle_id]["description"]

    evaluation = evaluate_and_adapt_puzzle(
        puzzle_id=puzzle_id,
        player_attempt=player_attempt,
        puzzle_solution=puzzle_solution,
        current_puzzle_state=current_puzzle_state,
        current_puzzle_description=current_puzzle_description, # Pass the resolved puzzle description
        theme=theme,
        location=location,
        difficulty=difficulty,
        narrative_archetype=narrative_archetype, # Pass optional parameter
    )

    if "error" in evaluation:
        logging.error(f"AI service failed to evaluate puzzle solution. Error: {evaluation['error']}")
        return jsonify({"error": evaluation["error"]}), 500

    logging.info(f"Successfully evaluated puzzle solution for puzzle: {puzzle_id}")
    return jsonify(evaluation), 200

@bp.route("/adjust_difficulty", methods=["POST"])
def adjust_difficulty_route():
    data = request.get_json()
    session_id = data.get("session_id")
    player_performance_metrics = data.get("player_performance_metrics") # This will likely be the puzzle_state

    if not session_id or not player_performance_metrics:
        return jsonify({"error": "Session ID and player performance metrics are required"}), 400

    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404

    # Call AI service to get difficulty adjustment recommendation
    adjustment_recommendation = adjust_difficulty_based_on_performance(
        puzzle_state=player_performance_metrics, # Passing performance metrics as puzzle_state
        theme=game_session.theme,
        location=game_session.location,
        overall_difficulty=game_session.difficulty,
        narrative_archetype=game_session.narrative_archetype,
    )

    if "error" in adjustment_recommendation:
        return jsonify({"error": adjustment_recommendation["error"]}), 500
    
    # Update game session with new difficulty or puzzle parameters if suggested by AI
    # For now, we'll just store the recommendation in the puzzle_state for simplicity,
    # or create a new field for difficulty adjustment.
    # The actual application of these parameters for future puzzle generation
    # will be handled by the generate_puzzle function later.

    # Example of storing recommendation in narrative_state for now
    # This might need a dedicated field in GameSession for 'difficulty_adjustment_parameters'
    # or a more sophisticated way to apply it.
    
    # For now, let's update the difficulty in the GameSession if AI recommends it
    new_difficulty = adjustment_recommendation.get("difficulty_adjustment")
    if new_difficulty and new_difficulty != "no_change":
        # In a real scenario, this would involve a mapping from "easier"/"harder" to actual difficulty levels.
        # For simplicity, we'll just update if the AI returns a valid difficulty string.
        # This will need to be carefully handled to avoid arbitrary string assignments.
        # For now, assuming direct mapping.
        updated_session = update_game_session(
            current_app.session,
            session_id,
            difficulty=new_difficulty # Update the session's difficulty
        )
        if not updated_session:
            return jsonify({"error": "Failed to update game session difficulty"}), 500
    else:
        updated_session = game_session # No difficulty change, use original session
    
    # Also store the suggested puzzle parameters for future use by generate_puzzle
    # This would ideally be in a dedicated field or handled more explicitly.
    # For now, we will add it to puzzle_state for the session to hold.
    new_puzzle_parameters = adjustment_recommendation.get("suggested_puzzle_parameters", {})
    if new_puzzle_parameters:
        updated_puzzle_state = updated_session.puzzle_state.copy()
        updated_puzzle_state["difficulty_adjustment_parameters"] = new_puzzle_parameters
        updated_session = update_game_session(
            current_app.session,
            session_id,
            puzzle_state=updated_puzzle_state
        )
        if not updated_session:
            return jsonify({"error": "Failed to update puzzle state with AI parameters"}), 500

    return jsonify(adjustment_recommendation), 200

@bp.route("/game_session/<int:session_id>/interact", methods=["POST"])
def interact(session_id):
    data = request.get_json()
    selected_option_index = data.get("option_index")
    player_attempt = data.get("player_attempt", "")

    if selected_option_index is None:
        return jsonify({"error": "Option index is required"}), 400

    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404

    options = get_contextual_options(game_session)

    if not (0 <= selected_option_index < len(options)):
        return jsonify({"error": "Invalid option index"}), 400

    chosen_option = options[selected_option_index]
    
    result = {"id": game_session.id, "current_room": game_session.current_room, "contextual_options": options}
    status_code = 200

    theme_id = game_session.theme
    theme_data = ROOM_DATA.get(theme_id)
    if not theme_data:
        return jsonify({"error": "Game theme data not found for session"}), 500

    # Process the chosen option
    if chosen_option == "Look around the room":
        current_room_info = theme_data["rooms"].get(game_session.current_room)
        if not current_room_info:
            return jsonify({"error": "Current room not found in theme data"}), 500
        result["message"] = current_room_info["description"]
    elif chosen_option == "Go back":
        game_history = list(game_session.game_history)
        if len(game_history) > 0:
            previous_room_id = game_history.pop()

            # Ensure previous_room_id is still within the current theme's rooms
            if previous_room_id not in theme_data["rooms"]:
                result["error"] = "Cannot go back to a room outside the current game's theme."
                status_code = 400
            else:
                updated_session = update_game_session(
                    current_app.session, session_id, current_room=previous_room_id, game_history=game_history
                )
                if not updated_session:
                    result["error"] = "Game session not found after update"
                    status_code = 500
                else:
                    # Explicitly re-fetch the session to get the latest puzzle_state
                    updated_session = get_game_session(current_app.session, session_id)
                    if not updated_session: # Should not happen, but for safety
                        return jsonify({"error": "Game session not found after re-fetch"}), 500
                    result["current_room"] = updated_session.current_room
                    result["contextual_options"] = get_contextual_options(updated_session)
        else:
            result["message"] = "You are in the first room and cannot go back."
            status_code = 400
    elif chosen_option.startswith("Go "):
        parts = chosen_option.split(" ")
        direction = parts[1].lower()
        
        current_room_id = game_session.current_room
        room_info = theme_data["rooms"].get(current_room_id)

        if not room_info:
            return jsonify({"error": "Current room not found in theme data"}), 500

        new_room_id = room_info["exits"].get(direction)

        if not new_room_id:
            result["error"] = f"Cannot move {direction} from {room_info['name']}."
            status_code = 400
        else:
            # Ensure the new_room_id is within the same theme
            if new_room_id not in theme_data["rooms"]:
                return jsonify({"error": "Cannot move to a room outside the current game's theme."}), 400

            game_history = list(game_session.game_history)
            game_history.append(current_room_id)

            # Generate new room description
            new_room_info = theme_data["rooms"].get(new_room_id)
            if not new_room_info:
                return jsonify({"error": "New room not found in theme data"}), 500
                
            room_context = {
                "name": new_room_info.get("name"),
                "exits": list(new_room_info.get("exits", {}).keys()),
                "puzzles": list(new_room_info.get("puzzles", {}).keys()),
                "items": new_room_info.get("items", []),
                "interactables": new_room_info.get("interactables", {}),
            }
            
            new_description = generate_room_description(
                theme=game_session.theme,
                scenario_name_for_ai_prompt=new_room_info["name"], # Pass the human-readable name of the new room
                narrative_state=game_session.narrative_state,
                room_context=room_context,
                current_room_id=new_room_id,
            )

            if new_description.startswith("Error:"):
                new_description = new_room_info.get("description", "A mysterious room.")

            updated_session = update_game_session(
                current_app.session,
                session_id,
                current_room=new_room_id,
                current_room_description=new_description,
                game_history=game_history,
            )
            if not updated_session:
                result["error"] = "Game session not found after update"
                status_code = 500
            else:
                updated_session = get_game_session(current_app.session, session_id)
                if not updated_session:
                    return jsonify({"error": "Game session not found after re-fetch"}), 500

                result["current_room"] = updated_session.current_room
                result["contextual_options"] = get_contextual_options(updated_session)
                
                theme_escape_chamber_id = f"{theme_id}_escape_chamber"
                if updated_session.current_room == theme_escape_chamber_id:
                    all_puzzle_ids_for_escape = []
                    for r_id, r_info in theme_data["rooms"].items():
                        if r_id != theme_escape_chamber_id:
                            all_puzzle_ids_for_escape.extend(r_info["puzzles"].keys())
                    
                    all_previous_puzzles_solved = all(
                        updated_session.puzzle_state.get(p_id, {}).get("solved", False) for p_id in all_puzzle_ids_for_escape
                    )

                    if all_previous_puzzles_solved:
                        return jsonify({"id": updated_session.id, "current_room": updated_session.current_room, "message": "You escaped!", "game_over": True})
    else: # This block handles all other interaction types (pick up, inspect, use, solve puzzle implicitly)
        is_successful, message, updated_session, ai_evaluation = player_action(
            current_app.session, session_id, chosen_option, player_attempt
        )
        
        if not updated_session:
            result["error"] = message
            status_code = 404
        elif "error" in ai_evaluation: # General AI evaluation error
            result["error"] = message
            result["ai_evaluation"] = ai_evaluation
            status_code = 500
        else:
            result["is_successful"] = is_successful
            result["message"] = message
            result["ai_evaluation"] = ai_evaluation # Pass AI evaluation to frontend for detailed feedback
            if updated_session:
                result["current_room"] = updated_session.current_room
                result["current_room_name"] = theme_data["rooms"].get(updated_session.current_room).get("name") # Added current_room_name
                result["current_room_description"] = updated_session.current_room_description # Added current_room_description
                result["contextual_options"] = get_contextual_options(updated_session)
                result["inventory"] = updated_session.inventory
                result["narrative_state"] = updated_session.narrative_state
                result["puzzle_state"] = updated_session.puzzle_state # Ensure puzzle state is updated

    return jsonify(result), status_code