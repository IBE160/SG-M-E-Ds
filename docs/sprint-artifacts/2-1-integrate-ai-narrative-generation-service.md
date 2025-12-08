# Story 2.1: Integrate AI Narrative Generation Service

Status: review

## Story

As a developer,
I want to integrate an AI service capable of generating narrative text,
So that we can dynamically create story elements for the game.

## Acceptance Criteria

1.  Given an AI narrative generation service (e.g., Gemini API), when a prompt is sent to the service (e.g., "Generate a mysterious story for an escape room set in an ancient tomb"), then the service returns a coherent narrative text.
2.  And the application can successfully receive and parse this narrative.

## Tasks / Subtasks

- [x] AC 1: Set up Gemini API access.
  - [x] Subtask: Obtain Gemini API key.
  - [x] Subtask: Securely store API key as an environment variable (e.g., in `.env` for local development).
- [x] AC 1: Install `google-generativeai` Python client library.
  - [x] Subtask: Add `google-generativeai` to `requirements.txt`.
  - [x] Subtask: Install dependencies.
- [x] AC 1, 2: Create `services/ai_service.py` for API interaction.
  - [x] Subtask: Implement a function to send a prompt to the Gemini API.
  - [x] Subtask: Implement logic to receive and parse the AI-generated narrative text.
  - [x] Subtask: Implement basic error handling for API calls.
- [x] AC 1, 2: Create Flask API routes for narrative generation.
  - [x] Subtask: Define a `POST /generate_narrative` endpoint in `routes.py`.
  - [x] Subtask: This endpoint will receive a prompt from the frontend, call `services/ai_service.py`, and return the generated narrative.
  - [x] Subtask: Secure API keys by ensuring they are only accessed server-side.
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for `services/ai_service.py`, mocking the Gemini API to verify prompt construction, API calls, and response parsing.
  - [x] Subtask: Write integration tests for the `POST /generate_narrative` Flask route, verifying interaction with `services/ai_service.py` and correct narrative return.

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
-   **API Pattern for AI interactions:** Flask API Routes to secure AI API keys and provide simple RESTful endpoints.
-   **Prompt Management Strategy:** Structured prompting with narrative archetypes.
-   **Performance:** Background Processing (Celery, Redis) deferred for slow AI generation.
-   **Error Handling:** Centralized error handling within Flask with user-friendly feedback via toast notifications and retry options for AI failures.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 1.5: Display Basic Visuals for Rooms (Status: drafted)**

-   **Goal:** See a background image for each room, So that the game feels more immersive.
-   **Acceptance Criteria:** When the player enters a new room and the room description is displayed, then a corresponding background image for that room is also displayed.
-   **Key Technical Notes:** Sourcing and preparing image assets, mapping rooms to images, and dynamic display of background images in Jinja2 templates.
-   **Relevant Learnings for Story 2.1:**
    *   The use of Flask routes for backend communication and Jinja2 templates for UI rendering is established.
    *   Basic asset management (local `static/images/`) and accessibility considerations are understood.
    *   This story introduces external API integration, which is a new pattern.

[Source: docs/sprint-artifacts/1-5-display-basic-visuals-for-rooms.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md]
- [Source: docs/sprint-artifacts/1-5-display-basic-visuals-for-rooms.md]

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/2-1-integrate-ai-narrative-generation-service.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List
- Implemented AI narrative generation service integration. Created `services/ai_service.py` for Gemini API interaction, added a `POST /generate_narrative` endpoint in `routes.py`, and secured API key access. Developed comprehensive unit tests for `ai_service.py` and integration tests for the new Flask route, ensuring all functionalities are covered and passing.

### File List
- Modified: `ai-escape-app/routes.py`
- Modified: `ai-escape-app/tests/integration/test_narrative_route.py`
- Modified: `ai-escape-app/tests/unit/test_ai_service.py`
- Modified: `ai-escape-app/tests/conftest.py`
- Created: `ai-escape-app/services/ai_service.py`

## Change Log

- **2025-12-08**: Completed integration of AI narrative generation service (Story 2.1).
