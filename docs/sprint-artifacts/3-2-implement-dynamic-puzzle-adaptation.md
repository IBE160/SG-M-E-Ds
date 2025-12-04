# Story 3.2: Implement Dynamic Puzzle Adaptation

Status: ready-for-dev

## Story

As a game designer,
I want the AI to dynamically adapt puzzles based on player actions and game state,
So that the challenges feel responsive and personalized.

## Acceptance Criteria

1.  Given a puzzle has been generated, when the player attempts a solution, then the AI evaluates the attempt and adapts the puzzle's difficulty or provides contextual hints if needed.
2.  And the game state reflects the puzzle's progression.

## Tasks / Subtasks

- [ ] AC 1: Extend `services/ai_service.py` for puzzle adaptation.
  - [ ] Subtask: Implement a function to evaluate player attempts against puzzle solutions.
  - [ ] Subtask: Formulate prompts for the Gemini API to request adaptations (e.g., hints, difficulty adjustments) based on player performance and `GameSession.puzzle_state`.
  - [ ] Subtask: Implement logic to parse AI-generated adaptations.
- [ ] AC 1: Create or update Flask API route for player puzzle interaction/adaptation.
  - [ ] Subtask: Define a `POST /evaluate_puzzle_solution` endpoint in `routes.py`.
  - [ ] Subtask: This endpoint will receive player attempts, call `services/ai_service.py` for evaluation and adaptation, and return feedback/adapted puzzle details.
- [ ] AC 2: Integrate puzzle adaptation with game state.
  - [ ] Subtask: Update `GameSession.puzzle_state` to reflect puzzle progression, AI adaptations, or hints provided.
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for `services/ai_service.py` functions, mocking the Gemini API to verify evaluation and adaptation logic.
  - [ ] Subtask: Write integration tests for `POST /evaluate_puzzle_solution` Flask route, verifying API interaction and `GameSession.puzzle_state` updates.
  - [ ] Subtask: Manual/Exploratory testing to assess the responsiveness and personalization of AI puzzle adaptations.

## Dev Notes

### Requirements Context Summary

**From Epic 3: The AI Puzzle Master**
-   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.
-   **Rationale:** This introduces the complexity of dynamic puzzles only after the narrative framework is stable. It uses "Puzzle Dependency Chains" to ensure all generated games are solvable.

**From PRD (Product Requirements Document) - FR-005: Detailed specifications for puzzle types**
-   **FR-005:** Detailed specifications for puzzle types and the AI's adaptation logic will be developed.

**From Architecture Document (`docs/architecture.md`)**
-   **AI Service Integration:** Gemini Pro / Gemini 1.5 Pro.
-   **AI Client Library:** `google-generativeai 0.8.5`.
-   **Prompt Management Strategy:** Structured Prompting with "Puzzle Dependency Chains".
-   **Data Architecture:** `GameSession.puzzleState` will be crucial for providing context to the AI for dynamic adaptation.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 3.1: Integrate AI Puzzle Generation Service (Status: ready-for-dev)**

-   **Goal:** Integrate an AI service capable of generating puzzles, So that we can dynamically create interactive challenges for the game.
-   **Acceptance Criteria:** Service returns coherent puzzle description and solution; application receives and parses puzzle.
-   **Key Technical Notes:** Ensuring Gemini API access, `google-generativeai` installation, extending `services/ai_service.py` for puzzle generation prompts and API calls, creating `POST /generate_puzzle` Flask endpoint.
-   **Relevant Learnings for Story 3.2:**
    *   The `services/ai_service.py` module and Flask API routes for AI interaction are well-established for narrative generation. This story will extend that functionality for puzzle generation.
    *   Prompt engineering techniques (from Story 2.x and 3.1) will be directly applicable to puzzle generation to ensure theme/location alignment.
    *   Secure API key handling and error handling (from Story 2.1) are already in place.

[Source: docs/sprint-artifacts/3-1-integrate-ai-puzzle-generation-service.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md]
- [Source: docs/sprint-artifacts/3-1-integrate-ai-puzzle-generation-service.md]

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/3-2-implement-dynamic-puzzle-adaptation.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
- **2025-12-04**: Story context regenerated.
