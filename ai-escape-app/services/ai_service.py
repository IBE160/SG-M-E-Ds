import os
import google.generativeai as genai
from dotenv import load_dotenv
from data.narrative_archetypes import NARRATIVE_ARCHETYPES
import json # New import
import logging # Added for structured logging

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv() # Load environment variables from .env file

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



def generate_narrative(prompt: str, narrative_archetype: str = None, theme: str = None, location: str = None) -> str:
    """
    Sends a prompt to the Gemini API and returns the generated narrative text.
    If a narrative_archetype is provided, it will be used to structure the story.
    """
    # Sanitize main prompt
    safe_prompt = _sanitize_input(prompt)

    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_beats = NARRATIVE_ARCHETYPES[narrative_archetype]["beats"]
        safe_prompt = f"""
        <user_prompt>{safe_prompt}</user_prompt>

        Please structure the story according to the following narrative beats:
        <narrative_beats>{_sanitize_input(archetype_beats)}</narrative_beats>
        """
    
    if theme and location:
        safe_prompt = f"""
        <user_prompt>{safe_prompt}</user_prompt>

        The story should be consistent with the following theme and location:
        Theme: <theme>{_sanitize_input(theme)}</theme>
        Location: <location>{_sanitize_input(location)}</location>
        """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(safe_prompt)
        # Assuming the narrative is directly in the text attribute of the response
        return response.text
    except Exception as e:
        # Basic error handling
        logging.error(f"Error generating narrative: {e}")
        return f"Error: Could not generate narrative. {e}"

def generate_room_description(theme: str, location: str, narrative_state: str, room_context: dict, current_room_id: str, narrative_archetype: str = None) -> str:
    """
    Generates a unique room description based on the game's context.
    The AI is aware of expanded themes including 'classic mystery', 'sci-fi', and 'underwater'.
    """
    archetype_info = ""
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_info = f"Narrative Archetype: {_sanitize_input(NARRATIVE_ARCHETYPES[narrative_archetype]['name'])}"

    prompt = f"""
    Generate a unique and descriptive room description for the room identified as '{_sanitize_input(current_room_id)}' in an escape room game.
    The description should be consistent with the provided theme, location, narrative, and room context.
    The available themes include 'classic mystery' (e.g., ancient library, mysterious observatory),
    'sci-fi' (e.g., sci-fi hangar, derelict spaceship), and 'underwater' (e.g., underwater laboratory).
    Ensure the description's style matches the selected theme and images used for these themes.

    {archetype_info}

    Theme: <theme>{_sanitize_input(theme)}</theme>
    Location: <location>{_sanitize_input(location)}</location>
    Narrative so far: <narrative_state>{_sanitize_input(narrative_state)}</narrative_state>
    Current Room Context: <room_context>{json.dumps(room_context)}</room_context>

    Description:
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error generating room description: {e}")
        return f"Error: Could not generate room description. {e}"


def generate_puzzle(puzzle_type: str, difficulty: str, theme: str, location: str, narrative_archetype: str = None, puzzle_context: dict = None, prerequisites: list = None, outcomes: list = None) -> dict:
    """
    Generates a puzzle description and solution based on game context and puzzle type,
    including explicit prerequisites and outcomes for dependency chains.
    The AI is aware of expanded themes including 'classic mystery', 'sci-fi', and 'underwater'.
    """
    archetype_info = ""
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_info = f"Narrative Archetype: {_sanitize_input(NARRATIVE_ARCHETYPES[narrative_archetype]['name'])}"

    context_info = ""
    if puzzle_context:
        context_info = f"<additional_context_json>{json.dumps(puzzle_context)}</additional_context_json>"

    prerequisites_info = ""
    if prerequisites:
        prerequisites_info = f"Prerequisites: {json.dumps(prerequisites)}. The puzzle should only be solvable if these are met."

    outcomes_info = ""
    if outcomes:
        outcomes_info = f"Outcomes: {json.dumps(outcomes)}. Solving this puzzle should lead to these outcomes."

    prompt = f"""
    Generate an escape room puzzle. The puzzle should be of type <puzzle_type>{_sanitize_input(puzzle_type)}</puzzle_type> and match the following criteria:

    Difficulty: <difficulty>{_sanitize_input(difficulty)}</difficulty>
    Theme: <theme>{_sanitize_input(theme)}</theme>
    Location: <location>{_sanitize_input(location)}</location>
    The available themes include 'classic mystery' (e.g., ancient library, mysterious observatory),
    'sci-fi' (e.g., sci-fi hangar, derelict spaceship), and 'underwater' (e.g., underwater laboratory).
    Ensure the puzzle's style and content matches the selected theme.

    {archetype_info}
    {context_info}
    {prerequisites_info}
    {outcomes_info}

    Provide the puzzle description, its solution, its prerequisites (as a list of strings), and its outcomes (as a list of strings) in a JSON format.

    Example format:
    {{
        "description": "What has an eye but cannot see?",
        "solution": "A needle",
        "prerequisites": ["found_magnifying_glass"],
        "outcomes": ["unlocked_secret_drawer"]
    }}

    Puzzle:
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        # Attempt to parse the response as JSON
        # No need to import json again if it's at the top level
        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Error generating puzzle: {e}")
        return {"error": f"Could not generate puzzle. {e}"}


