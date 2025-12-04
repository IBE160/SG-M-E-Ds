# Story 1.4: Implement the Core Interaction Model

Status: drafted

## Story

As a player,
I want to interact with the game world through a set of contextual options and a "go back" function,
So that I can navigate and solve puzzles.

## Acceptance Criteria

1.  Given the player is in a room with a "locked door" and a "note", when the game presents interaction options, then the options are displayed as a numbered list, such as: `1. Examine the locked door`, `2. Read the note`, `3. Look around the room`, `4. Go back`.
2.  And the player can select an option by entering the corresponding number.

## Tasks / Subtasks

- [ ] AC 1: Define a mechanism for generating contextual options.
  - [ ] Subtask: Based on the current room and game state (from `GameSession`), dynamically generate a list of possible interactions.
- [ ] AC 1: Implement rendering of interaction options.
  - [ ] Subtask: Display the generated options as a numbered list in the UI using Jinja2 templates and `.option-btn` elements.
  - [ ] Subtask: Ensure accessibility with keyboard navigation and visible focus indicators.
- [ ] AC 2: Implement player input handling.
  - [ ] Subtask: Create a Flask route to receive player's selected option (e.g., a number corresponding to an action).
- [ ] AC 2: Integrate player choices with game logic.
  - [ ] Subtask: Process the player's input and update the `GameSession` accordingly (e.g., move to a new room, add item to inventory, trigger puzzle logic).
  - [ ] Subtask: Implement a "go back" function that reverts the player to the previous room or state.
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for the contextual option generation logic.
  - [ ] Subtask: Write integration tests for Flask routes handling player input and verifying `GameSession` updates based on selected options.
  - [ ] Subtask: Write E2E tests to simulate player interaction and verify UI updates and game progression.

## Dev Notes

### Requirements Context Summary

**From Epic 1: Foundational Framework & A Single, Static Escape Room**
-   **Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a *single, hard-coded* story and puzzle chain.

**From PRD (Product Requirements Document) - FR-003: Hybrid Interaction Model, FR-004: Core Interaction Loop**
-   **FR-003:** Specifies a blend of text-based commands for interaction combined with dynamic visual feedback.
-   **FR-004:** Details players interacting with rooms and objects through a system of contextual options and a "go back" function.

**From Architecture Document (`docs/architecture.md`)**
-   **API Pattern for AI interactions:** Flask API Routes will handle communication between the frontend and AI generation logic (relevant for any backend interaction).
-   **UX/UI:** Accessibility Implementation (WCAG 2.1 Level AA compliant). Tailwind CSS for styling. User choices rendered as `.option-btn` elements. In-game navigation uses numbered options within the main text box (`.immersive-option`).

### Learnings from Previous Story

**From Story 1.3: Create a Static, Hard-coded Escape Room (Status: drafted)**

-   **Goal:** Create a single, hard-coded escape room with a few rooms and puzzles, So that we have a complete, playable experience to test the core mechanics.
-   **Acceptance Criteria:** A 3-room sequence with at least two distinct puzzles and a "You escaped!" message upon solving the final puzzle.
-   **Key Technical Notes:** Room descriptions, puzzle logic, and solutions will be hard-coded. Image assets for rooms stored locally in `static/images/`.
-   **Relevant Learnings for Story 1.4:**
    *   Story 1.3 will establish the static rooms and puzzles that Story 1.4 will then enable interaction with.
    *   The data structure for hard-coded room data and puzzle details defined in Story 1.3 will be the foundation for contextual options.
    *   The `services/game_logic.py` and `routes.py` from previous stories are the appropriate places to integrate new interaction logic.

[Source: docs/sprint-artifacts/1-3-create-a-static-hard-coded-escape-room.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]
- [Source: docs/sprint-artifacts/1-3-create-a-static-hard-coded-escape-room.md]

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/1-4-implement-the-core-interaction-model.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
