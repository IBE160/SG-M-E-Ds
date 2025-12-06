ROOM_DATA = {
    "ancient_library": {
        "name": "Ancient Library",
        "description": "Dusty shelves filled with forgotten tomes line the walls. A faint smell of old parchment hangs in the air. A grand, ornate desk sits in the center.",
        "image": "ancient_library.jpg", # New field
        "puzzles": {
            "observation_puzzle": {
                "description": "A cryptic inscription is carved into the desk: 'Seek the number in the stars, above the oldest knowledge.'",
                "solution": "3",  # Assuming '3' is a reasonable solution based on context
                "solved": False
            }
        },
        "exits": {"north": "mysterious_observatory"},
    },
    "mysterious_observatory": {
        "name": "Mysterious Observatory",
        "description": "A vast domed ceiling with a massive telescope pointed towards the heavens. Star charts are scattered across a wooden table.",
        "image": "mysterious_observatory.jpg", # New field
        "puzzles": {
            "riddle_puzzle": {
                "description": "I have cities, but no houses; forests, but no trees; and water, but no fish. What am I?",
                "solution": "map",
                "solved": False
            }
        },
        "exits": {"south": "ancient_library", "east": "escape_chamber"},
    },
    "escape_chamber": {
        "name": "Escape Chamber",
        "description": "A small, circular room with a single, heavy steel door. A complex lock mechanism is built into the door.",
        "image": "escape_chamber.jpg", # New field
        "puzzles": {}, # No puzzle here yet, it's the final room
        "exits": {"west": "mysterious_observatory"},
    },
}

# Define solution mapping for puzzles
PUZZLE_SOLUTIONS = {
    "observation_puzzle": "3",
    "riddle_puzzle": "map",
}
