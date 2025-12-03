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
*   **Related Functional Requirements (FRs):** FR-001 (Dynamic Content Generation), FR-005 (Detailed specifications for puzzle types), FR-009 (Small Puzzle Set)
*   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.
*   **Rationale:** This introduces the complexity of dynamic puzzles only after the narrative framework is stable. It uses "Puzzle Dependency Chains" to ensure all generated games are solvable.

### Story 3.1: Integrate AI Puzzle Generation Service
As a developer,
I want to integrate an AI service capable of generating puzzles,
So that we can dynamically create interactive challenges for the game.

**Acceptance Criteria:**

**Given** an AI puzzle generation service (e.g., Gemini API),
**When** a prompt is sent to the service (e.g., "Generate a riddle for a magical library theme"),
**Then** the service returns a coherent puzzle description and solution.
**And** the application can successfully receive and parse this puzzle.

**Prerequisites:** Story 2.1 (AI Narrative Generation Service)

**Technical Notes:** Similar to Story 2.1, this will use the **Gemini API (Gemini Pro / Gemini 1.5 Pro)** and **Flask API Routes** for secure interaction. Prompt engineering will focus on puzzle mechanics and types (e.g., Observation, Riddle, etc.). Background processing (**Celery with Redis**) may be needed for slow AI generation, but this is deferred.

### Story 3.2: Implement Dynamic Puzzle Adaptation
As a game designer,
I want the AI to dynamically adapt puzzles based on player actions and game state,
So that the challenges feel responsive and personalized.

**Acceptance Criteria:**

**Given** a puzzle has been generated,
**When** the player attempts a solution,
**Then** the AI evaluates the attempt and adapts the puzzle's difficulty or provides contextual hints if needed.
**And** the game state reflects the puzzle's progression.

**Prerequisites:** Story 3.1 (AI Puzzle Generation Service), Story 1.2 (Game State Management)

**Technical Notes:** This will require sophisticated prompt engineering to guide the AI's adaptation logic. Game state (`GameSession.puzzleState`) will be crucial for providing context to the AI for dynamic adaptation.

### Story 3.3: Implement Puzzle Dependency Chains
As a game designer,
I want to ensure AI-generated puzzles are always solvable and logically connected,
So that players never encounter unsolvable scenarios.

**Acceptance Criteria:**

**Given** a set of dynamically generated puzzles for an escape room,
**When** the AI generates the puzzle sequence,
**Then** the puzzles are arranged in a solvable dependency chain (e.g., key for door A is found by solving puzzle B).
**And** the game verifies the solvability of the generated chain.

**Prerequisites:** Story 3.2 (Dynamic Puzzle Adaptation)

**Technical Notes:** This will involve internal AI logic for managing puzzle prerequisites and outcomes, possibly through a graph-based representation in the prompt. This is a critical component of the **Structured Prompting Strategy** for puzzle coherence.

### Story 3.4: Integrate Player Puzzle Interaction
As a player,
I want to interact with puzzles using contextual options and input mechanisms,
So that I can attempt solutions and progress through the game.

**Acceptance Criteria:**

**Given** a puzzle is presented,
**When** the player selects an interaction option (e.g., "Examine the inscription", "Try combination 123"),
**Then** the game processes the input and provides feedback based on the AI's puzzle logic.

**Prerequisites:** Story 1.4 (Core Interaction Model), Story 3.1 (AI Puzzle Generation Service)

**Technical Notes:** This will utilize existing `.option-btn` components for choices and potentially integrate a text input for more complex puzzle answers. **Feedback Patterns** will be used to communicate success or failure of puzzle attempts, ensuring a consistent user experience.

### Epic 4: Expanding Variety and Replayability
*   **Related Functional Requirements (FRs):** FR-001 (Dynamic Content Generation), FR-002 (Player-Driven Customization), FR-005 (Detailed specifications for puzzle types), FR-006 (User flow for Game Setup)
*   **Goal:** Increase the breadth of content and player choice to deliver on the promise of endless replayability.
*   **Rationale:** This epic now focuses on scaling content (more themes, puzzles, visuals), which is a much lower risk after the core dynamic systems have been proven to be stable and coherent.

### Story 4.1: Implement Dynamic Difficulty Adjustment
As a game designer,
I want the AI to dynamically adjust the game's difficulty based on player performance,
So that the challenge remains engaging and fair.

**Acceptance Criteria:**

