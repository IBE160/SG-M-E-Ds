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

 