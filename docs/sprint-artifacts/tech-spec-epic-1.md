# Epic Technical Specification: Foundational Framework & A Single, Static Escape Room

Date: 2025-12-03
Author: BIP
Epic ID: 1
Status: Draft

---

## Overview

This Epic focuses on establishing the core technical foundation and delivering a complete, testable, end-to-end user experience within the "AI Escape" game. The primary goal is to build a single, hard-coded escape room with predefined stories and puzzles. This strategic approach ensures a stable and enjoyable game experience before integrating complex AI-driven content generation, providing a crucial "golden path" for validation and integration of the interaction model and narrative flow.

## Objectives and Scope

### In Scope (Epic 1)

*   **Project Initialization and Deployment Setup (Story 1.1):** Establish the basic Python Flask project structure, create a virtual environment, set up `requirements.txt`, generate an initial `README.md`, implement a minimal "Hello World" Flask application, and configure basic CI/CD for deployment readiness.
*   **Basic Game State Management (Story 1.2):** Implement a foundational system to track player progress, including current room, inventory, and other dynamic game elements using SQLAlchemy and a PostgreSQL-compatible database.
*   **Static, Hard-coded Escape Room (Story 1.3):** Create a playable sequence of 3 rooms with 2-3 distinct, hard-coded puzzles to validate core mechanics and user flow.
*   **Core Interaction Model (Story 1.4):** Develop a hybrid interaction model that allows players to navigate rooms and interact with objects through contextual text-based options and a "go back" function.
*   **Basic Visuals for Rooms (Story 1.5):** Display static background images for each room to enhance immersion, utilizing local storage for assets.

### Out of Scope (for Epic 1)

*   AI-driven narrative or puzzle generation (focus is on static content).
*   Dynamic difficulty adjustment.
*   Advanced UI elements beyond basic Flask templates and Tailwind CSS.
*   Background music, sound effects, or complex animations.
*   User authentication (will be addressed in Epic 5).
*   Load/Save game functionality (will be addressed in Epic 5).

## System Architecture Alignment

Epic 1 aligns with the foundational architectural decisions outlined in `docs/architecture.md`:

*   **Core Technologies:** Leverages Python (3.14.1) and Flask (3.1.2) as the web framework. Styling will use Tailwind CSS (4.1.17).
*   **Data Management:** Game state will be managed and persisted using Supabase (PostgreSQL 16.x) via SQLAlchemy (2.0.44) ORM and the `supabase` Python client library (2.24.0).
*   **Deployment:** Utilizes a standard Python web server deployment approach, including basic CI/CD via GitHub Actions.
*   **Asset Management:** Static images will be stored locally in the `static/images/` directory.
*   **Testing:** Adheres to the comprehensive testing strategy, employing Pytest for unit and integration tests, and Playwright for E2E tests.
*   **Project Structure:** Follows the modular Flask application layout, organizing `app.py`, `templates/`, `static/`, `models.py`, `routes.py`, and `services/game_logic.py`.

## Detailed Design

### Services and Modules

*   **`app.py`**: Main Flask application instance, responsible for creating and configuring the app, initializing database connection, and registering blueprints.
*   **`models.py`**: Defines the `GameSession` SQLAlchemy data model, tracking player progress, current room, inventory, and other game-related states.
*   **`services/game_logic.py`**: Contains core business logic for game state management, including CRUD operations for `GameSession` (create, retrieve, update, delete) and specific functions for player actions like updating inventory or changing rooms.
*   **`routes.py`**: Defines API endpoints for game interactions (e.g., `start_game`, `move_player`, `handle_inventory`), communicating with `services/game_logic.py` and returning JSON responses.
*   **`static/`**: Houses static frontend assets including `images/` for room backgrounds.
*   **`templates/`**: Contains Jinja2 HTML templates for rendering the basic game UI.

### Data Models and Contracts

The primary data model is `GameSession` (defined in `models.py`):

```python
class GameSession(Base):
    __tablename__ = 'game_sessions'
    id = Column(Integer, primary_key=True)
    player_id = Column(String, nullable=False)
    current_room = Column(String, default="start_room")
    inventory = Column(JSON, default=[]) # Stores a list of strings
    game_history = Column(JSON, default=[]) # Stores dict for AI context
    narrative_state = Column(JSON, default={}) # Stores dict for AI context
    puzzle_state = Column(JSON, default={}) # Stores dict for AI puzzle context
    start_time = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    theme = Column(String, default="mystery")
    location = Column(String, default="mansion")
    difficulty = Column(String, default="medium")
```
Contracts for `inventory`, `game_history`, `narrative_state`, `puzzle_state` are JSON types, allowing flexible schema within a NoSQL-like pattern over PostgreSQL.

