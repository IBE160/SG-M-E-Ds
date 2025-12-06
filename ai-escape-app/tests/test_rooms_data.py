import pytest
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS


def test_room_data_structure():
    assert isinstance(ROOM_DATA, dict)
    assert len(ROOM_DATA) == 3

    for room_id, room_info in ROOM_DATA.items():
        assert "name" in room_info
        assert "description" in room_info
        assert "puzzles" in room_info
        assert isinstance(room_info["puzzles"], dict)
        assert "exits" in room_info
        assert isinstance(room_info["exits"], dict)

def test_specific_room_data():
    # Test ancient_library
    library = ROOM_DATA.get("ancient_library")
    assert library is not None
    assert library["name"] == "Ancient Library"
    assert "observation_puzzle" in library["puzzles"]
    assert library["puzzles"]["observation_puzzle"]["solution"] == "3"
    assert library["exits"] == {"north": "mysterious_observatory"}

    # Test mysterious_observatory
    observatory = ROOM_DATA.get("mysterious_observatory")
    assert observatory is not None
    assert observatory["name"] == "Mysterious Observatory"
    assert "riddle_puzzle" in observatory["puzzles"]
    assert observatory["puzzles"]["riddle_puzzle"]["solution"] == "map"
    assert observatory["exits"] == {"south": "ancient_library", "east": "escape_chamber"}

    # Test escape_chamber
    chamber = ROOM_DATA.get("escape_chamber")
    assert chamber is not None
    assert chamber["name"] == "Escape Chamber"
    assert chamber["puzzles"] == {}
    assert chamber["exits"] == {"west": "mysterious_observatory"}

def test_puzzle_solutions_mapping():
    assert isinstance(PUZZLE_SOLUTIONS, dict)
    assert PUZZLE_SOLUTIONS["observation_puzzle"] == "3"
    assert PUZZLE_SOLUTIONS["riddle_puzzle"] == "map"
