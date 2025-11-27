# Test Suite Documentation

## Setup Instructions
1.  **Install Dependencies**: Make sure you have Node.js (v20.11.0 recommended, see `.nvmrc`) installed.
    Run `npm install` in the project root to install Playwright and other necessary test dependencies.

## Running Tests
-   **Run all E2E tests**:
    `npm run test:e2e`
-   **Run tests with UI mode (Playwright UI)**:
    `npm run test:e2e -- --ui`
-   **Run tests in headed mode (browser visible)**:
    `npm run test:e2e -- --headed`
-   **Debug tests (with Playwright Inspector)**:
    `npm run test:e2e -- --debug`
-   **Show HTML test report after a run**:
    `npx playwright show-report test-results/html`

## Architecture Overview
This test suite is built using Playwright and follows a robust architecture:

-   **Fixtures**: Custom fixtures (e.g., `userFactory`) are defined in `tests/support/fixtures/index.ts`. They allow for setup and teardown of test-specific resources (like creating and cleaning up test users).
-   **Data Factories**: Located in `tests/support/fixtures/factories/`, these factories use `faker` to generate realistic test data and handle API calls for seeding data and cleaning up.
-   **Page Object Models (Optional)**: While not strictly enforced for all tests, consider using page objects in `tests/support/page-objects/` for complex pages to improve maintainability and readability.

## Best Practices
-   **Selector Strategy**: Always use `data-testid` attributes for selecting UI elements in your tests to make them resilient to DOM changes.
-   **Test Isolation**: Each test should be isolated and not depend on the state of previous tests. Use fixtures for setting up and tearing down test data.
-   **Explicit Assertions**: Use clear and explicit assertions (`expect`) to verify expected behavior.
-   **Cleanup**: Ensure all test data created during a test is properly cleaned up (e.g., via `userFactory.cleanup()`).

## CI Integration
Tests are configured to run in a Continuous Integration (CI) pipeline:
-   `fullyParallel`: Tests run in parallel for faster execution.
-   `retries`: Tests are retried 2 times on CI to mitigate flakiness.
-   `reporter`: HTML and JUnit XML reports are generated (`test-results/html`, `test-results/junit.xml`).
-   **Failure Artifacts**: Screenshots, videos, and traces are retained only on failure to aid debugging and reduce storage.

## Knowledge Base References
-   **Fixture architecture pattern**: Pure function → fixture → `mergeTests` composition with auto-cleanup.
-   **Data factories**: Faker-based factories with overrides, nested factories, API seeding, auto-cleanup.
-   **Network-first testing safeguards**: Intercept before navigate, HAR capture, deterministic waiting.
-   **Playwright-specific configuration**: Environment-based, timeout standards, artifact output, parallelization, project config.
-   **Test quality**: Deterministic, isolated with cleanup, explicit assertions, length/time limits.
