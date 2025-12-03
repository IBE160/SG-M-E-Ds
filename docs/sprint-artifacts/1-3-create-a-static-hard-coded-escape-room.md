# Story 1.3: Create a Static, Hard-coded Escape Room

Status: drafted

## Story

As a game designer,
I want to create a single, hard-coded escape room with a few rooms and puzzles,
So that we have a complete, playable experience to test the core mechanics.

## Acceptance Criteria

1.  Given the game has started, when the player navigates through the rooms, then they encounter a 3-room sequence with at least two distinct puzzles (e.g., an observation puzzle in Room 1, a riddle in Room 2).
2.  And solving the final puzzle in Room 3 triggers a "You escaped!" message.

## Tasks / Subtasks

- [ ] AC 1: Design and define the 3-room sequence and puzzles.
  - [ ] Subtask: Identify names and descriptions for Room 1, Room 2, Room 3.
  - [ ] Subtask: Define at least two distinct puzzle types and their solutions for Room 1 and Room 2.
- [ ] AC 1: Implement the hard-coded room data.
  - [ ] Subtask: Create a data structure (e.g., Python dictionary in a new module like `data/rooms.py`) to hold room descriptions, connected rooms, and puzzle details.
- [ ] AC 1: Implement the hard-coded puzzle logic.
  - [ ] Subtask: Create functions in `services/game_logic.py` to evaluate puzzle solutions for the defined puzzles.
- [ ] AC 1: Integrate room navigation logic with Flask routes.
  - [ ] Subtask: Modify existing `move_player` route or create new routes to handle transitions between the 3 hard-coded rooms.
- [ ] AC 2: Implement "You escaped!" message display.
  - [ ] Subtask: Add logic to `routes.py` to detect completion of the final puzzle and render an escape message (e.g., via a new template or a message in the existing UI).
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for the hard-coded room data structure.
  - [ ] Subtask: Write unit tests for puzzle logic functions.
  - [ ] Subtask: Write integration tests for Flask routes handling room navigation and puzzle interaction, verifying correct state changes and "You escaped!" trigger.

## Dev Notes

### Requirements Context Summary

**From Epic 1: Foundational Framework & A Single, Static Escape Room**
-   **Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a *single, hard-coded* story and puzzle chain.
-   **Rationale:** This ensures a working, enjoyable game *before* introducing the complexity of AI. It provides a "golden path" to test against and forces the integration of the interaction model and narrative flow from the start.

**From PRD (Product Requirements Document) - FR-009: Small Puzzle Set, FR-004: Core Interaction Loop**
-   **FR-009:** Specifies 2-3 distinct puzzle types (e.g., Observation, Riddle) that the AI can adapt (for future, but relevant for this story to define static puzzles).
-   **FR-004:** Relates to players interacting with rooms and objects through contextual options.

**From Architecture Document (`docs/architecture.md`)**
-   **Project Structure:** `static/images/` for images.
-   **Testing Strategy:** E2E Tests (Playwright) for full user flows. Unit and Integration tests using Pytest.
-   **API Pattern:** Flask API routes will handle communication between the frontend and backend game logic.
-   **Game State Transition Flow:** `GameSession` updates based on player actions (movement, interaction).

### Learnings from Previous Story

**From Story 1.2: Implement Basic Game State Management (Status: done)**

-   **Completion Notes List:**
    *   Defined GameSession data model using SQLAlchemy, including the addition of `SQLAlchemy` and `supabase` to `requirements.txt` and configuring database connection.
    *   Implemented basic CRUD operations for GameSession in `services/game_logic.py`, ensuring correct tracking of inventory updates.
    *   Integrated GameSession updates with Flask routes by modifying `app.py` and creating `routes.py` with dedicated API endpoints for game session management.
    *   Implemented comprehensive unit tests for the GameSession model and CRUD operations, and integration tests for all new Flask API routes, with all tests passing successfully.
-   **File List:**
    *   `ai-escape-app/models.py`
    *   `ai-escape-app/services/game_logic.py`
    *   `ai-escape-app/routes.py`
    *   `ai-escape-app/requirements.txt` (updated with SQLAlchemy, supabase)
    *   `ai-escape-app/tests/test_game_logic.py`
    *   `ai-escape-app/tests/test_app.py` (updated)

**Relevant Learnings for Story 1.3:**
- `GameSession` model and CRUD operations are established in `models.py` and `services/game_logic.py`, which will be foundational for tracking room and puzzle states.
- Flask routes and API endpoints are already set up in `routes.py`, providing the framework for integrating new navigation and interaction logic.
- The testing framework (Pytest) and initial test patterns are in place, ensuring new puzzle logic and routes can be properly tested.

[Source: docs/sprint-artifacts/1-2-implement-basic-game-state-management.md#Dev-Agent-Record]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]
- [Source: docs/sprint-artifacts/1-2-implement-basic-game-state-management.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
