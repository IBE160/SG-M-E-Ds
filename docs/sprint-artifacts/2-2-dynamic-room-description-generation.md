# Story 2.2: Dynamic Room Description Generation

Status: review

## Story

As a game designer,
I want the AI to dynamically generate unique room descriptions based on the chosen theme and narrative,
So that each playthrough offers fresh environments.

## Acceptance Criteria

1.  Given a game with a selected theme and an ongoing narrative, when the AI is prompted for a room description, including the theme and a narrative summary, then the AI generates a unique description for that room that is consistent with both the theme and the narrative.
2.  And this description is displayed to the player.

## Tasks / Subtasks

- [x] AC 1: Extend `services/ai_service.py` to generate room descriptions.
  - [x] Subtask: Implement a function to formulate prompts for room descriptions, incorporating current game `theme`, `location`, `narrative_state`, and `room_context` (from `GameSession`).
  - [x] Subtask: Call the Gemini API to generate the room description.
- [x] AC 1, 2: Create or update Flask API route for room description generation.
  - [x] Subtask: Define a `POST /generate_room_description` endpoint in `routes.py`.
  - [x] Subtask: This endpoint will receive context, call `services/ai_service.py`, and return the generated room description.
- [x] AC 2: Integrate dynamic room descriptions with UI.
  - [x] Subtask: Modify existing Jinja2 templates (e.g., `templates/game.html`) to display the dynamically generated room description.
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for the room description generation logic in `services/ai_service.py`, mocking the Gemini API.
  - [x] Subtask: Write integration tests for the `POST /generate_room_description` Flask route, verifying API interaction and proper display.

- [x] Subtask: Write E2E tests to visually confirm that dynamic room descriptions are displayed.
## Dev Notes
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

**From Story 2.1: Integrate AI Narrative Generation Service (Status: ready-for-dev)**

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
- docs/sprint-artifacts/2-2-dynamic-room-description-generation.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List
- Extended `ai_service` to generate dynamic room descriptions based on game context. Added a new `POST /generate_room_description` endpoint. Updated the `GameSession` model to store the dynamic description. Created a basic `game.html` template and a route to render it. Added unit and integration tests for the new functionality.

- ✅ Implemented E2E tests to visually confirm dynamic room descriptions are displayed.
### File List
### File List
- Modified: `ai-escape-app/services/ai_service.py`
- Modified: `ai-escape-app/routes.py`
- Modified: `ai-escape-app/models.py`
- Modified: `ai-escape-app/tests/unit/test_ai_service.py`
- Created: `ai-escape-app/templates/game.html`
- Created: `ai-escape-app/tests/integration/test_room_description_route.py`
- Modified: `ai-escape-app/tests/integration/test_save_load_routes.py`

- ai-escape-app/tests/e2e/test_room_description_display.py (new)
## Change Log
## Change Log

- **2025-12-03**: Story created.
- **2025-12-08**: Completed dynamic room description generation (Story 2.2).
- **2025-12-04**: Story context regenerated.
- **2025-12-09**: E2E tests for dynamic room description display implemented and verified.
- **2025-12-09**: Fixed E2E test failures by ensuring Flask app is running during tests and mocking AI service calls in relevant integration tests. Updated `routes.py` to correctly trigger room description generation during player movement and `test_save_load_routes.py` to mock AI service calls.

## Senior Developer Review (AI)

**Reviewer:** BIP
**Date:** 2025-12-09
**Outcome:** APPROVE with minor suggestions

**Summary:**
The story "Dynamic Room Description Generation" (Story 2.2) has been implemented and is ready for integration. All acceptance criteria are met, and all completed tasks have been verified. The team successfully addressed issues encountered during testing related to Playwright browser installation and mocking AI service calls in integration tests.

**Key Findings:**

*   **LOW Severity:**
    *   **Finding:** No Epic Tech Spec found for Epic 2.
    *   **Rationale:** The absence of a dedicated technical specification for Epic 2 means architectural guidance for this epic relies solely on the main `architecture.md` and story-level details. While not blocking, a dedicated tech spec would provide more explicit guidance.

**Acceptance Criteria Coverage:**

| AC# | Description                                                                                                                                                                                                                | Status       | Evidence                                                                                                                                                                                                                                                             |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Given a game with a selected theme and an ongoing narrative, when the AI is prompted for a room description, including the theme and a narrative summary, then the AI generates a unique description for that room that is consistent with both the theme and the narrative. | IMPLEMENTED  | `ai-escape-app/routes.py` (interact route triggers `generate_room_description`), `ai-escape-app/services/ai_service.py` (`generate_room_description` logic), `ai-escape-app/tests/e2e/test_room_description_display.py` (test verifies dynamic change). |
| 2   | And this description is displayed to the player.                                                                                                                                                                           | IMPLEMENTED  | `ai-escape-app/routes.py` (`get_session` returns `current_room_description`), `ai-escape-app/templates/game.html` (renders `#room-description`), `ai-escape-app/tests/e2e/test_room_description_display.py` (test verifies display).                            |

