from flask import Blueprint, current_app, jsonify, request, render_template
from services.game_logic import (
    create_game_session,
    get_game_session,
    update_game_session,
    update_player_inventory,
    solve_puzzle,
    get_contextual_options,
)
from services.ai_service import generate_narrative, generate_room_description, generate_puzzle
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS

bp = Blueprint("main", __name__)


@bp.route("/")
def hello_world():
    return "Hello, World!"


@bp.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
    player_id = data.get("player_id")
    theme = data.get("theme")
    location = data.get("location")
    difficulty = data.get("difficulty")

    if not player_id:
        return jsonify({"error": "Player ID is required"}), 400

    new_session = create_game_session(
        current_app.session, player_id, theme, location, difficulty
    )
    return (
        jsonify(
            {
                "id": new_session.id,
                "player_id": new_session.player_id,
                "current_room": new_session.current_room,
                "inventory": new_session.inventory,
            }
        ),
        201,
    )

@bp.route("/game/<int:session_id>")
def game_view(session_id):
    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return "Game session not found", 404

    current_room_info = ROOM_DATA.get(game_session.current_room)
    room_name = current_room_info.get("name") if current_room_info else "A mysterious place"
    room_description = current_room_info.get("description") if current_room_info else "You find yourself in an unknown room."

    return render_template(
        "game.html",
        session_id=session_id,
        room_name=room_name,
        room_description=room_description,
    )


