# Story 4.1: Implement Dynamic Difficulty Adjustment

Status: drafted

## Story

As a game designer,
I want the AI to dynamically adjust the game's difficulty based on player performance,
So that the challenge remains engaging and fair.

## Acceptance Criteria

1.  Given a player's performance in a series of puzzles (e.g., time taken, hints used), when the AI evaluates this performance, then the AI subtly adjusts parameters for future puzzles (e.g., complexity, number of steps) to maintain an optimal challenge level.

## Tasks / Subtasks

- [ ] AC 1: Extend `GameSession` to track player performance metrics.
  - [ ] Subtask: Identify relevant player performance metrics (e.g., time taken per puzzle, hints used, number of attempts).
  - [ ] Subtask: Add or update fields in `GameSession.puzzle_state` or `GameSession.game_history` (in `models.py`) to store these metrics.
- [ ] AC 1: Extend `services/game_logic.py` to collect and evaluate performance metrics.
  - [ ] Subtask: Implement functions to collect and process player performance data after puzzle interactions.
- [ ] AC 1: Extend `services/ai_service.py` for dynamic difficulty adjustment.
  - [ ] Subtask: Implement a function to formulate prompts for the Gemini API that include player performance metrics.
  - [ ] Subtask: Guide the AI to subtly adjust puzzle generation parameters (e.g., complexity, number of steps) based on these metrics.
- [ ] AC 1: Create or update Flask API routes for difficulty adjustment.
  - [ ] Subtask: Define a `POST /adjust_difficulty` endpoint in `routes.py` to receive player performance data and trigger AI adjustment.
- [ ] AC 1: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for the performance metric tracking and evaluation logic in `services/game_logic.py`.
  - [ ] Subtask: Write unit tests for `services/ai_service.py` functions, mocking the Gemini API to verify prompt construction and difficulty adjustment logic.
  - [ ] Subtask: Write integration tests for the `POST /adjust_difficulty` Flask route, verifying API interaction and `GameSession` updates.
  - [ ] Subtask: Manual/Exploratory testing to assess the effectiveness and fairness of dynamic difficulty adjustment.

## Dev Notes

### Requirements Context Summary

**From Epic 4: Expanding Variety and Replayability**
-   **Goal:** Increase the breadth of content and player choice to deliver on the promise of endless replayability.

**From PRD (Product Requirements Document) - FR-001: Dynamic Content Generation, Future Consideration: Advanced AI**
-   **FR-001:** The AI dynamically generates and adapts puzzles.
-   **Future Consideration: Advanced AI:** Implementing dynamic difficulty adjustment to maintain player engagement.

**From Architecture Document (`docs/architecture.md`)**
-   **AI Integration (for dynamic difficulty adjustment):** Utilizes Gemini Pro / Gemini 1.5 Pro.
-   **Prompt Management Strategy:** Structured Prompting will incorporate player performance metrics.
-   **Game State Management & Persistence:** `GameSession` (`GameSession.gameHistory` and `GameSession.puzzleState`) will track player performance metrics.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 3.4: Integrate Player Puzzle Interaction (Status: drafted)**

-   **Goal:** Interact with puzzles using contextual options and input mechanisms, So that I can attempt solutions and progress through the game.
-   **Acceptance Criteria:** Player selects interaction option, game processes input and provides feedback based on AI's puzzle logic.
-   **Key Technical Notes:** Extending Flask routes for puzzle interaction, implementing UI for puzzle interaction, integrating AI puzzle logic feedback, using `.option-btn` components, "Feedback Patterns".
-   **Relevant Learnings for Story 4.1:**
    *   The established Flask API routes and `services/ai_service.py` provide the foundation for submitting player performance metrics and receiving AI adjustments.
    *   `GameSession` is the central point for game state, which can be extended to track performance metrics.
    *   Prompt engineering experience from previous AI-related stories will be crucial for guiding the AI in difficulty adjustments.

[Source: docs/sprint-artifacts/3-4-integrate-player-puzzle-interaction.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md]
- [Source: docs/sprint-artifacts/3-4-integrate-player-puzzle-interaction.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
