# CI/CD Pipeline Guide

This document provides an overview of the Continuous Integration and Continuous Deployment (CI/CD) pipeline for this project.

## Pipeline Overview

The CI pipeline is defined in `.github/workflows/test.yml` and is designed to ensure code quality, catch regressions, and detect flaky tests.

### Pipeline Stages

1.  **Test**: Runs the full Playwright test suite. The tests are parallelized across 4 jobs (shards) to ensure fast execution.
2.  **Burn-in**: After the `test` stage succeeds on a pull request, this stage runs the entire test suite 10 times in a loop. Its purpose is to detect non-deterministic or "flaky" tests that might pass sometimes and fail other times. A single failure in this loop will fail the stage.

### Triggers

The pipeline is triggered on:
-   Any `push` to the `main` branch.
-   Any `pull_request` targeting the `main` branch.

## How to Run Locally

You can simulate the CI pipeline locally to debug issues before pushing code.

```bash
./scripts/ci-local.sh
```
This script runs the test suite and a reduced burn-in loop (3 iterations).

## Debugging Failed CI Runs

When a CI job fails, you can find detailed information in the "Actions" tab of the GitHub repository.

1.  **Test Failures**: For failures in the `Test` stage, download the `test-results` artifact for the failed shard. This artifact contains:
    *   A full HTML report.
    *   Screenshots and videos of the failed tests.
    *   A Playwright trace file (`trace.zip`), which provides an exhaustive, step-by-step view of the test execution.

2.  **Burn-in Failures**: Failures in this stage indicate a flaky test. Download the `burn-in-failures` artifact to investigate.

## Secrets and Environment Variables

The CI pipeline relies on secrets for sensitive data (e.g., API keys, notification webhooks). These are configured in the repository's "Settings > Secrets and variables > Actions" page. For a full list of required secrets, see `docs/ci-secrets-checklist.md`.
