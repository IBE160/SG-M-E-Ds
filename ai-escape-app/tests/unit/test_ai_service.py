import pytest
from unittest.mock import patch, MagicMock
import os
import json # Added import for json
from services.ai_service import generate_narrative, generate_room_description, generate_puzzle, evaluate_and_adapt_puzzle, adjust_difficulty_based_on_performance
from data.narrative_archetypes import NARRATIVE_ARCHETYPES


# Mock the os.getenv to control GEMINI_API_KEY for tests
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key"}):
        yield

@patch('services.ai_service.genai')
def test_generate_narrative_success(mock_genai):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = "Generated narrative text."
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    prompt = "Generate a short story."
    result = generate_narrative(prompt)

    # Assertions
    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once_with(prompt)
    assert result == "Generated narrative text."

@patch('services.ai_service.genai')
def test_generate_narrative_api_error(mock_genai):
    # Setup mock to raise an exception
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("API Error")

    prompt = "Generate a story causing an error."
    result = generate_narrative(prompt)

    # Assertions
    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once_with(prompt)
    assert "Error: Could not generate narrative. API Error" in result

@patch('services.ai_service.genai')
def test_generate_room_description_success(mock_genai):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = "A dusty room with a single flickering candle."
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    theme = "haunted"
    location = "mansion"
    narrative_state = "The player has just entered the mansion."
    room_context = {"name": "Entrance Hall", "exits": ["north"], "puzzles": [], "items": []}

    result = generate_room_description(theme, location, narrative_state, room_context)

    # Assertions
    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    assert result == "A dusty room with a single flickering candle."
    # You could also add more specific assertions about the prompt content here if needed

@patch('services.ai_service.genai')
def test_generate_narrative_with_archetype(mock_genai):
    mock_genai.GenerativeModel.return_value.generate_content.return_value.text = "A story."

    generate_narrative("A hero's tale", narrative_archetype="heros_journey")

    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    prompt = mock_genai.GenerativeModel.return_value.generate_content.call_args[0][0]
    assert "A hero's tale" in prompt
    assert "The Call to Adventure" in prompt

@patch('services.ai_service.genai')
def test_generate_room_description_with_archetype(mock_genai):
    mock_genai.GenerativeModel.return_value.generate_content.return_value.text = "A room."

    generate_room_description("theme", "location", "state", {}, narrative_archetype="mystery")

    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    prompt = mock_genai.GenerativeModel.return_value.generate_content.call_args[0][0]
    assert "Narrative Archetype: Classic Mystery" in prompt

@patch('services.ai_service.genai')
def test_generate_narrative_with_theme_and_location(mock_genai):
    mock_genai.GenerativeModel.return_value.generate_content.return_value.text = "A themed narrative."

    generate_narrative("A prompt for the story.", theme="space", location="mars colony")

    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    prompt = mock_genai.GenerativeModel.return_value.generate_content.call_args[0][0]
    assert "A prompt for the story." in prompt
    assert "Theme: space" in prompt
    assert "Location: mars colony" in prompt

@patch('services.ai_service.genai')
def test_generate_puzzle_success(mock_genai):
    mock_response = MagicMock()
    mock_response.text = '{"description": "What has an eye but cannot see?", "solution": "A needle"}'
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    puzzle_type = "Riddle"
    difficulty = "easy"
    theme = "fantasy"
    location = "magical forest"
    narrative_archetype = "mystery"
    puzzle_context = {"item_present": "magical orb"}

    result = generate_puzzle(
        puzzle_type=puzzle_type,
        difficulty=difficulty,
        theme=theme,
        location=location,
        narrative_archetype=narrative_archetype,
        puzzle_context=puzzle_context
    )

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    
    assert result == {"description": "What has an eye but cannot see?", "solution": "A needle"}
    
    # Assert that the prompt contains the relevant information
    prompt = mock_genai.GenerativeModel.return_value.generate_content.call_args[0][0]
    assert "Generate an escape room puzzle" in prompt
    assert f"Difficulty: {difficulty}" in prompt
    assert f"Theme: {theme}" in prompt
    assert f"Location: {location}" in prompt
    assert f"Narrative Archetype: {NARRATIVE_ARCHETYPES[narrative_archetype]['name']}" in prompt
    assert f"Additional context: {puzzle_context}" in prompt

