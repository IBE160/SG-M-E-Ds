# Epic Technical Specification: Expanding Variety and Replayability

Date: 2025-12-03
Author: BIP
Epic ID: 4
Status: Draft

---

## Overview

This Epic aims to significantly increase the breadth of content and player choice within the "AI Escape" game, delivering on the promise of endless replayability. Building on the core dynamic systems established in previous epics, Epic 4 focuses on scaling game content through more themes, puzzles, and visuals. This is a lower-risk endeavor now that the foundational AI-driven narrative and puzzle generation systems have proven stable and coherent, allowing for a concentrated effort on enhancing player customization and overall game variety.

## Objectives and Scope

### In Scope (Epic 4)

*   **Implement Dynamic Difficulty Adjustment (Story 4.1):** Enable the AI to dynamically adjust game difficulty based on player performance, ensuring an engaging and fair challenge.
*   **Expand Library of Visual Assets and Themes (Story 4.2):** Integrate additional visual assets and themes to offer players more diverse and immersive choices for their escape rooms, consistent with AI generation.
*   **Implement Enhanced Game Setup Flow (Story 4.3):** Provide an enhanced game setup experience with more options and clearer guidance for players to customize their gameplay effectively.

### Out of Scope (for Epic 4)

*   Core game state management (addressed in Epic 1).
*   AI narrative generation (addressed in Epic 2).
*   AI puzzle generation and adaptation (addressed in Epic 3).
*   Complex background processing for slow AI generation (deferred).
*   User authentication (addressed in Epic 5).
*   Load/Save game functionality (addressed in Epic 5).

## System Architecture Alignment

Epic 4 aligns with critical architectural decisions related to AI integration, asset management, and UX outlined in `docs/architecture.md`:

*   **AI Integration (for dynamic difficulty adjustment):** Utilizes Gemini Pro / Gemini 1.5 Pro to influence puzzle generation parameters based on player performance.
*   **Asset Management:** Local storage in `static/images/` will be expanded to accommodate new visual assets.
*   **Prompt Management Strategy:** Structured Prompting will be refined to incorporate player performance metrics for difficulty adjustment and expanded theme parameters.
*   **UX/UI:** Enhanced Game Setup Flow will leverage existing `.option-btn` components and improved instructional text, consistent with the UX design.
*   **Game State Management:** `GameSession` (`GameSession.gameHistory` and `GameSession.puzzleState`) will be crucial for tracking player performance metrics, which will feed into the AI for dynamic difficulty adjustments.

## Detailed Design

### Services and Modules

*   **`services/ai_service.py`**: This module will be further extended to incorporate logic for dynamic difficulty adjustment. It will receive player performance metrics and use them to inform prompt engineering for subsequent puzzle generation and adaptation. It will also handle expanded theme parameters.
*   **`routes.py`**: Flask API endpoints will be adapted to pass player performance data to `services/ai_service.py` for difficulty adjustment. New endpoints might be introduced or existing ones enhanced to handle the expanded game setup options.
*   **`GameSession` in `models.py`**: The `GameSession` model will be utilized to track player performance metrics (e.g., number of hints used, time taken per puzzle) necessary for dynamic difficulty adjustment.
*   **`static/images/`**: The local image asset library will be expanded to support new themes and locations.
*   **`templates/`**: Frontend templates will be updated to present new theme, location, and difficulty options, along with clear descriptions in the game setup flow.

### Data Models and Contracts

The `GameSession` model (defined in `models.py`) will be augmented or its existing fields (e.g., `game_history`, `puzzle_state`) will be leveraged to store player performance metrics.

*   `GameSession`: Will track player performance (e.g., `time_taken_per_puzzle`, `hints_used`) to inform dynamic difficulty.

### APIs and Interfaces

*   `POST /adjust_difficulty`: An API endpoint to send player performance metrics to the backend for AI-driven difficulty adjustment.
    *   **Request Body:** `{"session_id": int, "player_performance_metrics": "JSON_object"}`
    *   **Response:** `{"session_id": int, "adjusted_difficulty_parameters": "JSON_object"}`
*   `GET /game_setup_options`: An API endpoint to retrieve expanded theme, location, and difficulty options.
    *   **Response:** `{"themes": list, "locations": list, "difficulties": list}`

### Workflows and Sequencing

1.  **Dynamic Difficulty Adjustment (Story 4.1):** Backend collects player performance metrics (e.g., from `GameSession` updates). These metrics are passed to `services/ai_service.py` via an API endpoint, influencing subsequent AI generation prompts for puzzles.
2.  **Asset Expansion (Story 4.2):** New images are added to `static/images/`. AI generation prompts in `services/ai_service.py` are updated to reflect the expanded library of themes and locations.
3.  **Enhanced Game Setup Flow (Story 4.3):** Frontend presents expanded options based on data from backend endpoints. Player choices are saved to `GameSession`, influencing AI generation parameters.

## Non-Functional Requirements

### Performance

*   **Latency:** API responses for state updates (movement, inventory) should ideally be under 200ms for a smooth player experience.
*   **Throughput:** The system should support up to 10 concurrent active game sessions without degradation in response time.
*   **Scalability:** The Flask application will be deployed in a manner that supports horizontal scaling by adding more instances behind a load balancer. Supabase handles database scaling.
*   **AI Response Time:** AI-driven difficulty adjustments should not introduce noticeable latency during gameplay. Metrics collection and prompt adjustments should be efficient.

### Security

