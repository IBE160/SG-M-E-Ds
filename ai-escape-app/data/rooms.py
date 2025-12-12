# data/rooms.py

ROOM_DATA = {
    "forgotten_library": {
        "start_room": "forgotten_library_entrance",
        "rooms": {
            "forgotten_library_entrance": {
                "name": "Forgotten Library Entrance",
                "description": "A musty, silent library, long untouched. Bookshelves filled with decaying volumes line the walls, and dust motes dance in the faint light. There's a grand entrance.",
                "image": "forgotten_library.jpg",
                "puzzles": {},
                "exits": {"north": "forgotten_library_study"},
            },
            "forgotten_library_study": {
                "name": "Forgotten Library Study",
                "description": "A small, secluded study within the library, filled with rare manuscripts and a single, locked desk.",
                "image": "forgotten_library.jpg", # Reusing image
                "puzzles": {
                    "desk_puzzle": {
                        "description": "The desk has an intricate lock. A note nearby reads: 'The number of forgotten tales.'",
                        "solution": "7",
                        "solved": False
                    }
                },
                "exits": {"south": "forgotten_library_entrance", "east": "forgotten_library_escape_chamber"},
            },
            "forgotten_library_escape_chamber": {
                "name": "Forgotten Library Exit",
                "description": "You've found the secret exit from the Forgotten Library!",
                "image": "forgotten_library.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "sci_fi_hangar": {
        "start_room": "sci-fi_hangar_main",
        "rooms": {
            "sci-fi_hangar_main": {
                "name": "Sci-Fi Hangar Main",
                "description": "The vast space hums with the dormant power of starships. Metallic walls gleam under the faint, blue emergency lights. A control console stands at one end.",
                "image": "scifi_hangar.jpg",
                "puzzles": {
                    "console_puzzle": {
                        "description": "A deactivated console displays a series of cryptic symbols. Input the sequence to power up.",
                        "solution": "ALPHA7",
                        "solved": False
                    }
                },
                "exits": {"east": "sci-fi_hangar_storage"},
            },
            "sci-fi_hangar_storage": {
                "name": "Sci-Fi Hangar Storage",
                "description": "Rows of crates and old equipment. A heavy door leads further into the facility.",
                "image": "scifi_hangar.jpg",
                "puzzles": {},
                "exits": {"west": "sci-fi_hangar_main", "north": "sci_fi_hangar_escape_chamber"},
            },
            "sci_fi_hangar_escape_chamber": {
                "name": "Sci-Fi Hangar Escape Pods",
                "description": "You've reached the escape pods! Prepare for launch!",
                "image": "scifi_hangar.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "underwater_lab": {
        "start_room": "underwater_lab_entrance",
        "rooms": {
            "underwater_lab_entrance": {
                "name": "Underwater Laboratory Entrance",
                "description": "The deep blue light filters through thick portholes, revealing strange marine life outside. Bubbles gently rise from complex machinery.",
                "image": "underwater_lab.jpg",
                "puzzles": {
                    "pressure_puzzle": {
                        "description": "A pressure gauge needs recalibration. Adjust the three dials to match the deep-sea pressure reading: 5-2-8.",
                        "solution": "528",
                        "solved": False
                    }
                },
                "exits": {"north": "underwater_lab_biolabs"},
            },
            "underwater_lab_biolabs": {
                "name": "Underwater Laboratory Biolabs",
                "description": "Tanks with glowing specimens and complex life support systems. The hum of the lab is constant.",
                "image": "underwater_lab.jpg",
                "puzzles": {},
                "exits": {"south": "underwater_lab_entrance", "east": "underwater_lab_escape_chamber"},
            },
            "underwater_lab_escape_chamber": {
                "name": "Underwater Laboratory Exit",
                "description": "You've found the escape hatch from the Underwater Laboratory!",
                "image": "underwater_lab.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "spaceship": {
        "start_room": "spaceship_bridge",
        "rooms": {
            "spaceship_bridge": {
                "name": "Derelict Spaceship Bridge",
                "description": "The metallic silence of a derelict spaceship. Flickering emergency lights cast long shadows over control panels and abandoned cryogenic pods. The main viewscreen is dark.",
                "image": "spaceship.jpg",
                "puzzles": {},
                "exits": {"south": "spaceship_engine_room"},
            },
            "spaceship_engine_room": {
                "name": "Derelict Spaceship Engine Room",
                "description": "Massive, inert engines fill the room. Wires hang loosely, and the air smells faintly of burnt ozone. A small, service hatch is visible.",
                "image": "spaceship.jpg",
                "puzzles": {
                    "engine_puzzle": {
                        "description": "The diagnostic panel shows three critical relays offline. Restore power by inputting the correct sequence: Delta-Gamma-Epsilon.",
                        "solution": "DGE",
                        "solved": False
                    }
                },
                "exits": {"north": "spaceship_bridge", "west": "spaceship_escape_chamber"},
            },
            "spaceship_escape_chamber": {
                "name": "Derelict Spaceship Escape Hatch",
                "description": "You've activated the emergency escape hatch! Freedom!",
                "image": "spaceship.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "clown_funhouse": {
        "start_room": "clown_funhouse_entrance",
        "rooms": {
            "clown_funhouse_entrance": {
                "name": "Clown's Funhouse Entrance",
                "description": "Loud, garish colors assault your eyes, and the unsettling scent of stale popcorn fills the air. Mannequins with painted smiles leer from every corner. A giant inflatable clown guards the way.",
                "image": "clown_funhouse.jpg",
                "puzzles": {},
                "exits": {"north": "clown_funhouse_mirror_maze"},
            },
            "clown_funhouse_mirror_maze": {
                "name": "Clown's Funhouse Mirror Maze",
                "description": "An endless labyrinth of distorted reflections. Laughter echoes eerily, making it hard to tell reality from illusion.",
                "image": "clown_funhouse.jpg",
                "puzzles": {
                    "maze_puzzle": {
                        "description": "Find the true path through the maze. The riddle on the wall says: 'I have many faces, but only one is true.'",
                        "solution": "truth",
                        "solved": False
                    }
                },
                "exits": {"south": "clown_funhouse_entrance", "east": "clown_funhouse_escape_chamber"},
            },
            "clown_funhouse_escape_chamber": {
                "name": "Clown's Funhouse Exit",
                "description": "You've found the way out of this hilarious (and terrifying) funhouse!",
                "image": "clown_funhouse.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "kids_room": {
        "start_room": "kids_room_play_area",
        "rooms": {
            "kids_room_play_area": {
                "name": "The Oversized Playroom",
                "description": "Giant building blocks and a towering teddy bear dominate this room. Everything feels strangely out of proportion.",
                "image": "kids_room.jpg",
                "puzzles": {},
                "exits": {"east": "kids_room_toy_chest"},
            },
            "kids_room_toy_chest": {
                "name": "The Toy Chest Corner",
                "description": "A massive, overflowing toy chest sits in the corner. It seems to hold the key to an exit.",
                "image": "kids_room.jpg", # Reusing image
                "puzzles": {
                    "toy_puzzle": {
                        "description": "Arrange the colored blocks in the order of the rainbow: Red, Orange, Yellow, Green, Blue, Indigo, Violet.",
                        "solution": "ROYGBIV",
                        "solved": False
                    }
                },
                "exits": {"west": "kids_room_play_area", "north": "kids_room_escape_chamber"},
            },
            "kids_room_escape_chamber": {
                "name": "Kids Room Exit",
                "description": "You've found a hidden slide leading out of the oversized playroom!",
                "image": "kids_room.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "candy_wonderland": {
        "start_room": "candy_wonderland_path",
        "rooms": {
            "candy_wonderland_path": {
                "name": "Candy Wonderland Path",
                "description": "A dazzling landscape made entirely of sweets. Lollipops form trees, rivers flow with chocolate, and gingerbread houses stand on hills of ice cream.",
                "image": "candy_wonderland.jpg",
                "puzzles": {},
                "exits": {"north": "candy_wonderland_gingerbread_house"},
            },
            "candy_wonderland_gingerbread_house": {
                "name": "Candy Wonderland Gingerbread House",
                "description": "A house built of gingerbread and frosting, with gumdrop windows and candy cane pillars. It smells delicious!",
                "image": "candy_wonderland.jpg", # Reusing image
                "puzzles": {
                    "gingerbread_puzzle": {
                        "description": "The frosting on the door forms a sequence: 1-2-3-5-8. What's next?",
                        "solution": "13",
                        "solved": False
                    }
                },
                "exits": {"south": "candy_wonderland_path", "west": "candy_wonderland_escape_chamber"},
            },
            "candy_wonderland_escape_chamber": {
                "name": "Candy Wonderland Exit",
                "description": "You've found a secret path made of candy leading out of Wonderland!",
                "image": "candy_wonderland.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "abandoned_mansion": {
        "start_room": "mansion_foyer",
        "rooms": {
            "mansion_foyer": {
                "name": "Abandoned Mansion Foyer",
                "description": "Dust motes dance in sunbeams piercing the grimy windows of a once-grand hall. Cobwebs drape from chandeliers like tattered lace. A grand staircase leads upstairs.",
                "image": "abandoned_mansion.jpg",
                "puzzles": {
                    "mansion_riddle": {
                        "description": "I have a heart, but cannot love. I have a mouth, but cannot speak. I have a house, but cannot live. What am I?",
                        "solution": "bell",
                        "solved": False
                    }
                },
                "exits": {"north": "mansion_library"},
            },
            "mansion_library": {
                "name": "Abandoned Mansion Library",
                "description": "Shelves of decaying books fill this room, the silence broken only by the creaks of the old house. A fireplace holds cold ashes.",
                "image": "abandoned_mansion.jpg",
                "puzzles": {},
                "exits": {"south": "mansion_foyer", "west": "abandoned_mansion_escape_chamber"},
            },
            "abandoned_mansion_escape_chamber": {
                "name": "Abandoned Mansion Secret Passage",
                "description": "You found a secret passage leading out of the mansion!",
                "image": "abandoned_mansion.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "ancient_tomb": {
        "start_room": "tomb_entrance",
        "rooms": {
            "tomb_entrance": {
                "name": "Ancient Tomb Entrance",
                "description": "Hieroglyphs cover every inch of the cold stone walls. The air is dry and smells of dust and ancient rituals. A massive sarcophagus dominates the center.",
                "image": "ancient_tomb.jpg",
                "puzzles": {
                    "hieroglyph_puzzle": {
                        "description": "Arrange the ancient tiles to reveal the name of the forgotten pharaoh.",
                        "solution": "RAMSES",
                        "solved": False
                    }
                },
                "exits": {"west": "tomb_chamber"},
            },
            "tomb_chamber": {
                "name": "Ancient Tomb Chamber",
                "description": "A hidden chamber, darker and colder than the entrance. Strange artifacts rest on pedestals, and a faint hum can be heard.",
                "image": "ancient_tomb.jpg", # Reusing image
                "puzzles": {},
                "exits": {"east": "tomb_entrance", "north": "ancient_tomb_escape_chamber"},
            },
            "ancient_tomb_escape_chamber": {
                "name": "Ancient Tomb Secret Exit",
                "description": "You've unearthed a hidden passage out of the tomb!",
                "image": "ancient_tomb.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
    "asylum": {
        "start_room": "asylum_reception",
        "rooms": {
            "asylum_reception": {
                "name": "Abandoned Asylum Reception",
                "description": "A chilling silence hangs heavy in the air of this abandoned asylum. Rusty medical equipment lies scattered, hinting at past horrors. The reception desk is covered in dust.",
                "image": "asylum.jpg",
                "puzzles": {},
                "exits": {"north": "asylum_wards"},
            },
            "asylum_wards": {
                "name": "Abandoned Asylum Wards",
                "description": "Long corridors lined with empty patient rooms. The air is heavy with despair, and shadows seem to dance at the edge of your vision.",
                "image": "asylum.jpg", # Reusing image
                "puzzles": {
                    "patient_files_puzzle": {
                        "description": "A set of patient files are scattered. Find the file marked with a broken key icon and read the three-digit code: 4-8-2.",
                        "solution": "482",
                        "solved": False
                    }
                },
                "exits": {"south": "asylum_reception", "east": "asylum_escape_chamber"},
            },
            "asylum_escape_chamber": {
                "name": "Abandoned Asylum Exit",
                "description": "You've found a way to slip out of the haunted asylum!",
                "image": "asylum.jpg", # Reusing image
                "puzzles": {},
                "exits": {},
            },
        }
    },
}

# Define solution mapping for puzzles
PUZZLE_SOLUTIONS = {
    "desk_puzzle": "7",
    "console_puzzle": "ALPHA7",
    "pressure_puzzle": "528",
    "engine_puzzle": "DGE",
    "maze_puzzle": "truth",
    "toy_puzzle": "ROYGBIV",
    "gingerbread_puzzle": "13",
    "mansion_riddle": "bell",
    "hieroglyph_puzzle": "RAMSES",
    "patient_files_puzzle": "482",
}
