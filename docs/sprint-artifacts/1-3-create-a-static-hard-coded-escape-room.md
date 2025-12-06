# Story 1.3: Create a Static, Hard-coded Escape Room

Status: review

## Story

As a game designer,
I want to create a single, hard-coded escape room with a few rooms and puzzles,
So that we have a complete, playable experience to test the core mechanics.

## Acceptance Criteria

1.  Given the game has started, when the player navigates through the rooms, then they encounter a 3-room sequence with at least two distinct puzzles (e.g., an observation puzzle in Room 1, a riddle in Room 2).
2.  And solving the final puzzle in Room 3 triggers a "You escaped!" message.

## Tasks / Subtasks

- [x] AC 1: Design and define the 3-room sequence and puzzles.
  - [x] Subtask: Identify names and descriptions for Room 1, Room 2, Room 3.
  - [x] Subtask: Define at least two distinct puzzle types and their solutions for Room 1 and Room 2.
- [x] AC 1: Implement the hard-coded room data.
  - [x] Subtask: Create a data structure (e.g., Python dictionary in a new module like `data/rooms.py`) to hold room descriptions, connected rooms, and puzzle details.
- [x] AC 1: Implement the hard-coded puzzle logic.
  - [x] Subtask: Create functions in `services/game_logic.py` to evaluate puzzle solutions for the defined puzzles.
- [x] AC 1: Integrate room navigation logic with Flask routes.
  - [x] Subtask: Modify existing `move_player` route or create new routes to handle transitions between the 3 hard-coded rooms.
- [x] AC 2: Implement "You escaped!" message display.
  - [x] Subtask: Add logic to `routes.py` to detect completion of the final puzzle and render an escape message (e.g., via a new template or a message in the existing UI).
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for the hard-coded room data structure.
  - [x] Subtask: Write unit tests for puzzle logic functions.
  - [x] Subtask: Write integration tests for Flask routes handling room navigation and puzzle interaction, verifying correct state changes and "You escaped!" trigger.

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

- docs/sprint-artifacts/1-3-create-a-static-hard-coded-escape-room.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

- **2025-12-04**: Planned and implemented AC 1: Designed 3-room sequence (`ancient_library`, `mysterious_observatory`, `escape_chamber`) and two distinct puzzles (`observation_puzzle`, `riddle_puzzle`). Created `ai-escape-app/data/rooms.py` to hold hard-coded room and puzzle data.

### Completion Notes List
- Added `solve_puzzle` function to `ai-escape-app/services/game_logic.py` to evaluate puzzle solutions.
- Added comprehensive unit tests for `solve_puzzle` function in `ai-escape-app/tests/test_game_logic.py`, ensuring correct logic for solving puzzles, handling incorrect solutions, already solved puzzles, and invalid inputs. All tests passed.
- Modified `ai-escape-app/routes.py` `move_player` route to use `ROOM_DATA` for valid room transitions and added `solve_puzzle_route` for puzzle interaction.
- Updated `ai-escape-app/tests/test_app.py` to include integration tests for valid/invalid room movements and correct/incorrect/already-solved puzzle attempts. All tests passed.
- Modified `ai-escape-app/routes.py` `move_player` function to include game completion logic, triggering "You escaped!" message upon entering `escape_chamber` if all prior puzzles are solved.
- Added new integration test `test_game_escape` in `ai-escape-app/tests/test_app.py` to verify the game escape logic, ensuring all puzzles are solved and the "You escaped!" message is triggered correctly. All tests passed.
- Verified `ai-escape-app/tests/test_rooms_data.py` covers unit tests for the room data structure.
- Verified `ai-escape-app/tests/test_game_logic.py` covers unit tests for puzzle logic functions.
- Verified `ai-escape-app/tests/test_app.py` covers integration tests for Flask routes handling room navigation and puzzle interaction, including the `test_game_escape` to verify the "You escaped!" trigger. All tests passed.

### File List
- ai-escape-app/
  - data/
    - rooms.py
  - services/
    - game_logic.py (modified)
  - routes.py (modified)
  - tests/
    - test_game_logic.py (modified)
    - test_app.py (modified)
    - test_rooms_data.py (new)

## Change Log

- **2025-12-03**: Story created.
- **2025-12-04**: Story context regenerated.
