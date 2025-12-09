import pytest
from playwright.sync_api import Page, expect, Browser
import re
import time

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_browser(browser: Browser):
    yield

def test_help_system_flow(page: Page):
    # 1. Start a new game to get to the game page
    page.goto(BASE_URL)
    page.locator("button.option-btn.large[data-mode='design-your-own']").click()
    page.locator("#theme-options .option-btn").first.click()
    page.locator("#setup-step-theme button.action-btn[data-action='next']").click()
    page.locator("#location-options .option-btn").first.click()
    page.locator("#setup-step-location button.action-btn[data-action='next']").click()
    page.locator("#difficulty-options .option-btn").first.click()
    page.locator("#setup-step-difficulty button.action-btn[data-action='start']").click()

    # Verify redirection to /game/<session_id>
    expect(page).to_have_url(re.compile(f"{BASE_URL}/game/[0-9]+"))

    # 2. Click the "Help" button
    page.locator("#help-btn").click()

    # 3. Assert the help modal appears and contains expected content
    expect(page.locator("#help-modal")).to_be_visible()
    expect(page.locator("#help-modal h2")).to_have_text("Help & Information")
    expect(page.locator("#help-content-display h3:has-text('How to Play AI Escape')")).to_be_visible()
    expect(page.locator("#help-content-display p:has-text('Your goal is to explore mysterious rooms')")).to_be_visible()
    
    # 4. Close the modal
    page.locator("#close-help-modal").click()
    expect(page.locator("#help-modal")).not_to_be_visible()
