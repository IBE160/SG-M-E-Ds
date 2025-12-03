# Story 2.2: Dynamic Room Description Generation

Status: drafted

## Story

As a game designer,
I want the AI to dynamically generate unique room descriptions based on the chosen theme and narrative,
So that each playthrough offers fresh environments.

## Acceptance Criteria

1.  Given a game with a selected theme and an ongoing narrative, when the AI is prompted for a room description, including the theme and a narrative summary, then the AI generates a unique description for that room that is consistent with both the theme and the narrative.
2.  And this description is displayed to the player.

## Tasks / Subtasks

- [ ] AC 1: Extend `services/ai_service.py` to generate room descriptions.
  - [ ] Subtask: Implement a function to formulate prompts for room descriptions, incorporating current game `theme`, `location`, `narrative_state`, and `room_context` (from `GameSession`).
  - [ ] Subtask: Call the Gemini API to generate the room description.
- [ ] AC 1, 2: Create or update Flask API route for room description generation.
  - [ ] Subtask: Define a `POST /generate_room_description` endpoint in `routes.py`.
  - [ ] Subtask: This endpoint will receive context, call `services/ai_service.py`, and return the generated room description.
- [ ] AC 2: Integrate dynamic room descriptions with UI.
  - [ ] Subtask: Modify existing Jinja2 templates (e.g., `templates/game.html`) to display the dynamically generated room description.
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for the room description generation logic in `services/ai_service.py`, mocking the Gemini API.
  - [ ] Subtask: Write integration tests for the `POST /generate_room_description` Flask route, verifying API interaction and proper display.
  - [ ] Subtask: Write E2E tests to visually confirm that dynamic room descriptions are displayed.

## Dev Notes

### Requirements Context Summary

**From Epic 2: Introducing the AI Storyteller**
-   **Goal:** Replace the static story and room descriptions from Epic 1 with AI-generated content, while ensuring coherence.
-   **Rationale:** This isolates the challenge of narrative generation from puzzle generation. It directly integrates "Narrative Archetypes" to ensure the story is logical, tackling a key risk early.

**From PRD (Product Requirements Document) - FR-001: Dynamic Content Generation, FR-007: AI-Generated Narrative**
-   **FR-001:** The AI generates unique storylines.
-   **FR-007:** The core ability for the AI to create a unique story.

**From Architecture Document (`docs/architecture.md`)**
-   **AI Service Integration:** Gemini Pro / Gemini 1.5 Pro.
-   **AI Client Library:** `google-generativeai 0.8.5`.
-   **Prompt Management Strategy:** Structured Prompting with Narrative Archetypes.
-   **API Pattern for AI interactions:** Flask API Routes.
-   **Game State Management & Persistence:** `GameSession.narrativeState` is crucial for context.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 2.1: Integrate AI Narrative Generation Service (Status: drafted)**

-   **Goal:** Integrate an AI service capable of generating narrative text, So that we can dynamically create story elements for the game.
-   **Acceptance Criteria:** Service returns coherent narrative text; application successfully receives and parses narrative.
-   **Key Technical Notes:** Setting up Gemini API access, installing `google-generativeai`, creating `services/ai_service.py` for API interaction, creating Flask API routes for narrative generation.
-   **Relevant Learnings for Story 2.2:**
    *   The `services/ai_service.py` module and Flask API routes for AI interaction are now established. Story 2.2 will extend these existing components.
    *   The approach for secure API key handling and basic error handling from Story 2.1 will be directly applicable.
    *   Emphasis on Structured Prompting Strategy for coherent AI generation remains crucial.

[Source: docs/sprint-artifacts/2-1-integrate-ai-narrative-generation-service.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md]
- [Source: docs/sprint-artifacts/2-1-integrate-ai-narrative-generation-service.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
