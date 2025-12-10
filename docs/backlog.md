# Engineering Backlog

This backlog collects cross-cutting or future action items that emerge from reviews and planning.

Routing guidance:

- Use this file for non-urgent optimizations, refactors, or follow-ups that span multiple stories/epics.
- Must-fix items to ship a story belong in that story’s `Tasks / Subtasks`.
- Same-epic improvements may also be captured under the epic Tech Spec `Post-Review Follow-ups` section.

| Date | Story | Epic | Type | Severity | Owner | Status | Notes |
| ---- | ----- | ---- | ---- | -------- | ----- | ------ | ----- |
| 2025-12-09 | 1.1 | 1 | Bug | High | TBD | Open | AC3: Modify `ai-escape-app/app.py` to return a simple "Hello World" string. [file: `ai-escape-app/app.py`] |
| 2025-12-09 | 1.1 | 1 | Bug | High | TBD | Open | AC3: Update `ai-escape-app/tests/test_app.py`'s `test_index_page` or add new test to assert `b"Hello, World!"`. [file: `ai-escape-app/tests/test_app.py`] |
| 2025-12-09 | 1.1 | 1 | Clarification | Medium | TBD | Open | Clarify whether "Deploy to chosen free-tier service" subtask for AC3 requires actual deployment or just documentation. |
| 2025-12-09 | 1.1 | 1 | Enhancement | Low | TBD | Open | Ensure `.github/workflows/ci.yml` explicitly runs all Python tests (`pytest`). [file: `ai-escape-app/.github/workflows/ci.yml`] |
| 2025-12-10 | 3.1 | 3 | Security | High | TBD | Open | Implement robust input sanitization and escaping for user-provided data in AI prompts. [file: `ai-escape-app/services/ai_service.py` lines: 95-121] |
| 2025-12-10 | 3.1 | 3 | Observability | Medium | TBD | Open | Replace `print()` with structured JSON logging in `ai_service.py` functions. [file: `ai-escape-app/services/ai_service.py` lines: `try-except` blocks] |
| 2025-12-10 | 3.1 | 3 | Observability | Medium | TBD | Open | Implement structured JSON logging for requests/errors in `routes.py::generate_puzzle_route`. [file: `ai-escape-app/routes.py` lines: 331-352] |
| 2025-12-10 | 3.1 | 3 | Refactor | Low | TBD | Open | Consider more granular exception handling in `ai_service.py` functions. |
| 2025-12-10 | 3.1 | 3 | Refactor | Low | TBD | Open | Consider basic internal input validation within `ai_service.py::generate_puzzle` parameters. |
| 2025-12-10 | 3.3 | 3 | Test | Medium | TBD | Open | Add dedicated unit tests for the `verify_puzzle_solvability` function in `ai-escape-app/services/game_logic.py`. [file: `ai-escape-app/tests/test_game_logic.py`] |