*   **API Keys:** All sensitive API keys (e.g., Gemini API, if used for dynamic difficulty adjustment) will be stored as server-side environment variables and never exposed to the client. Flask API Routes serve as a secure gateway.
*   **Communication:** All client-server communication will utilize HTTPS/SSL.
*   **Data Validation:** All incoming API requests will undergo validation to prevent malformed data.
*   **Data Integrity:** Player performance metrics used for difficulty adjustment must be secure and tamper-proof.

### Reliability/Availability

*   **Uptime:** Target 99.9% uptime for the application API.
*   **Data Durability:** Supabase (PostgreSQL) provides managed backups and replication to ensure data durability.
*   **Error Handling:** Robust error handling in Flask API routes, providing clear error messages for failed operations.
*   **Consistency:** AI-generated content must remain consistent with expanded themes and locations.
*   **Difficulty Scaling:** The dynamic difficulty adjustment must reliably provide an optimal challenge, avoiding situations that are too easy or too hard.

### Observability

*   **Logging:** Structured JSON logging will be implemented using Python's `logging` module, capturing `timestamp`, `level`, `message`, `request_id`, and relevant context for all API interactions and state changes. Logs will be output to `stdout` for collection by a centralized logging service.
*   **Performance Metrics Logging:** Logging of player performance metrics and AI-driven difficulty adjustments for analysis and system improvement.
*   **Asset Loading Metrics:** Monitoring asset loading times and success rates.

## Dependencies and Integrations

*   **Python Libraries:** Flask, SQLAlchemy, supabase, python-dotenv, gunicorn, pytest, `google-generativeai`.
*   **External APIs:** Google Gemini API.
*   **Existing Components:** Relies on `GameSession` model (Epic 1), AI service integration (`services/ai_service.py` from Epic 2, Epic 3).
*   **Visual Assets:** Expanded library of static images in `static/images/`.

## Acceptance Criteria (Authoritative)

The acceptance criteria for Epic 4 are derived directly from its constituent user stories:

### Story 4.1: Implement Dynamic Difficulty Adjustment
*   **Given** a player's performance in a series of puzzles, **when** the AI evaluates this performance, **then** the AI subtly adjusts parameters for future puzzles to maintain an optimal challenge level.

### Story 4.2: Expand Library of Visual Assets and Themes
*   **Given** a new set of images and themes are added to the game, **when** a player selects a new theme, **then** the AI can generate room descriptions and puzzles consistent with the expanded library.

### Story 4.3: Implement Enhanced Game Setup Flow
*   **Given** the game setup menu, **when** I navigate through the options, **then** I can choose from an expanded list of themes, locations, puzzle types, and difficulty levels, with clear descriptions for each.

## Traceability Mapping

| Acceptance Criteria (AC) | Spec Section(s) | Component(s)/API(s) | Test Idea |
|---|---|---|---|
| **AC 4.1.1** AI adjusts difficulty | PRD: FR-001, Arch: Advanced AI | `services/ai_service.py` | Unit test: Simulate player performance, verify AI adjusts puzzle generation parameters |
| **AC 4.2.1** AI generates content consistent with new themes | PRD: FR-001, Arch: Asset Management | `services/ai_service.py`, `static/images/` | Unit test: Prompt AI with new theme, verify consistent content |
| **AC 4.3.1** Expanded themes/locations/difficulty options | PRD: FR-002, Arch: UX/UI | `routes.py`, `templates/` | E2E test: Verify game setup UI presents expanded options |

## Risks, Assumptions, Open Questions

### Risks

*   **AI Coherence (for expanded content):** Ensuring AI-generated content (narrative, puzzles, descriptions) remains coherent and logical when incorporating expanded themes and visual assets.
    *   *Mitigation:* Robust prompt engineering, testing with diverse themes, and iterative refinement of AI models.
*   **Difficulty Adjustment Accuracy:** The risk of the AI over- or under-adjusting difficulty, leading to player frustration or boredom.
    *   *Mitigation:* Careful selection of player performance metrics, fine-tuning of AI difficulty parameters, and extensive playtesting.

### Assumptions

*   **Gemini API Capabilities (for dynamic difficulty):** The Gemini API is capable of receiving player performance metrics and adjusting its content generation parameters (for puzzles, hints, etc.) accordingly to achieve dynamic difficulty.
*   **Effectiveness of Prompt Engineering for difficulty:** That specific prompt engineering techniques can effectively guide the AI to implement nuanced difficulty adjustments.
*   **Scalability of Asset Management:** The local `static/images/` directory will be sufficient for the expanded library during MVP.

### Open Questions

*   **Specific metrics for player performance:** What precise metrics (e.g., time to solve, hints used, number of attempts) will be used to gauge player performance for difficulty adjustment.
*   **Granularity of difficulty adjustment:** How subtly or drastically will the AI adjust difficulty parameters (e.g., slight change in riddle complexity, adding/removing red herrings).
*   **User Experience for expanded setup:** How to best present the expanded themes, locations, and difficulty choices to the player for a seamless and intuitive setup experience.

## Test Strategy Summary

A multi-layered testing strategy will be employed for Epic 4:

*   **Unit Tests:** Using Pytest for `services/ai_service.py` functions related to processing player performance metrics and generating content with adjusted difficulty parameters. Mocking the Gemini API will be essential.
*   **Integration Tests:** Using Pytest for Flask API routes that handle player performance submission and game setup option retrieval, ensuring correct interaction with backend logic.
*   **Manual Testing/Exploratory Testing:** Extensive manual playtesting will be crucial for evaluating the impact of dynamic difficulty adjustment on player engagement, and verifying the consistency of AI-generated content across expanded themes.
*   **A/B Testing (Potential Future):** Consider A/B testing different difficulty adjustment algorithms or prompt engineering strategies to optimize player experience.
