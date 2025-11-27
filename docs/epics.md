# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** Friday, 14 November 2025
**Project Level:** 3
**Target Scale:** single-user

---

## Overview

## Enhanced Epic Structure

### Epic 1: Foundational Framework & A Single, Static Escape Room
*   **Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a *single, hard-coded* story and puzzle chain.
*   **Rationale:** This ensures we have a working, enjoyable game *before* introducing the complexity of AI. It provides a "golden path" to test against and forces the integration of the interaction model and narrative flow from the start.

### Epic 2: Introducing the AI Storyteller
*   **Goal:** Replace the static story and room descriptions from Epic 1 with AI-generated content, while ensuring coherence.
*   **Rationale:** This isolates the challenge of narrative generation from puzzle generation. It directly integrates "Narrative Archetypes" to ensure the story is logical, tackling a key risk early.

### Epic 3: The AI Puzzle Master
*   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.
*   **Rationale:** This introduces the complexity of dynamic puzzles only after the narrative framework is stable. It uses "Puzzle Dependency Chains" to ensure all generated games are solvable.

### Epic 4: Expanding Variety and Replayability
*   **Goal:** Increase the breadth of content and player choice to deliver on the promise of endless replayability.
*   **Rationale:** This epic now focuses on scaling content (more themes, puzzles, visuals), which is a much lower risk after the core dynamic systems have been proven to be stable and coherent.

---

## Epic 1: Foundational Framework & A Single, Static Escape Room

**Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a *single, hard-coded* story and puzzle chain.

### Story 1.1: Project Initialization and Deployment Setup

As a developer,
I want to initialize the project structure and set up a basic deployment pipeline,
So that we have a foundation for building and deploying the game.

**Acceptance Criteria:**

**Given** a new project,
**When** the initialization script is run,
**Then** a standard project structure (e.g., `src`, `docs`, `tests`) is created.
**And** a basic `README.md` is generated with setup instructions.
**And** a simple "Hello World" version of the application can be automatically built and deployed to a free-tier cloud service (e.g., GitHub Pages, Vercel, Heroku).

**Prerequisites:** None.

**Technical Notes:** This will involve setting up the git repository, choosing a programming language and framework (e.g., Python with Flask/FastAPI, or Node.js with Express), and creating a simple CI/CD pipeline using GitHub Actions or similar.

### Story 1.2: Implement Basic Game State Management

As a developer,
I want to implement a basic game state management system,
So that we can track the player's progress through the escape room.

**Acceptance Criteria:**

**Given** a new game is started,
**When** the player moves from "Room 1" to "Room 2",
**Then** the game state object is updated to `{'current_room': 'Room 2'}`.
**And** when the player interacts with the "key" in "Room 2",
**Then** the game state object is updated to `{'inventory': ['key']}`.

**Prerequisites:** Story 1.1

**Technical Notes:** This could be a simple in-memory object or a more sophisticated state management library, depending on the chosen framework.

### Story 1.3: Create a Static, Hard-coded Escape Room

As a game designer,
I want to create a single, hard-coded escape room with a few rooms and puzzles,
So that we have a complete, playable experience to test the core mechanics.

**Acceptance Criteria:**

**Given** the game has started,
**When** the player navigates through the rooms,
**Then** they encounter a 3-room sequence with at least two distinct puzzles (e.g., an observation puzzle in Room 1, a riddle in Room 2).
**And** solving the final puzzle in Room 3 triggers a "You escaped!" message.

**Prerequisites:** Story 1.2

**Technical Notes:** The room descriptions, puzzle logic, and solutions will be hard-coded for this story. This will serve as the "golden path" for testing.

### Story 1.4: Implement the Core Interaction Model

As a player,
I want to interact with the game world through a set of contextual options and a "go back" function,
So that I can navigate and solve puzzles.

**Acceptance Criteria:**

**Given** the player is in a room with a "locked door" and a "note",
**When** the game presents interaction options,
**Then** the options are displayed as a numbered list, such as: `1. Examine the locked door`, `2. Read the note`, `3. Look around the room`, `4. Go back`.
**And** the player can select an option by entering the corresponding number.

**Prerequisites:** Story 1.3

**Technical Notes:** The interaction model will present four contextual options based on the hard-coded room and puzzle data.

### Story 1.5: Display Basic Visuals for Rooms

As a player,
I want to see a background image for each room,
So that the game feels more immersive.

**Acceptance Criteria:**

**Given** the player enters a new room,
**When** the room description is displayed,
**Then** a corresponding background image for that room is also displayed.

**Prerequisites:** Story 1.3

**Technical Notes:** This will involve creating a simple mapping between the hard-coded rooms and a library of pre-selected, free-to-use images sourced from a platform like Unsplash or Pexels, ensuring licenses are compatible with the project.

