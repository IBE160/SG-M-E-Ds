# Epic Technical Specification: Introducing the AI Storyteller

Date: 2025-12-03
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This Epic focuses on transitioning the "AI Escape" game from static, hard-coded story and room descriptions (as established in Epic 1) to dynamically generated content powered by AI. The primary goal is to integrate an AI service for narrative generation and ensure the coherence of these generated stories and room descriptions. This approach isolates the complexity of narrative AI from puzzle generation, allowing for focused development and early mitigation of risks associated with maintaining logical consistency in AI-driven storytelling through the direct integration of "Narrative Archetypes."

## Objectives and Scope

### In Scope (Epic 2)

*   **Integrate AI Narrative Generation Service (Story 2.1):** Set up API keys, handle API requests/responses for an AI service (Gemini API) to dynamically create story elements, and secure API keys via Flask routes.
*   **Dynamic Room Description Generation (Story 2.2):** Implement logic for the AI to generate unique room descriptions consistent with chosen themes and ongoing narratives.
*   **Implement Narrative Archetypes for Coherence (Story 2.3):** Guide the AI with predefined narrative structures to ensure generated stories remain coherent and logical across playthroughs.
*   **Dynamic Theme and Location Integration (Story 2.4):** Ensure chosen themes and locations influence AI-generated stories and room descriptions, making player customization impactful.

### Out of Scope (for Epic 2)

*   AI-driven puzzle generation (addressed in Epic 3).
*   Dynamic difficulty adjustment (addressed in Epic 4).
*   Complex background processing for slow AI generation (deferred).
*   User authentication (addressed in Epic 5).
*   Load/Save game functionality (addressed in Epic 5).

## System Architecture Alignment

Epic 2 aligns with critical architectural decisions related to AI integration outlined in `docs/architecture.md`:

*   **AI Service Integration:** Utilizes Gemini Pro / Gemini 1.5 Pro for narrative generation.
*   **AI Client Library:** Employs `google-generativeai 0.8.5` for interacting with the Gemini API.
*   **Prompt Management Strategy:** Relies on Structured Prompting with Narrative Archetypes to ensure coherence.
*   **API Pattern for AI interactions:** Flask API Routes will secure AI API keys and provide RESTful endpoints for frontend interaction with AI generation logic.
*   **Performance:** Background processing using Celery with Redis is a "Nice-to-Have" decision, deferred until performance testing indicates a need for slow AI generation.
*   **Error Handling:** Centralized error handling within Flask with user-friendly feedback via toast notifications and retry options for AI failures.

## Detailed Design

### Services and Modules

*   **`services/ai_service.py`**: This new module will encapsulate all interactions with the Gemini API. It will handle prompt engineering, API requests, response parsing, and error handling for narrative generation.
*   **`routes.py`**: New Flask API endpoints will be added to handle requests for dynamic story elements and room descriptions, acting as a secure intermediary between the frontend and `services/ai_service.py`.
*   **`GameSession` in `models.py`**: The `narrative_state` field will be crucial for storing the ongoing narrative context provided to the AI and the generated story elements. `puzzle_state` could also be influenced by the narrative.

### Data Models and Contracts

The `GameSession` model (defined in `models.py`) remains central, with its `narrative_state` (JSON object) and `puzzle_state` (JSON object) fields being actively utilized to store and convey AI-generated content and context.

*   `narrative_state`: A JSON object that will hold the evolving story context for the AI, ensuring consistency.

### APIs and Interfaces

*   `POST /generate_narrative`: An API endpoint to request AI-generated narrative text.
    *   **Request Body:** `{"prompt": "string", "theme": "string", "location": "string", "context": "JSON_object"}`
    *   **Response:** `{"narrative": "string", "updated_narrative_state": "JSON_object"}`
*   `POST /generate_room_description`: An API endpoint to request AI-generated room descriptions.
    *   **Request Body:** `{"theme": "string", "location": "string", "narrative_summary": "string", "room_context": "JSON_object"}`
    *   **Response:** `{"room_description": "string"}`

### Workflows and Sequencing

