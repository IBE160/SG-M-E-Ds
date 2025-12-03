# Story 1.5: Display Basic Visuals for Rooms

Status: drafted

## Story

As a player,
I want to see a background image for each room,
So that the game feels more immersive.

## Acceptance Criteria

1.  Given the player enters a new room, when the room description is displayed, then a corresponding background image for that room is also displayed.

## Tasks / Subtasks

- [ ] AC 1: Source and prepare image assets.
  - [ ] Subtask: Select a library of free-to-use images for each hard-coded room (e.g., Room 1, Room 2, Room 3).
  - [ ] Subtask: Store images in `ai-escape-app/static/images/`.
- [ ] AC 1: Create a mapping between rooms and image assets.
  - [ ] Subtask: Update the room data structure (e.g., in `data/rooms.py` from Story 1.3) to include a reference to the corresponding image file for each room.
- [ ] AC 1: Implement dynamic display of background images.
  - [ ] Subtask: Modify the Jinja2 templates (e.g., `templates/game.html`) to dynamically load and display the background image based on the `current_room` in the `GameSession`.
  - [ ] Subtask: Ensure images are responsive and accessible (e.g., using `alt=""` for decorative images).
- [ ] AC 1: Implement unit and integration tests.
  - [ ] Subtask: Write unit tests for the room-to-image mapping data structure.
  - [ ] Subtask: Write integration tests to verify that Flask routes correctly pass image data to templates.
  - [ ] Subtask: Write E2E tests to visually confirm that the correct background image is displayed for each room in the UI.

## Dev Notes

### Requirements Context Summary

**From Epic 1: Foundational Framework & A Single, Static Escape Room**
-   **Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a *single, hard-coded* story and puzzle chain.

**From PRD (Product Requirements Document) - FR-010: Basic Visuals**
-   **FR-010:** Specifies a pre-selected, free-to-use image library organized by theme to provide atmospheric background images for rooms.

**From Architecture Document (`docs/architecture.md`)**
-   **Asset Management/Storage:** Start with local storage in `static/` directory. Easily migratable to CDN for scalability.
-   **UX/UI:** Accessibility Implementation (WCAG 2.1 Level AA compliant color contrast). Tailwind CSS for styling. Visual foundation with a defined color system and typography. Project Structure: `static/images/` for images.

### Learnings from Previous Story

**From Story 1.4: Implement the Core Interaction Model (Status: drafted)**

-   **Goal:** Interact with the game world through a set of contextual options and a "go back" function, So that I can navigate and solve puzzles.
-   **Acceptance Criteria:** Displaying numbered lists of options, and selecting an option by entering the corresponding number.
-   **Key Technical Notes:** Uses Flask API Routes for communication, `.option-btn` elements, `.immersive-option` for navigation, accessibility with keyboard navigation and focus indicators.
-   **Relevant Learnings for Story 1.5:**
    *   Story 1.4 focuses on the interaction logic, which will be critical for triggering room changes.
    *   The use of Jinja2 templates and Flask routes for UI rendering and backend communication is established, providing the necessary framework for displaying dynamic background images.
    *   Accessibility considerations and styling (Tailwind CSS) from previous stories are directly applicable.

[Source: docs/sprint-artifacts/1-4-implement-the-core-interaction-model.md]

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- [Source: docs/prd.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]
- [Source: docs/sprint-artifacts/1-4-implement-the-core-interaction-model.md]

## Dev Agent Record

### Context Reference

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.
