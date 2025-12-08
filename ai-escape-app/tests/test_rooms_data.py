import pytest
from data.rooms import ROOM_DATA, PUZZLE_SOLUTIONS


def test_room_data_structure():
    assert isinstance(ROOM_DATA, dict)
    assert len(ROOM_DATA) == 5

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

    # Test sci-fi_hangar
    hangar = ROOM_DATA.get("sci-fi_hangar")
    assert hangar is not None
    assert hangar["name"] == "Sci-Fi Hangar"
    assert "console_puzzle" in hangar["puzzles"]
    assert hangar["puzzles"]["console_puzzle"]["solution"] == "ALPHA7"
    assert hangar["exits"] == {"east": "underwater_lab"}

    # Test underwater_lab
    lab = ROOM_DATA.get("underwater_lab")
    assert lab is not None
    assert lab["name"] == "Underwater Laboratory"
    assert "pressure_puzzle" in lab["puzzles"]
    assert lab["puzzles"]["pressure_puzzle"]["solution"] == "528"
    assert lab["exits"] == {"west": "sci-fi_hangar"}


def test_puzzle_solutions_mapping():
    assert isinstance(PUZZLE_SOLUTIONS, dict)
    assert PUZZLE_SOLUTIONS["observation_puzzle"] == "3"
    assert PUZZLE_SOLUTIONS["riddle_puzzle"] == "map"
    assert PUZZLE_SOLUTIONS["console_puzzle"] == "ALPHA7"
    assert PUZZLE_SOLUTIONS["pressure_puzzle"] == "528"


def test_room_images_exist():
    for room_id, room_info in ROOM_DATA.items():
        assert "image" in room_info
        assert isinstance(room_info["image"], str)
        assert room_info["image"].endswith(".jpg") or room_info["image"].endswith(".png")

def test_specific_room_images():
    assert ROOM_DATA["ancient_library"]["image"] == "ancient_library.jpg"
    assert ROOM_DATA["mysterious_observatory"]["image"] == "mysterious_observatory.jpg"
    assert ROOM_DATA["escape_chamber"]["image"] == "escape_chamber.jpg"
    assert ROOM_DATA["sci-fi_hangar"]["image"] == "scifi_hangar.jpg"
    assert ROOM_DATA["underwater_lab"]["image"] == "underwater_lab.jpg"