# Epic Technical Specification: The AI Puzzle Master

Date: 2025-12-03
Author: BIP
Epic ID: 3
Status: Draft

---

## Overview

This Epic focuses on empowering the AI to dynamically generate and adapt puzzles within the "AI Escape" game, building upon the coherent narrative framework established in Epic 2. The primary goal is to introduce the complexity of dynamic puzzles only after the narrative is stable, utilizing "Puzzle Dependency Chains" to ensure all AI-generated games are solvable and logically consistent. This is a critical step towards achieving true replayability and player engagement by providing responsive and personalized challenges.

## Objectives and Scope

### In Scope (Epic 3)

*   **Integrate AI Puzzle Generation Service (Story 3.1):** Integrate an AI service (Gemini API) to dynamically create interactive puzzle challenges, handling API requests and responses.
*   **Implement Dynamic Puzzle Adaptation (Story 3.2):** Enable the AI to dynamically adapt puzzles based on player actions and game state, providing responsive and personalized challenges.
*   **Implement Puzzle Dependency Chains (Story 3.3):** Ensure AI-generated puzzles are always solvable and logically connected, preventing unsolvable scenarios through internal AI logic.
*   **Integrate Player Puzzle Interaction (Story 3.4):** Allow players to interact with puzzles using contextual options and input mechanisms, and provide feedback based on AI puzzle logic.

### Out of Scope (for Epic 3)

*   Core game state management (addressed in Epic 1).
*   AI narrative generation (addressed in Epic 2).
*   Visual asset expansion (addressed in Epic 4).
*   Dynamic difficulty adjustment beyond puzzle adaptation (addressed in Epic 4).
*   Background music, sound effects, or complex animations.
*   User authentication (addressed in Epic 5).
*   Load/Save game functionality (addressed in Epic 5).

## System Architecture Alignment

Epic 3 heavily aligns with critical architectural decisions related to AI integration outlined in `docs/architecture.md`:

*   **AI Service Integration:** Utilizes Gemini Pro / Gemini 1.5 Pro for puzzle generation.
*   **AI Client Library:** Employs `google-generativeai 0.8.5` for interacting with the Gemini API.
*   **Prompt Management Strategy:** Relies on Structured Prompting with "Puzzle Dependency Chains" to ensure solvable and coherent puzzles.
*   **API Pattern for AI interactions:** Flask API Routes will secure AI API keys and provide RESTful endpoints for frontend interaction with AI generation logic.
*   **Performance:** Background processing using Celery with Redis is a "Nice-to-Have" decision, deferred until performance testing indicates a need for slow AI generation.
*   **Data Architecture:** `GameSession.puzzleState` will be crucial for providing context to the AI for dynamic adaptation.

## Detailed Design

### Services and Modules

*   **`services/ai_service.py`**: This module will be extended to include functionality for puzzle generation, adaptation, and evaluation using the Gemini API. This will involve sophisticated prompt engineering to guide the AI's adaptation logic and manage puzzle prerequisites/outcomes.
*   **`routes.py`**: New Flask API endpoints will be added to handle requests for dynamic puzzle generation, player interaction with puzzles, and puzzle adaptation. These endpoints will communicate with `services/ai_service.py`.
*   **`GameSession` in `models.py`**: The `puzzle_state` field (JSON object) will be actively utilized to store the current state of puzzles, necessary for AI adaptation and dependency tracking.

### Data Models and Contracts

The `GameSession` model (defined in `models.py`) remains central, with its `puzzle_state` (JSON object) field being actively utilized to store and convey AI-generated content and context related to puzzles.

*   `puzzle_state`: A JSON object that will hold the evolving puzzle context for the AI, ensuring solvability and logical connection.

### APIs and Interfaces

*   `POST /generate_puzzle`: An API endpoint to request AI-generated puzzles.
    *   **Request Body:** `{"prompt": "string", "theme": "string", "location": "string", "difficulty": "string", "context": "JSON_object"}`
    *   **Response:** `{"puzzle_description": "string", "solution_mechanism": "string", "updated_puzzle_state": "JSON_object"}`
*   `POST /evaluate_puzzle_solution`: An API endpoint to send a player's solution attempt and receive AI evaluation.
    *   **Request Body:** `{"session_id": int, "puzzle_id": "string", "player_attempt": "string", "puzzle_state": "JSON_object"}`
    *   **Response:** `{"feedback": "string", "is_solved": bool, "updated_puzzle_state": "JSON_object"}`
*   `POST /adapt_puzzle`: An API endpoint to request AI to adapt a puzzle based on game state.
    *   **Request Body:** `{"session_id": int, "puzzle_id": "string", "game_state_context": "JSON_object"}`
    *   **Response:** `{"adapted_puzzle_description": "string", "updated_puzzle_state": "JSON_object"}`

