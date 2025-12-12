# data/game_options.py

GAME_SETUP_OPTIONS = {
    "themes": [
        {"id": "mystery", "name": "Classic Mystery", "description": "Solve a perplexing whodunit in an old mansion or ancient library."},
        {"id": "sci-fi", "name": "Sci-Fi Adventure", "description": "Explore futuristic landscapes and derelict spaceships, facing technological puzzles."},
        {"id": "fantasy", "name": "Fantasy Quest", "description": "Embark on an epic journey through magical realms, encountering mythical creatures and enchanted artifacts."},
        {"id": "horror", "name": "Supernatural Horror", "description": "Survive a terrifying encounter with the unknown in a haunted asylum or cursed crypt."},
        {"id": "underwater", "name": "Deep Sea Exploration", "description": "Navigate the crushing depths in an underwater lab, unraveling marine mysteries."},
        {"id": "noir_detective", "name": "Noir Detective", "description": "Step into a gritty, black-and-white world of fedoras and femme fatales."},
        {"id": "steampunk_mystery", "name": "Steampunk Mystery", "description": "A retro-futuristic world powered by steam, gears, and intricate puzzles."},
        {"id": "post_apocalyptic", "name": "Post-Apocalyptic", "description": "Scavenge for clues in a desolate, fallen world."}
    ],
    "locations": [
        {"id": "ancient_library", "name": "Ancient Library", "description": "A dusty, knowledge-filled sanctuary."},
        {"id": "mysterious_observatory", "name": "Mysterious Observatory", "description": "A celestial dome filled with star charts and arcane instruments."},
        {"id": "escape_chamber", "name": "Escape Chamber", "description": "The final room, heavy steel door, complex lock."},
        {"id": "sci_fi_hangar", "name": "Sci-Fi Hangar", "description": "A vast space for starships, humming with dormant power."},
        {"id": "underwater_lab", "name": "Underwater Laboratory", "description": "Deep blue light, complex machinery, and strange marine life."},
        {"id": "abandoned_mansion", "name": "Abandoned Mansion", "description": "A sprawling, decaying estate with secrets hidden in every shadow."},

        {"id": "ancient_tomb", "name": "Ancient Tomb", "description": "Explore the forgotten burial grounds of an ancient civilization."}
    ],
    "puzzle_types": [
        {"id": "riddle", "name": "Riddle", "description": "Classic word puzzles requiring lateral thinking."},
        {"id": "logic", "name": "Logic Puzzle", "description": "Deduction and pattern recognition challenges."},
        {"id": "observation", "name": "Observation Puzzle", "description": "Requires keen eye for detail in the environment."},
        {"id": "mechanical", "name": "Mechanical Puzzle", "description": "Involves manipulating physical (or virtual) mechanisms."},
        {"id": "cipher", "name": "Cipher/Code", "description": "Deciphering hidden messages and codes."},
        {"id": "musical", "name": "Musical Puzzle", "description": "Solve puzzles using melodies, rhythms, or instruments."},
        {"id": "pattern_recognition", "name": "Pattern Recognition", "description": "Identify and reproduce sequences in visual or auditory data."},
        {"id": "encryption", "name": "Encryption Puzzle", "description": "Break complex codes and ciphers."}
    ],
    "difficulty_levels": [
        {"id": "easy", "name": "Easy", "description": "Gentle introduction, more hints, straightforward puzzles."},
        {"id": "medium", "name": "Medium", "description": "Balanced challenge, moderate hints, engaging puzzles."},
        {"id": "hard", "name": "Hard", "description": "Demanding puzzles, minimal hints, for experienced players."},
        {"id": "insane", "name": "Insane", "description": "Only for the truly masochistic. No hints, brutal puzzles, unforgiving."}
    ]
}
