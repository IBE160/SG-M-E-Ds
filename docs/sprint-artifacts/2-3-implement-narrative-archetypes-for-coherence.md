Status: done

## Story

As a game designer,
I want to guide the AI with narrative archetypes or story skeletons,
So that the generated stories remain coherent and logical across playthroughs.

## Acceptance Criteria

1.  Given a set of predefined narrative archetypes, when the AI generates a story, then the generated story follows the key structural beats of the selected archetype, while still allowing for creative variation in plot details, characters, and events.
2.  And the story flow feels logical and purposeful to the player.

## Tasks / Subtasks

- [x] AC 1: Define narrative archetypes.
  - [x] Subtask: Identify and document key narrative archetypes (e.g., Hero's Journey, Rags to Riches) and their structural beats.
  - [x] Subtask: Represent archetypes in a structured format (e.g., JSON or Python data structures) accessible by `services/ai_service.py`.
- [x] AC 1: Implement prompt engineering for narrative archetypes.
  - [x] Subtask: Modify `services/ai_service.py` to incorporate archetype instructions into prompts sent to the Gemini API.
  - [x] Subtask: Ensure prompts guide the AI to generate content consistent with the chosen archetype's structural beats.
- [x] AC 2: Integrate archetype selection into game state.
  - [x] Subtask: Update `GameSession.narrative_state` to include the selected narrative archetype.
- [x] AC 1, 2: Implement unit and integration tests.
  - [x] Subtask: Write unit tests for prompt generation logic, verifying archetype instructions are correctly embedded.
  - [x] Subtask: Write integration tests for API endpoints that trigger narrative generation, ensuring the AI receives and utilizes archetype context.
  - [ ] Subtask: Manual/Exploratory testing to assess the coherence and logic of AI-generated stories against selected archetypes.

### Review Follow-ups (AI)
- [ ] [Medium] Complete "Manual/Exploratory testing to assess the coherence and logic of AI-generated stories against selected archetypes" subtask to fully verify Acceptance Criterion 2.

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
- docs/sprint-artifacts/2-3-implement-narrative-archetypes-for-coherence.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List
- Defined narrative archetypes in a new `data/narrative_archetypes.py` file. Modified the `ai_service` to incorporate these archetypes into prompts for both narrative and room description generation, guiding the AI for more coherent stories. Updated the `GameSession` model to include the selected archetype. Added and updated unit and integration tests to verify the new functionality.

### File List
- Modified: `ai-escape-app/services/ai_service.py`
- Modified: `ai-escape-app/routes.py`
- Modified: `ai-escape-app/models.py`
- Modified: `ai-escape-app/tests/unit/test_ai_service.py`
- Modified: `ai-escape-app/tests/integration/test_narrative_route.py`
- Modified: `ai-escape-app/tests/integration/test_room_description_route.py`
- Created: `ai-escape-app/data/narrative_archetypes.py`

## Change Log

- **2025-12-03**: Story created.
- **2025-12-08**: Implemented narrative archetypes for coherence (Story 2.3).
- **2025-12-04**: Story context regenerated.
- **2025-12-10**: Re-review complete. Outcome: Approved. All blocking issues resolved.

### Senior Developer Review (AI) - Re-review

-   **Reviewer:** BIP
-   **Date:** 2025-12-10
-   **Outcome:** Approve
-   **Summary:** The initial review requested changes related to an incomplete manual testing task. The user has waived this requirement. A full code review was performed, and minor logging inconsistencies were identified and fixed. The story is now approved.

## Senior Developer Review (AI)

**Reviewer:** BIP
**Date:** 2025-12-09
**Outcome:** CHANGES REQUESTED

**Summary:**
The story "Implement Narrative Archetypes for Coherence" (Story 2.3) has been partially implemented. While the technical mechanisms for incorporating narrative archetypes are in place and tested, the crucial Acceptance Criterion 2, which assesses the logical and purposeful feel of the AI-generated story flow, remains unverified due to an incomplete manual/exploratory testing subtask.

**Key Findings:**

*   **MEDIUM Severity:**
    *   **Finding:** Acceptance Criterion 2 (AC2) - "And the story flow feels logical and purposeful to the player." is not fully verified.
    *   **Rationale:** Verification of AC2 explicitly relies on the "Manual/Exploratory testing to assess the coherence and logic of AI-generated stories against selected archetypes" subtask, which is currently marked as incomplete. Without this testing, the AI's ability to generate coherent stories based on archetypes from a user perspective cannot be confirmed.
*   **LOW Severity:**
    *   **Finding:** No Epic Tech Spec found for Epic 2.
    *   **Rationale:** The absence of a dedicated technical specification for Epic 2 means architectural guidance for this epic relies solely on the main `architecture.md` and story-level details. While not blocking, a dedicated tech spec would provide more explicit guidance.

**Acceptance Criteria Coverage:**

| AC# | Description                                                                                                                                                                                                                                                                                        | Status    | Evidence                                                                                                                                                                                                                                                                                                                                                                  |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Given a set of predefined narrative archetypes, when the AI generates a story, then the generated story follows the key structural beats of the selected archetype, while still allowing for creative variation in plot details, characters, and events. | IMPLEMENTED | `ai-escape-app/data/narrative_archetypes.py` (defines archetypes), `ai-escape-app/services/ai_service.py` (`generate_narrative`, `generate_room_description` functions incorporate archetype instructions), `ai-escape-app/tests/unit/test_ai_service.py`, `ai-escape-app/tests/integration/test_narrative_route.py`, `ai-escape-app/tests/integration/test_room_description_route.py`. |
| 2   | And the story flow feels logical and purposeful to the player.                                                                                                                                                                                                                                     | PARTIAL   | Requires completion of the manual/exploratory testing subtask for full verification. The current automated tests verify the mechanism, not the qualitative outcome.                                                                                                                                                                                                |

**Summary: 1 of 2 acceptance criteria fully implemented, 1 partial.**

**Task Completion Validation:**

| Task                                                                                                                                                                  | Marked As | Verified As        | Evidence                                                                                                                                                                                                                                                                                                                                                                                        |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AC 1: Define narrative archetypes.                                                                                                                                    | [x]       | VERIFIED COMPLETE  | `ai-escape-app/data/narrative_archetypes.py`                                                                                                                                                                                                                                                                                                                                                    |
|   Subtask: Identify and document key narrative archetypes (e.g., Hero's Journey, Rags to Riches) and their structural beats.                                          | [x]       | VERIFIED COMPLETE  | `ai-escape-app/data/narrative_archetypes.py`                                                                                                                                                                                                                                                                                                                                                    |
|   Subtask: Represent archetypes in a structured format (e.g., JSON or Python data structures) accessible by `services/ai_service.py`.                               | [x]       | VERIFIED COMPLETE  | `ai-escape-app/data/narrative_archetypes.py`                                                                                                                                                                                                                                                                                                                                                    |
| AC 1: Implement prompt engineering for narrative archetypes.                                                                                                          | [x]       | VERIFIED COMPLETE  | `ai-escape-app/services/ai_service.py`                                                                                                                                                                                                                                                                                                                                                        |
|   Subtask: Modify `services/ai_service.py` to incorporate archetype instructions into prompts sent to the Gemini API.                                                 | [x]       | VERIFIED COMPLETE  | `ai-escape-app/services/ai_service.py` (`_get_narrative_archetype_prompt_snippet` and usage).                                                                                                                                                                                                                                                                                                     |
|   Subtask: Ensure prompts guide the AI to generate content consistent with the chosen archetype's structural beats.                                                   | [x]       | VERIFIED COMPLETE  | `ai-escape-app/services/ai_service.py` (prompt construction logic).                                                                                                                                                                                                                                                                                                                               |
| AC 2: Integrate archetype selection into game state.                                                                                                                  | [x]       | VERIFIED COMPLETE  | `ai-escape-app/models.py` (`GameSession` model updated), `ai-escape-app/routes.py` (`start_game`, `get_session` routes).                                                                                                                                                                                                                                                                      |
|   Subtask: Update `GameSession.narrative_state` to include the selected narrative archetype.                                                                          | [x]       | VERIFIED COMPLETE  | `ai-escape-app/models.py` (`GameSession` model updated for narrative_archetype).                                                                                                                                                                                                                                                                                                                  |
| AC 1, 2: Implement unit and integration tests.                                                                                                                        | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/unit/test_ai_service.py`, `ai-escape-app/tests/integration/test_narrative_route.py`, `ai-escape-app/tests/integration/test_room_description_route.py`.                                                                                                                                                                                                                 |
|   Subtask: Write unit tests for prompt generation logic, verifying archetype instructions are correctly embedded.                                                     | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/unit/test_ai_service.py`.                                                                                                                                                                                                                                                                                                                                                    |
|   Subtask: Write integration tests for API endpoints that trigger narrative generation, ensuring the AI receives and utilizes archetype context.                      | [x]       | VERIFIED COMPLETE  | `ai-escape-app/tests/integration/test_narrative_route.py`, `ai-escape-app/tests/integration/test_room_description_route.py`.                                                                                                                                                                                                                                                                      |
|   Subtask: Manual/Exploratory testing to assess the coherence and logic of AI-generated stories against selected archetypes.                                          | [ ]       | INCOMPLETE         | Task is explicitly marked as incomplete in the story file.                                                                                                                                                                                                                                                                                                                                        |

**Summary: 7 of 7 completed tasks verified, 0 questionable, 0 falsely marked complete. 1 incomplete task.**

**Test Coverage and Gaps:**
- Unit and integration tests cover the technical implementation of archetype integration.
- A notable gap is the absence of verification for AC2, dependent on manual/exploratory testing.

**Architectural Alignment:**
- The implementation aligns with the architectural decisions regarding AI service integration (Gemini Pro), client library usage, prompt management strategy (structured prompting with narrative archetypes), and game state management (`GameSession.narrative_state`).

**Security Notes:**
- Prompts are constructed from internally defined archetypes. The previous advisory regarding prompt injection best practices for dynamic prompt construction (from Story 2.2 review) remains relevant here as well, especially if archetype content were ever to be influenced by external input.

**Best-Practices and References:**
- Python/Flask best practices appear to be followed.
- Testing strategy is comprehensive for automated tests.
- Reiterate importance of applying Gemini API prompt engineering best practices (e.g., clarity, context, examples, role definition, iteration) for future AI-related development, especially with dynamic prompt components like narrative archetypes.

### Action Items

**Code Changes Required:**
- [ ] [Medium] Complete "Manual/Exploratory testing to assess the coherence and logic of AI-generated stories against selected archetypes" subtask to fully verify Acceptance Criterion 2.

**Advisory Notes:**
- Note: No Epic Tech Spec found for Epic 2. (Low Severity)
- Note: Reiterate importance of applying Gemini API prompt engineering best practices (e.g., clarity, context, examples, role definition, iteration) for future AI-related development, especially with dynamic prompt components like narrative archetypes.
