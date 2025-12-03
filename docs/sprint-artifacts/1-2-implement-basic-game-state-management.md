# Story 1.2: Implement Basic Game State Management

Status: ready-for-dev

## Story

As a developer,
I want to implement a basic game state management system,
So that we can track the player's progress through the escape room.

## Acceptance Criteria

1. Given a new game is started, when the player moves from "Room 1" to "Room 2", then the game state object is updated to `{'current_room': 'Room 2'}`.
2. And when the player interacts with the "key" in "Room 2", then the game state object is updated to `{'inventory': ['key']}`.

## Tasks / Subtasks

- [ ] AC 1: Define `GameSession` data model using SQLAlchemy.
  - [ ] Subtask: Create `models.py` to define the `GameSession` class with `currentRoom`, `inventory`, `gameHistory`, `narrativeState`, `puzzleState`, `startTime`, `lastUpdated`, `theme`, `location`, `difficulty` fields. [Source: docs/architecture.md#Data-Architecture]
  - [ ] Subtask: Configure SQLAlchemy to connect to Supabase (PostgreSQL). [Source: docs/architecture.md#Data-Persistence]
- [ ] AC 1: Implement basic CRUD operations for `GameSession`.
  - [ ] Subtask: Create function to initialize a new `GameSession` (start game).
  - [ ] Subtask: Create function to retrieve an existing `GameSession`.
  - [ ] Subtask: Create function to update `GameSession` (e.g., `currentRoom`).
- [ ] AC 1: Integrate `GameSession` updates with Flask routes.
  - [ ] Subtask: Create a Flask route for player movement that updates `currentRoom` in `GameSession`. [Source: docs/architecture.md#Game-State-Transition-Flow]
- [ ] AC 2: Extend `GameSession` update function for `inventory` management.
  - [ ] Subtask: Implement logic to add items to `inventory` list within `GameSession`.
  - [ ] Subtask: Implement logic to remove items from `inventory` list within `GameSession`.
- [ ] AC 2: Integrate `inventory` updates with Flask routes.
  - [ ] Subtask: Create a Flask route for player interaction that updates `inventory` in `GameSession`. [Source: docs/architecture.md#Game-State-Transition-Flow]
- [ ] AC 1, 2: Implement unit tests for `GameSession` model definition and CRUD operations.
- [ ] AC 1, 2: Implement integration tests for Flask routes that update `GameSession` fields (`currentRoom`, `inventory`).

## Dev Notes

### Requirements Context Summary

**From Epic 1: Foundational Framework & A Single, Static Escape Room**
-   **Goal:** Build a robust technical foundation and a complete, testable, end-to-end user experience with a single, hard-coded story and puzzle chain.

**From PRD (Product Requirements Document) - FR-002: Player-Driven Customization (Game Setup)**
-   **Relevance:** Game state management is fundamental to enabling player customization features, as player choices need to be tracked and persisted.

**From Architecture Document (`docs/architecture.md`)**
-   **Data Persistence:** Managed and persisted using Supabase (PostgreSQL 16.x), accessed via SQLAlchemy (2.0.44) ORM and the supabase (2.24.0) Python client library.
-   **Core Data Model:** `GameSession` entity will track `id`, `playerId`, `currentRoom`, `inventory`, `gameHistory`, `narrativeState`, `puzzleState`, `startTime`, `lastUpdated`, `theme`, `location`, `difficulty`.
-   **Game State Transition Flow:** Describes how a `GameSession` is created at "Start Game" and updated on "Player Action" and "AI Response & State Change" cycles. This ensures authoritative server-side state management.

### General Technical Notes

-   **Relevant architecture patterns and constraints:**
    *   Game State Management & Persistence using Supabase (PostgreSQL) and SQLAlchemy. [Source: docs/architecture.md#Data-Persistence]
    *   Game State Transition Flow (`GameSession` creation and updates). [Source: docs/architecture.md#Game-State-Transition-Flow]
    *   Flask API Routes for backend interaction. [Source: docs/architecture.md#API-Pattern-for-AI-interactions]
-   **Source tree components to touch:**
    *   `models.py` (for `GameSession` definition)
    *   `services/game_logic.py` (for CRUD operations)
    *   `routes.py` (for Flask endpoints to update game state)
    *   `requirements.txt` (for `SQLAlchemy`, `supabase` client library)
    *   `tests/` (for new unit and integration tests)
-   **Testing standards summary:**
    *   Unit Tests (Pytest with `pytest-mock`) for model and service logic. [Source: docs/architecture.md#Comprehensive-Testing-Strategy]
    *   Integration Tests (Pytest) for Flask routes updating game state. [Source: docs/architecture.md#Comprehensive-Testing-Strategy]

### Learnings from Previous Story

**From Story 1.1: Project Initialization and Deployment Setup (Status: ready-for-dev)**

-   **Initial Project Setup:** Story 1.1 established the foundational Python Flask project structure, including:
    *   Creation of the `ai-escape-app/` directory and Python virtual environment (`venv`).
    *   Basic Flask app structure (`app.py`, `static/`, `templates/`, `config.py`, `instance/`, `models.py`, `routes.py`, `services/`, `tests/`).
    *   Setup of `.env` and `.flaskenv` for environment variables.
    *   Definition of `requirements.txt` with initial dependencies (`Flask`, `python-dotenv`).
    *   Basic CI/CD pipeline configuration (GitHub Actions).
-   **Core Technologies Established:** Python (3.14.1), Flask (3.1.2), Tailwind CSS (4.1.17), Pytest, Black, Flake8.
-   **Relevant Files Created:** `app.py`, `requirements.txt`, `.env`, `.flaskenv`, `.github/workflows/`, initial `tests/`.

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### Structure Alignment Summary

Story 1.1 established the initial Python Flask project structure. This story should align with the structure created in Story 1.1. No dedicated `unified-project-structure.md` document exists. The project structure should adhere to the guidelines provided in the Architecture Document (`docs/architecture.md`).

### References

- [Source: docs/epics.md]
- [Source: docs/architecture.md]
- Cite all technical details with source paths and sections, eg. [Source: docs/<file>.md#Section]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/1-2-implement-basic-game-state-management.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **2025-12-03**: Story created.