import os
import google.generativeai as genai
from dotenv import load_dotenv
from data.narrative_archetypes import NARRATIVE_ARCHETYPES
import json # New import
import logging # Added for structured logging

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv(dotenv_path='ai-escape-app/.flaskenv') # Load environment variables from .flaskenv file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENABLED = False # Initialize flag

if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY not found in environment variables. Gemini AI features are disabled.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_ENABLED = True
        logging.info("Gemini AI features are enabled.")
    except Exception as e:
        logging.error(f"Failed to configure Gemini API with provided key: {e}. Gemini AI features are disabled.")
        GEMINI_API_KEY = None # Clear key if configuration fails
        GEMINI_ENABLED = False


def _sanitize_input(text: str) -> str:
    """
    A basic sanitizer to prevent simple prompt injection by escaping characters
    that might be used to manipulate structured prompts (e.g., f-string syntax).
    A more robust solution for production might involve more complex validation
    or allow-listing of inputs.
    """
    if not isinstance(text, str):
        return text
    return text.replace('{', '{{').replace('}', '}}')


# Initialize Gemini Model conditionally
model = None
if GEMINI_ENABLED:
    try:
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        logging.error(f"Failed to initialize Gemini GenerativeModel: {e}. Gemini AI features are disabled.")
        GEMINI_ENABLED = False
        model = None
        
if not GEMINI_ENABLED:
    logging.info("Gemini AI is not available. All AI functions will return deterministic/stubbed responses.")


def generate_narrative(prompt: str, narrative_archetype: str = None, theme: str = None, location: str = None) -> str:
    """
    Returns a static narrative for the game.
    If GEMINI_ENABLED, it would call AI. Otherwise, deterministic.
    """
    if GEMINI_ENABLED and model:
        # Placeholder for actual AI call if it were to be re-enabled
        # response = model.generate_content(...)
        # return response.text
        logging.info("Gemini is enabled but generate_narrative is stubbed for deterministic mode.")
    logging.info(f"Deterministic: generate_narrative called with prompt: {prompt}")
    return "You find yourself in a mysterious place. Your adventure begins!" # Static narrative


def generate_room_description(theme: str, scenario_name_for_ai_prompt: str, narrative_state: dict, room_context: dict, current_room_id: str, narrative_archetype: str = None) -> str:
    """
    Returns a static room description based on the provided room_context.
    NO AI CALLS are made in this function.
    """
    logging.info(f"Deterministic: generate_room_description called for room {current_room_id}")
    # Prioritize description from room_context, fall back to a generic message
    return room_context.get("description", f"You are in a {scenario_name_for_ai_prompt.lower()} room. It is quite mysterious.")


def generate_puzzle(puzzle_type: str, difficulty: str, theme: str, location: str, narrative_archetype: str = None, puzzle_context: dict = None, prerequisites: list = None, outcomes: list = None) -> dict:
    """
    Returns a static puzzle definition for the game.
    NO AI CALLS are made in this function.
    """
    logging.info(f"Deterministic: generate_puzzle called for type {puzzle_type}, theme {theme}")
    # This function is not currently called directly in the game logic for existing puzzles,
    # but rather for dynamically generating new ones. For deterministic logic, we'll return a generic error.
    return {"error": "Dynamic puzzle generation is disabled for deterministic mode."}


def _normalize_player_attempt(player_attempt: str) -> str:
    """
    Normalizes player's natural language attempt into a canonical semantic action.
    """
    normalized_attempt = player_attempt.strip().lower()

    # Mappings for ancient_symbol_door_puzzle
    if any(phrase in normalized_attempt for phrase in ["examine symbol", "inspect symbol", "touch eye", "look at eye"]):
        return "examine_glowing_symbol"
    if any(phrase == normalized_attempt for phrase in ["eyetears"]) or \
       any(phrase in normalized_attempt for phrase in ["input eyetears", "type eyetears", "enter eyetears", "solve door", "solve symbol"]):
        return "eyetears"
    
    # Mappings for desk_puzzle
    if any(phrase in normalized_attempt for phrase in ["inspect desk", "examine desk", "look at desk"]):
        return "inspect_desk"
    if any(phrase == normalized_attempt for phrase in ["7"]) or \
       any(phrase in normalized_attempt for phrase in ["input 7", "type 7", "enter 7", "open desk"]):
        return "7"

    # Mappings for final_escape_puzzle
    if any(phrase in normalized_attempt for phrase in ["escape library", "exit library", "escape"]):
        return "escape_the_library"
    
    # Handle item usage normalization for the 'Use [item] on [target]' actions
    if normalized_attempt.startswith("use "):
        parts = normalized_attempt.split(" on ", 1)
        if len(parts) == 2:
            item_id = parts[0].replace("use ", "").strip().replace(' ', '_')
            target_name = parts[1].strip().replace(' ', '_')
            return f"use_{item_id}_on_{target_name}"
        else: # Generic use item without target
            item_id = normalized_attempt.replace("use ", "").strip().replace(' ', '_')
            return f"use_{item_id}"

    return normalized_attempt # Fallback to raw attempt if no specific mapping


