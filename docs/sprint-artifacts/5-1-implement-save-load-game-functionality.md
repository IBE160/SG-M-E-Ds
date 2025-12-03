# Story 5.1: Implement Save/Load Game Functionality

Status: drafted

## Story

As a player,
I want to save my game progress and load it later,
So that I can continue my adventure at any time.

## Acceptance Criteria

1.  Given I am in the middle of a game, when I select the "Save Game" option, then my current progress (e.g., room, inventory, narrative state) is saved.
2.  And from the main menu, I can select "Load Game" to resume from my saved state.

## Tasks / Subtasks

- [ ] AC 1: Extend `services/game_logic.py` to handle save game operations.
  - [ ] Subtask: Implement a function to serialize the current `GameSession` state and store it in the database.
- [ ] AC 2: Extend `services/game_logic.py` to handle load game operations.
  - [ ] Subtask: Implement a function to retrieve a saved `GameSession` from the database and deserialize it.
- [ ] AC 1, 2: Create Flask API routes for save/load functionality.
  - [ ] Subtask: Define a `POST /save_game` endpoint in `routes.py` to trigger game saving.
  - [ ] Subtask: Define a `GET /load_game/<int:session_id>` endpoint in `routes.py` to retrieve a specific saved game.
  - [ ] Subtask: Define a `GET /saved_games` endpoint to list available saved games (e.g., for display in a "Load Game" screen).
- [ ] AC 1, 2: Implement UI for save/load interaction.
  - [ ] Subtask: Create/modify Jinja2 templates for a "Save Game" option (e.g., in a pause menu) and a "Load Game" screen (e.g., displaying a list of saved games).
  - [ ] Subtask: Implement client-side logic to call the save/load API endpoints.
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for `services/game_logic.py` functions related to serialization, deserialization, and database interaction for save/load.
  - [ ] Subtask: Write integration tests for Flask routes (`/save_game`, `/load_game`, `/saved_games`), verifying correct data persistence and retrieval.
  - [ ] Subtask: Write E2E tests to simulate player saving and loading games, verifying state is correctly preserved and restored.

## Dev Notes

### Requirements Context Summary

**From Epic 5: Game Utility Features**
-   **Goal:** Provide players with essential utility features such as saving/loading games, getting help, and adjusting options.

**From PRD (Product Requirements Document) - Future Consideration: Progression Management**
-   **Progression Management:** Building save/load game functionality.
-   **Note on Scope Discrepancy:** The `prd.md` explicitly lists "Load/Save game functionality" as "Out of Scope (MVP)". Its inclusion in this epic suggests a change in MVP scope or that Epic 5 is intended for a post-MVP phase, or that it is now considered In Scope. For the purpose of this tech spec, it is treated as In Scope.

**From Architecture Document (`docs/architecture.md`)**
-   **Data Persistence:** Supabase (PostgreSQL) managed via SQLAlchemy ORM.
-   **Game State Management & Persistence:** `GameSession` entity will track game state.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 4.3: Implement Enhanced Game Setup Flow (Status: drafted)**

-   **Goal:** An enhanced game setup flow with more options and clearer guidance, So that I can customize my experience more effectively.
-   **Acceptance Criteria:** Choose from an expanded list of themes, locations, puzzle types, and difficulty levels, with clear descriptions for each.
-   **Key Technical Notes:** Defining expanded options, `GET /game_setup_options` API, enhanced UI using Jinja2 templates and `.option-btn` components, integrating choices with `GameSession` initialization.
-   **Relevant Learnings for Story 5.1:**
    *   The `GameSession` model is the central storage for player choices and game state, making it directly relevant for save/load operations.
    *   Flask API routes and Jinja2 templates are established for frontend-backend communication and UI rendering, providing the framework for save/load interfaces.
    *   The use of SQLAlchemy for data persistence is foundational for saving and loading `GameSession` objects.

[Source: docs/sprint-artifacts/4-3-implement-enhanced-game-setup-flow.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-5.md]
- [Source: docs/sprint-artifacts/4-3-implement-enhanced-game-setup-flow.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
