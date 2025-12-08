import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_narrative(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the generated narrative text.
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

def generate_room_description(theme: str, location: str, narrative_state: str, room_context: dict) -> str:
    """
    Generates a unique room description based on the game's context.

    Args:
        theme: The overall theme of the escape room (e.g., "haunted mansion").
        location: The specific location of the escape room (e.g., "abandoned asylum").
        narrative_state: A summary of the story so far.
        room_context: A dictionary containing details about the current room, 
                      such as its name, exits, puzzles, and items.
                      Example: {'name': 'Room Name', 'exits': ['north', 'south'], 'puzzles': ['puzzle_1'], 'items': ['key']}

    Returns:
        A unique, AI-generated description for the room.
    """
    prompt = f"""
    Generate a unique and descriptive room description for an escape room game.
    The description should be consistent with the provided theme, location, narrative, and room context.

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
