import os
import google.generativeai as genai
from dotenv import load_dotenv
from data.narrative_archetypes import NARRATIVE_ARCHETYPES

load_dotenv() # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_narrative(prompt: str, narrative_archetype: str = None, theme: str = None, location: str = None) -> str:
    """
    Sends a prompt to the Gemini API and returns the generated narrative text.
    If a narrative_archetype is provided, it will be used to structure the story.
    """
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_beats = NARRATIVE_ARCHETYPES[narrative_archetype]["beats"]
        prompt = f"""
        {prompt}

        Please structure the story according to the following narrative beats:
        {archetype_beats}
        """
    
    if theme and location:
        prompt = f"""
        {prompt}

        The story should be consistent with the following theme and location:
        Theme: {theme}
        Location: {location}
        """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        # Assuming the narrative is directly in the text attribute of the response
        return response.text
    except Exception as e:
        # Basic error handling
        print(f"Error generating narrative: {e}")
        return f"Error: Could not generate narrative. {e}"

def generate_room_description(theme: str, location: str, narrative_state: str, room_context: dict, narrative_archetype: str = None) -> str:
    """
    Generates a unique room description based on the game's context.
    """
    archetype_info = ""
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_info = f"Narrative Archetype: {NARRATIVE_ARCHETYPES[narrative_archetype]['name']}"

    prompt = f"""
    Generate a unique and descriptive room description for an escape room game.
    The description should be consistent with the provided theme, location, narrative, and room context.
    {archetype_info}

    Theme: {theme}
    Location: {location}
    Narrative so far: {narrative_state}
    Current Room Context: {room_context}

    Description:
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating room description: {e}")
        return f"Error: Could not generate room description. {e}"


def generate_puzzle(puzzle_type: str, difficulty: str, theme: str, location: str, narrative_archetype: str = None, puzzle_context: dict = None) -> dict:
    """
    Generates a puzzle description and solution based on game context and puzzle type.

    Args:
        puzzle_type: The type of puzzle to generate (e.g., "Riddle", "Observation").
        difficulty: The difficulty level of the puzzle.
        theme: The overall theme of the escape room.
        location: The specific location of the escape room.
        narrative_archetype: The selected narrative archetype, if any.
        puzzle_context: Additional context for the puzzle (e.g., items in the room).

    Returns:
        A dictionary containing the puzzle 'description' and 'solution'.
    """
    archetype_info = ""
    if narrative_archetype and narrative_archetype in NARRATIVE_ARCHETYPES:
        archetype_info = f"Narrative Archetype: {NARRATIVE_ARCHETYPES[narrative_archetype]['name']}"

    context_info = ""
    if puzzle_context:
        context_info = f"Additional context: {puzzle_context}"

    prompt = f"""
    Generate an escape room puzzle. The puzzle should be a {puzzle_type} and match the following criteria:

    Difficulty: {difficulty}
    Theme: {theme}
    Location: {location}
    {archetype_info}
    {context_info}

    Provide the puzzle description and its solution in a JSON format with two keys: "description" and "solution".

    Example format:
    {{
        "description": "What has an eye but cannot see?",
        "solution": "A needle"
    }}

    Puzzle:
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        # Attempt to parse the response as JSON
        import json
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating puzzle: {e}")
        return {"error": f"Could not generate puzzle. {e}"}
