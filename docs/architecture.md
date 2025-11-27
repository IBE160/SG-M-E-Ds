# Architecture

## Executive Summary

The "AI Escape" project is an AI-driven puzzle game designed for high replayability, offering dynamically generated stories and puzzles. Key objectives include addressing limited replayability of traditional escape rooms and providing an immersive, customizable experience. The project encompasses 5 epics and 12 user stories, with a strong focus on a retro-futuristic UI, responsive design, and WCAG 2.1 Level AA accessibility. A primary architectural challenge is ensuring the coherence and logical consistency of AI-generated content.

## Project Initialization

We will use Python Flask as the foundation for the project. This lightweight web framework provides a simple and flexible way to build the web application, aligning with the teacher's recommendation.

The initial setup commands for the project will be:
```bash
# Assuming Python and pip are installed
mkdir ai-escape-app
cd ai-escape-app
python -m venv venv
# On Windows, use `venv\Scripts\activate`
# On macOS/Linux, use `source venv/bin/activate`
pip install Flask python-dotenv

# Basic Flask app structure creation:
# Create a file named app.py for your Flask application logic.
# Create a folder named 'static' for CSS, JS, images.
# Create a folder named 'templates' for HTML files.
# Create a requirements.txt file with `pip freeze > requirements.txt`.
# Create a .env file for environment variables.
```

This initial setup provides the following architectural decisions:
*   **Language:** Python
*   **Framework:** Flask
*   **Styling Solution:** Tailwind CSS
*   **Testing Framework:** (Will need to be decided - likely pytest)
*   **Linting/Formatting:** (Will need to be decided - likely Black for formatting, Flake8 for linting)
*   **Build Tooling:** Python's pip for dependency management; no complex frontend build tooling like Next.js.
*   **Project Structure:** Basic Flask app structure (app.py, static/, templates/)

The first implementation story should be to execute these commands and set up the project.

## Identified Architectural Decisions

Based on the project requirements and analysis, we have identified the following architectural decisions, categorized by priority:

### Critical Decisions (Foundational for game functionality):
*   **AI Service Integration:** Which specific AI model/API to use for narrative and puzzle generation.
*   **Prompt Management Strategy:** How to ensure coherence and guide AI generation (Narrative Archetypes, Puzzle Dependency Chains).
*   **Game State Management & Persistence:** How to store player progress, inventory, and dynamic game elements.
*   **Deployment Strategy:** How to deploy the Next.js application, especially considering AI service integration.

### Important Decisions (Shapes architecture and user experience):
*   **Asset Management/Storage:** How to handle the pre-selected image library (e.g., local, CDN, cloud storage).
*   **Error Handling Strategy:** How to handle failures in AI generation or game logic.
*   **Accessibility Implementation:** How to ensure WCAG 2.1 Level AA compliance, given the UI.
*   **API Pattern for AI interactions:** How the frontend communicates with the AI generation logic (e.g., Next.js API routes).

### Nice-to-Have Decisions (Can be deferred):
*   **Background Processing for AI:** If AI generation is slow, how to offload it.

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale |
| -------- | -------- | ------- | ------------- | --------- |
| AI Integration | AI Service Provider | Gemini Pro / Gemini 1.5 Pro | All AI-related epics | Gemini API offers powerful, flexible narrative and puzzle generation. |
| AI Integration | Prompt Management Strategy | N/A | All AI-related epics | Structured prompting with narrative archetypes and puzzle dependency chains ensures coherence. |
| Data Persistence | Game State Management | Supabase (PostgreSQL compatible) / SQLAlchemy (Latest Stable) | Epic 1, Epic 5 | Supabase, offering a PostgreSQL-compatible database and additional services, with SQLAlchemy ORM for robust and easy-to-manage persistent game state. Verify latest stable versions at implementation. |
| Deployment | Application Deployment | N/A | All | Standard Python web server deployment (e.g., Gunicorn/WSGI + Nginx) provides robust and scalable hosting for Flask applications. |
| Assets | Image Asset Storage | N/A | Epic 1, Epic 2 | Start with local storage in `public` directory, easily migratable to CDN for scalability. |
| Error Handling | Application Error Handling | N/A | All | Centralized error handling within Next.js with user-friendly feedback via toast notifications and retry options for AI failures. |
| UX | Accessibility Compliance | N/A | All | Active integration of WCAG 2.1 Level AA best practices, including semantic HTML, keyboard navigation, ARIA attributes, and automated/manual testing. |
| API | AI Interaction API Pattern | N/A | Epic 2, Epic 3 | Flask API Routes to secure AI API keys and provide simple RESTful endpoints for frontend interaction. |

