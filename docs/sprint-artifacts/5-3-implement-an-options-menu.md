# Story 5.3: Implement an Options Menu

Status: review

## Story

As a player,
I want to adjust game options like sound effects,
So that I can customize my experience.

## Acceptance Criteria

1.  Given I am in the game, when I select the "Options" menu, then a screen or dialog appears with options to adjust settings (e.g., sound volume).
2.  And changing these settings affects the game accordingly.

## Tasks / Subtasks

- [x] AC 1: Define game settings.
  - [x] Subtask: Identify adjustable game settings (e.g., sound volume, music volume, language, display preferences).
  - [x] Subtask: Document default values and valid ranges/options for each setting.
- [x] AC 1: Create a Flask API route for updating player settings.
  - [x] Subtask: Define a `POST /update_options` endpoint in `routes.py` to receive and process player setting changes.
- [x] AC 1: Implement UI for the Options menu.
  - [x] Subtask: Create a new Jinja2 template or modify an existing one to display the options menu within a modal pattern.
  - [x] Subtask: Utilize appropriate "Form Patterns" (e.g., Toggle Switches for binary, Select Menus for lists, Range Sliders for volume) for each setting.
  - [x] Subtask: Ensure the options menu is accessible from various points in the game UI.
- [x] AC 2: Integrate setting changes with game logic.
  - [x] Subtask: Implement logic in `services/game_logic.py` (or a new `services/settings.py` module) to apply adjusted settings to the game (e.g., update sound volume).
  - [x] Subtask: Persist user settings in the database (e.g., in a `PlayerSettings` model or within `GameSession`).
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for the settings management logic (e.g., validating settings, applying changes).
  - [x] Subtask: Write integration tests for the `POST /update_options` Flask route, verifying correct setting updates and persistence.
  - [x] Subtask: Write E2E tests to simulate player adjusting settings and verifying the changes affect the game as expected.

## Dev Notes

### Requirements Context Summary

**From Epic 5: Game Utility Features**
-   **Goal:** Provide players with essential utility features such as saving/loading games, getting help, and adjusting options.

**From Architecture Document (`docs/architecture.md`)**
-   **UX/UI:** Modal Pattern for Help/Options menu. Form Patterns (Toggle Switch, Select Menu, Range Slider).
-   **Testing Strategy:** Unit, Integration Tests using Pytest, E2E Tests (Playwright).

### Learnings from Previous Story

**From Story 5.2: Create a Help/Information System (Status: drafted)**

-   **Goal:** Access help or information about the game, So that I can understand the rules and objectives.
-   **Acceptance Criteria:** A screen or dialog appears with information when "Help" is selected.
-   **Key Technical Notes:** Defining help content, `GET /help_content` API, UI implementation using modal pattern.
-   **Relevant Learnings for Story 5.3:**
    *   The use of Flask API routes and Jinja2 templates for serving and displaying dynamic content within modal patterns is well-established and directly applicable for the Options menu.
    *   The pattern for defining game content (e.g., help text) and serving it via API endpoints will be useful for defining game settings.
    *   Considerations for UI responsiveness and accessibility from previous stories will be relevant for the Options modal.

[Source: docs/sprint-artifacts/5-2-create-a-help-information-system.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-5.md]
- [Source: docs/sprint-artifacts/5-2-create-a-help-information-system.md]

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/5-3-implement-an-options-menu.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

- Implemented Options Menu functionality, including:
    - Defined game settings structure in `ai-escape-app/data/game_settings.py`.
    - Created `PlayerSettings` model in `ai-escape-app/models.py` for persisting player-specific settings.
    - Implemented `get_player_settings` and `update_player_settings` logic in `ai-escape-app/services/settings.py`.
    - Added new API routes in `routes.py`: `GET /game_settings`, `GET /player_settings/<player_id>`, and updated `POST /update_options`.
    - Integrated UI for Options menu in `templates/game.html`, including button, modal structure, and client-side JavaScript logic for fetching, rendering, and updating settings.
- Created comprehensive unit, integration, and E2E tests for options menu functionality. All tests are passing.

### File List

- ai-escape-app/data/game_settings.py (new)
- ai-escape-app/models.py (modified)
- ai-escape-app/services/settings.py (new)
- ai-escape-app/routes.py (modified)
- ai-escape-app/templates/game.html (modified)
- ai-escape-app/tests/unit/test_settings_service.py (new)
- ai-escape-app/tests/integration/test_settings_routes.py (new)
- ai-escape-app/tests/e2e/test_options_menu_flow.py (new)

## Change Log

- **2025-12-03**: Story created.
- **2025-12-09**: Implemented Options Menu functionality, including settings definition, data models, service logic, API routes, UI integration, and comprehensive test coverage.
