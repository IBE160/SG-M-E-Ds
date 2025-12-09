import pytest
from data.help_content import HELP_CONTENT

def test_help_content_structure():
    """
    Tests the basic structure and presence of expected sections in HELP_CONTENT.
    """
    assert isinstance(HELP_CONTENT, dict)
    assert "how_to_play" in HELP_CONTENT
    assert "current_objective" in HELP_CONTENT
    assert "game_controls" in HELP_CONTENT
    assert "general_tips" in HELP_CONTENT

    for section_key, section_data in HELP_CONTENT.items():
        assert isinstance(section_data, dict)
        assert "title" in section_data
        assert isinstance(section_data["title"], str)
        assert "content" in section_data
        assert isinstance(section_data["content"], list)
        assert len(section_data["content"]) > 0
        for paragraph in section_data["content"]:
            assert isinstance(paragraph, str)

def test_help_content_how_to_play_details():
    """
    Tests specific content within the "how_to_play" section.
    """
    how_to_play = HELP_CONTENT["how_to_play"]
    assert how_to_play["title"] == "How to Play AI Escape"
    assert "explore mysterious rooms" in how_to_play["content"][1]

def test_help_content_game_controls_details():
    """
    Tests specific content within the "game_controls" section.
    """
    game_controls = HELP_CONTENT["game_controls"]
    assert game_controls["title"] == "Game Controls"
    assert "Click 'Save Game'" in game_controls["content"][4]
