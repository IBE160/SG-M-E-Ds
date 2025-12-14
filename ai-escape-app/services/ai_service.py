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

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)

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


# Initialize Gemini Model
model = genai.GenerativeModel('gemini-pro')


def generate_narrative(prompt: str, narrative_archetype: str = None, theme: str = None, location: str = None) -> str:
    """
    Returns a static narrative for the game.
    NO AI CALLS are made in this function.
    """
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


def evaluate_and_adapt_puzzle(
    puzzle_id: str,
    player_attempt: str,
    puzzle_solution: str, # This is the "ultimate" solution for the puzzle as defined in ROOM_DATA
    current_puzzle_state: dict, # This is the puzzle's dynamic state from GameSession.puzzle_state
    current_puzzle_description: str, # Initial description from ROOM_DATA
    theme: str,
    location: str,
    difficulty: str,
    narrative_archetype: str = None,
    current_inventory: list = None
) -> dict:
    """
    Evaluates a puzzle solution attempt or item usage using deterministic logic.
    Returns a structured dictionary with evaluation, feedback, and potential game state updates.
    NO AI CALLS are made in this function.
    """
    logging.info(f"Deterministic: evaluate_and_adapt_puzzle called for puzzle {puzzle_id} with attempt {player_attempt}")

    # --- Initial State Setup ---
    is_correct = False
    feedback = "That doesn't seem to work."
    puzzle_status = current_puzzle_state.get("status", "unsolved")
    items_found = []
    items_consumed = []
    game_state_changes = {}
    puzzle_progress = {}
    
    # Retrieve full puzzle definition (ROOM_DATA is the source of truth for static defs)
    # Note: 'location' in the parameters here is actually the current room_id.
    # We need to access ROOM_DATA from a different scope or pass room_info explicitly if needed.
    # For this deterministic logic, we'll assume the full puzzle_definition is sufficient.

    # --- Handle already solved puzzles ---
    if current_puzzle_state.get("solved", False):
        return {"is_correct": True, "feedback": f"You have already solved the '{puzzle_id.replace('_', ' ').title()}' puzzle.", "puzzle_status": "solved"}

    # --- Handle "I need a hint" request ---
    if player_attempt.lower() == "i need a hint":
        # A simple, static hint based on description for now, as no AI is called.
        return {
            "is_correct": False,
            "feedback": "Here's a hint.",
            "hint": f"Think about the description: '{current_puzzle_description}'.",
            "puzzle_status": "unsolved"
        }

    # --- Determine if it's an item usage attempt ---
    if player_attempt.lower().startswith("use "):
        parts = player_attempt.lower().split(" on ", 1)
        if len(parts) == 2:
            item_id = parts[0].replace("use ", "").strip().replace(' ', '_')
            target_name_attempt = parts[1].strip().replace(' ', '_')
            
            # --- Inventory Validation ---
            if item_id not in current_inventory:
                return {"is_correct": False, "feedback": "You don't have that item.", "puzzle_status": "unsolved"}

            # --- Target Validation (Does the item match the current puzzle?) ---
            # This logic assumes the 'target_name_attempt' refers to the 'puzzle_id'
            # Or the 'name' field of the puzzle.
            # For this context, we will directly check against the current puzzle_id.
            
            # We also need to get the full puzzle definition to check items_required
            # We need to import ROOM_DATA here, or pass puzzle_definition.
            # Assuming puzzle_definition is available and correct here.
            
            # Placeholder for retrieving puzzle_definition. In reality, solve_puzzle will pass it.
            # This function is called from solve_puzzle and use_item, which already have puzzle_definition.
            # Let's assume the caller ensures this context.
            # For simplicity, we're already passed `puzzle_solution` which implies we know the puzzle context.
            # The actual puzzle definition from ROOM_DATA needs to be accessed here to check `items_required`.
            from data.rooms import ROOM_DATA # Temporarily import here for access
            room_static_info = ROOM_DATA.get(theme, {}).get("rooms", {}).get(location, {})
            puzzle_definition = room_static_info.get("puzzles", {}).get(puzzle_id)

            if not puzzle_definition:
                 return {"is_correct": False, "feedback": "Puzzle definition not found for this target. (Internal Error)", "puzzle_status": "unsolved"}

            if item_id not in puzzle_definition.get("items_required", []):
                return {"is_correct": False, "feedback": "That item doesn't work here.", "puzzle_status": "unsolved"}
            
            # --- Correct Item Usage (deterministic) ---
            # If the item is in inventory and is required by the puzzle, it's a success
            is_correct = True
            feedback = f"You successfully used the {item_id.replace('_', ' ')}!"
            puzzle_status = "solved" # Or "item_used" depending on how we track partial progress
            items_consumed.append(item_id) # Assume item is consumed on correct use

            # Apply outcomes defined in the puzzle_definition
            for outcome in puzzle_definition.get("outcomes", []):
                game_state_changes[outcome] = True # e.g., "door_unlocked"
            for item_to_reveal in puzzle_definition.get("reveal_on_solve", []):
                items_found.append(item_to_reveal) # e.g., "keycard"
            
            # No further puzzle_progress here, assuming single-step item usage for solve

        else: # Malformed "Use" command
            feedback = "Invalid 'Use' command format. Try 'Use [item] on [target]'."
            is_correct = False
    else:
        # --- Direct Solution Attempt (non-item usage) ---
        if player_attempt.lower() == puzzle_solution.lower():
            is_correct = True
            feedback = f"You correctly solved the '{puzzle_definition.get('name', puzzle_id.replace('_', ' ').title())}' puzzle!"
            puzzle_status = "solved"
            
            # Apply outcomes defined in the puzzle_definition
            for outcome in puzzle_definition.get("outcomes", []):
                game_state_changes[outcome] = True # e.g., "door_unlocked_north"
            for item_to_reveal in puzzle_definition.get("reveal_on_solve", []):
                items_found.append(item_to_reveal)

        else:
            is_correct = False
            feedback = "That's not quite right. Try again."
            puzzle_status = "unsolved"

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "hint": "", # No hints from deterministic logic unless specifically coded
        "puzzle_status": puzzle_status,
        "next_step_description": "",
        "difficulty_adjustment_suggestion": "none",
        "new_puzzle_state": {},
        "items_found": items_found,
        "items_consumed": items_consumed,
        "game_state_changes": game_state_changes,
        "puzzle_progress": puzzle_progress
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