def evaluate_and_adapt_puzzle(
    puzzle_id: str,
    player_attempt: str,
    puzzle_solution: str | list[str], # Can now be a string or a list of semantic actions
    current_puzzle_state: dict,
    current_puzzle_description: str,
    theme: str,
    location: str,
    difficulty: str,
    narrative_archetype: str = None,
    current_inventory: list = None
) -> dict:
    """
    Evaluates a puzzle solution attempt or item usage using deterministic logic.
    Handles multi-step puzzles by comparing player attempts against a list of semantic actions.
    Returns a structured dictionary with evaluation, feedback, and potential game state updates.
    NO AI CALLS are made in this function.
    """
    logging.info(f"Deterministic: evaluate_and_adapt_puzzle called for puzzle {puzzle_id} with attempt '{player_attempt}'")

    # --- Initial State Setup ---
    is_correct = False
    feedback = "That doesn't seem to work."
    puzzle_status = current_puzzle_state.get("status", "unsolved")
    items_found = []
    items_consumed = []
    game_state_changes = {}
    
    # Retrieve full puzzle definition (ROOM_DATA is the source of truth for static defs)
    from data.rooms import ROOM_DATA # Import here to access ROOM_DATA in a clean way
    room_static_info = ROOM_DATA.get(theme, {}).get("rooms", {}).get(location, {})
    puzzle_definition = room_static_info.get("puzzles", {}).get(puzzle_id)

    if not puzzle_definition:
        logging.error(f"Puzzle definition not found for {puzzle_id} in {theme}/{location}")
        return {"is_correct": False, "feedback": "Puzzle definition not found. (Internal Error)", "puzzle_status": "unsolved"}

    # --- Check if puzzle is already solved ---
    if current_puzzle_state.get("solved", False):
        return {"is_correct": True, "feedback": f"You have already solved the '{puzzle_definition['name']}' puzzle.", "puzzle_status": "solved"}

    # --- Handle "I need a hint" request ---
    if _normalize_player_attempt(player_attempt) == "i need a hint":
        hint_message = f"Think about the description: '{current_puzzle_description}'."
        current_step_index = current_puzzle_state.get("current_step_index", 0)
        
        if puzzle_definition.get("clues") and current_step_index < len(puzzle_definition["clues"]):
            hint_message = puzzle_definition["clues"][current_step_index]
        elif puzzle_definition.get("clues"): # If there are clues but no specific one for this step
            hint_message = puzzle_definition["clues"][-1] # Return the last available clue

        return {
            "is_correct": False,
            "feedback": "Here's a hint.",
            "hint": hint_message,
            "puzzle_status": "unsolved"
        }

    # Normalize player attempt to a canonical semantic action
    normalized_player_action = _normalize_player_attempt(player_attempt)
    logging.info(f"Normalized player action: '{normalized_player_action}' for puzzle {puzzle_id}")

    # --- Unified single-step puzzle logic ---
    if isinstance(puzzle_solution, list):
        puzzle_solution = "".join(puzzle_solution).lower() # Flatten list solutions for direct comparison
    else:
        puzzle_solution = str(puzzle_solution).lower() # Ensure solution is a lowercase string for comparison
    
    # Handle item usage (e.g., "USE_ITEM_ON_TARGET")
    if normalized_player_action.startswith("use_"):
        parts = normalized_player_action.split("_on_", 1)
        item_id_attempt = parts[0].replace("use_", "").strip()
        target_name_attempt = parts[1].strip() if len(parts) == 2 else ""

        # Check if the player has the item in inventory
        if item_id_attempt not in [item.lower().replace(' ', '_') for item in current_inventory]:
            return {"is_correct": False, "feedback": "You don't have that item.", "puzzle_status": "unsolved"}

        # Compare the normalized action against the puzzle solution
        if normalized_player_action == puzzle_solution:
            is_correct = True
            feedback = f"You successfully used the {item_id_attempt.replace('_', ' ')}!"
            puzzle_status = "solved"
            items_consumed.append(item_id_attempt) # Consume the item used
            # Apply outcomes
            for outcome in puzzle_definition.get("outcomes", []):
                game_state_changes[outcome] = True
            for item_to_reveal in puzzle_definition.get("reveal_on_solve", []):
                items_found.append(item_to_reveal)
        else:
            is_correct = False
            feedback = "That item doesn't work here."
            puzzle_status = "unsolved"
    
    # Handle direct text input solution
    else:
        if normalized_player_action == puzzle_solution:
            is_correct = True
            feedback = f"You correctly solved the '{puzzle_definition['name']}' puzzle!"
            puzzle_status = "solved"
            # Apply outcomes
            for outcome in puzzle_definition.get("outcomes", []):
                game_state_changes[outcome] = True
            for item_to_reveal in puzzle_definition.get("reveal_on_solve", []):
                items_found.append(item_to_reveal)
        else:
            is_correct = False
            feedback = "That's not quite right. Try again."
            puzzle_status = "unsolved"

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "hint": "", # Hints are handled separately
        "puzzle_status": puzzle_status,
        "next_step_description": "",
        "difficulty_adjustment_suggestion": "none",
        "new_puzzle_state": {}, # No partial progress states
        "items_found": items_found,
        "game_state_changes": game_state_changes
    }



def adjust_difficulty_based_on_performance(
    puzzle_state: dict,
    theme: str,
    location: str,
    overall_difficulty: str,
    narrative_archetype: str = None,
) -> dict:
    """
    STUB: Adjusts game difficulty based on player performance using the Gemini API.
    Returns a structured dictionary with difficulty adjustment suggestions.
    """
    logging.info(f"STUB: adjust_difficulty_based_on_performance called with puzzle_state {puzzle_state}")
    return {"difficulty_adjustment": "none", "reason": "STUB: No adjustment.", "suggested_puzzle_parameters": {}}