1.  **AI Service Integration (Story 2.1):** Set up `google-generativeai` client in `services/ai_service.py` and create Flask routes to expose its functionality securely.
2.  **Dynamic Room Description (Story 2.2):** Frontend requests room descriptions via a new Flask endpoint. Backend formulates a prompt using `GameSession` context (theme, narrative state) and `ai_service.py`. AI generates and returns description.
3.  **Narrative Archetype Application (Story 2.3):** During narrative generation, prompts passed to `ai_service.py` will embed logic or instructions based on selected narrative archetypes to guide AI output.
4.  **Theme/Location Influence (Story 2.4):** Player's chosen theme and location are passed as parameters in AI generation prompts from the Flask routes to `ai_service.py`, influencing the generated content.
5.  **Game State Update:** AI-generated content (narrative, room descriptions) is parsed by the backend and used to update the `GameSession.narrative_state` field in the database.

## Non-Functional Requirements

### Performance

*   **Latency:** API responses for state updates (movement, inventory) should ideally be under 200ms for a smooth player experience.
*   **Throughput:** The system should support up to 10 concurrent active game sessions without degradation in response time.
*   **Scalability:** The Flask application will be deployed in a manner that supports horizontal scaling by adding more instances behind a load balancer. Supabase handles database scaling.
*   **AI Response Time:** While initial implementation may be synchronous, potential for high latency from AI API calls necessitates consideration of background processing. Target AI response time for narrative elements should be reasonable for user experience (e.g., within 5-10 seconds for initial draft, faster for incremental updates).

### Security

*   **API Keys:** All sensitive API keys (e.g., Gemini API) will be stored as server-side environment variables and never exposed to the client. Flask API Routes serve as a secure gateway.
*   **Communication:** All client-server communication will utilize HTTPS/SSL.
*   **Data Validation:** All incoming API requests will undergo validation to prevent malformed data.
*   **Prompt Injection:** Implement input sanitization and validation for all user-provided inputs that are used in AI prompts to mitigate prompt injection risks.
*   **Data Privacy:** Ensure no sensitive user data is inadvertently sent to the AI service.

### Reliability/Availability

*   **Uptime:** Target 99.9% uptime for the application API.
*   **Data Durability:** Supabase (PostgreSQL) provides managed backups and replication to ensure data durability.
*   **Error Handling:** Robust error handling in Flask API routes, providing clear error messages for failed operations.
*   **AI Service Dependency:** Application reliability is now dependent on the availability and performance of the Gemini API. Implement robust retry mechanisms and fallback strategies for AI service failures.

### Observability

*   **Logging:** Structured JSON logging will be implemented using Python's `logging` module, capturing `timestamp`, `level`, `message`, `request_id`, and relevant context for all API interactions and state changes. Logs will be output to `stdout` for collection by a centralized logging service.
*   **AI Interaction Logging:** Enhance logging to include details of AI prompts, responses, and any errors from the Gemini API. This will be critical for debugging AI behavior and performance. Log additional context suchs as `prompt_id` or `ai_model_version`.

## Dependencies and Integrations

*   **Python Libraries:** Flask, SQLAlchemy, supabase, python-dotenv, gunicorn, pytest, `google-generativeai`.
*   **External APIs:** Google Gemini API.
*   **Background Processing (Deferred):** Celery with Redis for asynchronous AI calls if needed.
*   **Existing Components:** Relies heavily on the `GameSession` model and database persistence established in Epic 1.

## Acceptance Criteria (Authoritative)

The acceptance criteria for Epic 2 are derived directly from its constituent user stories:

### Story 2.1: Integrate AI Narrative Generation Service
*   **Given** an AI narrative generation service (e.g., Gemini API), **when** a prompt is sent to the service (e.g., "Generate a mysterious story..."), **then** the service returns a coherent narrative text.
*   **And** the application can successfully receive and parse this narrative.

### Story 2.2: Dynamic Room Description Generation
*   **Given** a game with a selected theme and an ongoing narrative, **when** the AI is prompted for a room description, **then** the AI generates a unique description for that room that is consistent with both the theme and the narrative.
*   **And** this description is displayed to the player.

