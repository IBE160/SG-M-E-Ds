# Story 2.4: Dynamic Theme and Location Integration

Status: ready-for-dev

## Story

As a player,
I want my chosen theme and location to influence the AI-generated story and room descriptions,
So that my customization choices feel impactful.

## Acceptance Criteria

1.  Given the player selects a theme (e.g., "Space Station") and location (e.g., "Mars Colony"), when the AI generates the narrative and room descriptions, then the content consistently reflects the chosen theme and location.

## Tasks / Subtasks

- [ ] AC 1: Update `GameSession` model to store theme and location.
  - [ ] Subtask: Ensure `GameSession` in `models.py` has fields for `theme` and `location` (already present with defaults).
- [ ] AC 1: Modify AI prompt generation in `services/ai_service.py`.
  - [ ] Subtask: Ensure prompts sent to the Gemini API for narrative and room description generation include the `theme` and `location` from the `GameSession`.
  - [ ] Subtask: Implement prompt engineering techniques to emphasize consistency with chosen theme/location.
- [ ] AC 1: Integrate theme/location selection into `start_game` API.
  - [ ] Subtask: Update the `POST /start_game` route in `routes.py` to receive `theme` and `location` parameters and pass them to `create_game_session`.
- [ ] AC 1: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for `services/ai_service.py` to verify that `theme` and `location` are correctly embedded in prompts.
  - [ ] Subtask: Write integration tests for the `POST /start_game` route to confirm `GameSession` is initialized with chosen `theme` and `location`.
  - [ ] Subtask: Manual/Exploratory testing to visually confirm that AI-generated content (narrative, room descriptions) is consistent with the selected theme and location.

## Dev Notes

### Requirements Context Summary

**From Epic 2: Introducing the AI Storyteller**
-   **Goal:** Replace the static story and room descriptions from Epic 1 with AI-generated content, while ensuring coherence.

**From PRD (Product Requirements Document) - FR-001: Dynamic Content Generation, FR-002: Player-Driven Customization**
-   **FR-001:** The AI generates unique storylines, and creates room descriptions based on user input.
-   **FR-002:** Players tailor their adventure by choosing a theme, location, difficulty level.

**From Architecture Document (`docs/architecture.md`)**
-   **AI Service Integration:** Gemini Pro / Gemini 1.5 Pro.
-   **AI Client Library:** `google-generativeai 0.8.5`.
-   **Prompt Management Strategy:** Structured Prompting.
-   **Game State Management & Persistence:** `GameSession` entity will track `theme` and `location`.
-   **API Pattern for AI interactions:** Flask API Routes.

### Learnings from Previous Story

**From Story 2.3: Implement Narrative Archetypes for Coherence (Status: drafted)**

-   **Goal:** Guide the AI with narrative archetypes or story skeletons, So that the generated stories remain coherent and logical across playthroughs.
-   **Acceptance Criteria:** Generated story follows key structural beats of selected archetype; story flow feels logical.
-   **Key Technical Notes:** Defining and representing narrative archetypes, implementing prompt engineering to incorporate archetype instructions in `services/ai_service.py`, integrating archetype selection into `GameSession.narrative_state`.
-   **Relevant Learnings for Story 2.4:**
    *   The use of `services/ai_service.py` for prompt engineering and AI interaction is well-established. This story will extend that functionality to include `theme` and `location` parameters.
    *   `GameSession.narrative_state` is already identified for storing narrative context, making it suitable for extending with theme and location information.
    *   The `POST /start_game` route (from Epic 1) and its interaction with `create_game_session` (from Epic 1) will be modified.

[Source: docs/sprint-artifacts/2-3-implement-narrative-archetypes-for-coherence.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md]
- [Source: docs/sprint-artifacts/2-3-implement-narrative-archetypes-for-coherence.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
- **2025-12-04**: Story context regenerated.
