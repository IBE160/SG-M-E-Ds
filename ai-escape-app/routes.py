from flask import Blueprint, current_app, jsonify, request
from services.game_logic import (
    create_game_session,
    get_game_session,
    update_game_session,
    update_player_inventory,
)

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
    new_room = data.get("new_room")

    if not new_room:
        return jsonify({"error": "New room is required"}), 400

    updated_session = update_game_session(
        current_app.session, session_id, current_room=new_room
    )
    if not updated_session:
        return jsonify({"error": "Game session not found"}), 404
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