### Story 2.3: Implement Narrative Archetypes for Coherence
*   **Given** a set of predefined narrative archetypes, **when** the AI generates a story, **then** the generated story follows the key structural beats of the selected archetype, while still allowing for creative variation.
*   **And** the story flow feels logical and purposeful to the player.

### Story 2.4: Dynamic Theme and Location Integration
*   **Given** the player selects a theme (e.g., "Space Station") and location (e.g., "Mars Colony"), **when** the AI generates the narrative and room descriptions, **then** the content consistently reflects the chosen theme and location.

## Traceability Mapping

| Acceptance Criteria (AC) | Spec Section(s) | Component(s)/API(s) | Test Idea |
|---|---|---|---|
| **AC 2.1.1** AI service returns narrative | PRD: FR-007, Arch: AI Service Integration | `services/ai_service.py` | Unit test: Mock Gemini API, verify response parsing |
| **AC 2.1.2** App receives/parses narrative | PRD: FR-007, Arch: API Pattern for AI | `routes.py`, `services/ai_service.py` | Integration test: API call to Flask route, verify narrative is stored/processed |
| **AC 2.2.1** AI generates themed room description | PRD: FR-001, Arch: Prompt Management | `services/ai_service.py` | Unit test: Prompt AI with theme/narrative, verify description consistency |
| **AC 2.2.2** Description displayed | PRD: FR-001 | `routes.py`, `templates/` | E2E test: Play game, verify dynamic room descriptions |
| **AC 2.3.1** AI story follows archetypes | PRD: FR-007, Arch: Prompt Management | `services/ai_service.py` | Unit test: Generate story with archetype, verify structure |
| **AC 2.3.2** Story flow logical | PRD: FR-007 | `services/ai_service.py` | Manual/User Acceptance Test: Evaluate generated story for coherence |
| **AC 2.4.1** Content reflects theme/location | PRD: FR-002, Arch: Prompt Management | `services/ai_service.py` | Unit test: Prompt AI with specific theme/location, verify content reflects it |

## Risks, Assumptions, Open Questions

### Risks

*   **AI Coherence:** The primary risk is that AI-generated narratives and room descriptions may lack coherence, logical consistency, or quality, leading to a poor player experience.
    *   *Mitigation:* Extensive prompt engineering, implementation of "Narrative Archetypes," and rigorous testing of AI outputs.
*   **AI API Cost & Rate Limits:** Excessive calls to the Gemini API could incur significant costs or hit rate limits.
    *   *Mitigation:* Implement caching for AI responses, optimize prompt size, and consider background processing for high-latency calls (deferred).
*   **AI Latency:** Slow AI response times could degrade user experience.
    *   *Mitigation:* Asynchronous processing (deferred to Celery/Redis), client-side loading indicators.

### Assumptions

*   **Gemini API Capabilities:** The Gemini API is capable of generating sufficiently coherent and creative narratives and room descriptions based on provided prompts and context.
*   **Structured Prompting Effectiveness:** The defined Structured Prompting Strategy (including narrative archetypes) will be effective in guiding AI generation.
*   **Network Reliability:** Stable internet connection for API calls to Gemini.

### Open Questions

*   **Prompt Engineering Details:** Precise phrasing and structure of prompts for optimal AI output are subject to iteration and refinement.
*   **Handling Unexpected AI Outputs:** Strategies for dealing with truly nonsensical or inappropriate AI responses.
*   **User Feedback on AI Content:** How to gather and integrate player feedback to continuously improve AI-generated content.

## Test Strategy Summary

A multi-layered testing strategy will be employed for Epic 2:

*   **Unit Tests:** Using Pytest to test individual functions in `services/ai_service.py` for API interaction, response parsing, and prompt construction. Mocking the Gemini API will be essential.
*   **Integration Tests:** Using Pytest for Flask API routes in `routes.py` to ensure correct interaction with `services/ai_service.py` and proper updates to `GameSession.narrative_state`.
*   **Manual Testing/Exploratory Testing:** Extensive manual testing will be crucial to evaluate the quality, coherence, and consistency of AI-generated narratives and room descriptions. This will be the primary method for validating Acceptance Criteria related to subjective quality.
*   **Performance Testing (Deferred):** Load testing of AI API endpoints to identify potential bottlenecks and validate the need for background processing.
