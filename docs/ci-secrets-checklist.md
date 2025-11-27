# CI/CD Secrets Checklist

This document lists the secrets required for the CI/CD pipeline to function correctly. Secrets should be configured in the repository's "Settings > Secrets and variables > Actions" page on GitHub.

## Required Secrets

| Secret Name | Description | Used In |
|---|---|---|
| `SLACK_WEBHOOK_URL` | (Optional) The webhook URL for sending Slack notifications on build failures. | `test.yml` (if notifications are enabled) |
| `TEST_USER_PASSWORD` | (Optional) The password for a test user account if required for E2E tests. | Environment variables for tests |
| `TEST_API_KEY` | (Optional) An API key required for tests to interact with a backend service. | Environment variables for tests |

---

## Security Best Practices

-   **NEVER** hardcode secrets in the source code or CI configuration files.
-   Use the secrets management system provided by your CI platform (e.g., GitHub Actions Secrets).
-   Limit access to secrets.
-   Rotate secrets regularly.
