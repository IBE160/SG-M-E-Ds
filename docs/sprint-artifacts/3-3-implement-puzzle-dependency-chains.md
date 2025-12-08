# Story 3.3: Implement Puzzle Dependency Chains

Status: review

## Story

As a game designer,
I want to ensure AI-generated puzzles are always solvable and logically connected,
So that players never encounter unsolvable scenarios.

## Acceptance Criteria

1.  Given a set of dynamically generated puzzles for an escape room, when the AI generates the puzzle sequence, then the puzzles are arranged in a solvable dependency chain (e.g., key for door A is found by solving puzzle B).
2.  And the game verifies the solvability of the generated chain.

## Tasks / Subtasks

- [x] AC 1: Extend `services/ai_service.py` for puzzle dependency logic.
  - [x] Subtask: Implement functions to formulate prompts that instruct the Gemini API to generate puzzles with explicit prerequisites and outcomes.
  - [x] Subtask: Consider graph-based representations of puzzle dependencies within prompts.
- [x] AC 1, 2: Implement internal logic for verifying puzzle solvability.
  - [x] Subtask: Develop functions in `services/game_logic.py` to analyze a generated puzzle sequence and confirm its solvability.
  - [x] Subtask: This might involve simulating puzzle progression or checking for circular dependencies.
- [x] AC 2: Integrate puzzle verification with game state.
  - [x] Subtask: Update `GameSession.puzzle_state` to store metadata about puzzle dependencies and solvability status.
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for puzzle dependency logic in `services/ai_service.py`, mocking the Gemini API to verify correct prompt construction.
  - [x] Subtask: Write unit tests for the puzzle solvability verification functions in `services/game_logic.py`.
  - [x] Subtask: Integration tests for API endpoints that trigger puzzle generation, ensuring that only solvable sequences are created.

## Dev Notes

### Requirements Context Summary

**From Epic 3: The AI Puzzle Master**
-   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.
-   **Rationale:** This introduces the complexity of dynamic puzzles only after the narrative framework is stable. It uses "Puzzle Dependency Chains" to ensure all generated games are solvable.

**From PRD (Product Requirements Document) - FR-005: Detailed specifications for puzzle types**
-   **FR-005:** Detailed specifications for puzzle types.

**From Architecture Document (`docs/architecture.md`)**
-   **AI Service Integration:** Gemini Pro / Gemini 1.5 Pro.
-   **AI Client Library:** `google-generativeai 0.8.5`.
-   **Prompt Management Strategy:** Structured Prompting with "Puzzle Dependency Chains".
-   **Data Architecture:** `GameSession.puzzleState` will be crucial for puzzle context.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 3.2: Implement Dynamic Puzzle Adaptation (Status: drafted)**

-   **Goal:** The AI to dynamically adapt puzzles based on player actions and game state, So that the challenges feel responsive and personalized.
-   **Acceptance Criteria:** AI evaluates player attempts and adapts puzzles/provides hints; game state reflects progression.
-   **Key Technical Notes:** Extending `services/ai_service.py` for evaluation/adaptation prompts, `POST /evaluate_puzzle_solution` route, updating `GameSession.puzzle_state`.
-   **Relevant Learnings for Story 3.3:**
    *   The `services/ai_service.py` module is the central point for AI puzzle interaction, where dependency logic will be integrated.
    *   `GameSession.puzzle_state` is the established mechanism for tracking puzzle-related context, making it suitable for storing dependency metadata.
    *   Prompt engineering techniques are vital for guiding the AI's behavior and will be extended for dependency chains.

[Source: docs/sprint-artifacts/3-2-implement-dynamic-puzzle-adaptation.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md]
- [Source: docs/sprint-artifacts/3-2-implement-dynamic-puzzle-adaptation.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List
- Extended `ai_service.py` with the ability to generate puzzles with explicit prerequisites and outcomes, enabling the AI to create solvable dependency chains. Implemented internal logic in `game_logic.py` to verify the solvability of generated puzzle sequences. Updated `GameSession` model to store puzzle dependency metadata. Developed comprehensive unit and integration tests to ensure these functionalities are working correctly and preventing unsolvable scenarios.

### File List
- Modified: `ai-escape-app/services/ai_service.py`
- Modified: `ai-escape-app/services/game_logic.py`
- Modified: `ai-escape-app/models.py`
- Modified: `ai-escape-app/tests/unit/test_ai_service.py`
- Modified: `ai-escape-app/tests/integration/test_puzzle_route.py`
- Created: `ai-escape-app/tests/unit/test_game_logic.py`

## Change Log

- **2025-12-03**: Story created.
- **2025-12-08**: Implemented puzzle dependency chains (Story 3.3).
- **2025-12-04**: Story context regenerated.
