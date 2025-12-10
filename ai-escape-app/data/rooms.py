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
    "sci-fi_hangar": { # New room/theme
        "name": "Sci-Fi Hangar",
        "description": "The vast space hums with the dormant power of starships. Metallic walls gleam under the faint, blue emergency lights.",
        "image": "scifi_hangar.jpg",
        "puzzles": {
            "console_puzzle": {
                "description": "A deactivated console displays a series of cryptic symbols. Input the sequence to power up.",
                "solution": "ALPHA7",
                "solved": False
            }
        },
        "exits": {"east": "underwater_lab"}
    },
    "underwater_lab": { # New room/theme
        "name": "Underwater Laboratory",
        "description": "The deep blue light filters through thick portholes, revealing strange marine life outside. Bubbles gently rise from complex machinery.",
        "image": "underwater_lab.jpg",
        "puzzles": {
            "pressure_puzzle": {
                "description": "A pressure gauge needs recalibration. Adjust the three dials to match the deep-sea pressure reading: 5-2-8.",
                "solution": "528",
                "solved": False
            }
        },
        "exits": {"west": "sci-fi_hangar"}
    },
    "abandoned_mansion": {
        "name": "Abandoned Mansion",
        "description": "Dust motes dance in sunbeams piercing the grimy windows of a once-grand hall. Cobwebs drape from chandeliers like tattered lace.",
        "image": "Abandiond Mansion.jpg", # Corrected image name
        "puzzles": {
            "mansion_riddle": {
                "description": "I have a heart, but cannot love. I have a mouth, but cannot speak. I have a house, but cannot live. What am I?",
                "solution": "bell",
                "solved": False
            }
        },
        "exits": {"north": "hidden_attic"} # Placeholder exit
    },
    "ancient_tomb": {
        "name": "Ancient Tomb",
        "description": "Hieroglyphs cover every inch of the cold stone walls. The air is dry and smells of dust and ancient rituals. A massive sarcophagus dominates the center.",
        "image": "ancient Tomb.jpg", # Corrected image name
        "puzzles": {
            "hieroglyph_puzzle": {
                "description": "Arrange the ancient tiles to reveal the name of the forgotten pharaoh.",
                "solution": "RAMSES",
                "solved": False
            }
        },
        "exits": {"south": "oasis_ruins"} # Placeholder exit
    }
}

# Define solution mapping for puzzles
PUZZLE_SOLUTIONS = {
    "observation_puzzle": "3",
    "riddle_puzzle": "map",
    "console_puzzle": "ALPHA7",
    "pressure_puzzle": "528",
    "mansion_riddle": "bell",
    "hieroglyph_puzzle": "RAMSES",
}