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


def generate_narrative(prompt: str, narrative_archetype: str = None, theme: str = None, location: str = None) -> str:
    """
    (Bypassed AI Call) Returns a static narrative.
    """
    logging.info(f"Bypassing AI for generate_narrative. Prompt: {prompt}, Theme: {theme}, Location: {location}")
    return "You find yourself in a place of mystery, ready for adventure!"


def generate_room_description(theme: str, scenario_name_for_ai_prompt: str, narrative_state: str, room_context: dict, current_room_id: str, narrative_archetype: str = None) -> str:
    """
    (Bypassed AI Call) Returns a static room description.
    """
    logging.info(f"Bypassing AI for generate_room_description. Room: {current_room_id}, Scenario: {scenario_name_for_ai_prompt}")
    return f"You are in the {room_context.get('name', current_room_id)}. It's a placeholder description. Exits: {', '.join(room_context.get('exits', []))}"


def generate_puzzle(puzzle_type: str, difficulty: str, theme: str, location: str, narrative_archetype: str = None, puzzle_context: dict = None, prerequisites: list = None, outcomes: list = None) -> dict:
    """
    (Bypassed AI Call) Returns a static puzzle.
    """
    logging.info(f"Bypassing AI for generate_puzzle. Type: {puzzle_type}, Difficulty: {difficulty}")
    return {
        "description": f"This is a placeholder {puzzle_type} puzzle for {location}.",
        "solution": "placeholder_solution",
        "prerequisites": [],
        "outcomes": [],
    }


def evaluate_and_adapt_puzzle(
    puzzle_id: str,
    player_attempt: str,
    puzzle_solution: str,
    current_puzzle_state: dict,
    current_puzzle_description: str,
    theme: str,
    location: str,
    difficulty: str,
    narrative_archetype: str = None,
) -> dict:
    """
    (Bypassed AI Call) Returns a static puzzle evaluation.
    """
    logging.info(f"Bypassing AI for evaluate_and_adapt_puzzle. Puzzle: {puzzle_id}, Attempt: {player_attempt}")
    is_correct = (player_attempt.lower() == puzzle_solution.lower())
    feedback = "This is placeholder feedback."
    if is_correct:
        feedback = "Correct! Placeholder feedback."
    else:
        feedback = "Incorrect. Placeholder feedback."

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "hint": "Placeholder hint.",
        "difficulty_adjustment_suggestion": "none",
    }


def adjust_difficulty_based_on_performance(
    puzzle_state: dict,
    theme: str,
    location: str,
    overall_difficulty: str,
    narrative_archetype: str = None,
) -> dict:
    """
    (Bypassed AI Call) Returns a static difficulty adjustment suggestion.
    """
    logging.info(f"Bypassing AI for adjust_difficulty_based_on_performance. Difficulty: {overall_difficulty}")
    return {
        "difficulty_adjustment": "none",
        "suggested_puzzle_parameters": {},
    }