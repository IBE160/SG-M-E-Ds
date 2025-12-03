# Story 4.2: Expand Library of Visual Assets and Themes

Status: drafted

## Story

As a game designer,
I want to expand the available library of visual assets and themes,
So that players have more diverse and immersive choices for their escape rooms.

## Acceptance Criteria

1.  Given a new set of images and themes are added to the game, when a player selects a new theme, then the AI can generate room descriptions and puzzles consistent with the expanded library.

## Tasks / Subtasks

- [ ] AC 1: Curate and integrate new visual assets.
  - [ ] Subtask: Source and select additional free-to-use images corresponding to new themes.
  - [ ] Subtask: Store new images in `ai-escape-app/static/images/`.
- [ ] AC 1: Update AI's understanding of available themes.
  - [ ] Subtask: Modify `services/ai_service.py` to update prompt engineering based on the expanded library of themes and corresponding visual asset availability.
  - [ ] Subtask: Ensure AI can generate consistent room descriptions and puzzles for new themes.
- [ ] AC 1: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests to verify the new image assets are correctly located and mapped to themes.
  - [ ] Subtask: Write unit tests for `services/ai_service.py` functions, mocking the Gemini API to verify prompt construction for new themes.
  - [ ] Subtask: Manual/Exploratory testing to assess the visual consistency of AI-generated content with new themes.

## Dev Notes

### Requirements Context Summary

**From Epic 4: Expanding Variety and Replayability**
-   **Goal:** Increase the breadth of content and player choice to deliver on the promise of endless replayability.

**From PRD (Product Requirements Document) - FR-001: Dynamic Content Generation, Future Consideration: Content Expansion**
-   **FR-001:** The AI generates unique storylines, and creates room descriptions based on user input.
-   **Future Consideration: Content Expansion:** Significantly growing the variety of puzzle types and the library of visual assets.

**From Architecture Document (`docs/architecture.md`)**
-   **Asset Management/Storage:** Local storage in `static/` directory will be expanded. Easily migratable to CDN for scalability.
-   **AI Integration:** Utilizes Gemini Pro / Gemini 1.5 Pro (for content generation).
-   **Prompt Management Strategy:** Structured Prompting Strategy.
-   **Testing Strategy:** Unit, Integration Tests using Pytest.

### Learnings from Previous Story

**From Story 4.1: Implement Dynamic Difficulty Adjustment (Status: drafted)**

-   **Goal:** The AI to dynamically adjust the game's difficulty based on player performance, So that the challenge remains engaging and fair.
-   **Acceptance Criteria:** AI evaluates player performance and subtly adjusts parameters for future puzzles.
-   **Key Technical Notes:** Extending `GameSession` to track player performance metrics, extending `services/game_logic.py` for metric evaluation, extending `services/ai_service.py` for difficulty adjustment prompts, creating `POST /adjust_difficulty` API.
-   **Relevant Learnings for Story 4.2:**
    *   `services/ai_service.py` is the central module for AI content generation and adaptation, making it the logical place to update AI's understanding of new themes.
    *   Flask routes are established for backend communication.
    *   The `GameSession` model is extensible for new parameters like theme/location if needed for future game state saving/loading.

[Source: docs/sprint-artifacts/4-1-implement-dynamic-difficulty-adjustment.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md]
- [Source: docs/sprint-artifacts/4-1-implement-dynamic-difficulty-adjustment.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