**Given** a player's performance in a series of puzzles (e.g., time taken, hints used),
**When** the AI evaluates this performance,
**Then** the AI subtly adjusts parameters for future puzzles (e.g., complexity, number of steps) to maintain an optimal challenge level.

**Prerequisites:** Story 3.2 (Implement Dynamic Puzzle Adaptation), Story 1.2 (Game State Management)

**Technical Notes:** This will require the `GameSession` to track player performance metrics. AI prompt engineering will incorporate these metrics to influence puzzle generation parameters, which aligns with the "Advanced AI" future consideration in the PRD.

### Story 4.2: Expand Library of Visual Assets and Themes
As a game designer,
I want to expand the available library of visual assets and themes,
So that players have more diverse and immersive choices for their escape rooms.

**Acceptance Criteria:**

**Given** a new set of images and themes are added to the game,
**When** a player selects a new theme,
**Then** the AI can generate room descriptions and puzzles consistent with the expanded library.

**Prerequisites:** Story 1.5 (Display Basic Visuals for Rooms)

**Technical Notes:** This involves curating and integrating more free-to-use images into the `static/images/` directory and updating the AI's understanding of available themes through prompt adjustments (Structured Prompting Strategy).

### Story 4.3: Implement Enhanced Game Setup Flow
As a player,
I want an enhanced game setup flow with more options and clearer guidance,
So that I can customize my experience more effectively.

**Acceptance Criteria:**

**Given** the game setup menu,
**When** I navigate through the options,
**Then** I can choose from an expanded list of themes, locations, puzzle types, and difficulty levels, with clear descriptions for each.

**Prerequisites:** Story 2.4 (Dynamic Theme and Location Integration)

**Technical Notes:** The UX design already specifies a "New Game Creation" flow with "Design Your Own" and "AI-Driven" modes. This story will enhance the "Design Your Own" wizard with expanded options, potentially using `.option-btn` components and improved instructional text from the UX design's "User Journey Flows" and "Component and Pattern Library" sections.

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

**Technical Notes:** This will involve setting up the git repository. We will use **Python (3.14.1)** with **Flask (3.1.2)** as the web framework. **Tailwind CSS (4.1.17)** will be used for styling. **Pytest** will be the testing framework, **Black** for formatting, and **Flake8** for linting. **Python's pip** will manage dependencies. A basic CI/CD pipeline using GitHub Actions or similar will be implemented. The project structure will follow a modular Flask layout with `app.py`, `static/`, `templates/`, `models.py`, `routes.py`, and `services/` directories.

### Story 1.2: Implement Basic Game State Management

As a developer,
I want to implement a basic game state management system,
So that we can track the player's progress through the escape room.

**Related Functional Requirements (FRs):** FR-002 (Player-Driven Customization)

**Acceptance Criteria:**

**Given** a new game is started,
**When** the player moves from "Room 1" to "Room 2",
**Then** the game state object is updated to `{'current_room': 'Room 2'}`.
**And** when the player interacts with the "key" in "Room 2",
**Then** the game state object is updated to `{'inventory': ['key']}`.

**Prerequisites:** Story 1.1

**Technical Notes:** Game state will be managed and persisted using **Supabase (PostgreSQL 16.x)** as the database, accessed via **SQLAlchemy (2.0.44)** ORM and the **supabase (2.24.0)** Python client library. The core data model will be `GameSession`, including fields like `id`, `playerId`, `currentRoom`, `inventory`, `gameHistory`, `narrativeState`, `puzzleState`, `startTime`, `lastUpdated`, `theme`, `location`, `difficulty`. This ensures authoritative server-side state management.

### Story 1.3: Create a Static, Hard-coded Escape Room

As a game designer,
I want to create a single, hard-coded escape room with a few rooms and puzzles,
So that we have a complete, playable experience to test the core mechanics.

**Related Functional Requirements (FRs):** FR-009 (Small Puzzle Set), FR-004 (Core Interaction Loop)

**Acceptance Criteria:**

**Given** the game has started,
**When** the player navigates through the rooms,
**Then** they encounter a 3-room sequence with at least two distinct puzzles (e.g., an observation puzzle in Room 1, a riddle in Room 2).
**And** solving the final puzzle in Room 3 triggers a "You escaped!" message.

**Prerequisites:** Story 1.2

**Technical Notes:** The room descriptions, puzzle logic, and solutions will be hard-coded for this story. This will serve as the "golden path" for testing. Image assets for rooms will be stored locally in the `static/images/` directory.

### Story 1.4: Implement the Core Interaction Model