@patch('services.ai_service.genai')
def test_generate_puzzle_api_error(mock_genai):
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("Puzzle API Error")

    result = generate_puzzle(
        puzzle_type="Riddle", difficulty="easy", theme="fantasy", location="magical forest"
    )

    assert "error" in result
    assert "Could not generate puzzle. Puzzle API Error" in result["error"]


@patch('services.ai_service.genai')
def test_evaluate_and_adapt_puzzle_correct_solution(mock_genai):
    mock_response = MagicMock()
    mock_response.text = '{"is_correct": true, "feedback": "Excellent!", "hint": null, "difficulty_adjustment_suggestion": "none"}'
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    result = evaluate_and_adapt_puzzle(
        puzzle_id="test_puzzle",
        player_attempt="correct answer",
        puzzle_solution="correct answer",
        current_puzzle_state={},
        current_puzzle_description="A test puzzle.", # New argument
        theme="fantasy",
        location="forest",
        difficulty="medium",
    )

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    assert result["is_correct"] is True
    assert result["feedback"] == "Excellent!"

@patch('services.ai_service.genai')
def test_evaluate_and_adapt_puzzle_incorrect_solution(mock_genai):
    mock_response = MagicMock()
    mock_response.text = '{"is_correct": false, "feedback": "Try again.", "hint": "Look for patterns.", "difficulty_adjustment_suggestion": "none"}'
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    result = evaluate_and_adapt_puzzle(
        puzzle_id="test_puzzle",
        player_attempt="wrong answer",
        puzzle_solution="correct answer",
        current_puzzle_state={},
        current_puzzle_description="A test puzzle.", # New argument
        theme="fantasy",
        location="forest",
        difficulty="medium",
    )

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    assert result["is_correct"] is False
    assert result["feedback"] == "Try again."
    assert result["hint"] == "Look for patterns."

@patch('services.ai_service.genai')
def test_evaluate_and_adapt_puzzle_api_error(mock_genai):
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("Adaptation API Error")

    result = evaluate_and_adapt_puzzle(
        puzzle_id="test_puzzle",
        player_attempt="some attempt",
        puzzle_solution="solution",
        current_puzzle_state={},
        current_puzzle_description="A test puzzle.", # New argument
        theme="fantasy",
        location="forest",
        difficulty="medium",
    )

    assert "error" in result
    assert "Could not evaluate and adapt puzzle. Adaptation API Error" in result["error"]

@patch('services.ai_service.genai')
def test_evaluate_and_adapt_puzzle_prompt_content(mock_genai):
    mock_response = MagicMock()
    mock_response.text = '{"is_correct": true, "feedback": "Prompt content tested."}'
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    puzzle_id = "test_puzzle_123"
    player_attempt = "my attempt"
    puzzle_solution = "the correct solution"
    current_puzzle_state = {"attempts": 2, "hints_given": 1}
    current_puzzle_description = "A very descriptive puzzle here." # New argument
    theme = "sci-fi"
    location = "spaceship"
    difficulty = "hard"
    narrative_archetype = "mystery"

    evaluate_and_adapt_puzzle(
        puzzle_id=puzzle_id,
        player_attempt=player_attempt,
        puzzle_solution=puzzle_solution,
        current_puzzle_state=current_puzzle_state,
        current_puzzle_description=current_puzzle_description, # New argument
        theme=theme,
        location=location,
        difficulty=difficulty,
        narrative_archetype=narrative_archetype,
    )

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
    
    # Get the prompt argument passed to generate_content
    call_args, _ = mock_genai.GenerativeModel.return_value.generate_content.call_args
    prompt = call_args[0]

    assert f"Puzzle ID: {puzzle_id}" in prompt
    assert f"Correct Solution: {puzzle_solution}" in prompt
    assert f"Player's Attempt: {player_attempt}" in prompt
    assert f"Current Puzzle State: {current_puzzle_state}" in prompt
    assert f"Current Puzzle Description: {current_puzzle_description}" in prompt
    assert f"Theme: {theme}" in prompt
    assert f"Location: {location}" in prompt
    assert f"Difficulty: {difficulty}" in prompt
    assert f"Narrative Archetype: {NARRATIVE_ARCHETYPES[narrative_archetype]['name']}" in prompt
    assert "Evaluate their attempt and provide feedback" in prompt
    assert '"is_correct": boolean' in prompt
    