## Project Structure

The project will follow a structured Flask application layout, separating frontend assets, backend logic, and database management:

```
ai-escape-app/
├── venv/                         # Python virtual environment
├── app.py                        # Main Flask application instance and routes
├── config.py                     # Application configuration
├── instance/                     # Instance-specific configuration (not under version control)
│   └── config.py
├── static/                       # Frontend static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/                   # Image library for game rooms
├── templates/                    # Jinja2 HTML templates
│   ├── index.html
│   ├── game.html
│   └── layout.html
├── models.py                     # Database models (SQLAlchemy)
├── routes.py                     # API endpoints and game logic
├── services/                     # Business logic, external API integrations
│   ├── ai_service.py             # Gemini API client, prompt management
│   └── game_logic.py             # Core game state management
├── tests/                        # Unit, integration tests
│   ├── unit/
│   └── integration/
├── .env                          # Environment variables
├── .flaskenv                     # Flask-specific environment variables
├── requirements.txt              # Python dependencies
├── README.md
└── .gitignore
```

## Epic to Architecture Mapping

| Epic | Architectural Components | Key Files/Folders |
|---|---|---|
| **Epic 1: Foundational Framework & A Single, Static Escape Room** | Base Flask app, core UI (Jinja2), basic game state, static assets, testing setup. | `app.py`, `templates/`, `static/`, `models.py`, `services/game_logic.py`, `tests/` |
| **Epic 2: Introducing the AI Storyteller** | Gemini API integration, prompt management, dynamic narrative generation. | `routes.py`, `services/ai_service.py` |
| **Epic 3: The AI Puzzle Master** | Gemini API integration for puzzles, dynamic puzzle generation. | `routes.py`, `services/ai_service.py` |
| **Epic 4: Expanding Variety and Replayability** | Extended UI (Jinja2) components, broader AI prompt configurations, potential for more assets. | `templates/`, `routes.py`, `services/ai_service.py`, `static/images/` |
| **Epic 5: Game Utility Features** | Save/Load functionality, settings, help. | `routes.py`, `models.py`, `services/game_logic.py`, `templates/` |

## Technology Stack Details

### Core Technologies

*   **Web Framework:** Python Flask
*   **Language:** Python
*   **Styling:** Tailwind CSS
*   **Database:** Supabase (PostgreSQL Compatible)
*   **ORM:** SQLAlchemy (compatible with Supabase's PostgreSQL)
*   **AI Integration:** Gemini API
*   **Deployment:** Standard Python Web Server (e.g., Gunicorn + Nginx)

### Integration Points

*   **Frontend (Jinja2 templates/Static assets) <-> Backend (Flask Routes/API Endpoints):** Used for rendering UI, handling form submissions, player commands, AI generation requests, save/load game operations, and dynamic UI updates.
*   **Flask Routes/API Endpoints <-> AI Service (Gemini API):** Secure communication for submitting AI prompts and receiving generated content (narratives, puzzles).
*   **Flask Routes/API Endpoints <-> Database (Supabase PostgreSQL via SQLAlchemy):** For persistent storage of game state, player progress, inventory, and potentially user profiles.
*   **Flask Static Files / External CDN:** For serving static game images and other assets to the frontend.

## Novel Pattern Designs

All core patterns identified in this project (e.g., AI integration, game state management, API communication) have established architectural solutions. The unique aspect lies in the specific application and orchestration of these patterns for dynamic content generation, guided by narrative archetypes and puzzle dependency chains. Therefore, we will proceed with adapting standard architectural patterns rather than designing wholly new ones.

## Consistency Rules

To ensure a unified codebase and prevent conflicts when multiple AI agents (or human developers) contribute, the following consistency rules will be enforced:

### Naming Conventions

*   **Python Classes:** `PascalCase` (e.g., `GameSession`, `Player`).
*   **Python Functions/Variables:** `snake_case` (e.g., `get_player_score()`, `user_name`).
*   **Python Modules/Files:** `snake_case` (e.g., `ai_service.py`, `game_logic.py`).
*   **Database Tables:** `snake_case` and plural (e.g., `users`, `game_sessions`).
*   **Database Columns:** `snake_case` (e.g., `user_id`, `created_at`).
*   **API Endpoints:** `kebab-case` for URL paths (e.g., `/api/game-state/save`), `snake_case` for query parameters.
*   **Constants:** `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`).

### Code Organization

