## Case Title  

AI Escape Room  

  

## Background  

- Traditional escape rooms are physical, but many people want a more accessible, digital experience.    

- An AI-driven text-based escape room allows players to solve puzzles and experience the excitement through a text interface without being physically present.  

  

## Purpose  

- Create an AI-driven text-based escape room where the player interacts through text commands, solves puzzles and finds clues to escape the room.    

  

## Target Users  

- Players who enjoy escape rooms and puzzles   

- Users who want an interactive AI experience   

- Students and teachers who can use it for learning or entertainment  

  

## Core Functionality  

  

### Must Have (MVP)  

- **Interpret player commands**: the player can type commands like look, open, take, read, use.  

- **Inventory management**: the player can collect and use objects.  

- **Puzzle status tracking**: the system keeps track of doors, codes, and solved puzzles.  

- **Descriptions and hints**: AI generates room descriptions and hints based on the player’s actions.  

  

### Nice to Have (Optional Extensions)  

- Time limit or move limit.   

- Support for multiple rooms and levels.   

- Randomly generated rooms and puzzles.   

- Multiplayer mode.  

  

## Data Requirements  

- **Player commands**: user input (look, take, use).  

- **Inventory**: objects collected by the player.  

- **Status**: solved puzzles, available actions, doors/locks.  

- **Log** (optional): number of moves or time used.  

  

  

## User Stories (optional)  

1. As a player, I want to see a room description so that I understand which objects I can interact with.   

2. As a player, I want to collect objects so that I can use them later to solve puzzles.   

3. As a player, I want to receive hints when I am stuck so that I can progress in the game.  

  

## Technical Constraints  

- Must support a text interface (terminal or simple UI).   

- Must store and update game status (JSON or similar).   

- AI should generate dynamic descriptions and hints.   

- Gameplay should be responsive and fast.  

  

## Success Criteria  

- The player can enter commands and receive meaningful responses.   

- Inventory and status are updated dynamically.   

- The game can be completed by solving puzzles and finding the key to escape.   

- Multiple rooms and puzzles can be added in later versions.  

 
### User Flow
## Player / Student Flow (Singleplayer)

# Login / Access

The player starts the application and logs in with their account (or plays as a guest).

The system checks for existing save files and displays the main menu with options:

Continue Game → Resume last session from “My Games.”

New Game → Start a new escape room experience.

History → View past playthroughs and performance logs.

# New Game Setup

When starting a new game, the player customizes preferences before the game begins:

Theme: Choose between Scary, Mystery, Futuristic, or Classic.

Difficulty: Normal or Assist (affects hint frequency and puzzle complexity). Can choose the difficulty: easy, normal, hard

Once preferences are confirmed, the game initializes the first room (JSON state created and stored).

# Introduction

The AI presents the setting and context of the escape room.

Example:
“You wake up in a dimly lit laboratory. A single locked door stands before you. You need to find a way out.”

The interface briefly explains how to interact (e.g., supported commands and how to request hints).

# Exploration & Interaction

The player interacts exclusively through text commands such as:
look around, examine desk, take key, use key on door, read note.

The command parser validates inputs and updates the game state (inventory, puzzles, flags).

The AI generates context-aware responses and dynamic room descriptions after each action.

# Puzzle Solving

The player investigates objects, collects clues, and solves at least three core puzzles (e.g., keypad, riddle, hidden mechanism).

Each puzzle has a defined state (solved: true/false) stored in the JSON game state.

If the player is stuck, they can use the hint command to receive AI-generated guidance (two-tier hint system: gentle → explicit).

# Saving & Loading

The player can manually type save or the system autosaves progress at checkpoints (after solving a puzzle or unlocking a new item).

Saved games are accessible from My Games in the main menu, allowing players to continue later.

# Winning & Completion

Once all required puzzles are solved, the player unlocks the final door.

The AI narrates the escape sequence and displays a summary:

Puzzles solved, moves taken, time spent, and hints used.

The player can then:

Replay with a new theme, or

Return to Main Menu to view their history.

## Teacher / Instructor Flow (Observer Role)

# Access / Setup

The instructor logs into an admin or observer account.

They can predefine which theme or puzzle configuration the students will use for classroom sessions.

Teachers may choose to lock the difficulty level or enable/disable hints for assessment purposes.

# Monitoring / Observation

During gameplay, the instructor can observe progress through a summary dashboard or exported logs (e.g., via Supabase or local JSON):

Number of moves

Puzzles solved

Hints requested

Completion time

The instructor does not participate in gameplay.

# Reflection & Learning Discussion

After the session, teachers review gameplay logs with students to discuss:

Logical reasoning and problem-solving steps

Efficiency (fewest moves or minimal hints)

How AI-generated hints supported the learning experience

Logs can optionally be exported (CSV/JSON) for documentation or analysis