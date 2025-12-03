# Story 4.3: Implement Enhanced Game Setup Flow

Status: drafted

## Story

As a player,
I want an enhanced game setup flow with more options and clearer guidance,
So that I can customize my experience more effectively.

## Acceptance Criteria

1.  Given the game setup menu, when I navigate through the options, then I can choose from an expanded list of themes, locations, puzzle types, and difficulty levels, with clear descriptions for each.

## Tasks / Subtasks

- [ ] AC 1: Define expanded lists of themes, locations, puzzle types, and difficulty levels.
  - [ ] Subtask: Document the new options and their descriptions.
  - [ ] Subtask: Store these options in a structured format accessible by the backend (e.g., configuration file, database).
- [ ] AC 1: Create or update Flask API routes to expose game setup options.
  - [ ] Subtask: Define a `GET /game_setup_options` endpoint in `routes.py` to retrieve the expanded list of choices.
- [ ] AC 1: Implement enhanced UI for game setup.
  - [ ] Subtask: Modify Jinja2 templates (e.g., `templates/game_setup.html`) to present the expanded options clearly.
  - [ ] Subtask: Utilize `.option-btn` components and incorporate improved instructional text from UX design specifications.
- [ ] AC 1: Integrate player choices with `GameSession` initialization.
  - [ ] Subtask: Ensure selected themes, locations, puzzle types, and difficulty levels are passed to `create_game_session` (Story 1.2) and stored in `GameSession`.
- [ ] AC 1: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for the data structure holding game setup options.
  - [ ] Subtask: Write integration tests for the `GET /game_setup_options` Flask route, verifying correct option retrieval.
  - [ ] Subtask: Write E2E tests to simulate player interaction with the enhanced game setup flow and verify correct option display and selection.

## Dev Notes

### Requirements Context Summary

**From Epic 4: Expanding Variety and Replayability**
-   **Goal:** Increase the breadth of content and player choice to deliver on the promise of endless replayability.

**From PRD (Product Requirements Document) - FR-002: Player-Driven Customization, FR-006: User flow for Game Setup**
-   **FR-002:** Players tailor their adventure by choosing a theme, location, difficulty level.
-   **FR-006:** User flow for the Game Setup will guide the player through choices.

**From Architecture Document (`docs/architecture.md`)**
-   **UX:** Enhanced Game Setup Flow will leverage existing `.option-btn` components and improved instructional text, consistent with the UX design.
-   **API Pattern for AI interactions:** Flask API Routes will handle communication between the frontend and backend (relevant for retrieving options).
-   **Game State Management:** Player choices will be stored in `GameSession`.
-   **Testing Strategy:** E2E Tests using Playwright.

### Learnings from Previous Story

**From Story 4.2: Expand Library of Visual Assets and Themes (Status: drafted)**

-   **Goal:** Expand the available library of visual assets and themes, So that players have more diverse and immersive choices for their escape rooms.
-   **Acceptance Criteria:** AI can generate room descriptions and puzzles consistent with the expanded library when a new set of images and themes are added and selected.
-   **Key Technical Notes:** Curating and integrating new visual assets in `static/images/`, updating AI's understanding of themes in `services/ai_service.py` via prompt engineering.
-   **Relevant Learnings for Story 4.3:**
    *   The expansion of themes and assets in Story 4.2 directly informs the new options presented in this enhanced game setup flow.
    *   Flask API routes are established for backend-frontend communication, which will be used to serve the expanded list of options.
    *   The `GameSession` model is the central storage for player choices, including theme and location.

[Source: docs/sprint-artifacts/4-2-expand-library-of-visual-assets-and-themes.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md]
- [Source: docs/sprint-artifacts/4-2-expand-library-of-visual-assets-and-themes.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
