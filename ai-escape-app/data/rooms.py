# data/rooms.py

# IMPORTANT NOTE ON PUZZLE STRUCTURE:
# While this ROOM_DATA defines initial 'puzzles' with a 'description' and a 'solution',
# the actual puzzle progression, hints, and dynamic adaptation are managed by the
# AI service (ai_service.py) and stored within the GameSession's 'puzzle_state'
# in game_logic.py.
#
# The 'solution' provided here should be considered the correct input for the
# initial step of the puzzle, or the ultimate solution if it's a single-step puzzle.
# The AI will interpret this solution, evaluate player attempts against it,
# provide feedback, and guide multi-step puzzles, updating the dynamic
# 'puzzle_state' in the game session accordingly.

ROOM_DATA = {
    "forgotten_library": {
        "intro_story": "You awaken to a throbbing headache and the smell of damp earth. Your eyes flutter open to reveal a dimly lit, circular chamber carved from rough, ancient stone. A low, guttural hum vibrates through the floor, a constant, unsettling presence. Your last memory is a hushed whisper about a lost artifact, now believed to be hidden deep within these forbidden crypts. To escape, you must find the legendary 'Whispering Amulet' and bring its power to light. The air is heavy with history and a palpable sense of dread.",
        "start_room": "forgotten_library_entrance",
        "rooms": {
            "forgotten_library_entrance": {
                "name": "Forgotten Library Entrance",
                "description": "The antechamber is perfectly circular, its walls smooth but for the occasional rough-hewn symbol. The only source of light comes from a flickering, ethereal glow emanating from a heavy, iron-banded door directly opposite where you lay. A small, overturned stone bench lies near the wall to your left, its surface covered in a fine layer of dust. The hum feels strongest here, almost vibrating your teeth.",
                "image": "forgotten_library.jpg",
                "puzzles": {
                    "ancient_symbol_door_puzzle": {
                        "name": "Ancient Symbol Door Puzzle",
                        "description": "The heavy door is sealed by an intricate glowing symbol, an eye weeping three tears, etched into its surface. To open it, you must decipher the correct sequence of symbols.",
                        "solution": "EYETEARS", # Placeholder solution for now
                        "type": "symbol_sequence",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["forgotten_library_entrance_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": ["old_key"],
                "interactables": {
                    "heavy_door": {
                        "name": "Heavy Door",
                        "description": "A heavy, iron-banded door, emitting a faint glow.",
                        "actions": [
                            {
                                "label": "Inspect Door",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "ancient_symbol_door_puzzle",
                                    "message": "You inspect the heavy door, revealing an ancient symbol puzzle."
                                }
                            }
                        ]
                    },
                    "humming_floor": {
                        "name": "Humming Floor",
                        "description": "The floor beneath your feet vibrates with a persistent hum.",
                        "actions": [
                            {
                                "label": "Listen Hum",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The rhythmic hum is definitely mechanical, but intertwined with a faint, almost melodic whisper that seems to be just beyond your hearing. It feels like it's coming from *under* the door.",
                                    "message": "You focus on the unsettling hum."
                                }
                            }
                        ]
                    },
                    "stone_bench": {
                        "name": "Overturned Stone Bench",
                        "description": "A small, overturned stone bench.",
                        "actions": [
                            {
                                "label": "Check Bench",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The bench is heavy and seems fixed to the floor. Underneath it, you find a small, petrified sliver of wood, barely visible in the gloom. It looks like it might have been part of something larger.",
                                    "message": "You check the stone bench."
                                }
                            }
                        ]
                    }
                },
                "exits": {"north": "forgotten_library_study"},
            },
            "forgotten_library_study": {
                "name": "Forgotten Library Study",
                "description": "A small, secluded study within the library, filled with rare manuscripts and a single, locked desk.",
                "image": "forgotten_library.jpg", # Reusing image
                "puzzles": {
                    "desk_puzzle": {
                        "name": "Locked Desk Drawer",
                        "description": "The desk has an intricate lock. A note nearby reads: 'The number of forgotten tales.' You need a numeric code to open it.",
                        "solution": "7", # Original solution
                        "type": "code_entry",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["desk_drawer_open", "old_journal_found"],
                        "reveal_on_solve": ["old_journal"],
                        "triggers_event": "reveal_desk_content"
                    }
                },
                "items": [],
                "interactables": {
                    "desk_puzzle": { # Changed name to desk_lock for clarity
                        "name": "Intricate Desk Lock",
                        "description": "A grand wooden desk with an intricate lock.",
                        "actions": [
                            {
                                "label": "Inspect Desk",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "desk_puzzle",
                                    "message": "You inspect the intricate lock on the desk."
                                }
                            }
                        ]
                    },
                    "manuscript": {
                        "name": "Ancient Manuscript",
                        "description": "A fragile, leather-bound manuscript resting on a pedestal. It seems very old.",
                        "actions": [
                            {
                                "label": "Inspect Manuscript",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The manuscript is written in an archaic script, filled with astrological charts and cryptic prophecies. One page highlights a constellation resembling the 'Eye' symbol from the entrance door, surrounded by three distinct stars. This might be a clue for the door puzzle.",
                                    "message": "You carefully read the ancient manuscript."
                                }
                            }
                        ]
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
        "intro_story": "A jarring klaxon blares, echoing off polished chrome and blinking control panels. You bolt upright in the pilot's chair, a dull ache behind your eyes, and a frantic voice crackling over the comms: 'Bridge! We've lost primary power! Containment breach in Engineering! Get us out of here!' Your ship, the 'Stardust Wanderer', is plummeting towards an uncharted planet. Your mission: restore emergency power and jump to hyperspace before the ship breaks apart. The bridge is alive with flashing red lights and the smell of ozone.",
        "start_room": "sci-fi_hangar_main",
        "rooms": {
            "sci-fi_hangar_main": {
                "name": "Sci-Fi Hangar Main",
                "description": "The main command deck is a semicircle of glowing screens and intricate consoles. Your pilot's chair is central, facing the vast viewport that now shows swirling clouds of gas and rock. To your left, a navigation console blinks frantically with error messages. To your right, a communication station hisses static. Behind you, a large, heavy door with an illuminated 'ENGINEERING' sign is sealed shut, flickering between red and yellow.",
                "image": "scifi_hangar.jpg",
                "puzzles": {
                    "console_puzzle": {
                        "name": "Hangar Console Power-Up",
                        "description": "A deactivated console displays a series of cryptic symbols. Input the correct sequence to power up the hangar's main systems.",
                        "solution": "ALPHA7",
                        "type": "code_entry",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["hangar_power_restored", "engineering_door_power_online"],
                        "reveal_on_solve": [],
                        "triggers_event": "power_hangar_systems"
                    },
                    "engineering_door_lock": {
                        "name": "Engineering Door Lock",
                        "description": "The heavy engineering door is sealed. A digital keypad next to it requires a 4-digit access code.",
                        "solution": "1987", # Placeholder solution
                        "type": "code_entry",
                        "difficulty": "easy",
                        "prerequisites": ["hangar_power_restored"],
                        "outcomes": ["engineering_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_engineering_access"
                    }
                },
                "items": [],
                "interactables": {
                    "navigation_console": {
                        "name": "Navigation Console",
                        "description": "A console blinking frantically with error messages.",
                        "actions": [
                            {
                                "label": "Check Navigation",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "console_puzzle",
                                    "message": "You inspect the navigation console, realizing it needs to be powered up."
                                }
                            }
                        ]
                    },
                    "communication_station": {
                        "name": "Communication Station",
                        "description": "A communication station hissing static.",
                        "actions": [
                            {
                                "label": "Access Comms",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The comms system is mostly dead, but you pick up faint, distorted emergency broadcasts: '...containment... unstable... core meltdown imminent...' The frequency dial is stuck on a single, urgent channel.",
                                    "message": "You attempt to access the communication station."
                                }
                            }
                        ]
                    },
                    "engineering_door": {
                        "name": "Engineering Door",
                        "description": "A large, heavy door with an illuminated 'ENGINEERING' sign, flickering between red and yellow.",
                        "actions": [
                            {
                                "label": "Open Engineering",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "engineering_door_lock",
                                    "message": "You try to open the Engineering door, finding it locked by a keypad."
                                }
                            }
                        ]
                    },
                    "pilot_controls": {
                        "name": "Pilot Controls",
                        "description": "The main pilot's controls.",
                        "actions": [
                            {
                                "label": "Pilot Controls",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The joystick is unresponsive. All primary flight functions are dark. A small, unlabeled button on the side of the console glows faintly, pulsing with a weak, blue light. It feels strangely warm.",
                                    "message": "You examine the pilot controls."
                                }
                            }
                        ]
                    }
                }, # ADDED COMMA HERE
                "exits": {"east": "sci-fi_hangar_storage"}, # ADDED COMMA HERE
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
        "intro_story": "The crushing pressure of the deep sea is palpable even through the reinforced walls of the laboratory. You find yourself disoriented in a glowing, subaquatic station, alarms faintly blaring. A holographic message flickers, warning of a critical system failure and imminent implosion. Your only chance of survival is to reactivate the primary containment field before the structure gives way. The deep blue light filtering through thick portholes reveals strange marine life, indifferent to your plight.",
        "start_room": "underwater_lab_entrance",
        "rooms": {
            "underwater_lab_entrance": {
                "name": "Underwater Laboratory Entrance",
                "description": "You are in the main observation deck. Thick, reinforced portholes offer a panoramic view of the abyssal trench, illuminated by the lab's powerful external lights. Bubbles gently rise from complex, alien machinery embedded in the walls. A main control console with flickering lights is directly in front of you.",
                "image": "underwater_lab.jpg",
                "puzzles": {
                    "pressure_puzzle": {
                        "name": "Containment Field Recalibration",
                        "description": "A pressure gauge needs recalibration to stabilize the containment field. Adjust the three dials to match the deep-sea pressure reading: 5-2-8.",
                        "solution": "528",
                        "type": "code_entry",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["containment_field_stabilized"],
                        "reveal_on_solve": [],
                        "triggers_event": "stabilize_containment"
                    }
                },
                "items": [],
                "interactables": {
                    "control_console": {
                        "name": "Main Control Console",
                        "description": "A main control console with flickering lights.",
                        "actions": [
                            {
                                "label": "Inspect Console",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "pressure_puzzle",
                                    "message": "You inspect the main control console, revealing the containment field recalibration puzzle."
                                }
                            }
                        ]
                    },
                    "portholes": {
                        "name": "Thick Portholes",
                        "description": "Thick, reinforced portholes offering a view of the abyssal trench.",
                        "actions": [
                            {
                                "label": "Observe Portholes",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "Through the portholes, massive, bioluminescent creatures glide past, their eyes seeming to peer directly into the lab. The trench outside is a vast, inky blackness, hinting at unimaginable depths and dangers. A faint, almost imperceptible tremor occasionally shakes the glass.",
                                    "message": "You observe the portholes."
                                }
                            }
                        ]
                    },
                    "rising_bubbles": {
                        "name": "Rising Bubbles",
                        "description": "Bubbles gently rise from complex machinery embedded in the walls.",
                        "actions": [
                            {
                                "label": "Examine Bubbles",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The bubbles are oddly uniform in size and rise from tiny vents in the alien machinery. They don't appear to be leaks, but rather part of the system's normal operation, perhaps venting excess pressure or heat. A faint, sweet chemical odor emanates from them.",
                                    "message": "You examine the rising bubbles."
                                }
                            }
                        ]
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
        "intro_story": "A sudden, violent shudder rattles your hibernation pod, jolting you awake. The emergency lights of the 'Star-Drifter' flash erratically, painting the observation deck in hues of crimson and shadow. The ship's AI, a monotone voice in your ear, announces, 'Critical systems failure. Life support failing. Initiate emergency core reboot or perish.' Your mission: navigate the derelict vessel, restore power to the core, and get out before the oxygen runs out. The cold, metallic silence is punctuated by the rhythmic, agonizing groan of stressed bulkheads.",
        "start_room": "spaceship_bridge",
        "rooms": {
            "spaceship_bridge": {
                "name": "Derelict Spaceship Bridge",
                "description": "The metallic silence of a derelict spaceship. Flickering emergency lights cast long shadows over dead control panels and abandoned cryogenic pods. The main viewscreen is dark, showing only your own reflection. Your pilot's console, though mostly inert, has a single, blinking red button labeled 'Emergency Power Override'.",
                "image": "spaceship.jpg",
                "puzzles": {
                    "diagnostic_panel_puzzle": {
                        "name": "Pilot Console Diagnostic",
                        "description": "The diagnostic panel flickers, showing 'Core Power: Offline', 'Life Support: Critical', and 'Hyperdrive: Offline'. A sequence of three colored lights needs to be activated in the correct order to bring systems online.",
                        "solution": "REDGREENBLUE", # Placeholder solution
                        "type": "sequence_input",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["core_power_online", "life_support_online"],
                        "reveal_on_solve": [],
                        "triggers_event": "restore_bridge_power"
                    },
                    "cryo_pod_datapads_puzzle": {
                        "name": "Cryo-Pod Data-Pad",
                        "description": "One pod has a data-pad wedged in its control panel. Its screen is cracked but emits a faint, greenish glow, displaying corrupted log entries. Decipher the passcode to access crew logs.",
                        "solution": "08675309", # Placeholder solution
                        "type": "code_entry",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["crew_logs_accessed"],
                        "reveal_on_solve": ["security_keycard"],
                        "triggers_event": "reveal_security_keycard"
                    }
                },
                "items": [],
                "interactables": {
                    "pilot_console": {
                        "name": "Pilot Console",
                        "description": "Your pilot's console, mostly inert.",
                        "actions": [
                            {
                                "label": "Inspect Console",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "diagnostic_panel_puzzle",
                                    "message": "You inspect the pilot console, revealing a diagnostic puzzle."
                                }
                            },
                            {
                                "label": "Press Button",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "You press the blinking red button labeled 'Emergency Power Override'. A weak surge of power ripples through the console, and the main viewscreen briefly flickers to life, displaying a distorted image of a nebula before dying again. A faint, acrid smell of burnt wiring fills the air.",
                                    "message": "You press the emergency button."
                                }
                            }
                        ]
                    },
                    "main_viewscreen": {
                        "name": "Main Viewscreen",
                        "description": "The main viewscreen, currently dark.",
                        "actions": [
                            {
                                "label": "Check Viewscreen",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The viewscreen remains dark, reflecting only the dim emergency lights of the bridge. Tracing its edges, you notice a small, recessed panel that seems designed to open with a specific tool.",
                                    "message": "You check the main viewscreen."
                                }
                            }
                        ]
                    },
                    "cryo_pods": {
                        "name": "Cryogenic Pods",
                        "description": "Abandoned cryogenic pods lining the walls.",
                        "actions": [
                            {
                                "label": "Examine Pods",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "cryo_pod_datapads_puzzle",
                                    "message": "You examine the cryogenic pods, finding a data-pad with a puzzle."
                                }
                            }
                        ]
                    }
                },
                "exits": {"south": "spaceship_engine_room"}
            }, # ADDED COMMA HERE
            "spaceship_engine_room": {
                "name": "Derelict Spaceship Engine Room",
                "description": "Massive, inert engines fill the room. Wires hang loosely, and the air smells faintly of burnt ozone. A small, service hatch is visible.",
                "image": "spaceship.jpg",
                "puzzles": {
                    "engine_puzzle": {
                        "name": "Engine Diagnostic Puzzle",
                        "description": "The diagnostic panel shows three critical relays offline. Restore power by inputting the correct sequence: Delta-Gamma-Epsilon.",
                        "solution": "DGE",
                        "type": "sequence_input",
                        "difficulty": "medium",
                        "prerequisites": ["core_power_online"],
                        "outcomes": ["engine_power_restored"],
                        "reveal_on_solve": [],
                        "triggers_event": "restore_engine_power"
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
        "intro_story": "A chilling, disembodied giggle echoes through dusty, abandoned machinery. You find yourself in a cavernous, dark factory, the air thick with the smell of old plastic and ozone. Rows of silent, unsettling toy parts lie everywhere, their blank eyes seeming to follow your every move. You were searching for your lost younger sibling, who vanished near this derelict building weeks ago. A note, clutched in your hand, simply says: 'She's here. Find the 'Heart of the Toymaker' to bring her back.' A profound sense of unease and childish horror pervades the space.",
        "start_room": "clown_funhouse_entrance",
        "rooms": {
            "clown_funhouse_entrance": {
                "name": "Clown's Funhouse Entrance",
                "description": "You stand at the beginning of a long, silent assembly line. Conveyor belts stretch into the gloom, laden with half-finished dolls, headless teddy bears, and stacks of painted eyes. To your left, a control panel covered in rusted switches and unlabeled buttons sits dormant. To your right, a large, metal bin overflowing with discarded toy limbs creates a macabre mound. A single, working light bulb swings precariously overhead, casting dancing shadows.",
                "image": "clown_funhouse.jpg",
                "puzzles": {
                    "missing_gear_puzzle": {
                        "name": "Conveyor Belt Missing Gear",
                        "description": "The conveyor belt is stalled. You notice a crucial gear is missing from the mechanism. Find a replacement gear to get it moving.",
                        "solution": "USE_GEAR", # Solution implies using an item
                        "type": "object_use",
                        "difficulty": "medium",
                        "prerequisites": ["small_gear_found"],
                        "outcomes": ["conveyor_belt_active"],
                        "reveal_on_solve": [],
                        "triggers_event": "activate_conveyor_belt"
                    },
                    "control_panel_sequence_puzzle": {
                        "name": "Control Panel Sequence",
                        "description": "The control panel has four unlabeled buttons that need to be pressed in the correct order to activate the machinery. A faint diagram nearby hints at the pattern: 'Circle, Square, Triangle, Star'.",
                        "solution": "CSTS", # Placeholder solution
                        "type": "sequence_input",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["machine_activated"],
                        "reveal_on_solve": [],
                        "triggers_event": "activate_toy_machine"
                    }
                }, # No initial puzzles here
                "items": [],
                "interactables": {
                    "conveyor_belt": {
                        "name": "Conveyor Belt",
                        "description": "A long, silent assembly line conveyor belt, laden with toy parts.",
                        "actions": [
                            {
                                "label": "Inspect Conveyor",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "missing_gear_puzzle",
                                    "message": "You inspect the conveyor belt, noticing a missing gear."
                                }
                            }
                        ]
                    },
                    "control_panel": {
                        "name": "Control Panel",
                        "description": "A control panel covered in rusted switches and unlabeled buttons.",
                        "actions": [
                            {
                                "label": "Press Switches",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "control_panel_sequence_puzzle",
                                    "message": "You try pressing the switches, realizing it's a sequence puzzle."
                                }
                            }
                        ]
                    },
                    "metal_bin": {
                        "name": "Metal Bin",
                        "description": "A large, metal bin overflowing with discarded toy limbs.",
                        "actions": [
                            {
                                "label": "Dig Bin",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The bin is full of unsettling toy parts – arms, legs, heads with vacant stares. Deep inside, you find a small, child's drawing, crumpled. It depicts a smiling sun and a large, mechanical heart. You also find a small, rusty gear.",
                                    "message": "You dig through the bin of toy parts and find a small gear."
                                }
                            }
                        ]
                    },
                    "assembly_line_path": {
                        "name": "Assembly Line Path",
                        "description": "The path along the assembly line, stretching into the gloom.",
                        "actions": [
                            {
                                "label": "Follow Belt",
                                "effect": {
                                    "type": "new_room", # Special effect to indicate changing room
                                    "target": "clown_funhouse_mirror_maze", # Target room ID
                                    "message": "You follow the assembly line deeper into the factory."
                                }
                            }
                        ]
                    }
                },
                "exits": {"north": "clown_funhouse_mirror_maze"},
            }, # ADDED COMMA HERE
            "clown_funhouse_mirror_maze": {
                "name": "Clown's Funhouse Mirror Maze",
                "description": "An endless labyrinth of distorted reflections. Laughter echoes eerily, making it hard to tell reality from illusion.",
                "image": "clown_funhouse.jpg",
                "puzzles": {
                    "maze_puzzle": {
                        "name": "Mirror Maze Riddle",
                        "description": "Find the true path through the maze. The riddle on the wall says: 'I have many faces, but only one is true.'",
                        "solution": "TRUTH", # Solution is case-insensitive for AI
                        "type": "riddle",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["maze_solved"],
                        "reveal_on_solve": [],
                        "triggers_event": "reveal_maze_exit"
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
        "intro_story": "A disorienting burst of color and a cacophony of distorted nursery rhymes greet you as you regain consciousness. Everything is enormous – giant building blocks tower over you, and a colossal teddy bear looms menacingly in the corner. You've somehow shrunk and are trapped in a gargantuan child's room. Your goal: find a way to return to your normal size and escape this whimsical, yet terrifying, prison before playtime truly begins. The air smells faintly of forgotten candy and plastic.",
        "start_room": "kids_room_play_area",
        "rooms": {
            "kids_room_play_area": {
                "name": "The Oversized Playroom",
                "description": "You are in a vast playroom. Giant building blocks, each the size of a small car, are scattered across the floor. A towering, one-eyed teddy bear, nearly filling the corner, watches with a stitched smile. To your right, a colossal toy chest, its lid slightly ajar, promises both secrets and dangers. Everything feels strangely out of proportion.",
                "image": "kids_room.jpg",
                "puzzles": {
                    "building_block_color_puzzle": {
                        "name": "Giant Building Block Puzzle",
                        "description": "The giant building blocks have faded crayon markings. One block has a drawing of a key, and nearby blocks are colored Red, Blue, Yellow. A note says 'Color of the Key'. Enter the color sequence.",
                        "solution": "YELLOWBLUE", # Placeholder solution for now
                        "type": "code_entry",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["blocks_moved", "small_key_found"],
                        "reveal_on_solve": ["small_key"],
                        "triggers_event": "reveal_key_under_blocks"
                    },
                    "teddy_bear_zipper_puzzle": {
                        "name": "Teddy Bear Zipper",
                        "description": "The towering teddy bear has a small, zippered pouch on its belly, but the zipper is stuck. It needs a specific tool or action to open.",
                        "solution": "USE_KNIFE", # Placeholder - implies an item
                        "type": "object_use",
                        "difficulty": "medium",
                        "prerequisites": ["sharp_tool_found"], # Example prerequisite
                        "outcomes": ["bear_pouch_open", "bear_note_found"],
                        "reveal_on_solve": ["bear_note"],
                        "triggers_event": "open_teddy_bear_pouch"
                    }
                }, # No initial puzzles here
                "items": [],
                "interactables": {
                    "building_blocks": {
                        "name": "Giant Building Blocks",
                        "description": "Giant building blocks, each the size of a small car.",
                        "actions": [
                            {
                                "label": "Inspect Blocks",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "building_block_color_puzzle",
                                    "message": "You inspect the giant building blocks, noticing a color puzzle."
                                }
                            }
                        ]
                    },
                    "teddy_bear": {
                        "name": "Towering Teddy Bear",
                        "description": "A towering, one-eyed teddy bear, nearly filling the corner.",
                        "actions": [
                            {
                                "label": "Examine Bear",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "teddy_bear_zipper_puzzle",
                                    "message": "You examine the towering teddy bear, finding a stuck zipper."
                                }
                            }
                        ]
                    },
                    "toy_chest": {
                        "name": "Colossal Toy Chest",
                        "description": "A colossal toy chest, its lid slightly ajar.",
                        "actions": [
                            {
                                "label": "Check Toy Chest",
                                "effect": {
                                    "type": "new_room", # Special effect to indicate changing room
                                    "target": "kids_room_toy_chest", # Target room ID
                                    "message": "You cautiously approach the toy chest and peek inside."
                                }
                            }
                        ]
                    },
                    "room_walls": {
                        "name": "Room Walls",
                        "description": "The brightly painted walls of the playroom.",
                        "actions": [
                            {
                                "label": "Observe Walls",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The walls are painted with whimsical murals of cartoon animals. One mural of a smiling sun has a peculiar reflection, as if a small, metallic object is embedded behind its painted rays.",
                                    "message": "You observe the playroom walls."
                                }
                            }
                        ]
                    }
                },
                "exits": {"east": "kids_room_toy_chest"},
            },
            "kids_room_toy_chest": {
                "name": "The Toy Chest Corner",
                "description": "A massive, overflowing toy chest sits in the corner. It seems to hold the key to an exit.",
                "image": "kids_room.jpg", # Reusing image
                "puzzles": {
                    "toy_puzzle": {
                        "name": "Toy Block Sequence Puzzle",
                        "description": "Arrange the colored blocks in the order of the rainbow: Red, Orange, Yellow, Green, Blue, Indigo, Violet.",
                        "solution": "ROYGBIV",
                        "type": "sequence_input",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["toy_chest_open"],
                        "reveal_on_solve": ["toy_car"],
                        "triggers_event": "reveal_toy_chest_contents"
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
        "intro_story": "A dizzying rush of vibrant colors and the overwhelming scent of sugar hits you like a wave. You find yourself in a fantastical landscape where lollipop trees sway, rivers of chocolate gently flow, and gingerbread houses stand on hills of whipped cream. You have no memory of how you arrived in this saccharine world, but a tiny, shimmering fairy flits past, leaving a trail of glitter and a whispered warning: 'The Sugar Queen's feast begins at dusk. Escape before you become the main course!' Your goal: find the hidden portal back to your own world before the sweet enchantment becomes a permanent, sticky trap.",
        "start_room": "candy_wonderland_path",
        "rooms": {
            "candy_wonderland_path": {
                "name": "Candy Wonderland Path",
                "description": "You stand on a path paved with rainbow-colored gumdrops. Towering lollipops form a kaleidoscopic forest, and the air shimmers with edible glitter. Ahead, a grand gingerbread house, adorned with candy cane pillars and gumdrop windows, beckons from atop a hill of ice cream. A faint, sweet melody drifts from its direction.",
                "image": "candy_wonderland.jpg",
                "puzzles": {
                    "lollipop_rune_puzzle": {
                        "name": "Lollipop Rune Sequence",
                        "description": "The lollipops have tiny, intricately carved messages on their sticks, almost like ancient runes. A few stand out, forming a sequence: 'Sun, Moon, Star, Cloud'. To activate the path, you must trace the correct rune sequence.",
                        "solution": "SUNMOONSTARCLOUD", # Placeholder solution
                        "type": "sequence_input",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["path_activated"],
                        "reveal_on_solve": [],
                        "triggers_event": "activate_candy_path"
                    }
                }, # No initial puzzles here
                "items": [],
                "interactables": {
                    "gumdrop_path": {
                        "name": "Gumdrop Path",
                        "description": "A path paved with rainbow-colored gumdrops.",
                        "actions": [
                            {
                                "label": "Taste Path",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "You cautiously taste a gumdrop from the path. It's surprisingly fresh and chewy, bursting with a flavor you can't quite place – a mix of cherry, lime, and something subtly magical.",
                                    "message": "You taste a gumdrop from the path."
                                }
                            }
                        ]
                    },
                    "lollipop_forest": {
                        "name": "Lollipop Forest",
                        "description": "Towering lollipops forming a kaleidoscopic forest.",
                        "actions": [
                            {
                                "label": "Inspect Lollipops",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "lollipop_rune_puzzle",
                                    "message": "You inspect the towering lollipops, noticing ancient runes on their sticks."
                                }
                            }
                        ]
                    },
                    "gingerbread_house_view": {
                        "name": "Gingerbread House View",
                        "description": "A grand gingerbread house beckons from atop a hill of ice cream.",
                        "actions": [
                            {
                                "label": "Look Gingerbread",
                                "effect": {
                                    "type": "new_room", # Special effect to indicate changing room
                                    "target": "candy_wonderland_gingerbread_house", # Target room ID
                                    "message": "You head towards the enticing gingerbread house."
                                }
                            },
                            {
                                "label": "Listen Melody",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The faint, sweet melody becomes clearer. It's a whimsical tune, almost like a music box, emanating directly from the gingerbread house. It sounds both inviting and subtly hypnotic.",
                                    "message": "You listen closely to the melody from the gingerbread house."
                                }
                            }
                        ]
                    }
                },
                "exits": {"north": "candy_wonderland_gingerbread_house"},
            }, # ADDED COMMA HERE
            "candy_wonderland_gingerbread_house": {
                "name": "Candy Wonderland Gingerbread House",
                "description": "A house built of gingerbread and frosting, with gumdrop windows and candy cane pillars. It smells delicious!",
                "image": "candy_wonderland.jpg", # Reusing image
                "puzzles": {
                    "gingerbread_puzzle": {
                        "name": "Gingerbread Door Sequence",
                        "description": "The frosting on the door forms a sequence: 1-2-3-5-8. What's next in the Fibonacci sequence?",
                        "solution": "13",
                        "type": "numeric_code",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["gingerbread_door_open"],
                        "reveal_on_solve": [],
                        "triggers_event": "open_gingerbread_house_door"
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
        "intro_story": "A sudden, chilling draft awakens you to the opulent decay of a grand foyer. Dust motes dance in thin sunbeams piercing grimy, gothic windows. Cobwebs drape from chandeliers like tattered lace, and the air is heavy with the scent of mildew and forgotten secrets. You recall accepting a dare to spend a night in the infamous Blackwood Manor, a place rumored to hold the vengeful spirit of its former owner. Your mission: uncover the manor's dark secret and find a way out before dawn, or become another permanent resident. The house creaks and groans around you, a living, breathing entity.",
        "start_room": "mansion_foyer",
        "rooms": {
            "mansion_foyer": {
                "name": "Abandoned Mansion Foyer",
                "description": "You stand in the decaying grandeur of the mansion's foyer. A sweeping, dust-laden staircase curves elegantly upwards into shadow. To your left, a massive, ornate grandfather clock stands silently, its pendulum still. To your right, a heavy, velvet curtain conceals what might be a doorway. The main entrance, a colossal pair of double doors behind you, is sealed shut with heavy, iron chains.",
                "image": "abandoned_mansion.jpg",
                "puzzles": {
                    "mansion_riddle": {
                        "name": "Mansion Riddle",
                        "description": "I have a heart, but cannot love. I have a mouth, but cannot speak. I have a house, but cannot live. What am I?",
                        "solution": "BELL", # Original solution
                        "type": "riddle",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["library_secret_revealed"],
                        "reveal_on_solve": [],
                        "triggers_event": "reveal_library_secret"
                    },
                    "clock_hand_puzzle": {
                        "name": "Grandfather Clock Hands",
                        "description": "The clock's face is cracked, its hands frozen at a quarter past midnight. You notice three small, numbered dials beneath the clock face. You need to set the time correctly to activate something.",
                        "solution": "300", # Placeholder for 3:00
                        "type": "numeric_code",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["clock_secret_revealed"],
                        "reveal_on_solve": ["ornate_key"],
                        "triggers_event": "reveal_key_from_clock"
                    }
                },
                "items": [],
                "interactables": {
                    "grandfather_clock": {
                        "name": "Grandfather Clock",
                        "description": "A massive, ornate grandfather clock, silently standing.",
                        "actions": [
                            {
                                "label": "Inspect Clock",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "clock_hand_puzzle",
                                    "message": "You inspect the grandfather clock, finding a puzzle with its hands."
                                }
                            }
                        ]
                    },
                    "velvet_curtain": {
                        "name": "Velvet Curtain",
                        "description": "A heavy, velvet curtain concealing a potential doorway.",
                        "actions": [
                            {
                                "label": "Examine Curtains",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "You pull back the heavy velvet curtain. Behind it, a darkened archway leads to what appears to be a library. The air there is even heavier with the scent of old paper and dust. A faint inscription above the archway reads: 'Seek truth in tales, for silence holds the answer.'",
                                    "message": "You examine the velvet curtain."
                                }
                            },
                            {
                                "label": "Solve Riddle",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "mansion_riddle",
                                    "message": "You try to solve the riddle hinted at by the curtain."
                                }
                            }
                        ]
                    },
                    "main_doors_chains": {
                        "name": "Main Door Chains",
                        "description": "Heavy, iron chains sealing the colossal main entrance doors.",
                        "actions": [
                            {
                                "label": "Check Chains",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The chains are thick and rusted, wrapped securely around the main double doors. There's no obvious way to break them, and the lock is a complex, old-fashioned padlock that would require a very specific key or tool.",
                                    "message": "You check the chains on the main doors."
                                }
                            }
                        ]
                    },
                    "grand_staircase": {
                        "name": "Grand Staircase",
                        "description": "A sweeping, dust-laden staircase curving elegantly upwards.",
                        "actions": [
                            {
                                "label": "Climb Stairs",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The stairs creak ominously under your weight, each step kicking up clouds of dust. The upper landing is shrouded in deeper shadow, and a faint, cold whisper seems to drift down from above.",
                                    "message": "You climb the grand staircase."
                                }
                            }
                        ]
                    }
                },
                "exits": {"north": "mansion_library"},
            }, # ADDED COMMA HERE
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
        "intro_story": "A rush of stale, dry air fills your lungs as you struggle awake, eyes burning from the dust. Hieroglyphs cover every inch of the cold stone walls around you, depicting ancient gods and forgotten pharaohs. The air is thick with the smell of dust and ancient rituals. You remember venturing into this forbidden tomb in search of the legendary 'Eye of Osiris', a jewel said to grant passage between worlds. Now, the heavy stone door has sealed behind you. Your mission: uncover the tomb's secrets and retrieve the Eye to escape before becoming another forgotten relic. A faint, low rumble vibrates through the stone beneath your feet.",
        "start_room": "tomb_entrance",
        "rooms": {
            "tomb_entrance": {
                "name": "Ancient Tomb Entrance",
                "description": "You are in the main antechamber of a vast, ancient tomb. Hieroglyphs of incredible detail cover every inch of the cold stone walls. A massive sarcophagus, intricately carved with a pharaoh's likeness, dominates the center of the room. Its lid appears to be slightly ajar. To your left, a dark passage leads deeper into the earth, while behind you, the entrance is now a solid, unyielding wall of stone.",
                "image": "ancient_tomb.jpg",
                "puzzles": {
                    "hieroglyph_puzzle": {
                        "name": "Hieroglyph Sequence",
                        "description": "Arrange the ancient tiles to reveal the name of the forgotten pharaoh. The symbols suggest a sequence corresponding to 'RAMSES'.",
                        "solution": "RAMSES", # Original solution
                        "type": "symbol_sequence",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["hieroglyphs_deciphered"],
                        "reveal_on_solve": [],
                        "triggers_event": "reveal_tomb_door_clue"
                    },
                    "sarcophagus_lid_puzzle": {
                        "name": "Sarcophagus Lid Mechanism",
                        "description": "The sarcophagus lid is incredibly heavy. You notice a recessed panel with three rotating discs on its side, each displaying a different animal: 'Jackal, Falcon, Scarab'. You need to align them correctly to move the lid.",
                        "solution": "JACKALFALCONSCARAB", # Placeholder solution
                        "type": "sequence_input",
                        "difficulty": "hard",
                        "prerequisites": [],
                        "outcomes": ["sarcophagus_open"],
                        "reveal_on_solve": ["ancient_scroll"],
                        "triggers_event": "open_sarcophagus"
                    }
                },
                "items": [],
                "interactables": {
                    "sarcophagus": {
                        "name": "Massive Sarcophagus",
                        "description": "A massive sarcophagus, intricately carved with a pharaoh's likeness. Its lid is slightly ajar.",
                        "actions": [
                            {
                                "label": "Inspect Sarcophagus",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "sarcophagus_lid_puzzle",
                                    "message": "You inspect the sarcophagus, revealing a lid mechanism puzzle."
                                }
                            }
                        ]
                    },
                    "hieroglyphic_walls": {
                        "name": "Hieroglyphic Walls",
                        "description": "Walls covered in hieroglyphs of incredible detail.",
                        "actions": [
                            {
                                "label": "Examine Hieroglyphs",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "hieroglyph_puzzle",
                                    "message": "You examine the hieroglyphs, finding a puzzle within their patterns."
                                }
                            }
                        ]
                    },
                    "dark_passage": {
                        "name": "Dark Passage",
                        "description": "A dark passage leading deeper into the earth.",
                        "actions": [
                            {
                                "label": "Check Passage",
                                "effect": {
                                    "type": "new_room",
                                    "target": "tomb_chamber",
                                    "message": "You venture into the dark passage."
                                }
                            }
                        ]
                    },
                    "floor_rumble": {
                        "name": "Floor Rumble",
                        "description": "A faint, low rumble vibrates through the stone beneath your feet.",
                        "actions": [
                            {
                                "label": "Listen Rumble",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The rumble is faint but persistent, a deep, rhythmic thrumming that seems to come from somewhere beneath the sarcophagus. It's too deep to be machinery, almost geological, like a distant, massive force.",
                                    "message": "You listen to the rumble beneath the floor."
                                }
                            }
                        ]
                    }
                },
                "exits": {"west": "tomb_chamber"},
            }, # ADDED COMMA HERE
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
        "intro_story": "A chilling silence hangs heavy in the air, broken only by the drip of unseen water. You find yourself disoriented on the cold, tiled floor of what appears to be an abandoned asylum. Rusty medical equipment lies scattered, hinting at past horrors, and the lingering scent of antiseptic and fear assaults your senses. You were investigating the disappearance of a renowned psychiatrist who mysteriously vanished from this very institution decades ago. Now, the heavy iron doors have slammed shut behind you, and a whisper warns, 'None escape the sanatorium.' Your mission: uncover the truth behind the disappearances and find a way to break free before you too become a permanent resident. The oppressive atmosphere seems to press in on you.",
        "start_room": "asylum_reception",
        "rooms": {
            "asylum_reception": {
                "name": "Abandoned Asylum Reception",
                "description": "You are in the dilapidated reception area of the asylum. A grand, but dusty, wooden reception desk stands before a shattered window. To your left, a row of rusted filing cabinets leans precariously. To your right, a corridor stretches into darkness, lined with closed patient room doors. The main entrance, a pair of heavy iron doors behind you, is barred from the outside.",
                "image": "asylum.jpg",
                "puzzles": {
                    "patient_log_puzzle": {
                        "name": "Patient Log Book Code",
                        "description": "A faded patient log book lies on the desk. Most entries are illegible, but one name, 'Dr. Eldridge', is clearly visible next to an entry for 'Patient Zero' and a series of cryptic numbers that seem to be a code.",
                        "solution": "314", # Placeholder solution
                        "type": "numeric_code",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["patient_zero_code_found"],
                        "reveal_on_solve": [],
                        "triggers_event": "reveal_cabinet_clue"
                    },
                    "filing_cabinet_lock_puzzle": {
                        "name": "Locked Filing Cabinet",
                        "description": "A drawer on the filing cabinet is jammed shut. Through a small gap, you can see the edge of a folder marked 'Restricted'. The drawer is secured by a combination lock.",
                        "solution": "1897", # Placeholder solution
                        "type": "code_entry",
                        "difficulty": "easy",
                        "prerequisites": ["patient_zero_code_found"], # Requires code from patient log
                        "outcomes": ["cabinet_unlocked", "restricted_folder_found"],
                        "reveal_on_solve": ["restricted_folder"],
                        "triggers_event": "open_filing_cabinet"
                    }
                }, # No initial puzzles here
                "items": [],
                "interactables": {
                    "reception_desk": {
                        "name": "Reception Desk",
                        "description": "A grand, but dusty, wooden reception desk.",
                        "actions": [
                            {
                                "label": "Inspect Desk",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "patient_log_puzzle",
                                    "message": "You inspect the reception desk, finding a patient log with a code puzzle."
                                }
                            }
                        ]
                    },
                    "filing_cabinets": {
                        "name": "Filing Cabinets",
                        "description": "A row of rusted filing cabinets.",
                        "actions": [
                            {
                                "label": "Examine Cabinets",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "filing_cabinet_lock_puzzle",
                                    "message": "You examine the filing cabinets, noticing a locked drawer."
                                }
                            }
                        ]
                    },
                    "shattered_window": {
                        "name": "Shattered Window",
                        "description": "A shattered window behind the reception desk.",
                        "actions": [
                            {
                                "label": "Look Window",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "Through the shattered window, you can see only overgrown, thorny bushes and a high, crumbling brick wall topped with barbed wire. Escape this way is impossible, but you notice a glint of metal in the bushes below, perhaps something dropped from an upper floor.",
                                    "message": "You look through the shattered window."
                                }
                            }
                        ]
                    },
                    "dark_corridor": {
                        "name": "Dark Corridor",
                        "description": "A corridor stretching into darkness, lined with closed patient room doors.",
                        "actions": [
                            {
                                "label": "Check Corridor",
                                "effect": {
                                    "type": "new_room",
                                    "target": "asylum_wards",
                                    "message": "You cautiously enter the dark corridor."
                                }
                            }
                        ]
                    }
                },
                "exits": {"north": "asylum_wards"},
            }, # ADDED COMMA HERE
            "asylum_wards": {
                "name": "Abandoned Asylum Wards",
                "description": "Long corridors lined with empty patient rooms. The air is heavy with despair, and shadows seem to dance at the edge of your vision.",
                "image": "asylum.jpg", # Reusing image
                "puzzles": {
                    "patient_files_puzzle": {
                        "name": "Patient Files Code",
                        "description": "A set of patient files are scattered. Find the file marked with a broken key icon and read the three-digit code: 4-8-2. You need to enter this code to unlock the next room.",
                        "solution": "482",
                        "type": "numeric_code",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["patient_files_accessed"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_next_room_code"
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