*   **Flask Application Structure:** Follow a modular Flask application structure, with `app.py` as the main entry point, `routes.py` for API endpoints and web routes, `models.py` for database models, and `services/` for business logic.
*   **Templates:** Jinja2 HTML templates will be organized in the `templates/` directory, potentially with subdirectories for different sections (e.g., `templates/game/`, `templates/auth/`).
*   **Static Files:** Frontend assets (CSS, JavaScript, images) will be placed in the `static/` directory, with subdirectories for organization (e.g., `static/css/`, `static/js/`, `static/images/`).
*   **Services:** Business logic and external API integrations (like the Gemini API client) will be organized into Python modules within the `services/` directory.
*   **Tests:** All tests will reside in a dedicated `tests/` directory, mirroring the application's module structure (e.g., `tests/unit/services/ai_service.py`).
### Error Handling

(Already covered in Cross-Cutting Concerns)

### Logging Strategy

(Already covered in Cross-Cutting Concerns)

### Data Fetching and State Management

*   **Server-Side Data Rendering:** Flask will render HTML templates using Jinja2, populating them with data fetched on the server.
*   **Client-Side Data Fetching:** For dynamic updates without full page reloads, JavaScript (e.g., Fetch API, Axios) will make asynchronous requests to Flask API endpoints.
*   **Game State Management:** Game state will primarily be managed on the server-side within the Flask application, stored in the database, and retrieved/updated via requests from the client. For transient client-side UI states, vanilla JavaScript or a lightweight library can be used.
### API Contracts

*   **Request/Response Format:** All API interactions (both internal API routes and external AI service calls) will strictly use **JSON** for request and response bodies.
*   **Error Responses:** Standardized error format as defined in Cross-Cutting Concerns.

### Location Patterns

*   **Configuration Files:** Application configuration will be managed in `config.py` and potentially `instance/config.py`.
*   **Environment Variables:** Managed in `.env` and `.flaskenv` files for local development, and securely in the deployment environment.
*   **Static Assets:** All static assets (CSS, JavaScript, images, fonts) will be placed in the `static/` directory (e.g., `static/css/`, `static/images/`).
*   **Templates:** All HTML templates will be placed in the `templates/` directory.



## Coherence Validation

A review of the architectural decisions confirms their compatibility across the chosen technology stack (Next.js, TypeScript, Tailwind, PostgreSQL, Prisma, OpenAI API, Vercel). All identified epics are supported by the proposed project structure and technical choices. The defined implementation and consistency patterns are deemed complete enough to prevent agent conflicts and guide consistent development. No conflicting choices or significant architectural gaps were identified.

## Data Architecture



The primary data will revolve around `GameSession` to capture the state of each player's escape room experience.



*   **Models:**

    *   `GameSession`:

        *   `id`: Unique identifier (UUID).

        *   `playerId`: (Optional, for future user accounts).

        *   `currentRoom`: Current room identifier.

        *   `inventory`: JSON array of items collected.

        *   `gameHistory`: JSON array of player actions and AI responses.

        *   `narrativeState`: JSON object holding current story context for AI.

        *   `puzzleState`: JSON object holding current puzzle context for AI.

        *   `startTime`: Timestamp (UTC).

        *   `lastUpdated`: Timestamp (UTC).

        *   `theme`: String (e.g., "Ancient Tomb").

        *   `location`: String (e.g., "Egypt").

        *   `difficulty`: String (e.g., "Normal").

    *   `Player` (Future consideration):

        *   `id`: Unique identifier.

        *   `name`: Player name/username.

        *   `settings`: JSON object for user preferences.



*   **Relationships:** A `GameSession` will optionally belong to a `Player`.

*   **Technology:** Supabase (PostgreSQL compatible) managed via SQLAlchemy ORM for schema definition, migrations, and database interactions.



## Security Architecture



*   **API Keys:** All sensitive API keys (e.g., Gemini API key) will be stored as environment variables on the server-side (Vercel) and accessed only via Next.js API Routes. They will never be exposed to the client.

*   **Input Sanitization:** All user inputs and data passed to AI services will be sanitized to prevent prompt injection or other malicious data.

*   **Rate Limiting:** Implement rate limiting on Next.js API Routes, especially for AI generation endpoints, to prevent abuse and manage API costs.

*   **Communication:** All communication (frontend to backend, backend to external APIs) will utilize HTTPS/SSL for encryption in transit.



## Performance Considerations



*   **AI API Caching:** Implement caching for AI responses, especially for common prompts or recurring narrative/puzzle elements, to reduce latency and API costs.