**Summary: 2 of 2 acceptance criteria fully implemented.**

**Task Completion Validation:**

| Task                                                                                                                                        | Marked As | Verified As        | Evidence                                                                                                                                                                                                                                                              |
|---------------------------------------------------------------------------------------------------------------------------------------------|-----------|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AC 1: Extend `services/ai_service.py` to generate room descriptions.                                                                      | [x]       | VERIFIED COMPLETE  | `ai-escape-app/services/ai_service.py` (generate_room_description function and prompt construction).                                                                                                                                                                  |
|   Subtask: Implement a function to formulate prompts for room descriptions, incorporating current game `theme`, `location`, `narrative_state`, and `room_context` (from `GameSession`). | [x]       | VERIFIED COMPLETE  | `ai-escape-app/services/ai_service.py` (`generate_room_description` parameters and prompt construction).                                                                                                                                                              |
|   Subtask: Call the Gemini API to generate the room description.                                                                           | [x]       | VERIFIED COMPLETE  | `ai-escape-app/services/ai_service.py` (`generate_room_description` uses `model.generate_content`).                                                                                                                                                                   |
| AC 1, 2: Create or update Flask API route for room description generation.                                                                | [x]       | VERIFIED COMPLETE  | `ai-escape-app/routes.py` (`@bp.route("/generate_room_description", methods=["POST"])` endpoint definition).                                                                                                                                                          |
|   Subtask: Define a `POST /generate_room_description` endpoint in `routes.py`.                                                            | [x]       | VERIFIED COMPLETE  | `ai-escape-app/routes.py` (definition of `generate_room_description_route`).                                                                                                                                                                                          |
|   Subtask: This endpoint will receive context, call `services/ai_service.py`, and return the generated room description.                    | [x]       | VERIFIED COMPLETE  | `ai-escape-app/routes.py` (`generate_room_description_route` calls `ai_service.generate_room_description`).                                                                                                                                                           |
| AC 2: Integrate dynamic room descriptions with UI.                                                                                        | [x]       | VERIFIED COMPLETE  | `ai-escape-app/templates/game.html` (display logic for `#room-description`).                                                                                                                                                                                          |
|   Subtask: Modify existing Jinja2 templates (e.g., `templates/game.html`) to display the dynamically generated room description.              | [x]       | VERIFIED COMPLETE  | `ai-escape-app/templates/game.html` (`<p id="room-description">{{ room_description }}</p>`).                                                                                                                                                                           |
| AC 1, 2: Implement unit and integration tests.                                                                                            | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/unit/test_ai_service.py` and `ai-escape-app/tests/integration/test_room_description_route.py`.                                                                                                                                                   |
|   Subtask: Write unit tests for the room description generation logic in `services/ai_service.py`, mocking the Gemini API.                   | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/unit/test_ai_service.py` (contains tests for `generate_room_description` with mocking).                                                                                                                                                         |
|   Subtask: Write integration tests for the `POST /generate_room_description` Flask route, verifying API interaction and proper display.       | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/integration/test_room_description_route.py` (contains tests for the route).                                                                                                                                                                      |
| Write E2E tests to visually confirm that dynamic room descriptions are displayed.                                                           | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/e2e/test_room_description_display.py` (contains `test_dynamic_room_description_displayed` which passed).                                                                                                                                     |

**Summary: 9 of 9 completed tasks verified, 0 questionable, 0 falsely marked complete.**

**Test Coverage and Gaps:**
- Comprehensive unit, integration, and E2E tests are in place and all pass.
- AI service calls are appropriately mocked in integration tests.
- Flask app execution during E2E tests is correctly handled.

**Architectural Alignment:**
- The implementation aligns with the architectural decisions regarding AI service integration (Gemini Pro), client library usage, prompt management strategy, API pattern, and testing strategy.

**Security Notes:**
- Prompts are constructed from controlled application inputs. Further review of `ai_service.py` prompt construction for robustness against potential (though currently not direct) user-controlled injection is recommended as a best practice.

**Best-Practices and References:**
- Python/Flask best practices appear to be followed.
- Testing strategy is comprehensive, using Pytest for unit/integration and Playwright for E2E.

### Action Items

**Advisory Notes:**
- Note: Consider enhancing prompt construction in `ai_service.py` for `generate_room_description` to include more robust sanitization or templating, even if current inputs are application-controlled, as a defensive best practice against future prompt injection vectors.
- Note: When developing further AI-related features, apply Gemini API prompt engineering best practices (e.g., clarity, context, examples, role definition, iteration) to ensure robust and predictable AI responses.