### APIs and Interfaces

*   `POST /start_game`: Initializes a new game session.
    *   **Request Body:** `{"player_id": "string", "theme": "string", "location": "string", "difficulty": "string"}`
    *   **Response:** `{"id": int, "player_id": "string", "current_room": "string", "inventory": list}`
*   `GET /game_session/<int:session_id>`: Retrieves a specific game session.
    *   **Response:** `GameSession` object serialized to JSON.
*   `POST /game_session/<int:session_id>/move`: Updates the player's current room.
    *   **Request Body:** `{"new_room": "string"}`
    *   **Response:** `{"id": int, "current_room": "string"}`
*   `POST /game_session/<int:session_id>/inventory`: Adds or removes an item from inventory.
    *   **Request Body:** `{"item": "string", "action": "add"|"remove"}`
    *   **Response:** `{"id": int, "inventory": list}`

### Workflows and Sequencing

1.  **Project Setup (Story 1.1):** Local environment setup, basic Flask app, `requirements.txt`, `README.md`, CI/CD.
2.  **Game State Initialization (Story 1.2):** Player initiates a new game (`POST /start_game`), `GameSession` created in DB, initial room/state returned.
3.  **Player Movement (Story 1.4):** Player selects movement option, client calls `POST /game_session/<id>/move`, backend updates `current_room` in `GameSession`.
4.  **Player Interaction (Story 1.4):** Player interacts with object (e.g., picks up item), client calls `POST /game_session/<id>/inventory`, backend updates `inventory`.
5.  **Room Rendering (Story 1.5):** After state update, client receives updated game state, renders corresponding background image from `static/images/` and new interaction options.

## Non-Functional Requirements

### Performance

*   **Latency:** API responses for state updates (movement, inventory) should ideally be under 200ms for a smooth player experience.
*   **Throughput:** The system should support up to 10 concurrent active game sessions without degradation in response time.
*   **Scalability:** The Flask application will be deployed in a manner that supports horizontal scaling by adding more instances behind a load balancer. Supabase handles database scaling.

### Security

*   **API Keys:** All sensitive API keys (e.g., Gemini API, if used in future epics) will be stored as server-side environment variables and never exposed to the client.
*   **Communication:** All client-server communication will utilize HTTPS/SSL.
*   **Data Validation:** All incoming API requests will undergo validation to prevent malformed data.

### Reliability/Availability

*   **Uptime:** Target 99.9% uptime for the application API.
*   **Data Durability:** Supabase (PostgreSQL) provides managed backups and replication to ensure data durability.
*   **Error Handling:** Robust error handling in Flask API routes, providing clear error messages for failed operations.

### Observability

*   **Logging:** Structured JSON logging will be implemented using Python's `logging` module, capturing `timestamp`, `level`, `message`, `request_id`, and relevant context for all API interactions and state changes. Logs will be output to `stdout` for collection by a centralized logging service.

## Dependencies and Integrations

*   **Python Libraries:** Flask, SQLAlchemy, supabase, python-dotenv, gunicorn, pytest.
*   **Database:** Supabase (PostgreSQL 16.x).
*   **Frontend:** Jinja2 for templating, basic JavaScript for client-side interactivity, Tailwind CSS for styling.
*   **Development Tools:** Git, Python virtual environments, Pip.
*   **CI/CD:** GitHub Actions for automated build and test.

## Acceptance Criteria (Authoritative)

The acceptance criteria for Epic 1 are derived directly from its constituent user stories:

### Story 1.1: Project Initialization and Deployment Setup
*   **Given** a new project, **when** the initialization script is run, **then** a standard project structure (`src`, `docs`, `tests`) is created.
*   **And** a basic `README.md` is generated with setup instructions.
*   **And** a simple "Hello World" version of the application can be automatically built and deployed to a free-tier cloud service.

### Story 1.2: Implement Basic Game State Management
*   **Given** a new game is started, **when** the player moves from "Room 1" to "Room 2", **then** the game state object is updated to `{'current_room': 'Room 2'}`.
*   **And** when the player interacts with the "key" in "Room 2", **then** the game state object is updated to `{'inventory': ['key']}`.

