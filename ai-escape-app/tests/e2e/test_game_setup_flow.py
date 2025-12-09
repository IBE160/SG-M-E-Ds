import pytest
from playwright.sync_api import Page, expect
import re

# Assuming a base URL for the local Flask app
# This could be configured via an environment variable or pytest config
BASE_URL = "http://127.0.0.1:5000" 

# Fixture to provide a Playwright page
# Requires 'pytest-playwright' to be installed
@pytest.fixture(scope="module", autouse=True)
def setup_teardown_browser(browser):
    # This fixture ensures a browser is launched and closed for the module
    yield

def test_game_setup_flow(page: Page):
    # 1. Navigate to the base URL
    page.goto(BASE_URL)
    expect(page).to_have_url(BASE_URL + "/")
    expect(page.locator("h1")).to_have_text("AI Escape")

    # 2. Click "DESIGN YOUR OWN"
    page.locator("button.option-btn.large[data-mode='design-your-own']").click()
    
    # Expect to see the game setup wizard
    expect(page.locator("#game-setup-wizard")).not_to_have_class("hidden")
    expect(page.locator("#setup-step-theme h2")).to_have_text("Step 1: Choose Your Theme")

    # 3. Select a Theme (e.g., "Classic Mystery")
    # The first option should be pre-selected, but let's explicitly click one
    page.locator("#theme-options button.option-btn:has-text('Classic Mystery')").click()
    expect(page.locator("#theme-options button.option-btn:has-text('Classic Mystery')")).to_have_class(re.compile(r"active"))

    # 4. Click "NEXT"
    page.locator("#setup-step-theme button.action-btn[data-action='next']").click()

    # Expect to move to Location step
    expect(page.locator("#setup-step-location")).not_to_have_class("hidden")
    expect(page.locator("#setup-step-location h2")).to_have_text("Step 2: Choose Your Location")

    # 5. Select a Location (e.g., "Ancient Library")
    page.locator("#location-options button.option-btn:has-text('Ancient Library')").click()
    expect(page.locator("#location-options button.option-btn:has-text('Ancient Library')")).to_have_class(re.compile(r"active"))

    # 6. Click "NEXT"
    page.locator("#setup-step-location button.action-btn[data-action='next']").click()

    # Expect to move to Difficulty step
    expect(page.locator("#setup-step-difficulty")).not_to_have_class("hidden")
    expect(page.locator("#setup-step-difficulty h2")).to_have_text("Step 3: Choose Difficulty")

    # 7. Select a Difficulty (e.g., "Easy")
    page.locator("#difficulty-options button.option-btn:has-text('Easy')").click()
    expect(page.locator("#difficulty-options button.option-btn:has-text('Easy')")).to_have_class(re.compile(r"active"))

    # 8. Click "START ADVENTURE"
    page.locator("#setup-step-difficulty button.action-btn[data-action='start']").click()

    # 9. Verify redirection to /game/<session_id>
    # This will wait for the navigation to complete
    expect(page).to_have_url(re.compile(f"{BASE_URL}/game/[0-9]+")) # Expect a URL like /game/1, /game/2, etc.

    # Further assertions on the game page can be added if needed,
    # e.g., checking for specific elements indicating a successful game start.
    expect(page.locator("h2")).to_be_visible()
    expect(page.locator("p#room-description")).to_be_visible()
