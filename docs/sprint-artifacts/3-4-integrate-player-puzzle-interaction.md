# Story 3.4: Integrate Player Puzzle Interaction

Status: ready-for-dev

## Story

As a player,
I want to interact with puzzles using contextual options and input mechanisms,
So that I can attempt solutions and progress through the game.

## Acceptance Criteria

1.  Given a puzzle is presented, when the player selects an interaction option (e.g., "Examine the inscription", "Try combination 123"), then the game processes the input and provides feedback based on the AI's puzzle logic.

## Tasks / Subtasks

- [ ] AC 1: Extend Flask routes for puzzle interaction.
  - [ ] Subtask: Modify or create new Flask routes (e.g., `POST /puzzle_interaction`) to receive player input for puzzle attempts.
  - [ ] Subtask: This route will communicate with `services/ai_service.py` to get AI feedback on the input.
- [ ] AC 1: Implement UI for puzzle interaction.
  - [ ] Subtask: Modify Jinja2 templates to display contextual interaction options for puzzles.
  - [ ] Subtask: Integrate text input mechanisms for more complex puzzle answers if required.
  - [ ] Subtask: Utilize existing `.option-btn` components where appropriate.
- [ ] AC 1: Integrate AI puzzle logic feedback.
  - [ ] Subtask: Parse feedback from `services/ai_service.py` (e.g., correct, incorrect, hint) and display it to the player in the UI.
  - [ ] Subtask: Ensure a consistent user experience with defined "Feedback Patterns".
- [ ] AC 1: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for `services/ai_service.py` functions related to evaluating player input for puzzles.
  - [ ] Subtask: Write integration tests for the Flask routes handling player puzzle interaction, verifying input processing and feedback generation.
  - [ ] Subtask: Write E2E tests to simulate player interaction with puzzles and verify correct feedback and game progression.

## Dev Notes

### Requirements Context Summary

**From Epic 3: The AI Puzzle Master**
-   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.

**From PRD (Product Requirements Document) - FR-004: Core Interaction Loop**
-   **FR-004:** Players interact with rooms and objects through a system of contextual options and a "go back" function.

**From Architecture Document (`docs/architecture.md`)**
-   **API Pattern for AI interactions:** Flask API Routes will handle communication between the frontend and AI generation logic.
-   **UX:** Core Interaction Model (contextual options, go back function).
-   **Error Handling Strategy:** Centralized error handling within Flask with user-friendly feedback.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 3.3: Implement Puzzle Dependency Chains (Status: drafted)**

-   **Goal:** Ensure AI-generated puzzles are always solvable and logically connected, So that players never encounter unsolvable scenarios.
-   **Acceptance Criteria:** Puzzles arranged in a solvable dependency chain; game verifies solvability.
-   **Key Technical Notes:** Extending `services/ai_service.py` for puzzle dependency logic and prompt engineering with graph-based representations; implementing internal logic (`services/game_logic.py`) for verifying puzzle solvability; updating `GameSession.puzzle_state` for dependency metadata.
-   **Relevant Learnings for Story 3.4:**
    *   `services/ai_service.py` is the central module for AI puzzle logic, and its functions for evaluating player input will be crucial for this story.
    *   The `routes.py` and existing Flask API pattern for frontend-backend communication are established, providing the framework for player interaction endpoints.
    *   The use of `GameSession.puzzle_state` for puzzle context is established.

[Source: docs/sprint-artifacts/3-3-implement-puzzle-dependency-chains.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md]
- [Source: docs/sprint-artifacts/3-3-implement-puzzle-dependency-chains.md]

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/3-4-integrate-player-puzzle-interaction.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
- **2025-12-04**: Story context regenerated.