As a player,
I want to interact with the game world through a set of contextual options and a "go back" function,
So that I can navigate and solve puzzles.

**Related Functional Requirements (FRs):** FR-003 (Hybrid Interaction Model), FR-004 (Core Interaction Loop)

**Acceptance Criteria:**

**Given** the player is in a room with a "locked door" and a "note",
**When** the game presents interaction options,
**Then** the options are displayed as a numbered list, such as: `1. Examine the locked door`, `2. Read the note`, `3. Look around the room`, `4. Go back`.
**And** the player can select an option by entering the corresponding number.

**Prerequisites:** Story 1.3

**Technical Notes:** The interaction model will present four contextual options based on the hard-coded room and puzzle data. This will be a hybrid interaction model combining text-based commands and dynamic visual feedback. User choices will be rendered as `.option-btn` elements. In-game navigation will use numbered options within the main text box (`.immersive-option`). **Accessibility** will be ensured with keyboard navigation and visible focus indicators (a 2px solid border using `--color-primary` for `:focus-visible`). Flask API Routes will handle communication between the frontend and AI generation logic.

### Story 1.5: Display Basic Visuals for Rooms

As a player,
I want to see a background image for each room,
So that the game feels more immersive.

**Related Functional Requirements (FRs):** FR-010 (Basic Visuals)

**Acceptance Criteria:**

**Given** the player enters a new room,
**When** the room description is displayed,
**Then** a corresponding background image for that room is also displayed.

**Prerequisites:** Story 1.3

**Technical Notes:** This will involve creating a simple mapping between the hard-coded rooms and a library of pre-selected, free-to-use images sourced from a platform like Unsplash or Pexels, ensuring licenses are compatible with the project. The visual foundation will establish a retro-futuristic, gritty, and immersive atmosphere using a defined color system (e.g., `--color-background: #212529`) and typography (Heading: `Press Start 2P`, Body: `Roboto Mono`). The application will be responsive across Mobile, Tablet, and Desktop breakpoints. Decorative background images will use `alt=""` for accessibility (WCAG 2.1 Level AA compliant color contrast). Image assets will be stored locally in the `static/images/` directory.

---

## Epic 2: Introducing the AI Storyteller

**Goal:** Replace the static story and room descriptions from Epic 1 with AI-generated content, while ensuring coherence.

### Story 2.1: Integrate AI Narrative Generation Service

As a developer,
I want to integrate an AI service capable of generating narrative text,
So that we can dynamically create story elements for the game.

**Related Functional Requirements (FRs):** FR-001 (Dynamic Content Generation), FR-007 (AI-Generated Narrative)

**Acceptance Criteria:**

**Given** an AI narrative generation service (e.g., Gemini API, OpenAI GPT),
**When** a prompt is sent to the service (e.g., "Generate a mysterious story for an escape room set in an ancient tomb"),
**Then** the service returns a coherent narrative text.
**And** the application can successfully receive and parse this narrative.

**Prerequisites:** Story 1.1 (Project Initialization), Story 1.2 (Game State Management)

**Technical Notes:** This will involve setting up API keys, handling API requests and responses, and basic error handling. The prompt engineering should include instructions to encourage creative and non-generic outputs. We will use **Gemini Pro / Gemini 1.5 Pro** via the **`google-generativeai 0.8.5`** Python client library. **Flask API Routes** will be used to secure AI API keys and provide simple RESTful endpoints for frontend interaction. Prompt management will utilize a **Structured Prompting Strategy** with narrative archetypes. If AI generation proves to be slow, **Celery with Redis** will be considered for background processing, but this is deferred. If AI generation fails, an inline error message will be displayed on the AI Prompt Screen with a retry button.

### Story 2.2: Dynamic Room Description Generation

As a game designer,
I want the AI to dynamically generate unique room descriptions based on the chosen theme and narrative,
So that each playthrough offers fresh environments.

**Related Functional Requirements (FRs):** FR-001 (Dynamic Content Generation), FR-007 (AI-Generated Narrative)

**Acceptance Criteria:**

**Given** a game with a selected theme and an ongoing narrative,
**When** the AI is prompted for a room description, including the theme and a narrative summary,
**Then** the AI generates a unique description for that room that is consistent with both the theme and the narrative.
**And** this description is displayed to the player.

**Prerequisites:** Story 2.1 (AI Narrative Generation), Story 1.3 (Static Escape Room - for context of rooms), Story 1.4 (Core Interaction Model - for displaying description).

