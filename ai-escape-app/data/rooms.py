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
                "description": "The antechamber is perfectly circular, its walls smooth but for the occasional rough-hewn symbol. The only source of light comes from a flickering, ethereal glow emanating from a heavy, iron-banded door directly opposite where you lay. An intricate glowing symbol, an eye weeping three tears, is etched into its surface, clearly sealing it. A small, overturned stone bench lies near the wall to your left, its surface covered in a fine layer of dust. The hum feels strongest here, almost vibrating your teeth.",
                "image": "forgotten_library.jpg",
                "puzzles": {
                    "ancient_symbol_door_puzzle": {
                        "name": "Ancient Symbol Door Puzzle",
                        "description": "The heavy door is sealed by an intricate glowing symbol, an eye weeping three tears, etched into its surface. To open it, you must enter the correct word.",
                        "solution": "EYETEARS", # Direct answer for the puzzle - now a single string
                        "expected_answer": "eyetears", # Direct answer for the puzzle - now a single string
                        "hint_levels": [
                            "Focus on the main components of the symbol. What literal images do you see?",
                            "You see an 'EYE' and 'THREE TEARS'. Can you form a single word from these observations?",
                            "Try combining the words you've identified into one. Think about what the 'eye' is doing with the 'tears'."
                        ],
                        "type": "word_entry",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["forgotten_library_entrance_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "heavy_door": {
                        "name": "Heavy Door",
                        "description": "A heavy, iron-banded door, emitting a faint glow and sealed by an ancient symbol.",
                        "actions": [
                            {
                                "label": "Examine Glowing Symbol",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "ancient_symbol_door_puzzle",
                                    "message": "You inspect the heavy door. It's sealed by a large, glowing EYE symbol with THREE tear-like markings beneath it. It appears to be a word-based lock."
                                }
                            },
                            {
                                "label": "Inspect the Door",
                                "effect": {
                                    "type": "narrative_update",
                                    "target": "current_room_description",
                                    "value": "The heavy, iron-banded door seems ancient. The glowing symbol is central, an eye with three tears. The craftsmanship suggests it responds to an input, perhaps a word. The hum is definitely stronger near the bottom.",
                                    "message": "You run your hands over the door, feeling the cold stone."
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
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the room.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "You take a moment to absorb your surroundings. The circular chamber emphasizes the central, glowing door. The 'eye' symbol with its 'tears' seems to be the only way forward. It feels like a story waiting to be told, or a word waiting to be spoken."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "forgotten_library_study"
            },
            "forgotten_library_study": {
                "name": "The Silent Study",
                "description": (
                    "You step into a small, dust-choked study. Unlike the previous chamber, "
                    "this room is unnervingly still. No hum. No echo. Even your own breath "
                    "feels intrusive. Towering shelves of ancient books absorb all sound, "
                    "and at the center stands an ornate desk, untouched by time."
                ),
                "main_puzzle": "silent_word_puzzle",

                "puzzles": {
                    "silent_word_puzzle": {
                        "name": "The Silent Word",
                        "description": (
                            "The desk’s lock is not mechanical, but conceptual. "
                            "It requires a single word — not spoken aloud, but understood. "
                            "The room itself seems to listen."
                        ),
                        "solution": "SILENCE",
                        "expected_answer": "silence",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "Pay attention to how this room feels different from the last.",
                            "Several texts mention the absence of sound as important.",
                            "The answer is not something you hear — it is what remains when all sound is gone."
                        ],
                        "outcomes": ["desk_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },

                "interactables": {
                    "ancient_manuscript": {
                        "name": "Ancient Manuscript",
                        "description": "A fragile manuscript lies open on a lectern.",
                        "actions": [
                            {
                                "label": "Inspect Manuscript",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": (
                                        "The manuscript speaks of scholars who believed "
                                        "truth could only be found when the world grew quiet.\n\n"
                                        "One passage is underlined:\n"
                                        "'Noise clouds meaning. Only in stillness does understanding remain.'"
                                    )
                                }
                            }
                        ]
                    },

                    "wall_inscription": {
                        "name": "Faded Wall Inscription",
                        "description": "A barely visible inscription etched into the stone.",
                        "actions": [
                            {
                                "label": "Examine Wall Inscription",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": (
                                        "You only notice the inscription when you stop moving.\n\n"
                                        "It reads:\n"
                                        "'Speak the key, yet make no sound.'"
                                    )
                                }
                            }
                        ]
                    },

                    "desk_lock": {
                        "name": "Desk Lock",
                        "description": "An ornate lock embedded into the desk’s surface.",
                        "actions": [
                            {
                                "label": "Inspect Desk Lock",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": (
                                        "The lock reacts to your presence, but not your touch.\n"
                                        "It seems to respond only when the room is completely still.\n\n"
                                        "Forcing an answer feels pointless."
                                    )
                                }
                            },
                            {
                                "label": "Attempt to Solve the Lock",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "silent_word_puzzle",
                                    "message": "You focus on the lock and consider the meaning of this silent place."
                                }
                            }
                        ]
                    },

                    "general_room_observation": {
                        "name": "Room Observation",
                        "description": "Take in the room.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": (
                                        "The longer you stand still, the clearer everything becomes.\n"
                                        "This room does not reward action — it rewards restraint."
                                    )
                                }
                            }
                        ]
                    }
                },

                "exits": {},
                "next_room_id": "forgotten_library_escape_chamber"
            },
            "forgotten_library_escape_chamber": {
                "name": "Forgotten Library Exit",
                "description": "You've found the secret exit from the Forgotten Library! A narrow passage, disguised as a crumbling bookshelf, leads to a winding tunnel with a faint glimmer of sunlight at its end. This is your chance to escape.",
                "image": "forgotten_library.jpg", # Reusing image
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_THE_LIBRARY"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "secret_exit": {
                        "name": "Secret Exit",
                        "description": "The narrow passage leading to freedom.",
                        "actions": [
                            {
                                "label": "Escape the Library",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You step into the light and leave the Forgotten Library behind."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
            },
        }
    },
    "sci_fi_hangar": {
        "intro_story": "A jarring klaxon blares, echoing off polished chrome and blinking control panels. You bolt upright in the pilot's chair, a dull ache behind your eyes, and a frantic voice crackling over the comms: 'Bridge! We've lost primary power! Containment breach in Engineering! Get us out of here!' Your ship, the 'Stardust Wanderer', is plummeting towards an uncharted planet. Your mission: restore emergency power and jump to hyperspace before the ship breaks apart. The bridge is alive with flashing red lights and the smell of ozone.",
        "start_room": "sci_fi_hangar_bridge",
        "rooms": {
            "sci_fi_hangar_bridge": {
                "name": "Stardust Wanderer Bridge",
                "description": "You are on the main command deck of the 'Stardust Wanderer', a semicircle of glowing screens and intricate consoles now mostly dark. Your pilot's chair is central, facing the vast viewport that shows swirling clouds of gas and rock – a planet you definitely weren't heading for. To your left, a navigation console blinks frantically with error messages, its data corrupted. To your right, a communication station hisses static, picking up distorted emergency broadcasts. Behind you, a large, heavy door with an illuminated 'ENGINEERING' sign is sealed shut, flickering ominously between red and yellow. A smaller auxiliary console sits beside it, its panel displaying an odd sequence of words.",
                "image": "scifi_hangar.jpg",
                "puzzles": {
                    "engineering_door_puzzle": {
                        "name": "Engineering Door Puzzle",
                        "description": "The digital lock on the Engineering door is unresponsive. A small, auxiliary console panel beside it displays a cryptic message: 'To proceed, align the energy frequency. The prime directive is 7. The alpha constant is key.' It seems to require a specific command to override the lock and restore access.",
                        "solution": "ALPHA7",
                        "expected_answer": "alpha7",
                        "hint_levels": [
                            "The message mentions 'prime directive is 7' and 'alpha constant is key'. Consider combining these words.",
                            "The console expects a single, concise command.",
                            "Think about what 'alpha' and '7' could represent together as a command."
                        ],
                        "type": "word_entry",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["engineering_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "engineering_door": {
                        "name": "Engineering Door",
                        "description": "A large, heavy door with an illuminated 'ENGINEERING' sign, flickering between red and yellow.",
                        "actions": [
                            {
                                "label": "Examine Door Lock",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "engineering_door_puzzle",
                                    "message": "You inspect the heavy door. The digital lock is flickering. A nearby console shows a cryptic message about energy frequency."
                                }
                            },
                            {
                                "label": "Try to Force Open",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The door is magnetically sealed. Brute force is not an option. The auxiliary console is clearly the intended interface."
                                }
                            }
                        ]
                    },
                    "navigation_console": {
                        "name": "Navigation Console",
                        "description": "A console blinking frantically with error messages.",
                        "actions": [
                            {
                                "label": "Check Navigation",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The navigation console is a mess of error messages: 'EXTERNAL POWER FAILURE', 'ORBITAL DECAY IMMINENT'. It's clear the ship is in serious trouble, and this console offers no immediate solutions."
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
                                    "message": "The comms system is mostly dead, but you pick up faint, distorted emergency broadcasts: '...containment... unstable... core meltdown imminent...'. The frequency dial is stuck on a single, urgent channel, broadcasting warnings."
                                }
                            }
                        ]
                    },
                    "pilot_controls": {
                        "name": "Pilot Controls",
                        "description": "The main pilot's controls.",
                        "actions": [
                            {
                                "label": "Examine Controls",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The flight controls are unresponsive. All primary flight functions are dark. A small, unlabeled button on the side of the console glows faintly. Pressing it does nothing. It feels inert without primary power."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the bridge.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The bridge is a scene of electronic chaos, yet the path forward is singular: the heavy door to Engineering. Its auxiliary console is the only interactive element that hints at a solution, suggesting a specific code or command is needed."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "sci_fi_hangar_engineering"
            },
            "sci_fi_hangar_engineering": {
                "name": "Engineering Deck",
                "description": "You step onto the Engineering deck. The air is thick with heat and the acrid smell of ozone. In the center of the room, the ship's massive core pulses with an unstable, angry red light, radiating danger. Sparks arc violently from a damaged conduit on the far wall. Your attention is drawn to a prominent console directly linked to the core – the Core Regulation Unit – which displays a critical alert: 'REBOOT SEQUENCE REQUIRED'.",
                "image": "scifi_hangar.jpg",
                "main_puzzle": "core_stabilization_puzzle",
                "puzzles": {
                    "core_stabilization_puzzle": {
                        "name": "Core Stabilization",
                        "description": "The Core Regulation Unit's monitor clearly states: 'THREE-PART REBOOT SEQUENCE REQUIRED: Power, Inertia, Coolant.' It demands a specific, ordered input to stabilize the core. You recall seeing a datapad nearby with a scrawled note, possibly a mnemonic.",
                        "solution": "PIC",
                        "expected_answer": "pic",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "The monitor explicitly lists the three words of the sequence: Power, Inertia, Coolant. Is there a way to condense this information?",
                            "Look for any physical notes or clues near the console that might abbreviate or simplify the sequence.",
                            "Consider the first letter of each word in the required sequence."
                        ],
                        "outcomes": ["core_stabilized"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "core_regulation_unit": {
                        "name": "Core Regulation Unit",
                        "description": "The console to stabilize the ship's core.",
                        "actions": [
                            {
                                "label": "Access Unit",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "core_stabilization_puzzle",
                                    "message": "You access the core regulation unit. The monitor prompts for a three-part reboot sequence, listing 'Power, Inertia, Coolant'."
                                }
                            }
                        ]
                    },
                    "damaged_conduit": {
                        "name": "Damaged Conduit",
                        "description": "A conduit on the far wall is spewing sparks.",
                        "actions": [
                            {
                                "label": "Inspect Conduit",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The conduit is too dangerous to approach due to the arcing electricity. It seems directly related to the core's instability; fixing the core should resolve this. It's too hot to touch."
                                }
                            }
                        ]
                    },
                    "maintenance_log": {
                        "name": "Maintenance Log",
                        "description": "A datapad lying on a console.",
                        "actions": [
                            {
                                "label": "Read Log",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The datapad's screen flickers. Most entries are corrupted, but one clear, scrawled note stands out: 'Core reboot sequence is vital. Remember the PIC procedure: Power, Inertia, Coolant. Don't mess it up.'"
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Engineering Deck.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The unstable core is clearly the heart of the problem. The Core Regulation Unit is directly connected to it, requiring a specific reboot sequence. A datapad or a diagram might hold the key to that sequence."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "sci_fi_hangar_escape_pods"
            },
            "sci_fi_hangar_escape_pods": {
                "name": "Sci-Fi Hangar Escape Pods",
                "description": "You've stabilized the core and the emergency lights have flickered to a steady green. The escape pods are now unlocked and ready for launch! Freedom is within reach.",
                "image": "scifi_hangar.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The escape submersible's console glows green with the message: 'READY FOR LAUNCH. INITIATE ESCAPE SEQUENCE.' All that remains is your final command to break free.",
                        "solution": ["ESCAPE_THE_SHIP"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "escape_hatch": {
                        "name": "Escape Hatch",
                        "description": "The hatch to the escape pod is open, a faint hum coming from within.",
                        "actions": [
                            {
                                "label": "Escape the Ship",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You climb into the escape pod. The hatch seals behind you with a hiss, and the launch sequence begins."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Escape Hatch.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The escape hatch is open and waiting. All systems are green for launch. Your objective is clear: initiate escape."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    },
    "underwater_lab": {
        "intro_story": "The crushing pressure of the deep sea is palpable even through the reinforced walls of the laboratory. You find yourself disoriented in a glowing, subaquatic station, alarms faintly blaring. A holographic message flickers, warning of a critical system failure and imminent implosion. Your only chance of survival is to reactivate the primary containment field before the structure gives way. The deep blue light filtering through thick portholes reveals strange marine life, indifferent to your plight.",
        "start_room": "underwater_lab_entrance",
        "rooms": {
            "underwater_lab_entrance": {
                "name": "Underwater Laboratory Entrance",
                "description": "You are in the main observation deck of the subaquatic lab. Thick, reinforced portholes offer a panoramic, albeit terrifying, view of the abyssal trench, illuminated by the lab's powerful external lights. The crushing pressure of the deep sea feels immense, and alarms faintly blare, warning of critical system failure. Bubbles gently rise from complex, alien machinery embedded in the walls. Directly in front of you stands a main control console with flickering lights, displaying 'PRESSURE LOCK ACTIVE'. A sealed bulkhead door blocks your only path forward, its panel showing a digital input field.",
                "image": "underwater_lab.jpg",
                "puzzles": {
                    "pressure_puzzle": {
                        "name": "Bulkhead Door Pressure Lock",
                        "description": "The bulkhead door's digital lock is clearly labeled 'PRESSURE EQUALIZATION'. The main control console nearby provides the exact deep-sea pressure reading necessary to open it: 'CURRENT PRESSURE: 5-2-8'. You must input this numerical sequence.",
                        "solution": "528",
                        "expected_answer": "528",
                        "type": "code_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "The console clearly displays the three-digit pressure reading needed for the lock. Look at the display.",
                            "The reading is directly presented as '5-2-8'.",
                            "Input the numbers in the order they are shown on the console display: Five, Two, Eight."
                        ],
                        "prerequisites": [],
                        "outcomes": ["containment_field_stabilized"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
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
                                    "message": "You inspect the main control console. It shows a pressure-sensitive lock on the bulkhead door and displays the current deep-sea pressure reading: '5-2-8'. This looks like the code."
                                }
                            }
                        ]
                    },
                    "portholes": {
                        "name": "Thick Portholes",
                        "description": "Thick, reinforced portholes offering a view of the abyssal trench.",
                        "actions": [
                            {                                "label": "Observe Portholes",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "Through the portholes, massive, bioluminescent creatures glide past, their eyes seeming to peer directly into the lab. The trench outside is a vast, inky blackness, hinting at unimaginable depths and dangers. The sheer pressure outside is a palpable force."
                                }
                            }
                        ]
                    },
                    "holographic_message": {
                        "name": "Holographic Message",
                        "description": "A flickering holographic message.",
                        "actions": [
                            {
                                "label": "View Message",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The holographic message repeats on a loop: 'Warning: Critical system failure. Imminent implosion. Primary containment field must be reactivated. Pressure equalization required for bulkhead access.' The word 'pressure' echoes, emphasizing the numerical aspect of the problem."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the observation deck.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The observation deck is filled with the ominous blare of alarms. The only way forward seems to be through the bulkhead door, which is sealed by a numerical pressure lock. The main control console and the holographic warnings both emphasize the critical need for pressure equalization, hinting at a numerical solution to the lock."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "underwater_lab_biolabs"
            },
            "underwater_lab_biolabs": {
                "name": "Underwater Laboratory Biolabs",
                "description": "You step into the biolabs, a stark contrast to the observation deck. Tanks of glowing, otherworldly specimens line the walls, their ethereal light casting strange shadows. Complex life support systems hum constantly, a mechanical heartbeat. At the far end of the room, a large access terminal glows, displaying 'ESCAPE POD BAY ACCESS - BIO-SIGNATURE REQUIRED'. This is clearly your gateway to freedom.",
                "image": "underwater_lab.jpg",
                "main_puzzle": "specimen_analysis_puzzle",
                "puzzles": {
                    "specimen_analysis_puzzle": {
                        "name": "Specimen Analysis",
                        "description": "The Escape Pod Bay access terminal demands a specific bio-signature. A note affixed to the terminal explicitly states: 'ONLY THE ALPHA SPECIMEN GRANTS ACCESS. OBSERVE ITS PULSE.' Nearby, the 'ALPHA' specimen tank contains a creature whose bioluminescence pulses in a distinct pattern. Research notes on a scattered desk suggest an abbreviated sequence for such patterns.",
                        "solution": "FDF",
                        "expected_answer": "fdf",
                        "type": "word_entry",
                        "difficulty": "medium",
                         "hint_levels": [
                            "The note explicitly states that the 'Alpha Specimen' grants access. You must identify and observe this particular specimen.",
                            "Focus on the unique light pattern of the creature in the 'ALPHA' tank. Can you translate this pattern (e.g., Flash, Dim, Flash) into a simple code or acronym? The research notes might confirm this.",
                            "The creature's light pattern is 'FLASH-DIM-FLASH'. Consider the first letter of each prominent part of this pattern to form the code."
                        ],
                        "outcomes": ["escape_pods_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "specimen_tanks": {
                        "name": "Specimen Tanks",
                        "description": "Tanks with glowing specimens.",
                        "actions": [
                            {
                                "label": "Inspect Tanks",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The tanks contain a variety of strange, glowing marine life. One tank, distinctly labeled 'ALPHA', holds a creature that pulses with a distinct light pattern: FLASH-DIM-FLASH. This specific pattern seems vital given the terminal's demands."
                                }
                            }
                        ]
                    },
                    "access_terminal": {
                        "name": "Access Terminal",
                        "description": "A terminal that seems to control access to the escape pods.",
                        "actions": [
                            {
                                "label": "Use Terminal",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "specimen_analysis_puzzle",
                                    "message": "You access the terminal. It prompts for a bio-signature sequence to unlock the escape pod bay. A note on the terminal clearly states: 'Only the Alpha Specimen can grant access; its pulse is the key.'"
                                }
                            }
                        ]
                    },
                    "research_notes": {
                        "name": "Research Notes",
                        "description": "Scattered research notes on a desk.",
                        "actions": [
                            {
                                "label": "Read Notes",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The scattered notes contain fragmented data on bioluminescent organisms. One section, heavily circled, describes the 'Alpha' specimen's pulse as 'F-D-F (Flash-Dim-Flash sequence)'. It explicitly states this is used for 'authentication protocols'."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Biolabs.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The biolabs are filled with soft, alien glows. The access terminal is your goal, and it's demanding a bio-signature from the 'Alpha' specimen. Both the specimen tank itself and the research notes seem to hold the pattern you need."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "underwater_lab_escape_chamber"
            },
            "underwater_lab_escape_chamber": {
                "name": "Underwater Laboratory Exit",
                "description": "The access terminal confirms: 'ESCAPE HATCH UNLOCKED. PROCEED TO SUBMERSIBLE.' The large, circular escape hatch is now open, revealing the small, cramped interior of an escape submersible. The path to freedom from the crushing deep is clear.",
                "image": "underwater_lab.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_THE_LAB"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "escape_hatch": {
                        "name": "Escape Hatch",
                        "description": "The escape hatch is now open, revealing a small escape submersible.",
                        "actions": [
                            {
                                "label": "Escape the Lab",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You climb into the escape submersible. The hatch seals behind you with a hiss, and the launch sequence begins. You leave the failing lab behind as you ascend towards the surface."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Escape Chamber.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The escape hatch is open and the submersible is ready. All systems are green for launch, promising salvation. Your objective is singular and clear: initiate escape."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    },
    "spaceship": {
        "intro_story": "A sudden, violent shudder rattles your hibernation pod, jolting you awake. The emergency lights of the 'Star-Drifter' flash erratically, painting the observation deck in hues of crimson and shadow. The ship's AI, a monotone voice in your ear, announces, 'Critical systems failure. Life support failing. Initiate emergency core reboot or perish.' Your mission: navigate the derelict vessel, restore power to the core, and get out before the oxygen runs out. The cold, metallic silence is punctuated by the rhythmic, agonizing groan of stressed bulkheads.",
        "start_room": "spaceship_bridge",
        "rooms": {
            "spaceship_bridge": {
                "name": "Derelict Spaceship Bridge",
                "description": "You are on the bridge of the derelict 'Star-Drifter'. A chilling metallic silence hangs heavy, broken only by the erratic flicker of emergency lights casting long shadows over dead control panels and abandoned cryogenic pods. The main viewscreen is dark, showing only your own ghostly reflection. A heavy blast door, marked 'ENGINE ROOM', blocks your path forward, its control panel utterly inert. The air is cold and thin, life support failing. The cryo-pods, however, seem to have had some auxiliary power recently.",
                "image": "spaceship.jpg",
                "puzzles": {
                    "bridge_power_puzzle": {
                        "name": "Bridge Power Puzzle",
                        "description": "The control panel for the Engine Room blast door is completely dark. However, a single data-pad, still glowing faintly from within a nearby cryo-pod, offers a critical piece of information: 'EMERGENCY POWER OVERRIDE SEQUENCE: R-G-B'. This code needs to be entered into the inert control panel for the blast door itself.",
                        "solution": "RGB",
                        "expected_answer": "rgb",
                        "hint_levels": [
                            "The data-pad in the cryo-pod explicitly states the override code: 'R-G-B'. This sequence refers to colors.",
                            "Consider the first letter of each color mentioned. How might these letters form a single input?",
                            "The code is given directly as 'RGB'. Input these three letters consecutively."
                        ],
                        "type": "word_entry",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["engine_room_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "blast_door": {
                        "name": "Blast Door",
                        "description": "A heavy blast door marked 'ENGINE ROOM'.",
                        "actions": [
                            {
                                "label": "Examine Door",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The blast door is sealed tight, impervious to physical force. The control panel beside it is dark and unresponsive, suggesting a power issue. The cryo-pods nearby might hold a clue to reactivating it."
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
                                    "puzzle_id": "bridge_power_puzzle",
                                    "message": "You examine the cryogenic pods. One has a data-pad wedged in its control panel, glowing faintly. Its screen displays a critical emergency power override code: 'R-G-B', before the power flickers again."
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
                                    "message": "The viewscreen remains dark, reflecting only the dim emergency lights. A small, recessed panel on its side hints at a manual override, but it appears to require a specific tool or key to open, which is nowhere in sight. It offers no immediate solution to the power problem."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Bridge.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The bridge is cold and dying. The Engine Room blast door is the only way to restore power, but its control panel is inert. The data-pad in the cryo-pod is the most promising lead for overriding the lock."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "spaceship_engine_room"
            },
            "spaceship_engine_room": {
                "name": "Derelict Spaceship Engine Room",
                "description": "You step into the cavernous Engine Room. Massive, inert engines loom in the shadows, their power silent. The air is heavy with the smell of burnt ozone and the faint, unsettling hum of a failing core. Loose wires hang precariously from the ceiling. A central diagnostic panel blinks erratically, displaying 'HYPERDRIVE OFFLINE - THREE CRITICAL RELAYS OFFLINE. REPAIR SEQUENCE REQUIRED.' This panel is clearly the key to restoring the hyperdrive.",
                "image": "spaceship.jpg",
                "main_puzzle": "engine_diagnostic_puzzle",
                "puzzles": {
                    "engine_diagnostic_puzzle": {
                        "name": "Engine Diagnostic Puzzle",
                        "description": "The diagnostic panel clearly indicates 'THREE CRITICAL RELAYS OFFLINE'. A hastily scribbled note directly on the panel provides the necessary repair sequence: 'D-G-E'. You must input this sequence into the panel to restore power.",
                        "solution": "DGE",
                        "expected_answer": "dge",
                        "type": "word_entry",
                        "difficulty": "medium",
                        "hint_levels": [
                            "The diagnostic panel itself contains the solution. Look closely at the 'scribbled note' mentioned in the description.",
                            "The note directly provides the three-letter sequence: D-G-E.",
                            "Simply enter the letters D, G, and E in the order they appear on the note to restore power."
                        ],
                        "prerequisites": [],
                        "outcomes": ["engine_power_restored"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "diagnostic_panel": {
                        "name": "Diagnostic Panel",
                        "description": "A diagnostic panel for the main engines.",
                        "actions": [
                            {
                                "label": "Use Panel",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "engine_diagnostic_puzzle",
                                    "message": "You access the diagnostic panel. It shows three critical relays offline, and a note scribbled directly on the panel: 'D-G-E'."
                                }
                            }
                        ]
                    },
                    "hanging_wires": {
                        "name": "Hanging Wires",
                        "description": "Loose wires hang from the ceiling.",
                        "actions": [
                            {
                                "label": "Inspect Wires",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "Loose, sparking wires hang precariously from conduits. It's too dangerous to touch them directly, and they appear to be part of the larger engine system. Trying to manipulate them directly would be futile; a systematic repair through the diagnostic panel is required."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Engine Room.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The engine room hums with a desperate, weak energy. The diagnostic panel is clearly the central point of interaction, demanding a specific repair sequence. The most obvious clue for this sequence is found directly on the panel itself."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "spaceship_escape_chamber"
            },
            "spaceship_escape_chamber": {
                "name": "Derelict Spaceship Escape Hatch",
                "description": "With the hyperdrive restored, the emergency power surges. The main alarm silences, replaced by a reassuring hum. The large, circular escape hatch has now hissed open, revealing the star-strewn void outside. Freedom awaits!",
                "image": "spaceship.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The escape hatch is fully open. A small console within the hatch entrance displays 'INITIATE JUMP TO HYPERSPACE'. Your escape is now a single, decisive action.",
                        "solution": ["ESCAPE_THE_SHIP"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "escape_hatch": {
                        "name": "Escape Hatch",
                        "description": "The escape hatch is now open, revealing a clear path to the void of space.",
                        "actions": [
                            {
                                "label": "Escape the Ship",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You activate the hyperdrive and launch away from the derelict ship, a ghost in the cosmic ballet."
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Escape Hatch.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The escape hatch is open. The console shows a clear route to safety. There's nothing left to do but make your final move."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    },
    "clown_funhouse": {
        "intro_story": "A chilling, disembodied giggle echoes through dusty, abandoned machinery. You find yourself in a cavernous, dark factory, the air thick with the smell of old plastic and ozone. Rows of silent, unsettling toy parts lie everywhere, their blank eyes seeming to follow your every move. You were searching for your lost younger sibling, who vanished near this derelict building weeks ago. A note, clutched in your hand, simply says: 'She's here. Find the 'Heart of the Toymaker' to bring her back.' A profound sense of unease and childish horror pervades the space.",
        "start_room": "clown_funhouse_entrance",
        "rooms": {
            "clown_funhouse_entrance": {
                "name": "Clown's Funhouse Entrance",
                "description": "You stand at the beginning of a long, silent assembly line. Conveyor belts stretch into the gloom, laden with half-finished dolls and unsettling, blank-eyed toys. The air is thick with the smell of old plastic and ozone. To your right, a large, metal bin overflows with discarded toy limbs. A single, working light bulb swings precariously overhead, casting dancing shadows. A garishly painted door with a large, grinning clown face blocks your path forward, featuring a keypad with four distinct colored buttons and a cryptic scrawl beside it.",
                "image": "clown_funhouse.jpg",
                "puzzles": {
                    "funhouse_door_puzzle": {
                        "name": "Funhouse Door Puzzle",
                        "description": "The keypad on the clown-faced door presents four colored buttons: Red, Yellow, Blue, Green. A hastily scrawled message on the wall nearby explicitly reads: 'RYBG'. This must be the sequence to open the door.",
                        "solution": "RYBG",
                        "expected_answer": "rybg",
                        "hint_levels": [
                            "The clue is written clearly on the wall: 'RYBG'.",
                            "The letters correspond to the colors of the buttons on the keypad.",
                            "Press the buttons in the order Red, Yellow, Blue, Green."
                        ],
                        "type": "word_entry",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["funhouse_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                                "interactables": {
                                    "clown_door": {
                                        "name": "Clown Door",
                                        "description": "A garishly painted door with a large, grinning clown face.",
                                        "actions": [
                                            {
                                                "label": "Examine Door",
                                                "effect": {
                                                    "type": "trigger_puzzle",
                                                    "puzzle_id": "funhouse_door_puzzle",
                                                    "message": "You inspect the heavy door. The digital lock is flickering. A nearby console shows a cryptic message about energy frequency."
                                                }
                                            },
                                            {
                                                "label": "Try to Force Open",
                                                "effect": {
                                                    "type": "narrative_update",
                                                    "message": "The door is magnetically sealed. Brute force is not an option. The auxiliary console is clearly the intended interface."
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
                                                    "message": "The bin is full of unsettling toy parts – arms, legs, heads with vacant stares. Deep inside, you find a small, child's drawing, crumpled. It depicts a smiling sun and a large, mechanical heart."
                                                }
                                            }
                                        ]
                                    },
                                    "conveyor_belt": {
                                        "name": "Conveyor Belt",
                                        "description": "A long, silent assembly line conveyor belt.",
                                        "actions": [
                                            {
                                                "label": "Inspect Belt",
                                                "effect": {
                                                    "type": "narrative_update",
                                                    "message": "The conveyor belt is still. It's covered in a thick layer of dust. It doesn't look like it has run in years."
                                                }
                                            }
                                        ]
                                    },
                                    "general_room_observation": {
                                        "name": "General Room Observation",
                                        "description": "General observations of the Funhouse Entrance.",
                                        "actions": [
                                            {
                                                "label": "Look around the room",
                                                "effect": {
                                                    "type": "narrative_update",
                                                    "message": "The room is unsettling, filled with discarded toy parts. The clown-faced door is the only clear exit, and its keypad demands a sequence of colors. The scrawl on the wall is the most obvious hint for this puzzle."
                                                }
                                            }
                                        ]
                                    }
                                },
                "exits": {},
                "next_room_id": "clown_funhouse_mirror_maze"
            },
            "clown_funhouse_mirror_maze": {
                "name": "Clown's Funhouse Mirror Maze",
                "description": "You push through the clown door and are immediately enveloped by a disorienting labyrinth of mirrors. Laughter echoes eerily, making it hard to tell reality from illusion. Your own reflection, and a thousand distorted versions of it, stretch into infinity. In the very center of this confusing maze stands a large, ornate mirror with a perplexing riddle etched into its surface, demanding your attention.",
                "image": "clown_funhouse.jpg",
                "main_puzzle": "maze_riddle_puzzle",
                "puzzles": {
                    "maze_riddle_puzzle": {
                        "name": "Mirror Maze Riddle",
                        "description": "The central mirror's surface glows with a riddle: 'I have no voice, but I can tell you stories. I have no legs, but I travel the world. What am I?' You must decipher the answer and, somehow, provide it to the mirror to find your way through this illusion.",
                        "solution": "BOOK",
                        "expected_answer": "book",
                        "hint_levels": [
                            "Consider objects commonly found in a library or study that fit the description of having a 'spine' and 'leaves' but are inanimate.",
                            "What object contains 'stories' and knowledge, can be carried anywhere, yet has no actual voice or means of physical travel?",
                            "The answer is an item that serves as a vessel for tales and information."
                        ],
                        "type": "word_entry",
                        "difficulty": "medium",
                        "prerequisites": [],
                        "outcomes": ["maze_solved"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "central_mirror": {
                        "name": "Central Mirror",
                        "description": "The central mirror in the maze.",
                        "actions": [
                            {
                                "label": "Read Riddle",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "maze_riddle_puzzle",
                                    "message": "You read the riddle etched into the central mirror. Its words speak of something that shares stories and travels widely, yet has no voice or legs."
                                }
                            }
                        ]
                    },
                    "distorted_reflections": {
                        "name": "Distorted Reflections",
                        "description": "The mirrors distort your reflection in unsettling ways.",
                        "actions": [
                            {
                                "label": "Look at Reflections",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "You see a thousand versions of yourself, all twisted and warped. The labyrinthine reflections make it difficult to focus, but one reflection briefly appears to be holding a book before it shifts and blurs again. Is that a hint, or just your mind playing tricks?"
                                }
                            }
                        ]
                    },
                    "general_room_observation": {
                        "name": "General Room Observation",
                        "description": "General observations of the Mirror Maze.",
                        "actions": [
                            {
                                "label": "Look around the room",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The mirror maze is disorienting and unsettling. The central mirror holds the key with its riddle. While the distorted reflections are confusing, they occasionally offer fleeting glimpses of a potential clue, suggesting a common object that holds stories."
                                }
                            }
                        ]
                    }
                },
    "kids_room": {
        "intro_story": "A disorienting burst of color and a cacophony of distorted nursery rhymes greet you as you regain consciousness. Everything is enormous – giant building blocks tower over you, and a colossal teddy bear looms menacingly in the corner. You've somehow shrunk and are trapped in a gargantuan child's room. Your goal: find a way to return to your normal size and escape this whimsical, yet terrifying, prison before playtime truly begins. The air smells faintly of forgotten candy and plastic.",
        "start_room": "kids_room_play_area",
        "rooms": {
            "kids_room_play_area": {
                "name": "The Oversized Playroom",
                "description": "You are in a vast playroom. Giant building blocks, each the size of a small car, are scattered across the floor. A towering, one-eyed teddy bear, nearly filling the corner, watches with a stitched smile. A door, disguised as a giant book, blocks the way forward.",
                "image": "kids_room.jpg",
                "puzzles": {
                    "play_area_puzzle": {
                        "name": "Giant Building Block Puzzle",
                        "description": "The giant book-door is locked. A riddle is written on its spine: 'I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?'.",
                        "solution": "MAP",
                        "expected_answer": "map",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "Think about something that represents places.",
                            "It's a flat object that can be folded.",
                            "You use it to find your way."
                        ],
                        "prerequisites": [],
                        "outcomes": ["book_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "book_door": {
                        "name": "Giant Book-Door",
                        "description": "A door disguised as a giant book.",
                        "actions": [
                            {
                                "label": "Examine Door",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "play_area_puzzle",
                                    "message": "You inspect the giant book-door. A riddle is written on its spine."
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
                                    "type": "narrative_update",
                                    "message": "The teddy bear's single button eye seems to follow you. It's unnerving."
                                }
                            }
                        ]
                    },
                    "building_blocks": {
                        "name": "Giant Building Blocks",
                        "description": "Giant building blocks scattered across the floor.",
                        "actions": [
                            {
                                "label": "Inspect Blocks",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The blocks are enormous. You could almost build a small house with them. One of them has a drawing of a map on it."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "kids_room_toy_chest"
            },
            "kids_room_toy_chest": {
                "name": "The Toy Chest Corner",
                "description": "You enter a corner of the room dominated by a massive, overflowing toy chest. It seems to hold the key to an exit. A small, locked door is visible behind the chest.",
                "image": "kids_room.jpg",
                "main_puzzle": "toy_block_puzzle",
                "puzzles": {
                    "toy_block_puzzle": {
                        "name": "Toy Block Sequence Puzzle",
                        "description": "A set of colored blocks on the toy chest must be arranged in the order of the rainbow to unlock the door behind it: Red, Orange, Yellow, Green, Blue, Indigo, Violet.",
                        "solution": "ROYGBIV",
                        "expected_answer": "roygbiv",
                        "type": "word_entry",
                        "difficulty": "medium",
                        "hint_levels": [
                            "The colors of the rainbow.",
                            "Think of the acronym.",
                            "Red, Orange, Yellow, Green, Blue, Indigo, Violet."
                        ],
                        "prerequisites": [],
                        "outcomes": ["toy_chest_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "toy_chest": {
                        "name": "Toy Chest",
                        "description": "A massive, overflowing toy chest.",
                        "actions": [
                            {
                                "label": "Inspect Toy Chest",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "toy_block_puzzle",
                                    "message": "You inspect the toy chest and see a set of colored blocks that can be arranged."
                                }
                            }
                        ]
                    },
                    "doll_house": {
                        "name": "Doll House",
                        "description": "A detailed doll house in the corner.",
                        "actions": [
                            {
                                "label": "Look in Doll House",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The doll house is a perfect miniature of a suburban home. The dolls inside are arranged as if they are having a tea party. One of the dolls is holding a tiny rainbow flag."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "kids_room_escape_chamber"
            },
            "kids_room_escape_chamber": {
                "name": "Kids Room Exit",
                "description": "You've found a hidden slide leading out of the oversized playroom!",
                "image": "kids_room.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_THE_ROOM"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "hidden_slide": {
                        "name": "Hidden Slide",
                        "description": "A slide hidden behind a curtain.",
                        "actions": [
                            {
                                "label": "Escape the Room",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You go down the slide and find yourself back to your normal size."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
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
                    "gumdrop_bridge_puzzle": {
                        "name": "Gumdrop Bridge Puzzle",
                        "description": "A river of chocolate blocks your path to the gingerbread house. A bridge of gumdrops is missing a piece. A nearby sign says: 'The sweetest rainbow will complete the path'. You see a sequence of colors on the bridge: Red, Orange, __, Green, Blue, Indigo, Violet.",
                        "solution": "YELLOW",
                        "expected_answer": "yellow",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "Think about the colors of the rainbow.",
                            "What color is between orange and green?",
                            "The missing color is yellow."
                        ],
                        "prerequisites": [],
                        "outcomes": ["bridge_repaired"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "chocolate_river": {
                        "name": "Chocolate River",
                        "description": "A flowing river of chocolate.",
                        "actions": [
                            {
                                "label": "Examine River",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "gumdrop_bridge_puzzle",
                                    "message": "You look at the chocolate river. A gumdrop bridge is incomplete."
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
                                    "type": "narrative_update",
                                    "message": "The lollipops are as tall as trees. They smell like a mix of every fruit imaginable."
                                }
                            }
                        ]
                    },
                    "gumdrop_path": {
                        "name": "Gumdrop Path",
                        "description": "A path paved with rainbow-colored gumdrops.",
                        "actions": [
                            {
                                "label": "Taste a Gumdrop",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "You pop a gumdrop in your mouth. It tastes like sunshine and rainbows. You feel a sudden burst of energy."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "candy_wonderland_gingerbread_house"
            },
            "candy_wonderland_gingerbread_house": {
                "name": "Candy Wonderland Gingerbread House",
                "description": "You enter the gingerbread house. It's made of gingerbread and frosting, with gumdrop windows and candy cane pillars. It smells delicious! A large, ornate door made of licorice blocks the way to the back of the house.",
                "image": "candy_wonderland.jpg",
                "main_puzzle": "gingerbread_door_puzzle",
                "puzzles": {
                    "gingerbread_door_puzzle": {
                        "name": "Gingerbread Door Sequence",
                        "description": "The licorice door has a keypad. A note on the wall says: 'The Fibonacci feast awaits'. The keypad shows a sequence: 1, 1, 2, 3, 5, 8, ...",
                        "solution": "13",
                        "expected_answer": "13",
                        "type": "word_entry",
                        "difficulty": "medium",
                        "hint_levels": [
                            "The note mentions the Fibonacci sequence.",
                            "Each number is the sum of the two preceding ones.",
                            "5 + 8 = 13."
                        ],
                        "prerequisites": [],
                        "outcomes": ["gingerbread_door_open"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "licorice_door": {
                        "name": "Licorice Door",
                        "description": "A large, ornate door made of licorice.",
                        "actions": [
                            {
                                "label": "Inspect Door",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "gingerbread_door_puzzle",
                                    "message": "You inspect the licorice door and its keypad."
                                }
                            }
                        ]
                    },
                    "candy_furniture": {
                        "name": "Candy Furniture",
                        "description": "Furniture made entirely of candy.",
                        "actions": [
                            {
                                "label": "Examine Furniture",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The furniture looks delicious, but also sticky. You notice a sequence of numbers carved into the back of a gingerbread chair: 1, 1, 2, 3, 5, 8..."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "candy_wonderland_escape_chamber"
            },
            "candy_wonderland_escape_chamber": {
                "name": "Candy Wonderland Exit",
                "description": "You've found a secret path made of candy leading out of Wonderland!",
                "image": "candy_wonderland.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_WONDERLAND"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "candy_path": {
                        "name": "Secret Candy Path",
                        "description": "A secret path made of candy.",
                        "actions": [
                            {
                                "label": "Escape Wonderland",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You follow the candy path and escape from Wonderland."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    },
    "abandoned_mansion": {
        "intro_story": "A sudden, chilling draft awakens you to the opulent decay of a grand foyer. Dust motes dance in thin sunbeams piercing grimy, gothic windows. Cobwebs drape from chandeliers like tattered lace, and the air is heavy with the scent of mildew and forgotten secrets. You recall accepting a dare to spend a night in the infamous Blackwood Manor, a place rumored to hold the vengeful spirit of its former owner. Your mission: uncover the manor's dark secret and find a way out before dawn, or become another permanent resident. The house creaks and groans around you, a living, breathing entity.",
        "start_room": "mansion_foyer",
        "rooms": {
            "mansion_foyer": {
                "name": "Abandoned Mansion Foyer",
                "description": "You stand in the decaying grandeur of the mansion's foyer. A sweeping, dust-laden staircase curves elegantly upwards into shadow. A massive, ornate grandfather clock stands silently, its pendulum still. A heavy, velvet curtain conceals a doorway to the library.",
                "image": "abandoned_mansion.jpg",
                "puzzles": {
                    "foyer_puzzle": {
                        "name": "Grandfather Clock Puzzle",
                        "description": "The grandfather clock's hands are frozen. A note on its face reads: 'When the witching hour strikes, the path shall open'. The clock hands can be moved.",
                        "solution": "1200",
                        "expected_answer": "1200",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "The 'witching hour' is a specific time.",
                            "It's associated with supernatural events at night.",
                            "The witching hour is midnight (12:00)."
                        ],
                        "prerequisites": [],
                        "outcomes": ["library_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "grandfather_clock": {
                        "name": "Grandfather Clock",
                        "description": "A massive, ornate grandfather clock.",
                        "actions": [
                            {
                                "label": "Inspect Clock",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "foyer_puzzle",
                                    "message": "You inspect the grandfather clock. Its hands are movable."
                                }
                            }
                        ]
                    },
                    "velvet_curtain": {
                        "name": "Velvet Curtain",
                        "description": "A heavy, velvet curtain.",
                        "actions": [
                            {
                                "label": "Look Behind Curtain",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "You pull back the curtain to reveal a large, oak door leading to the library. It's locked."
                                }
                            }
                        ]
                    },
                    "dusty_portrait": {
                        "name": "Dusty Portrait",
                        "description": "A large, dusty portrait of a stern-looking man.",
                        "actions": [
                            {
                                "label": "Examine Portrait",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The man's eyes seem to follow you. A plaque at the bottom reads 'Bartholomew Blackwood'. He looks like a man who enjoyed his secrets."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "mansion_library"
            },
            "mansion_library": {
                "name": "Abandoned Mansion Library",
                "description": "You enter a library where shelves of decaying books fill the room. The silence is broken only by the creaks of the old house. A fireplace holds cold ashes. A single, leather-bound book on a pedestal has a riddle on its cover.",
                "image": "abandoned_mansion.jpg",
                "main_puzzle": "library_riddle_puzzle",
                "puzzles": {
                    "library_riddle_puzzle": {
                        "name": "Library Riddle",
                        "description": "The riddle on the book reads: 'I have a spine, but no bones. I have leaves, but I'm not a tree. I have stories, but no voice. What am I?'",
                        "solution": "BOOK",
                        "expected_answer": "book",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "Think about what you are in.",
                            "What has a spine and leaves?",
                            "The answer is a book."
                        ],
                        "prerequisites": [],
                        "outcomes": ["secret_passage_revealed"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "riddle_book": {
                        "name": "Riddle Book",
                        "description": "A leather-bound book on a pedestal.",
                        "actions": [
                            {
                                "label": "Read Riddle",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "library_riddle_puzzle",
                                    "message": "You read the riddle on the book's cover."
                                }
                            }
                        ]
                    },
                    "fireplace": {
                        "name": "Fireplace",
                        "description": "A large fireplace with cold ashes.",
                        "actions": [
                            {
                                "label": "Inspect Fireplace",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The fireplace is cold and filled with ashes. You poke at them with a nearby fire iron, but find nothing of interest. A faint draft seems to be coming from the back of it."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "abandoned_mansion_escape_chamber"
            },
            "abandoned_mansion_escape_chamber": {
                "name": "Abandoned Mansion Secret Passage",
                "description": "You found a secret passage behind a bookshelf! It leads out of the mansion!",
                "image": "abandoned_mansion.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_THE_MANSION"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "secret_passage": {
                        "name": "Secret Passage",
                        "description": "A secret passage behind a bookshelf.",
                        "actions": [
                            {
                                "label": "Escape the Mansion",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You enter the secret passage and escape the mansion."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    },
    "ancient_tomb": {
        "intro_story": "A rush of stale, dry air fills your lungs as you struggle awake, eyes burning from the dust. Hieroglyphs cover every inch of the cold stone walls around you, depicting ancient gods and forgotten pharaohs. The air is thick with the smell of dust and ancient rituals. You remember venturing into this forbidden tomb in search of the legendary 'Eye of Osiris', a jewel said to grant passage between worlds. Now, the heavy stone door has sealed behind you. Your mission: uncover the tomb's secrets and retrieve the Eye to escape before becoming another forgotten relic. A faint, low rumble vibrates through the stone beneath your feet.",
        "start_room": "tomb_entrance",
        "rooms": {
            "tomb_entrance": {
                "name": "Ancient Tomb Entrance",
                "description": "You are in the main antechamber of a vast, ancient tomb. Hieroglyphs of incredible detail cover every inch of the cold stone walls. A massive stone door, covered in symbols, blocks the way forward.",
                "image": "ancient_tomb.jpg",
                "puzzles": {
                    "tomb_door_puzzle": {
                        "name": "Tomb Door Puzzle",
                        "description": "The stone door is covered in hieroglyphs. A prominent inscription reads: 'Speak the name of the sun god to proceed.'",
                        "solution": "RA",
                        "expected_answer": "ra",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "The sun god is a major figure in Egyptian mythology.",
                            "His name is short and simple.",
                            "The answer is 'Ra'."
                        ],
                        "prerequisites": [],
                        "outcomes": ["tomb_door_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
                "items": [],
                "interactables": {
                    "stone_door": {
                        "name": "Stone Door",
                        "description": "A massive stone door covered in symbols.",
                        "actions": [
                            {
                                "label": "Examine Door",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "tomb_door_puzzle",
                                    "message": "You inspect the stone door. An inscription provides a clue."
                                }
                            }
                        ]
                    },
                    "hieroglyphic_walls": {
                        "name": "Hieroglyphic Walls",
                        "description": "Walls covered in hieroglyphs.",
                        "actions": [
                            {
                                "label": "Examine Walls",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The hieroglyphs depict scenes of ancient rituals and offerings to the gods. One carving shows the sun god Ra, holding the ankh."
                                }
                            }
                        ]
                    },
                    "sandy_floor": {
                        "name": "Sandy Floor",
                        "description": "A sandy floor that covers most of the antechamber.",
                        "actions": [
                            {
                                "label": "Inspect Floor",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The sand is fine and ancient. You see faint outlines of what might be a trapdoor, but it's sealed shut."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "tomb_chamber"
            },
            "tomb_chamber": {
                "name": "Ancient Tomb Chamber",
                "description": "You enter a hidden chamber, darker and colder than the entrance. A massive sarcophagus, intricately carved with a pharaoh's likeness, dominates the center of the room. A secret passage is likely hidden here.",
                "image": "ancient_tomb.jpg",
                "main_puzzle": "sarcophagus_puzzle",
                "puzzles": {
                    "sarcophagus_puzzle": {
                        "name": "Sarcophagus Lid Mechanism",
                        "description": "The sarcophagus lid is incredibly heavy. You notice a recessed panel with three rotating discs on its side, each displaying a different animal: 'Jackal, Falcon, Scarab'. You need to align them correctly to reveal the exit.",
                        "solution": "JACKALFALCONSCARAB",
                        "expected_answer": "jackalfalconscarab",
                        "type": "word_entry",
                        "difficulty": "hard",
                        "hint_levels": [
                            "The animals are important symbols in Egyptian mythology.",
                            "Try to find a sequence in the hieroglyphs around the room.",
                            "The correct sequence is Jackal, Falcon, Scarab."
                        ],
                        "prerequisites": [],
                        "outcomes": ["sarcophagus_open"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "sarcophagus": {
                        "name": "Massive Sarcophagus",
                        "description": "A massive sarcophagus, intricately carved.",
                        "actions": [
                            {
                                "label": "Inspect Sarcophagus",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "sarcophagus_puzzle",
                                    "message": "You inspect the sarcophagus, revealing a lid mechanism puzzle."
                                }
                            }
                        ]
                    },
                    "canopic_jars": {
                        "name": "Canopic Jars",
                        "description": "A set of four canopic jars on a pedestal.",
                        "actions": [
                            {
                                "label": "Examine Jars",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The jars are carved with the heads of the four sons of Horus: a jackal, a falcon, a baboon, and a human. The jackal and falcon look newer than the others."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "ancient_tomb_escape_chamber"
            },
            "ancient_tomb_escape_chamber": {
                "name": "Ancient Tomb Secret Exit",
                "description": "You've unearthed a hidden passage out of the tomb!",
                "image": "ancient_tomb.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_THE_TOMB"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "secret_passage": {
                        "name": "Secret Passage",
                        "description": "A hidden passage.",
                        "actions": [
                            {
                                "label": "Escape the Tomb",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You crawl through the passage and emerge into the sunlight."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    },
    "asylum": {
        "intro_story": "A chilling silence hangs heavy in the air, broken only by the drip of unseen water. You find yourself disoriented on the cold, tiled floor of what appears to be an abandoned asylum. Rusty medical equipment lies scattered, hinting at past horrors, and the lingering scent of antiseptic and fear assaults your senses. You were investigating the disappearance of a renowned psychiatrist who mysteriously vanished from this very institution decades ago. Now, the heavy iron doors have slammed shut behind you, and a whisper warns, 'None escape the sanatorium.' Your mission: uncover the truth behind the disappearances and find a way to break free before you too become a permanent resident. The oppressive atmosphere seems to press in on you.",
        "start_room": "asylum_reception",
        "rooms": {
            "asylum_reception": {
                "name": "Abandoned Asylum Reception",
                "description": "You are in the dilapidated reception area of the asylum. A grand, but dusty, wooden reception desk stands before a shattered window. A corridor lined with closed patient room doors stretches into darkness, blocked by a heavy iron gate.",
                "image": "asylum.jpg",
                "puzzles": {
                    "reception_puzzle": {
                        "name": "Patient Log Book Code",
                        "description": "A faded patient log book lies on the desk. Most entries are illegible, but one name, 'Dr. Eldridge', is clearly visible next to an entry for 'Patient Zero' and a series of cryptic numbers: '3-1-4'. This must be the code for the gate.",
                        "solution": "314",
                        "expected_answer": "314",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "The code is in the patient log book.",
                            "Look for the entry for 'Patient Zero'.",
                            "The code is 314."
                        ],
                        "prerequisites": [],
                        "outcomes": ["gate_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_door_exit"
                    }
                },
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
                                    "puzzle_id": "reception_puzzle",
                                    "message": "You inspect the reception desk and find a patient log book."
                                }
                            }
                        ]
                    },
                    "iron_gate": {
                        "name": "Iron Gate",
                        "description": "A heavy iron gate blocking the corridor.",
                        "actions": [
                            {
                                "label": "Examine Gate",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The gate is locked with a numerical keypad."
                                }
                            }
                        ]
                    },
                    "shattered_window": {
                        "name": "Shattered Window",
                        "description": "A shattered window with a view of the overgrown grounds.",
                        "actions": [
                            {
                                "label": "Look Outside",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "The grounds are overgrown and surrounded by a high wall. There's no escape this way. You notice a faded number '3' painted on the wall outside."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "asylum_wards"
            },
            "asylum_wards": {
                "name": "Abandoned Asylum Wards",
                "description": "You enter a long corridor lined with empty patient rooms. The air is heavy with despair, and shadows seem to dance at the edge of your vision. A single door at the end of the hall is marked 'DOCTOR'S OFFICE'.",
                "image": "asylum.jpg",
                "main_puzzle": "wards_puzzle",
                "puzzles": {
                    "wards_puzzle": {
                        "name": "Patient Files Riddle",
                        "description": "The door to the doctor's office is locked. A plaque on the door reads: 'I have a face and two hands, but no arms or legs. What am I?'",
                        "solution": "CLOCK",
                        "expected_answer": "clock",
                        "type": "word_entry",
                        "difficulty": "easy",
                        "hint_levels": [
                            "Think of an object that tells time.",
                            "It has a face and hands.",
                            "The answer is a clock."
                        ],
                        "prerequisites": [],
                        "outcomes": ["office_unlocked"],
                        "reveal_on_solve": [],
                        "triggers_event": "unlock_exit"
                    }
                },
                "interactables": {
                    "office_door": {
                        "name": "Doctor's Office Door",
                        "description": "The door to the doctor's office.",
                        "actions": [
                            {
                                "label": "Inspect Door",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "wards_puzzle",
                                    "message": "You inspect the door and find a riddle."
                                }
                            }
                        ]
                    },
                    "patient_rooms": {
                        "name": "Patient Rooms",
                        "description": "The doors to the patient rooms are all slightly ajar.",
                        "actions": [
                            {
                                "label": "Peek into Rooms",
                                "effect": {
                                    "type": "narrative_update",
                                    "message": "You peek into a few rooms. They are all empty and bare, except for the faint scratching of tally marks on the walls. One room has a broken clock on the floor, its hands frozen at 3:14."
                                }
                            }
                        ]
                    }
                },
                "exits": {},
                "next_room_id": "asylum_escape_chamber"
            },
            "asylum_escape_chamber": {
                "name": "Abandoned Asylum Exit",
                "description": "You've found a way out of the asylum through the doctor's office!",
                "image": "asylum.jpg",
                "puzzles": {
                    "final_escape_puzzle": {
                        "name": "Final Escape",
                        "description": "The path to freedom lies ahead. Simply choose to escape.",
                        "solution": ["ESCAPE_THE_ASYLUM"],
                        "type": "action_trigger",
                        "difficulty": "easy",
                        "prerequisites": [],
                        "outcomes": ["game_completed"],
                        "reveal_on_solve": [],
                        "triggers_event": "escape_game"
                    }
                },
                "interactables": {
                    "secret_exit": {
                        "name": "Secret Exit",
                        "description": "A hidden exit from the asylum.",
                        "actions": [
                            {
                                "label": "Escape the Asylum",
                                "effect": {
                                    "type": "trigger_puzzle",
                                    "puzzle_id": "final_escape_puzzle",
                                    "message": "You slip out of the asylum, the whispers fading behind you."
                                }
                            }
                        ]
                    }
                },
                "exits": {}
            }
        }
    }
}

# Define solution mapping for puzzles
PUZZLE_SOLUTIONS = {
    "ancient_symbol_door_puzzle": "eyetears",
    "silent_word_puzzle": "silence",
    "engineering_door_puzzle": "alpha7",
    "core_stabilization_puzzle": "pic",
    "pressure_puzzle": "528",
    "specimen_analysis_puzzle": "fdf",
    "bridge_power_puzzle": "rgb",
    "engine_diagnostic_puzzle": "dge",
    "funhouse_door_puzzle": "rybg",
    "maze_riddle_puzzle": "book",
    "play_area_puzzle": "map",
    "toy_block_puzzle": "roygbiv",
    "gumdrop_bridge_puzzle": "yellow",
    "gingerbread_door_puzzle": "13",
    "foyer_puzzle": "1200",
    "library_riddle_puzzle": "book",
    "tomb_door_puzzle": "ra",
    "sarcophagus_puzzle": "jackalfalconscarab",
    "reception_puzzle": "314",
    "wards_puzzle": "clock",
}
