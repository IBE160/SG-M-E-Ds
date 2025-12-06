from flask import Blueprint, current_app, jsonify, request
from services.game_logic import (
    create_game_session,
    get_game_session,
    update_game_session,
    update_player_inventory,
    solve_puzzle,
)
from data.rooms import ROOM_DATA

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


@bp.route("/game_session/<int:session_id>", methods=["GET"])
def get_session(session_id):
    game_session = get_game_session(current_app.session, session_id)
    if not game_session:
        return jsonify({"error": "Game session not found"}), 404
    return jsonify(
        {
            "id": game_session.id,
            "player_id": game_session.player_id,
            "current_room": game_session.current_room,
            "inventory": game_session.inventory,
            "game_history": game_session.game_history,
            "narrative_state": game_session.narrative_state,
            "puzzle_state": game_session.puzzle_state,
            "theme": game_session.theme,
            "location": game_session.location,
            "difficulty": game_session.difficulty,
            "start_time": game_session.start_time.isoformat(),
            "last_updated": game_session.last_updated.isoformat(),
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

    updated_session = update_game_session(
        current_app.session, session_id, current_room=new_room_id
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
