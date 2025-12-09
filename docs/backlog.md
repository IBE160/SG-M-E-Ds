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