@patch('services.ai_service.genai')
def test_adjust_difficulty_based_on_performance_success(mock_genai):
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "difficulty_adjustment": "easier",
        "reasoning": "Player struggled with previous puzzle, suggest simpler mechanics.",
        "suggested_puzzle_parameters": {"complexity": "low", "hint_frequency": "high"}
    })
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    puzzle_state = {"puzzle1": {"attempts": 5, "hints_used": 2}}
    theme = "fantasy"
    location = "forest"
    overall_difficulty = "medium"
    narrative_archetype = "heros_journey"

    result = adjust_difficulty_based_on_performance(
        puzzle_state=puzzle_state,
        theme=theme,
        location=location,
        overall_difficulty=overall_difficulty,
        narrative_archetype=narrative_archetype,
    )

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()

    assert result["difficulty_adjustment"] == "easier"
    assert "Player struggled" in result["reasoning"]


@patch('services.ai_service.genai')
def test_adjust_difficulty_based_on_performance_prompt_content(mock_genai):
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "difficulty_adjustment": "no_change",
        "reasoning": "No adjustment needed.",
        "suggested_puzzle_parameters": {}
    })
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

    puzzle_state = {"puzzle1": {"attempts": 1, "hints_used": 0}}
    theme = "sci-fi"
    location = "moon_base"
    overall_difficulty = "hard"
    narrative_archetype = "mystery"

    adjust_difficulty_based_on_performance(
        puzzle_state=puzzle_state,
        theme=theme,
        location=location,
        overall_difficulty=overall_difficulty,
        narrative_archetype=narrative_archetype,
    )

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()

    call_args, _ = mock_genai.GenerativeModel.return_value.generate_content.call_args
    prompt = call_args[0]

    assert "Player Performance Metrics (puzzle_state):" in prompt
    assert f'"puzzle1": {{' in prompt # Check for start of puzzle1 metrics
    assert f'"attempts": 1' in prompt
    assert f'"hints_used": 0' in prompt
    assert f"Theme: {theme}" in prompt
    assert f"Location: {location}" in prompt
    assert f"Overall Difficulty: {overall_difficulty}" in prompt
    assert f"Narrative Archetype: {NARRATIVE_ARCHETYPES[narrative_archetype]['name']}" in prompt
    assert "recommend a subtle adjustment to the difficulty" in prompt
    assert '"difficulty_adjustment": string' in prompt


@patch('services.ai_service.genai')
def test_adjust_difficulty_based_on_performance_api_error(mock_genai):
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("Difficulty Adjustment API Error")

    puzzle_state = {"puzzle1": {"attempts": 1, "hints_used": 0}}
    theme = "fantasy"
    location = "forest"
    overall_difficulty = "medium"

    result = adjust_difficulty_based_on_performance(
        puzzle_state=puzzle_state,
        theme=theme,
        location=location,
        overall_difficulty=overall_difficulty,
    )

    assert "error" in result
    assert "Could not adjust difficulty. Difficulty Adjustment API Error" in result["error"]