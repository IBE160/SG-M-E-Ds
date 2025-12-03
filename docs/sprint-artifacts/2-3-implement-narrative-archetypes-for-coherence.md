# Story 2.3: Implement Narrative Archetypes for Coherence

Status: drafted

## Story

As a game designer,
I want to guide the AI with narrative archetypes or story skeletons,
So that the generated stories remain coherent and logical across playthroughs.

## Acceptance Criteria

1.  Given a set of predefined narrative archetypes, when the AI generates a story, then the generated story follows the key structural beats of the selected archetype, while still allowing for creative variation in plot details, characters, and events.
2.  And the story flow feels logical and purposeful to the player.

## Tasks / Subtasks

- [ ] AC 1: Define narrative archetypes.
  - [ ] Subtask: Identify and document key narrative archetypes (e.g., Hero's Journey, Rags to Riches) and their structural beats.
  - [ ] Subtask: Represent archetypes in a structured format (e.g., JSON or Python data structures) accessible by `services/ai_service.py`.
- [ ] AC 1: Implement prompt engineering for narrative archetypes.
  - [ ] Subtask: Modify `services/ai_service.py` to incorporate archetype instructions into prompts sent to the Gemini API.
  - [ ] Subtask: Ensure prompts guide the AI to generate content consistent with the chosen archetype's structural beats.
- [ ] AC 2: Integrate archetype selection into game state.
  - [ ] Subtask: Update `GameSession.narrative_state` to include the selected narrative archetype.
- [ ] AC 1, 2: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for prompt generation logic, verifying archetype instructions are correctly embedded.
  - [ ] Subtask: Write integration tests for API endpoints that trigger narrative generation, ensuring the AI receives and utilizes archetype context.
  - [ ] Subtask: Manual/Exploratory testing to assess the coherence and logic of AI-generated stories against selected archetypes.

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
-   **Game State Management & Persistence:** `GameSession.narrative_state` will store story context for AI.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 2.2: Dynamic Room Description Generation (Status: drafted)**

-   **Goal:** The AI to dynamically generate unique room descriptions based on the chosen theme and narrative, So that each playthrough offers fresh environments.
-   **Acceptance Criteria:** AI generates unique descriptions consistent with theme/narrative, and displayed to player.
-   **Key Technical Notes:** Extending `services/ai_service.py` for room descriptions, creating/updating Flask API route (`/generate_room_description`), integrating with Jinja2 templates.
-   **Relevant Learnings for Story 2.3:**
    *   The `services/ai_service.py` module and Flask API routes are established for AI content generation. This story will enhance the prompt engineering within `ai_service.py`.
    *   The importance of providing `theme`, `location`, `narrative_state`, and `room_context` to the AI for coherent generation is reinforced.
    *   The display mechanism for AI-generated text in Jinja2 templates is understood.

[Source: docs/sprint-artifacts/2-2-dynamic-room-description-generation.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md]
- [Source: docs/sprint-artifacts/2-2-dynamic-room-description-generation.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
