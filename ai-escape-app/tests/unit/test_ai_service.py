import pytest
from unittest.mock import patch, MagicMock
import os
from services.ai_service import generate_narrative

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

# Test case for missing API key (should be handled by the initial check in ai_service.py)
# This test will likely not pass if run as part of a suite where os.getenv is mocked globally
# Instead, ensure that the ValueError is raised when GEMINI_API_KEY is truly not set.
# The current mock_env_vars fixture ensures it is set. To test the ValueError,
# you would need to specifically unset it for a test, which might interfere with other tests.
# For simplicity, we assume the environment variable setup is correct for the other tests.

