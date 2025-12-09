import pytest
from data.game_options import GAME_SETUP_OPTIONS

def test_game_setup_options_structure():
    """
    Test that GAME_SETUP_OPTIONS is a dictionary and contains expected keys.
    """
    assert isinstance(GAME_SETUP_OPTIONS, dict)
    expected_keys = ["themes", "locations", "puzzle_types", "difficulty_levels"]
    for key in expected_keys:
        assert key in GAME_SETUP_OPTIONS
        assert isinstance(GAME_SETUP_OPTIONS[key], list)

def test_game_setup_options_item_structure():
    """
    Test that each item in GAME_SETUP_OPTIONS lists has the correct structure (id, name, description).
    """
    expected_item_keys = ["id", "name", "description"]
    for category_list in GAME_SETUP_OPTIONS.values():
        for item in category_list:
            assert isinstance(item, dict)
            for key in expected_item_keys:
                assert key in item
                assert isinstance(item[key], str)

def test_expanded_options_present():
    """
    Test that the newly added expanded options are present.
    """
    # Themes
    theme_ids = [t["id"] for t in GAME_SETUP_OPTIONS["themes"]]
    assert "noir_detective" in theme_ids
    assert "steampunk_mystery" in theme_ids
    assert "post_apocalyptic" in theme_ids

    # Locations
    location_ids = [l["id"] for l in GAME_SETUP_OPTIONS["locations"]]
    assert "abandoned_mansion" in location_ids
    assert "futuristic_cityscape" in location_ids
    assert "ancient_tomb" in location_ids

    # Puzzle Types
    puzzle_type_ids = [p["id"] for p in GAME_SETUP_OPTIONS["puzzle_types"]]
    assert "musical" in puzzle_type_ids
    assert "pattern_recognition" in puzzle_type_ids
    assert "encryption" in puzzle_type_ids

    # Difficulty Levels
    difficulty_ids = [d["id"] for d in GAME_SETUP_OPTIONS["difficulty_levels"]]
    assert "insane" in difficulty_ids
