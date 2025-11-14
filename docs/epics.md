# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** Friday, 14 November 2025
**Project Level:** 3
**Target Scale:** single-user

---

## Overview

## Enhanced Epic Structure

### Epic 1: Foundational Framework & A Single, Static Escape Room
*   **Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a *single, hard-coded* story and puzzle chain.
*   **Rationale:** This ensures we have a working, enjoyable game *before* introducing the complexity of AI. It provides a "golden path" to test against and forces the integration of the interaction model and narrative flow from the start.

### Epic 2: Introducing the AI Storyteller
*   **Goal:** Replace the static story and room descriptions from Epic 1 with AI-generated content, while ensuring coherence.
*   **Rationale:** This isolates the challenge of narrative generation from puzzle generation. It directly integrates "Narrative Archetypes" to ensure the story is logical, tackling a key risk early.

### Epic 3: The AI Puzzle Master
*   **Goal:** Empower the AI to dynamically generate and adapt puzzles within the coherent narrative framework.
*   **Rationale:** This introduces the complexity of dynamic puzzles only after the narrative framework is stable. It uses "Puzzle Dependency Chains" to ensure all generated games are solvable.

### Epic 4: Expanding Variety and Replayability
*   **Goal:** Increase the breadth of content and player choice to deliver on the promise of endless replayability.
*   **Rationale:** This epic now focuses on scaling content (more themes, puzzles, visuals), which is a much lower risk after the core dynamic systems have been proven to be stable and coherent.

---

<!-- Repeat for each epic (N = 1, 2, 3...) -->

## Epic {{N}}: {{epic_title_N}}

{{epic_goal_N}}

<!-- Repeat for each story (M = 1, 2, 3...) within epic N -->

### Story {{N}}.{{M}}: {{story_title_N_M}}

As a {{user_type}},
I want {{capability}},
So that {{value_benefit}}.

**Acceptance Criteria:**

**Given** {{precondition}}
**When** {{action}}
**Then** {{expected_outcome}}

**And** {{additional_criteria}}

**Prerequisites:** {{dependencies_on_previous_stories}}

**Technical Notes:** {{implementation_guidance}}

<!-- End story repeat -->

---

<!-- End epic repeat -->

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._
