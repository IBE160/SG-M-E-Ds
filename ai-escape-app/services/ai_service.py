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
    Generates a narrative using the Gemini API based on the provided prompt and context.
    """
    sanitized_prompt = _sanitize_input(prompt)
    full_prompt = (
        f"Generate a narrative for an AI Escape game based on the following:\n"
        f"Prompt: {sanitized_prompt}\n"
        f"Theme: {theme if theme else 'unspecified'}\n"
        f"Location: {location if location else 'unspecified'}\n"
        f"Narrative Archetype: {narrative_archetype if narrative_archetype else 'unspecified'}\n"
        f"Ensure the narrative is immersive and sets the scene for a puzzle game."
    )
    logging.info(f"Calling AI for generate_narrative. Prompt: {full_prompt[:100]}...") # Log first 100 chars
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logging.error(f"AI call failed for generate_narrative: {e}")
        return "Error: Could not generate narrative."


def generate_room_description(theme: str, scenario_name_for_ai_prompt: str, narrative_state: dict, room_context: dict, current_room_id: str, narrative_archetype: str = None) -> str:
    """
    Generates a detailed room description using the Gemini API.
    """
    sanitized_scenario_name = _sanitize_input(scenario_name_for_ai_prompt)
    sanitized_current_room_id = _sanitize_input(current_room_id)

    exits_list = ", ".join(room_context.get('exits', []))
    puzzles_list = ", ".join(room_context.get('puzzles', []))
    items_list = ", ".join(room_context.get('items', []))

    full_prompt = (
        f"You are the game master for an AI Escape room game. Generate a rich, immersive, and atmospheric description "
        f"for the following room, acting as the story introduction for the player. "
        f"The description should clearly explain where the player is, establish the ambiance, "
        f"and state the player's immediate goal for this room (e.g., finding a key, restoring power, unlocking a door). "
        f"It should also subtly hint at the types of puzzles or interactions the player might encounter "
        f"without explicitly listing game mechanics or solutions. "
        f"Ensure the story strongly matches the given theme and location.\n\n"
        f"Theme: {theme}\n"
        f"Scenario Name: {sanitized_scenario_name}\n"
        f"Room ID: {sanitized_current_room_id}\n"
        f"Current Game Narrative State: {json.dumps(narrative_state, indent=2)}\n" # Pass full narrative state for richer context
        f"Room Context (for AI's internal reference, do not explicitly list these in the description):\n"
        f"  Name: {room_context.get('name', sanitized_current_room_id)}\n"
        f"  Exits: {exits_list}\n"
        f"  Puzzles (unsolved): {puzzles_list}\n"
        f"  Items: {items_list}\n\n"
        f"Make it engaging and mysterious. "
        f"The goal is to provide a comprehensive sense of place and purpose to the player upon entering the room."
    )
    logging.info(f"Calling AI for generate_room_description. Room: {sanitized_current_room_id}, Prompt: {full_prompt[:200]}...")
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logging.error(f"AI call failed for generate_room_description: {e}")
        return f"Error: Could not generate description for {sanitized_scenario_name}."


def generate_puzzle(puzzle_type: str, difficulty: str, theme: str, location: str, narrative_archetype: str = None, puzzle_context: dict = None, prerequisites: list = None, outcomes: list = None) -> dict:
    """
    Generates a puzzle using the Gemini API.
    Returns a structured dictionary with puzzle details.
    """
    sanitized_puzzle_type = _sanitize_input(puzzle_type)
    sanitized_theme = _sanitize_input(theme)
    sanitized_location = _sanitize_input(location)
    
    context_str = json.dumps(puzzle_context) if puzzle_context else "None"
    prereq_str = ", ".join(prerequisites) if prerequisites else "None"
    outcomes_str = ", ".join(outcomes) if outcomes else "None"

    full_prompt = (
        f"You are an AI Game Master. Generate a new puzzle for an escape room game. "
        f"The puzzle should be interactive and clearly indicate what the player is trying to achieve. "
        f"Return your response as a JSON object only. Do NOT include any other text.\n\n"
        f"**JSON Schema:**\n"
        f"```json\n"
        f"{{\n"
        f'  "puzzle_id": string, // A unique identifier for the puzzle (e.g., "star_map_console")\n'
        f'  "description": string, // A detailed description of the puzzle for the player, clearly stating the objective\n'
        f'  "solution": string,    // The exact solution string (case-insensitive for comparison)\n'
        f'  "prerequisites": array, // (Optional) List of strings of prerequisites (e.g., "power_restored", "keycard_found")\n'
        f'  "outcomes": array,    // (Optional) List of strings of outcomes (e.g., "door_unlocked", "new_item_revealed")\n'
        f'  "puzzle_steps": array // (Optional) For multi-step puzzles, a list of dictionaries, each with "step_description" and "step_solution"\n'
        f'  "puzzle_type": string // (Optional) e.g., "code_entry", "object_interaction", "mechanism_sequence", "inspection"\n'
        f'  "items_required": array // (Optional) List of items needed to solve the puzzle (e.g., ["Rusty Key"])\n'
        f'  "item_discovered_on_solve": array // (Optional) List of items discovered when this puzzle is solved (e.g., ["Keycard"])\n'
        f"}}\n"
        f"```\n\n"
        f"**Game Context:**\n"
        f"- Theme: {sanitized_theme}\n"
        f"- Location: {sanitized_location}\n"
        f"- Difficulty: {difficulty}\n"
        f"- Narrative Archetype: {narrative_archetype if narrative_archetype else 'None'}\n"
        f"- Requested Puzzle Type: {sanitized_puzzle_type if sanitized_puzzle_type else 'any'}\n"
        f"- Additional Context: {context_str}\n"
        f"- Known Prerequisites: {prereq_str}\n"
        f"- Expected Outcomes: {outcomes_str}\n\n"
        f"Generate a puzzle that fits the context and difficulty. "
        f"The `description` must clearly state what the player needs to achieve. "
        f"For 'easy' difficulty: Puzzles should be straightforward, have fewer steps (ideally one), and clear objectives. Hints should be direct. "
        f"For 'medium' difficulty: Puzzles can have multiple steps, require some indirect clue-finding, and light exploration. "
        f"For 'hard' difficulty: Puzzles should be complex, multi-step, with hidden clues, and minimal direct guidance. They might require combining items or complex sequences. "
        f"Ensure the `solution` is concise and exact. "
        f"If the puzzle involves finding an item, specify it in `item_discovered_on_solve`. "
        f"If the puzzle requires an item from the player's inventory, specify it in `items_required`. "
        f"Ensure the generated JSON is valid and adheres strictly to the schema."
    )
    
    logging.info(f"Calling AI for generate_puzzle. Type: {sanitized_puzzle_type}, Difficulty: {difficulty}, Prompt: {full_prompt[:500]}...")
    try:
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        ai_puzzle = json.loads(response.text)
        logging.info(f"AI puzzle generation response: {ai_puzzle}")

        # Validate basic structure
        if not all(k in ai_puzzle for k in ["puzzle_id", "description", "solution"]):
            raise ValueError("AI puzzle response missing required keys.")

        return ai_puzzle
    except json.JSONDecodeError as e:
        logging.error(f"AI response for generate_puzzle was not valid JSON: {response.text[:500]}... Error: {e}")
        return {"error": "AI returned malformed response for puzzle generation.", "details": str(e)}
    except Exception as e:
        logging.error(f"AI call failed for generate_puzzle: {e}")
        return {"error": "An internal error occurred during puzzle generation.", "details": str(e)}


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
) -> dict:
    """
    Evaluates a puzzle solution attempt using the Gemini API and adapts the puzzle.
    Returns a structured dictionary with evaluation, feedback, hints, and potential puzzle state updates.
    """
    sanitized_puzzle_id = _sanitize_input(puzzle_id)
    sanitized_player_attempt = _sanitize_input(player_attempt)
    sanitized_current_puzzle_description = _sanitize_input(current_puzzle_description)

    # Use a chat-based model for multi-turn interaction or a model configured for JSON output
    # For now, we'll try to get JSON output directly from generate_content
    # by instructing the model clearly in the prompt.
    
    # Construct the full prompt for the AI
    full_prompt = (
        f"You are an AI Game Master assisting in an escape room game. "
        f"A player has made an attempt to solve a puzzle. Your task is to evaluate this attempt, "
        f"provide feedback, and suggest how the puzzle state might change. "
        f"Return your response as a JSON object only. Do NOT include any other text.\n\n"
        f"**JSON Schema:**\n"
        f"```json\n"
        f"{{\n"
        f'  "is_correct": boolean, // True if the attempt solves the current step or the whole puzzle\n'
        f'  "feedback": string,    // A message to the player about their attempt\n'
        f'  "hint": string,        // (Optional) A context-aware hint if the attempt is incorrect\n'
        f'  "puzzle_status": string, // e.g., "solved", "partially_solved", "unsolved", "failed"\n'
        f'  "next_step_description": string, // (Optional) For multi-step puzzles, what the player needs to do next (short, action-oriented phrase)\n'
        f'  "difficulty_adjustment_suggestion": string, // e.g., "make_easier", "make_harder", "none"\n'
        f'  "new_puzzle_state": object, // (Optional) Any updates to the puzzle\'s internal state (e.g., clues found, step completed)\n'
        f'  "items_found": array, // (Optional) List of strings of items discovered/obtained (e.g., ["Rusty Key", "Flashlight"])\n'
        f'  "game_state_changes": object, // (Optional) Dictionary of broader game state changes (e.g., {{"door_status": {{"main_door": "unlocked"}}}}, {{"power_grid": "online"}})\n'
        f'  "puzzle_progress": object // (Optional) Dictionary of specific progress within a puzzle (e.g., {{"lever_pulled": true}} or {{"riddle_part_1_solved": true}})\n'
        f"}}\n"
        f"```\n\n"
        f"**Game Context:**\n"
        f"- Theme: {theme}\n"
        f"- Location: {location}\n"
        f"- Difficulty: {difficulty}\n"
        f"- Narrative Archetype: {narrative_archetype if narrative_archetype else 'None'}\n\n"
        f"**Puzzle Details:**\n"
        f"- Puzzle ID: {sanitized_puzzle_id}\n"
        f"- Initial Description: {sanitized_current_puzzle_description}\n"
        f"- Known Solution (for your reference): {puzzle_solution}\n"
        f"- Current Puzzle State (dynamic): {current_puzzle_state}\n\n"
        f"**Player's Attempt:**\n"
        f"- Attempt: {sanitized_player_attempt}\n\n"
        f"Evaluate the attempt. If the player explicitly asked for a hint (e.g., `player_attempt` is 'I need a hint'), provide a hint. "
        f"Make sure 'feedback' is engaging and 'hint' is helpful but doesn't give away the solution too easily for higher difficulties. "
        f"Consider the `difficulty` when providing hints or adapting feedback. For 'hard' difficulty, be subtle. For 'easy', be more direct."
        f"If the `player_attempt` is the exact `puzzle_solution` (case-insensitive), set `is_correct` to true and `puzzle_status` to 'solved'."
        f"Otherwise, if the attempt is close or shows partial understanding, you can set `puzzle_status` to 'partially_solved' and provide `new_puzzle_state`. "
        f"If the action leads to finding an item, include `items_found`. If it changes a broader game state (like unlocking a door or turning on power), include `game_state_changes`. "
        f"If it's a specific step in a multi-part puzzle, use `puzzle_progress`. "
        f"Ensure the generated JSON is valid and adheres strictly to the schema. The `next_step_description` should be a short, actionable phrase like 'Inspect the safe' or 'Enter code'."
    )

    logging.info(f"Calling AI for evaluate_and_adapt_puzzle. Puzzle: {sanitized_puzzle_id}, Attempt: {sanitized_player_attempt}, Prompt: {full_prompt[:500]}...")
    try:
        # Use a generation configuration that encourages JSON output
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        
        # Parse the JSON response
        ai_evaluation = json.loads(response.text)
        logging.info(f"AI evaluation response: {ai_evaluation}")
        
        # Validate the response against the expected structure
        if not all(k in ai_evaluation for k in ["is_correct", "feedback", "puzzle_status"]):
            raise ValueError("AI response missing required keys.")
        
        return ai_evaluation

    except json.JSONDecodeError as e:
        logging.error(f"AI response was not valid JSON: {response.text[:500]}... Error: {e}")
        return {"is_correct": False, "feedback": "AI returned malformed response. Try again.", "puzzle_status": "unsolved", "error": "Malformed JSON from AI."}
    except Exception as e:
        logging.error(f"AI call failed for evaluate_and_adapt_puzzle: {e}")
        return {"is_correct": False, "feedback": "An internal error occurred. Please try again.", "puzzle_status": "unsolved", "error": str(e)}


def adjust_difficulty_based_on_performance(
    puzzle_state: dict,
    theme: str,
    location: str,
    overall_difficulty: str,
    narrative_archetype: str = None,
) -> dict:
    """
    Adjusts game difficulty based on player performance using the Gemini API.
    Returns a structured dictionary with difficulty adjustment suggestions.
    """
    sanitized_theme = _sanitize_input(theme)
    sanitized_location = _sanitize_input(location)

    full_prompt = (
        f"You are an AI Game Master. Analyze the player's performance based on the current puzzle state "
        f"and recommend an adjustment to the overall game difficulty. "
        f"Return your response as a JSON object only. Do NOT include any other text.\n\n"
        f"**JSON Schema:**\n"
        f"```json\n"
        f"{{\n"
        f'  "difficulty_adjustment": string, // e.g., "make_easier", "make_harder", "none"\n'
        f'  "reason": string,              // Explanation for the suggested adjustment\n'
        f'  "suggested_puzzle_parameters": object // (Optional) Parameters for future puzzle generation (e.g., "more_direct_clues", "fewer_steps")\n'
        f"}}\n"
        f"```\n\n"
        f"**Game Context:**\n"
        f"- Theme: {sanitized_theme}\n"
        f"- Location: {sanitized_location}\n"
        f"- Overall Difficulty: {overall_difficulty}\n"
        f"- Narrative Archetype: {narrative_archetype if narrative_archetype else 'None'}\n\n"
        f"**Current Puzzle State:**\n"
        f"{json.dumps(puzzle_state, indent=2)}\n\n"
        f"Analyze the `puzzle_state`. Look for patterns like many attempts, frequent hint usage, or rapid puzzle solving. "
        f"Suggest whether to 'make_easier', 'make_harder', or 'none' based on the player's performance relative to the `overall_difficulty`. "
        f"Provide a concise `reason`. If adjusting, suggest `suggested_puzzle_parameters` to guide future puzzle generation. "
        f"Ensure the generated JSON is valid and adheres strictly to the schema."
    )

    logging.info(f"Calling AI for adjust_difficulty_based_on_performance. Difficulty: {overall_difficulty}, Prompt: {full_prompt[:500]}...")
    try:
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        ai_adjustment = json.loads(response.text)
        logging.info(f"AI difficulty adjustment response: {ai_adjustment}")

        # Validate basic structure
        if not all(k in ai_adjustment for k in ["difficulty_adjustment", "reason"]):
            raise ValueError("AI adjustment response missing required keys.")

        return ai_adjustment
    except json.JSONDecodeError as e:
        logging.error(f"AI response for difficulty adjustment was not valid JSON: {response.text[:500]}... Error: {e}")
        return {"difficulty_adjustment": "none", "reason": "AI returned malformed response.", "error": str(e)}
    except Exception as e:
        logging.error(f"AI call failed for adjust_difficulty_based_on_performance: {e}")
        return {"difficulty_adjustment": "none", "reason": "An internal error occurred.", "error": str(e)}