**Technical Notes:** The AI prompt will need to include context about the current room, previous rooms, and the overall narrative to maintain coherence. The **Structured Prompting Strategy** will be crucial to guide AI generation effectively.

### Story 2.3: Implement Narrative Archetypes for Coherence

As a game designer,
I want to guide the AI with narrative archetypes or story skeletons,
So that the generated stories remain coherent and logical across playthroughs.

**Related Functional Requirements (FRs):** FR-001 (Dynamic Content Generation), FR-007 (AI-Generated Narrative)

**Acceptance Criteria:**

**Given** a set of predefined narrative archetypes,
**When** the AI generates a story,
**Then** the generated story follows the key structural beats of the selected archetype, while still allowing for creative variation in plot details, characters, and events.
**And** the story flow feels logical and purposeful to the player.

**Prerequisites:** Story 2.1 (AI Narrative Generation), Story 2.2 (Dynamic Room Description Generation).

**Technical Notes:** This could involve crafting specific AI prompts that include archetype instructions or using a multi-turn conversation with the AI to guide the narrative generation. The archetypes should also generate "narrative constraints" to keep the AI on track. This falls under the **Structured Prompting Strategy** to ensure coherence and guide AI generation.

### Story 2.4: Dynamic Theme and Location Integration

As a player,
I want my chosen theme and location to influence the AI-generated story and room descriptions,
So that my customization choices feel impactful.

**Related Functional Requirements (FRs):** FR-001 (Dynamic Content Generation), FR-002 (Player-Driven Customization)

**Acceptance Criteria:**

**Given** the player selects a theme (e.g., "Space Station") and location (e.g., "Mars Colony"),
**When** the AI generates the narrative and room descriptions,
**Then** the content consistently reflects the chosen theme and location.

**Prerequisites:** Story 2.2 (Dynamic Room Description Generation), Story 2.3 (Narrative Archetypes).

**Technical Notes:** The game setup flow will need to pass the chosen theme and location as parameters to the AI generation prompts. These parameters will be incorporated into the **Structured Prompting Strategy** to guide the AI's content generation, ensuring consistency with player choices.

---

## Epic 5: Game Utility Features

**Goal:** Provide players with essential utility features such as saving/loading games, getting help, and adjusting options.

### Story 5.1: Implement Save/Load Game Functionality

As a player,
I want to save my game progress and load it later,
So that I can continue my adventure at any time.

**Note on Scope:** The `prd.md` explicitly lists "Load/Save game functionality" as "Out of Scope (MVP)". Its inclusion here suggests a change in MVP scope or that Epic 5 is intended for a post-MVP phase. This discrepancy needs clarification.

**Acceptance Criteria:**

**Given** I am in the middle of a game,
**When** I select the "Save Game" option,
**Then** my current progress (e.g., room, inventory, narrative state) is saved.
**And** from the main menu, I can select "Load Game" to resume from my saved state.

**Prerequisites:** Story 1.2 (Game State Management)

**Technical Notes:** This will require serializing the game state and storing it using the `GameSession` model in **Supabase (PostgreSQL)** via **SQLAlchemy**. The "Load Game" screen (UX User Journey Flow) will display the saved game's name (e.g., location), the date it was saved, and the total time elapsed (HH:MM:SS). If a saved game fails to load or is corrupted, a clear message (e.g., "Failed to load game.") with "Try Again" or "Delete Save" options will be displayed (UX Error Handling). **Empty States** will be handled by displaying a "No Saved Games Yet!" message if no saves exist.

### Story 5.2: Create a Help/Information System

As a player,
I want to access help or information about the game,
So that I can understand the rules and objectives.

**Acceptance Criteria:**

**Given** I am in the game,
**When** I select the "Help" option,
**Then** a screen or dialog appears with information about how to play, the current objective, and any other relevant help text.

**Prerequisites:** None

**Technical Notes:** The help system should be accessible from anywhere in the game. It will be implemented using a **Modal Pattern** from the UX Design Specification, allowing it to display critical information without navigating away from the current screen.

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

**Technical Notes:** The options menu should be accessible from anywhere in the game. It will be implemented using a **Modal Pattern** from the UX Design Specification. Options will be presented using **Form Patterns**: **Toggle Switch (`.toggle-btn`)** for binary choices (e.g., sound on/off), **Select Menu (`<select>`)** for lists (e.g., language), and **Range Slider (`<input type="range">`)** for continuous adjustments (e.g., volume).

---

<!-- End epic repeat -->

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._
