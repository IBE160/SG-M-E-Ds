import pytest
from playwright.sync_api import Page, expect, Browser
import re
import time
from tests.integration.test_settings_routes import app_with_db # Import app_with_db
from models import PlayerSettings # Import PlayerSettings model

BASE_URL = "http://127.0.0.1:5000"
PLAYER_ID = "test_e2e_player" # Consistent player ID for E2E tests

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_browser(browser: Browser):
    yield

def test_options_menu_flow(page: Page):
    # Debug: Check current player settings before clearing
    debug_response = page.request.get(f"{BASE_URL}/player_settings/{PLAYER_ID}")
    print(f"DEBUG: Initial Player Settings before delete: {debug_response.json()}")

    # Clear PlayerSettings for a clean test run via API call
    page.request.delete(f"{BASE_URL}/player_settings/{PLAYER_ID}")
    page.reload() # Force a page reload to clear client-side state
    
    # 1. Start a new game to get to the game page
    page.goto(f"{BASE_URL}/game")
    page.locator("button.option-btn.large[data-mode='design-your-own']").click()
    page.locator("#theme-options .option-btn").first.click()
    page.locator("#setup-step-theme button.action-btn[data-action='next']").click()
    page.locator("#location-options .option-btn").first.click()
    page.locator("#setup-step-location button.action-btn[data-action='next']").click()
    page.locator("#difficulty-options .option-btn").first.click()
    page.locator("#setup-step-difficulty button.action-btn[data-action='start']").click()

    # Verify redirection to /game/<session_id>
    expect(page).to_have_url(re.compile(f"{BASE_URL}/game/[0-9]+"))
    expect(page.locator("h2").first).to_be_visible() # Room name visible

    # 2. Click the "Options" button
    page.locator("#options-btn").click()

    # 3. Assert the options modal appears and contains expected content
    expect(page.locator("#options-modal")).to_be_visible()
    expect(page.locator("#options-modal h2")).to_have_text("Game Options")
    expect(page.locator("#options-content-display h4:has-text('Sound Effects Volume')")).to_be_visible()
    expect(page.locator("#options-content-display input#setting-sound")).to_be_visible()
    expect(page.locator("#options-content-display h4:has-text('Language')")).to_be_visible()
    expect(page.locator("#options-content-display select#setting-language")).to_be_visible()

    # 4. Adjust a setting (e.g., sound volume slider)
    sound_slider = page.locator("input#setting-sound")
    actual_value = sound_slider.input_value()
    print(f"DEBUG: Sound slider actual value: {actual_value}")
    expect(sound_slider).to_have_value("80") # Default value from game_settings.py
    sound_slider.fill("10") # Set to 10
    expect(sound_slider).to_have_value("10")

    # 5. Save settings
    page.locator("#save-options-btn").click()
    # Expect a success alert
    page.on("dialog", lambda dialog: dialog.accept())
    time.sleep(1) # Allow save to process

    # 6. Verify the setting is persisted (re-open options and check value)
    page.locator("#options-btn").click() # Re-open options
    expect(page.locator("#options-modal")).to_be_visible()
    expect(page.locator("input#setting-sound")).to_have_value("10"); # Should be the new value

    # 7. Close modal
    page.locator("#close-options-modal").click()
    expect(page.locator("#options-modal")).not_to_be_visible()