### Workflows and Sequencing

1.  **AI Puzzle Service Integration (Story 3.1):** Extend `services/ai_service.py` with puzzle generation capabilities using the Gemini API. Create Flask routes for puzzle requests.
2.  **Dynamic Puzzle Adaptation (Story 3.2):** Player attempts a puzzle; backend sends `player_attempt` and `game_state_context` to `services/ai_service.py` via an API endpoint. AI evaluates and adapts.
3.  **Puzzle Dependency Chains (Story 3.3):** AI logic within `services/ai_service.py` (guided by prompt engineering) manages puzzle prerequisites and outcomes, potentially through graph-based representation, ensuring solvability before sending to client.
4.  **Player Puzzle Interaction (Story 3.4):** Frontend uses API endpoints (e.g., `POST /evaluate_puzzle_solution`) to send player interactions. Backend processes and provides feedback.
5.  **Game State Update:** AI-generated puzzle details and updates are parsed by the backend and used to update the `GameSession.puzzle_state` field in the database.

## Non-Functional Requirements

### Performance

*   **Latency:** API responses for state updates (movement, inventory) should ideally be under 200ms for a smooth player experience.
*   **Throughput:** The system should support up to 10 concurrent active game sessions without degradation in response time.
*   **Scalability:** The Flask application will be deployed in a manner that supports horizontal scaling by adding more instances behind a load balancer. Supabase handles database scaling.
*   **AI Response Time:** API responses for puzzle generation and evaluation may have higher latency than simple state updates. Loading indicators and potential deferred processing will be crucial. Target AI response time for puzzle generation/adaptation: 5-15 seconds. Background processing will be crucial if these times are not met synchronously.

### Security

*   **API Keys:** All sensitive API keys (e.g., Gemini API) will be stored as server-side environment variables and never exposed to the client. Flask API Routes serve as a secure gateway.
*   **Communication:** All client-server communication will utilize HTTPS/SSL.
*   **Data Validation:** All incoming API requests will undergo validation to prevent malformed data.
*   **Prompt Injection:** Robust input sanitization and validation for player inputs that influence AI puzzle generation.
*   **Data Privacy:** Ensure no sensitive user data is inadvertently sent to the AI service.
*   **Game State Integrity:** Ensure server-side validation of puzzle solutions and state changes to prevent client-side manipulation.

### Reliability/Availability

*   **Uptime:** Target 99.9% uptime for the application API.
*   **Data Durability:** Supabase (PostgreSQL) provides managed backups and replication to ensure data durability.
*   **Error Handling:** Robust error handling in Flask API routes, providing clear error messages for failed operations.
*   **AI Service Dependency:** Application reliability is highly dependent on the availability and performance of the Gemini API for puzzle services. Implement robust retry mechanisms and fallback strategies.
*   **Puzzle Solvability:** A critical reliability requirement is that AI-generated puzzle chains are always solvable, preventing player frustration.

### Observability

*   **Logging:** Structured JSON logging will be implemented using Python's `logging` module, capturing `timestamp`, `level`, `message`, `request_id`, and relevant context for all API interactions and state changes. Logs will be output to `stdout` for collection by a centralized logging service.
*   **AI Interaction Logging:** Enhanced logging will capture details of AI prompts for puzzle generation/adaptation, responses, and evaluation results. Log additional context such as `puzzle_id`, `player_attempt`, and `ai_model_version`.
*   **Game State Auditing:** Logging changes to `GameSession.puzzle_state` for debugging and post-game analysis of puzzle progression.

## Dependencies and Integrations

*   **Python Libraries:** Flask, SQLAlchemy, supabase, python-dotenv, gunicorn, pytest, `google-generativeai`.
*   **External APIs:** Google Gemini API.
*   **Background Processing (Deferred):** Celery with Redis for asynchronous AI calls for puzzle generation/adaptation if needed.
*   **Existing Components:** Relies heavily on the `GameSession` model and database persistence established in Epic 1, and the AI service integration (specifically `services/ai_service.py`) established in Epic 2.

## Acceptance Criteria (Authoritative)

The acceptance criteria for Epic 3 are derived directly from its constituent user stories:

### Story 3.1: Integrate AI Puzzle Generation Service
*   **Given** an AI puzzle generation service (e.g., Gemini API), **when** a prompt is sent to the service, **then** the service returns a coherent puzzle description and solution.
*   **And** the application can successfully receive and parse this puzzle.

