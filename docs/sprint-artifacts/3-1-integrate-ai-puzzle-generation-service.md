# Story 3.1: Integrate AI Puzzle Generation Service

Status: drafted

## Story

As a developer,
I want to integrate an AI service capable of generating puzzles,
So that we can dynamically create interactive challenges for the game.

## Acceptance Criteria

1.  Given an AI puzzle generation service (e.g., Gemini API), when a prompt is sent to the service (e.g., "Generate a riddle for a magical library theme"), then the service returns a coherent puzzle description and solution.
2.  And the application can successfully receive and parse this puzzle.

## Tasks / Subtasks

- [ ] AC 1: Ensure Gemini API access is configured.
  - [ ] Subtask: Verify Gemini API key is accessible (should be configured in Story 2.1).
- [ ] AC 1: Install `google-generativeai` Python client library (if not already installed).
  - [ ] Subtask: Verify `google-generativeai` is in `requirements.txt` and installed (should be from Story 2.1).
- [ ] AC 1, 2: Extend `services/ai_service.py` for puzzle generation.
  - [ ] Subtask: Implement a function to formulate prompts for puzzle generation, focusing on mechanics and types (e.g., Observation, Riddle).
  - [ ] Subtask: Call the Gemini API to generate puzzle descriptions and solutions.
  - [ ] Subtask: Implement logic to receive and parse the AI-generated puzzle.
- [ ] AC 1, 2: Create Flask API routes for puzzle generation.
  - [ ] Subtask: Define a `POST /generate_puzzle` endpoint in `routes.py`.
  - [ ] Subtask: This endpoint will receive a prompt/context, call `services/ai_service.py`, and return the generated puzzle.
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for `services/ai_service.py`, mocking the Gemini API to verify prompt construction, API calls, and response parsing for puzzles.
  - [ ] Subtask: Write integration tests for the `POST /generate_puzzle` Flask route, verifying interaction with `services/ai_service.py` and correct puzzle return.

## Dev Notes

### Requirements Context Summary

**From Epic 3: The AI Puzzle Master**
-   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.
-   **Rationale:** This introduces the complexity of dynamic puzzles only after the narrative framework is stable. It uses "Puzzle Dependency Chains" to ensure all generated games are solvable.

**From PRD (Product Requirements Document) - FR-001: Dynamic Content Generation, FR-005: Detailed specifications for puzzle types, FR-009: Small Puzzle Set**
-   **FR-001:** The AI generates unique storylines, adapts puzzles.
-   **FR-005:** Detailed specifications for puzzle types.
-   **FR-009:** Small Puzzle Set.

**From Architecture Document (`docs/architecture.md`)**
-   **AI Service Integration:** Gemini Pro / Gemini 1.5 Pro.
-   **AI Client Library:** `google-generativeai 0.8.5`.
-   **API Pattern for AI interactions:** Flask API Routes.
-   **Prompt Management Strategy:** Structured Prompting with Puzzle Dependency Chains.
-   **Performance:** Background Processing (Celery, Redis) deferred.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 2.4: Dynamic Theme and Location Integration (Status: drafted)**

-   **Goal:** My chosen theme and location to influence the AI-generated story and room descriptions, So that my customization choices feel impactful.
-   **Acceptance Criteria:** AI-generated content consistently reflects the chosen theme and location.
-   **Key Technical Notes:** Updating `GameSession` model for `theme`/`location`, modifying AI prompt generation in `services/ai_service.py` to include `theme`/`location`, integrating into `start_game` API.
-   **Relevant Learnings for Story 3.1:**
    *   The `services/ai_service.py` module and Flask API routes for AI interaction are well-established for narrative generation. This story will extend that functionality for puzzle generation.
    *   Prompt engineering techniques for consistency (from Story 2.4) will be directly applicable to puzzle generation to ensure theme/location alignment.
    *   Secure API key handling and error handling (from Story 2.1) are already in place.

[Source: docs/sprint-artifacts/2-4-dynamic-theme-and-location-integration.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md]
- [Source: docs/sprint-artifacts/2-4-dynamic-theme-and-location-integration.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