def evaluate_and_adapt_puzzle(
    puzzle_id: str,
    player_attempt: str,
    puzzle_solution: str,
    current_puzzle_state: dict,
    current_puzzle_description: str, # New argument
    theme: str,
    location: str,
    difficulty: str,
    narrative_archetype: str = None,
) -> dict:
    """
    Evaluates a player's puzzle attempt and requests adaptation (hint/difficulty adjustment) from Gemini API.
    """
    archetype_info = ""
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_info = f"Narrative Archetype: {_sanitize_input(NARRATIVE_ARCHETYPES[narrative_archetype]['name'])}"

    prompt = f"""
    A player attempted to solve a puzzle in an escape room. Evaluate their attempt and provide feedback,
    and optionally a hint or suggestion for adapting the puzzle's difficulty.

    Game Context:
    Theme: <theme>{_sanitize_input(theme)}</theme>
    Location: <location>{_sanitize_input(location)}</location>
    Difficulty: <difficulty>{_sanitize_input(difficulty)}</difficulty>
    {archetype_info}

    Puzzle Details:
    Puzzle ID: <puzzle_id>{_sanitize_input(puzzle_id)}</puzzle_id>
    Correct Solution: <puzzle_solution>{_sanitize_input(puzzle_solution)}</puzzle_solution>
    Player's Attempt: <player_attempt>{_sanitize_input(player_attempt)}</player_attempt>
    Current Puzzle State: <puzzle_state>{json.dumps(current_puzzle_state)}</puzzle_state>
    Current Puzzle Description: <puzzle_description>{_sanitize_input(current_puzzle_description)}</puzzle_description>

    Based on the player's attempt and the correct solution, provide the following in JSON format:
    - "is_correct": boolean (True if attempt matches solution, False otherwise)
    - "feedback": string (Concise feedback to the player)
    - "hint": string (Optional, a subtle hint if is_correct is False)
    - "difficulty_adjustment_suggestion": string (Optional, e.g., "increase", "decrease", "none")

    Example JSON response:
    {{
        "is_correct": false,
        "feedback": "Your answer is close, but not quite there.",
        "hint": "Think about the common use of the object in the riddle.",
        "difficulty_adjustment_suggestion": "none"
    }}

    Evaluation:
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Error evaluating and adapting puzzle: {e}")
        return {"error": f"Could not evaluate and adapt puzzle. {e}"}

def adjust_difficulty_based_on_performance(
    puzzle_state: dict,
    theme: str,
    location: str,
    overall_difficulty: str,
    narrative_archetype: str = None,
) -> dict:
    """
    Formulates a prompt for the Gemini API to recommend difficulty adjustments
    based on player performance metrics.
    """
    archetype_info = ""
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_info = f"Narrative Archetype: {_sanitize_input(NARRATIVE_ARCHETYPES[narrative_archetype]['name'])}"

    prompt = f"""
    A player is progressing through an escape room game. Based on their performance
    in past puzzles, recommend a subtle adjustment to the difficulty for future puzzles.

    Player Performance Metrics (puzzle_state):
    <player_performance>{json.dumps(puzzle_state, indent=2)}</player_performance>

    Game Context:
    Theme: <theme>{_sanitize_input(theme)}</theme>
    Location: <location>{_sanitize_input(location)}</location>
    Overall Difficulty: <difficulty>{_sanitize_input(overall_difficulty)}</difficulty>
    {archetype_info}

    Provide your recommendation in JSON format, including:
    - "difficulty_adjustment": string (e.g., "easier", "harder", "no_change")
    - "reasoning": string (brief explanation for the recommendation)
    - "suggested_puzzle_parameters": dict (e.g., {{"complexity": "low", "hint_frequency": "high"}})

    Example JSON response:
    {{
        "difficulty_adjustment": "easier",
        "reasoning": "Player struggled with previous puzzle, suggest simpler mechanics.",
        "suggested_puzzle_parameters": {{"complexity": "low", "hint_frequency": "high"}}
    }}

    Recommendation:
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Error adjusting difficulty: {e}")
        return {"error": f"Could not adjust difficulty. {e}"}