@bp.route("/game_session/<int:session_id>", methods=["GET"])
def get_session(session_id):
    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404
    
    contextual_options = get_contextual_options(game_session) # New line

    current_room_info = ROOM_DATA.get(game_session.current_room)
    room_image = None
    if current_room_info and "image" in current_room_info:
        room_image = f"/static/images/{current_room_info['image']}"

    return jsonify(
        {
            "id": game_session.id,
            "player_id": game_session.player_id,
            "current_room": game_session.current_room,
            "current_room_name": current_room_info.get("name") if current_room_info else game_session.current_room, # Added room name
            "current_room_description": game_session.current_room_description or (current_room_info.get("description") if current_room_info else ""), # Use dynamic description
            "current_room_image": room_image, # New field
            "inventory": game_session.inventory,
            "game_history": game_session.game_history,
            "narrative_state": game_session.narrative_state,
            "puzzle_state": game_session.puzzle_state,
            "theme": game_session.theme,
            "location": game_session.location,
            "difficulty": game_session.difficulty,
            "start_time": game_session.start_time.isoformat(),
            "last_updated": game_session.last_updated.isoformat(),
            "contextual_options": contextual_options,
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

    current_room_id = game_session.current_room
    room_info = ROOM_DATA.get(current_room_id)

    if not room_info:
        return jsonify({"error": "Current room not found in ROOM_DATA"}), 500

    new_room_id = room_info["exits"].get(direction.lower())

    if not new_room_id:
        return jsonify({"error": f"Cannot move {direction} from {room_info['name']}."}), 400

    # Generate new room description
    new_room_info = ROOM_DATA.get(new_room_id)
    if not new_room_info:
        return jsonify({"error": "New room not found in ROOM_DATA"}), 500
        
    room_context = {
        "name": new_room_info.get("name"),
        "exits": list(new_room_info.get("exits", {}).keys()),
        "puzzles": list(new_room_info.get("puzzles", {}).keys()),
        "items": new_room_info.get("items", []),
    }
    
    new_description = generate_room_description(
        theme=game_session.theme,
        location=game_session.location,
        narrative_state=game_session.narrative_state,
        room_context=room_context,
    )

    if new_description.startswith("Error:"):
        # Handle error in description generation, maybe fall back to static description
        new_description = new_room_info.get("description", "A mysterious room.")

    updated_session = update_game_session(
        current_app.session,
        session_id,
        current_room=new_room_id,
        current_room_description=new_description,
    )

    if not updated_session:
        return jsonify({"error": "Game session not found after update"}), 500 # Should not happen if game_session was found

    # Check for game completion after moving to escape_chamber
    if updated_session.current_room == "escape_chamber":
        # Check if all puzzles before the escape chamber are solved
        # This assumes the 'escape_chamber' has no puzzles itself, and escape is triggered
        # by solving all previous puzzles and entering the final room.
        
        # Get all puzzle IDs from ROOM_DATA excluding those in escape_chamber
        all_puzzle_ids = []
        for r_id, r_info in ROOM_DATA.items():
            if r_id != "escape_chamber":
                all_puzzle_ids.extend(r_info["puzzles"].keys())
        
        all_previous_puzzles_solved = all(
            updated_session.puzzle_state.get(p_id, False) for p_id in all_puzzle_ids
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
    puzzle_id = data.get("puzzle_id")
    solution_attempt = data.get("solution_attempt")

    if not puzzle_id or not solution_attempt:
        return jsonify({"error": "Puzzle ID and solution attempt are required"}), 400

    is_solved, message, updated_session = solve_puzzle(
        current_app.session, session_id, puzzle_id, solution_attempt
    )

    if not updated_session:
        return jsonify({"error": message}), 404 # Session not found case

    return jsonify({"is_solved": is_solved, "message": message, "session_id": updated_session.id})

@bp.route("/generate_narrative", methods=["POST"])
def generate_narrative_route():
    data = request.get_json()
    prompt = data.get("prompt")
    narrative_archetype = data.get("narrative_archetype")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    narrative = generate_narrative(prompt, narrative_archetype=narrative_archetype)

    if narrative.startswith("Error:"):
        return jsonify({"error": narrative}), 500
    
    return jsonify({"narrative": narrative}), 200

@bp.route("/generate_room_description", methods=["POST"])
def generate_room_description_route():
    data = request.get_json()
    theme = data.get("theme")
    location = data.get("location")
    narrative_state = data.get("narrative_state")
    room_context = data.get("room_context")
    narrative_archetype = data.get("narrative_archetype")

    if not all([theme, location, narrative_state, room_context]):
        return jsonify({"error": "Theme, location, narrative_state, and room_context are required"}), 400

    description = generate_room_description(
        theme, location, narrative_state, room_context, narrative_archetype=narrative_archetype
    )

    if description.startswith("Error:"):
        return jsonify({"error": description}), 500

    return jsonify({"description": description}), 200

@bp.route("/generate_puzzle", methods=["POST"])
def generate_puzzle_route():
    data = request.get_json()
    puzzle_type = data.get("puzzle_type")
    difficulty = data.get("difficulty")
    theme = data.get("theme")
    location = data.get("location")
    narrative_archetype = data.get("narrative_archetype")
    puzzle_context = data.get("puzzle_context")

    if not all([puzzle_type, difficulty, theme, location]):
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
        return jsonify({"error": puzzle["error"]}), 500

    return jsonify(puzzle), 200




@bp.route("/game_session/<int:session_id>/interact", methods=["POST"])
def interact(session_id):
    data = request.get_json()
    selected_option_index = data.get("option_index")

    if selected_option_index is None:
        return jsonify({"error": "Option index is required"}), 400

    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404

    options = get_contextual_options(game_session)

    if not (0 <= selected_option_index < len(options)):
        return jsonify({"error": "Invalid option index"}), 400

    chosen_option = options[selected_option_index]
    
    # Placeholder for the result of the action
    result = {"id": game_session.id, "current_room": game_session.current_room, "contextual_options": options}
    status_code = 200

    # Process the chosen option
    if chosen_option == "Look around the room":
        result["message"] = ROOM_DATA[game_session.current_room]["description"]
    elif chosen_option == "Go back":
        game_history = list(game_session.game_history) # Get a mutable copy
        if len(game_history) > 0:
            previous_room_id = game_history.pop()
            updated_session = update_game_session(
                current_app.session, session_id, current_room=previous_room_id, game_history=game_history
            )
            if not updated_session:
                result["error"] = "Game session not found after update"
                status_code = 500
            else:
                result["current_room"] = updated_session.current_room
                result["contextual_options"] = get_contextual_options(updated_session)
        else:
            result["message"] = "You are in the first room and cannot go back."
            status_code = 400 # Indicate that action was not successful
    elif chosen_option.startswith("Go "):
        parts = chosen_option.split(" ")
        direction = parts[1].lower()
        # Re-use move_player logic, but not by calling the route directly to avoid Flask context issues
        # Extract the logic here.
        
        current_room_id = game_session.current_room
        room_info = ROOM_DATA.get(current_room_id)
        new_room_id = room_info["exits"].get(direction)

        if not new_room_id:
            result["error"] = f"Cannot move {direction} from {room_info['name']}."
            status_code = 400
        else:
            # Push current room to game_history before moving
            game_history = list(game_session.game_history) # Get a mutable copy
            game_history.append(current_room_id)

            updated_session = update_game_session(
                current_app.session, session_id, current_room=new_room_id, game_history=game_history
            )
            if not updated_session:
                result["error"] = "Game session not found after update"
                status_code = 500
            else:
                result["current_room"] = updated_session.current_room
                result["contextual_options"] = get_contextual_options(updated_session) # Get options for new room
                # Check for game completion after moving to escape_chamber
                if updated_session.current_room == "escape_chamber":
                    all_puzzle_ids = []
                    for r_id, r_info in ROOM_DATA.items():
                        if r_id != "escape_chamber":
                            all_puzzle_ids.extend(r_info["puzzles"].keys())
                    
                    all_previous_puzzles_solved = all(
                        updated_session.puzzle_state.get(p_id, False) for p_id in all_puzzle_ids
                    )
                    if all_previous_puzzles_solved:
                        result["message"] = "You escaped!"
                        result["game_over"] = True

    elif chosen_option.startswith("Solve "):
        puzzle_id = chosen_option.replace("Solve ", "")
        
        # Get the correct solution directly from PUZZLE_SOLUTIONS
        solution_attempt = PUZZLE_SOLUTIONS.get(puzzle_id)

        if not solution_attempt:
            result["error"] = f"Solution for puzzle {puzzle_id} not found."
            status_code = 500
        else:
            is_solved, message, updated_session = solve_puzzle(
                current_app.session, session_id, puzzle_id, solution_attempt
            )
            if not updated_session:
                result["error"] = message
                status_code = 404
            else:
                result["is_solved"] = is_solved
                result["message"] = message
                result["contextual_options"] = get_contextual_options(updated_session) # Update options after solving

    return jsonify(result), status_code