---

## Epic 2: Introducing the AI Storyteller

**Goal:** Replace the static story and room descriptions from Epic 1 with AI-generated content, while ensuring coherence.

### Story 2.1: Integrate AI Narrative Generation Service

As a developer,
I want to integrate an AI service capable of generating narrative text,
So that we can dynamically create story elements for the game.

**Acceptance Criteria:**

**Given** an AI narrative generation service (e.g., Gemini API, OpenAI GPT),
**When** a prompt is sent to the service (e.g., "Generate a mysterious story for an escape room set in an ancient tomb"),
**Then** the service returns a coherent narrative text.
**And** the application can successfully receive and parse this narrative.

**Prerequisites:** Story 1.1 (Project Initialization), Story 1.2 (Game State Management)

**Technical Notes:** This will involve setting up API keys, handling API requests and responses, and basic error handling. The prompt engineering should include instructions to encourage creative and non-generic outputs.

### Story 2.2: Dynamic Room Description Generation

As a game designer,
I want the AI to dynamically generate unique room descriptions based on the chosen theme and narrative,
So that each playthrough offers fresh environments.

**Acceptance Criteria:**

**Given** a game with a selected theme and an ongoing narrative,
**When** the AI is prompted for a room description, including the theme and a narrative summary,
**Then** the AI generates a unique description for that room that is consistent with both the theme and the narrative.
**And** this description is displayed to the player.

**Prerequisites:** Story 2.1 (AI Narrative Generation), Story 1.3 (Static Escape Room - for context of rooms), Story 1.4 (Core Interaction Model - for displaying description).

**Technical Notes:** The AI prompt will need to include context about the current room, previous rooms, and the overall narrative to maintain coherence.

### Story 2.3: Implement Narrative Archetypes for Coherence

As a game designer,
I want to guide the AI with narrative archetypes or story skeletons,
So that the generated stories remain coherent and logical across playthroughs.

**Acceptance Criteria:**

**Given** a set of predefined narrative archetypes,
**When** the AI generates a story,
**Then** the generated story follows the key structural beats of the selected archetype, while still allowing for creative variation in plot details, characters, and events.
**And** the story flow feels logical and purposeful to the player.

**Prerequisites:** Story 2.1 (AI Narrative Generation), Story 2.2 (Dynamic Room Description Generation).

**Technical Notes:** This could involve crafting specific AI prompts that include archetype instructions or using a multi-turn conversation with the AI to guide the narrative generation. The archetypes should also generate "narrative constraints" to keep the AI on track.

### Story 2.4: Dynamic Theme and Location Integration

As a player,
I want my chosen theme and location to influence the AI-generated story and room descriptions,
So that my customization choices feel impactful.

**Acceptance Criteria:**

**Given** the player selects a theme (e.g., "Space Station") and location (e.g., "Mars Colony"),
**When** the AI generates the narrative and room descriptions,
**Then** the content consistently reflects the chosen theme and location.

**Prerequisites:** Story 2.2 (Dynamic Room Description Generation), Story 2.3 (Narrative Archetypes).

**Technical Notes:** The game setup flow will need to pass the chosen theme and location as parameters to the AI generation prompts.

---

## Epic 5: Game Utility Features

**Goal:** Provide players with essential utility features such as saving/loading games, getting help, and adjusting options.

### Story 5.1: Implement Save/Load Game Functionality

As a player,
I want to save my game progress and load it later,
So that I can continue my adventure at any time.

**Acceptance Criteria:**

**Given** I am in the middle of a game,
**When** I select the "Save Game" option,
**Then** my current progress (e.g., room, inventory, narrative state) is saved.
**And** from the main menu, I can select "Load Game" to resume from my saved state.

**Prerequisites:** Story 1.2 (Game State Management)

**Technical Notes:** This will require serializing the game state and storing it, either locally or on a server.

### Story 5.2: Create a Help/Information System

As a player,
I want to access help or information about the game,
So that I can understand the rules and objectives.

**Acceptance Criteria:**

**Given** I am in the game,
**When** I select the "Help" option,
**Then** a screen or dialog appears with information about how to play, the current objective, and any other relevant help text.

**Prerequisites:** None

**Technical Notes:** The help system should be accessible from anywhere in the game.

### Story 5.3: Implement an Options Menu

As a player,
I want to adjust game options like sound effects,
So that I can customize my experience.

**Acceptance Criteria:**

**Given** I am in the game,
**When** I select the "Options" menu,
**Then** a screen or dialog appears with options to adjust settings (e.g., sound volume).
**And** changing these settings affects the game accordingly.

**Prerequisites:** None

**Technical Notes:** The options menu should be accessible from anywhere in the game.

---

<!-- End epic repeat -->

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._
