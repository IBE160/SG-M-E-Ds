Status: review

## Story

As a player,
I want to save my game progress and load it later,
So that I can continue my adventure at any time.

## Acceptance Criteria

1.  Given I am in the middle of a game, when I select the "Save Game" option, then my current progress (e.g., room, inventory, narrative state) is saved.
2.  And from the main menu, I can select "Load Game" to resume from my saved state.

## Tasks / Subtasks

- [x] AC 1: Extend `services/game_logic.py` to handle save game operations.
  - [x] Subtask: Implement a function to serialize the current `GameSession` state and store it in the database.
- [x] AC 2: Extend `services/game_logic.py` to handle load game operations.
  - [x] Subtask: Implement a function to retrieve a saved `GameSession` from the database and deserialize it.
- [x] AC 1, 2: Create Flask API routes for save/load functionality.
  - [x] Subtask: Define a `POST /save_game` endpoint in `routes.py` to trigger game saving.
  - [x] Subtask: Define a `GET /load_game/<int:session_id>` endpoint in `routes.py` to retrieve a specific saved game.
  - [x] Subtask: Define a `GET /saved_games` endpoint to list available saved games (e.g., for display in a "Load Game" screen).
- [x] AC 1, 2: Implement UI for save/load interaction.
  - [x] Subtask: Create/modify Jinja2 templates for a "Save Game" option (e.g., in a pause menu) and a "Load Game" screen (e.g., displaying a list of saved games).
  - [x] Subtask: Implement client-side logic to call the save/load API endpoints.
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for `services/game_logic.py` functions related to serialization, deserialization, and database interaction for save/load.
  - [x] Subtask: Write integration tests for Flask routes (`/save_game`, `/load_game`, `/saved_games`), verifying correct data persistence and retrieval.
  - [x] Subtask: Write E2E tests to simulate player saving and loading games, verifying state is correctly preserved and restored.

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
- docs/sprint-artifacts/5-1-implement-save-load-game-functionality.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

- Implemented Save Game functionality in `services/game_logic.py`, including `save_game_state`, `load_game_state`, and `get_saved_games` functions.
- Modified `models.py` to include the `SavedGame` model and a `to_dict()` method for `GameSession`, along with a `player_id` for `SavedGame`.
- Added new API routes in `routes.py`: `POST /save_game`, `GET /load_game/<int:saved_game_id>`, and `GET /saved_games`.
- Implemented UI for Save/Load in `templates/index.html` (Load Game) and `templates/game.html` (Save Game), including client-side JavaScript logic.
- Created comprehensive unit, integration, and E2E tests for save/load functionality. All tests are passing.

### File List

- ai-escape-app/models.py (modified)
- ai-escape-app/services/game_logic.py (modified)
- ai-escape-app/routes.py (modified)
- ai-escape-app/templates/index.html (modified)
- ai-escape-app/templates/game.html (modified)
- ai-escape-app/tests/unit/test_game_logic_save_load.py (new)
- ai-escape-app/tests/integration/test_save_load_routes.py (new)
- ai-escape-app/tests/e2e/test_save_load_flow.py (new)

## Change Log

- **2025-12-03**: Story created.
- **2025-12-04**: Story context regenerated.
- **2025-12-09**: Implemented Save/Load Game functionality, including data model extensions, service logic, API routes, UI integration, and comprehensive test coverage.