### Story 3.2: Implement Dynamic Puzzle Adaptation
*   **Given** a puzzle has been generated, **when** the player attempts a solution, **then** the AI evaluates the attempt and adapts the puzzle's difficulty or provides contextual hints if needed.
*   **And** the game state reflects the puzzle's progression.

### Story 3.3: Implement Puzzle Dependency Chains
*   **Given** a set of dynamically generated puzzles for an escape room, **when** the AI generates the puzzle sequence, **then** the puzzles are arranged in a solvable dependency chain.
*   **And** the game verifies the solvability of the generated chain.

### Story 3.4: Integrate Player Puzzle Interaction
*   **Given** a puzzle is presented, **when** the player selects an interaction option, **then** the game processes the input and provides feedback based on the AI's puzzle logic.

## Traceability Mapping

| Acceptance Criteria (AC) | Spec Section(s) | Component(s)/API(s) | Test Idea |
|---|---|---|---|
| **AC 3.1.1** AI service returns puzzle | PRD: FR-005, Arch: AI Service Integration | `services/ai_service.py` | Unit test: Mock Gemini API, verify puzzle response parsing |
| **AC 3.1.2** App receives/parses puzzle | PRD: FR-005, Arch: API Pattern for AI | `routes.py`, `services/ai_service.py` | Integration test: API call to Flask route, verify puzzle is stored/processed |
| **AC 3.2.1** AI adapts puzzle based on player action | PRD: FR-005, Arch: Prompt Management | `services/ai_service.py` | Unit test: Simulate player attempt, verify AI adaptation logic |
| **AC 3.2.2** Game state reflects progression | PRD: FR-005, Arch: Game State Management | `services/game_logic.py`, `models.py` | Integration test: Verify `puzzle_state` updates after adaptation |
| **AC 3.3.1** Puzzles in solvable dependency chain | PRD: FR-005, Arch: Prompt Management | `services/ai_service.py` | Unit test: Simulate puzzle generation, verify dependency logic |
| **AC 3.3.2** Game verifies solvability | PRD: FR-005, Arch: Game State Management | `services/game_logic.py` | Unit test: Validate generated puzzle chain against solvability rules |
| **AC 3.4.1** Game processes player interaction | PRD: FR-004, Arch: API Pattern for AI | `routes.py`, `services/ai_service.py` | Integration test: Simulate player input, verify correct feedback |

## Risks, Assumptions, Open Questions

### Risks

*   **AI Coherence & Solvability:** Ensuring AI-generated puzzles are always coherent, fair, and solvable, especially within complex dependency chains, is a significant risk.
    *   *Mitigation:* Advanced prompt engineering, robust validation of AI outputs, and iterative refinement of puzzle generation logic.
*   **Performance of Complex AI Prompts:** Generating and adapting puzzles may require more complex AI interactions, potentially increasing latency and cost.
    *   *Mitigation:* Caching, prompt optimization, and background processing (Celery/Redis) if performance is critical.

### Assumptions

*   **Gemini API Capabilities:** The Gemini API can handle complex prompt engineering required for puzzle generation, adaptation, and dependency management.
*   **Effective Prompt Engineering:** The ability to craft prompts that consistently guide the AI to generate high-quality, solvable puzzles.
*   **Game State Accuracy:** `GameSession.puzzleState` accurately reflects the current puzzle context for AI interaction.

### Open Questions

*   **Puzzle Types and Mechanics:** Specific implementation details for different puzzle types (e.g., riddles, observation, combination locks) and how the AI will manage their mechanics.
*   **Feedback Mechanisms:** How player interactions with puzzles will be presented and evaluated by the AI (e.g., scoring, hints, partial successes).
*   **Integration with UI:** How dynamic puzzles and interaction options will be presented to the player in the UI.

## Test Strategy Summary

A multi-layered testing strategy will be employed for Epic 3:

*   **Unit Tests:** Using Pytest to test individual functions in `services/ai_service.py` related to puzzle generation, adaptation, and evaluation logic. Mocking the Gemini API will be crucial.
*   **Integration Tests:** Using Pytest for Flask API routes in `routes.py` to ensure correct interaction with `services/ai_service.py` and proper updates to `GameSession.puzzle_state`.
*   **Manual Testing/Exploratory Testing:** Extensive manual testing will be critical to evaluate the quality, coherence, solvability, and player experience of AI-generated puzzles. This will be the primary method for validating Acceptance Criteria related to subjective quality and logic.
*   **Automated Puzzle Validation:** Develop internal tools or scripts to automatically check the solvability and logical consistency of generated puzzle chains.
*   **Performance Testing (Deferred):** Load testing of AI puzzle API endpoints to identify potential bottlenecks.