### Story 1.3: Create a Static, Hard-coded Escape Room
*   **Given** the game has started, **when** the player navigates through the rooms, **then** they encounter a 3-room sequence with at least two distinct puzzles.
*   **And** solving the final puzzle in Room 3 triggers a "You escaped!" message.

### Story 1.4: Implement the Core Interaction Model
*   **Given** the player is in a room with a "locked door" and a "note", **when** the game presents interaction options, **then** the options are displayed as a numbered list.
*   **And** the player can select an option by entering the corresponding number.

### Story 1.5: Display Basic Visuals for Rooms
*   **Given** the player enters a new room, **when** the room description is displayed, **then** a corresponding background image for that room is also displayed.

## Traceability Mapping

| Acceptance Criteria (AC) | Spec Section(s) | Component(s)/API(s) | Test Idea |
|---|---|---|---|
| **AC 1.1.1** Project structure created | Architecture: Project Structure | File System, `ai-escape-app/` | Unit test: Check directory/file existence |
| **AC 1.1.2** `README.md` generated | Architecture: Project Initialization | `ai-escape-app/README.md` | Unit test: Check `README.md` content |
| **AC 1.1.3** "Hello World" deployed | Architecture: Deployment Strategy | `app.py`, CI/CD | Integration/E2E: Deploy "Hello World" to Render, verify access |
| **AC 1.2.1** `current_room` updated | Data Architecture: `GameSession` | `services/game_logic.py`, `routes.py` (`/move`) | Integration test: Simulate player movement API call, verify DB update |
| **AC 1.2.2** `inventory` updated | Data Architecture: `GameSession` | `services/game_logic.py`, `routes.py` (`/inventory`) | Integration test: Simulate inventory update API call, verify DB update |
| **AC 1.3.1** 3-room sequence, 2 puzzles | Epic 1: Story 1.3 | `routes.py`, `services/game_logic.py` | E2E test: Play through static game, verify rooms/puzzles |
| **AC 1.3.2** "You escaped!" message | Epic 1: Story 1.3 | `routes.py`, `templates/` | E2E test: Complete game, verify message |
| **AC 1.4.1** Contextual options displayed | Epic 1: Story 1.4 | `templates/`, `routes.py` | E2E test: Verify UI displays options based on context |
| **AC 1.4.2** Player selects option | Epic 1: Story 1.4 | `routes.py` | E2E test: Simulate player input, verify game response |
| **AC 1.5.1** Background image displayed | Epic 1: Story 1.5 | `templates/`, `static/images/` | E2E test: Verify images load correctly for each room |

## Risks, Assumptions, Open Questions

### Risks

*   **AI Coherence (Deferred):** While Epic 1 uses hard-coded content, future integration of AI (Epics 2, 3) carries the risk of incoherent or nonsensical narratives/puzzles. *Mitigation for Epic 1:* Not applicable as content is static.
*   **Database Connectivity:** Ensuring reliable connection to Supabase (PostgreSQL) in both development and production environments. *Mitigation:* Use environment variables for connection strings, robust error handling in `app.py` and `services/game_logic.py`.

### Assumptions

*   **Technology Stack Stability:** Python, Flask, SQLAlchemy, Supabase, Tailwind CSS will remain stable and well-supported throughout the MVP development.
*   **Local Development Environment:** Developers will have Python 3.14.1, pip, and Git installed.
*   **Supabase Access:** Developers will have necessary credentials to access Supabase databases for development.

### Open Questions

*   **Detailed UI/UX for specific interactions:** While core interaction model is defined, precise button layouts, animation timings, etc., are left for UI/UX design. (Handled by a separate UX Design Specification).
*   **Error Handling for AI (Deferred):** Specifics of how AI generation failures are communicated and retried (beyond basic message/retry button) are open.

## Test Strategy Summary

A multi-layered testing strategy will be employed for Epic 1:

*   **Unit Tests:** Using Pytest with `pytest-mock` (if needed) for individual functions and classes in `services/game_logic.py` and `models.py`. This includes testing CRUD operations and data model integrity.
*   **Integration Tests:** Using Pytest for Flask API routes in `routes.py` to ensure correct interaction with `services/game_logic.py` and the in-memory SQLite database. This will cover `start_game`, `move`, and `inventory` endpoints.
*   **End-to-End (E2E) Tests:** Using Playwright (or similar) to simulate full user flows through the static escape room, verifying UI rendering, interaction options, and game progression (Stories 1.3, 1.4, 1.5). These will be developed after core UI is established.
*   **Manual Testing:** Comprehensive manual testing will be conducted to verify the overall player experience and puzzle logic.