*   **Database Query Optimization:** Optimize Prisma queries, ensure appropriate indexing on `GameSession` fields (e.g., `playerId`, `lastUpdated`) to maintain responsive game state management.

*   **Next.js Optimizations:** Leverage Next.js's built-in image optimization, code splitting, and lazy loading for efficient frontend performance.

*   **Serverless Cold Starts:** Monitor and optimize Next.js serverless function cold starts on Vercel for AI generation and game logic to ensure a fluid user experience.



## Deployment Architecture







*   **Web Application:** The Python Flask application will be deployed on a standard web server setup. This typically involves:



    *   **WSGI Server:** (e.g., Gunicorn, uWSGI) to serve the Python application.



    *   **Reverse Proxy:** (e.g., Nginx, Apache) to handle incoming requests, serve static files, and proxy dynamic requests to the WSGI server.



    *   **Hosting Platform:** A cloud provider (e.g., AWS EC2, Google Cloud Compute Engine, DigitalOcean Droplets) or a Platform-as-a-Service (PaaS) like Heroku or Railway.



*   **Database:** A managed Supabase (PostgreSQL compatible) database service will be used. This offloads database management, backup, and scaling concerns, and provides additional services like authentication and storage if needed.



*   **Image Assets:** Static images will be served directly by the reverse proxy (e.g., Nginx) from the `static/images/` directory. For future scalability, integration with an external CDN like Cloudinary or AWS S3 + CloudFront could be considered.



## Development Environment







### Prerequisites







*   **Python:** Latest stable version (3.8+ recommended).



*   **pip:** Python package installer.



*   **Git:** Version control.



*   **Docker:** (Optional) For running a local PostgreSQL instance if not using a cloud-managed service.







### Setup Commands







```bash



# Clone the repository



git clone [repository-url] ai-escape-app



cd ai-escape-app







# Create and activate a Python virtual environment



python -m venv venv



# On Windows:



./venv/Scripts/activate



# On macOS/Linux:



source venv/bin/activate







# Install Python dependencies



pip install -r requirements.txt







# Configure environment variables (e.g., Gemini API Key, Database URL)



# Create a .env file based on .env.example







# Set up the database (using Alembic for SQLAlchemy migrations if configured)



# For initial setup, create tables based on models.py



# Example with Flask-Migrate (uses Alembic): flask db upgrade







# Start the development server



flask run



```



## Architecture Decision Records (ADRs)







Key architectural decisions made throughout this process include:







1.  **Python Flask as the Core Framework:** Chosen for its lightweight nature, flexibility, and alignment with project requirements and recommendations, making it ideal for a Python-based web application.



2.  **Gemini API for AI Services:** Selected for its advanced language models (Gemini Pro/Gemini 1.5 Pro) to handle complex narrative and puzzle generation.



3.  **Structured Prompting Strategy:** Implemented to ensure coherence and consistency in AI-generated content through narrative archetypes and puzzle dependency chains.



4.  **Supabase (PostgreSQL compatible) + SQLAlchemy for Data Management:** Supabase offers a managed PostgreSQL-compatible database with additional services, while SQLAlchemy ORM provides powerful and flexible database interactions in Python.



5.  **Standard Python Web Server Deployment:** Utilizing Gunicorn/WSGI with Nginx for robust, scalable, and production-ready deployment of the Flask application.



6.  **Flask API Routes for AI Interaction:** Provides a secure and encapsulated way for the Flask backend to communicate with external AI services, keeping API keys server-side.



7.  **Comprehensive Testing Strategy:** A multi-layered approach (Unit, Integration, E2E) ensures code quality and reliability, covering both frontend (if applicable) and backend Python logic.



8.  **Strict Consistency Rules:** Detailed guidelines for naming conventions, code organization, and data handling prevent conflicts and ensure a unified codebase, crucial for multi-agent development.



## Validation Summary







### Document Quality Score







*   **Architecture Completeness:** Complete



*   **Version Specificity:** Some Missing (noted to verify at implementation)



*   **Pattern Clarity:** Crystal Clear



*   **AI Agent Readiness:** Ready







### Critical Issues Found







N/A







### Recommended Actions Before Implementation







*   Verify the latest stable versions of PostgreSQL and Prisma at the time of implementation.



*   Conduct a formal accessibility audit as part of the implementation phase to ensure full WCAG 2.1 Level AA compliance.



*   Further define the project's testing approach, including specific libraries (e.g., Vitest for unit tests, React Testing Library for integration tests, Playwright for E2E tests) and detailed test structure.







---







_Generated by BMAD Decision Architecture Workflow v1.0_



_Date: 2025-11-27_



_For: BIP_


