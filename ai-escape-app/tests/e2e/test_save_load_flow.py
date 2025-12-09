import pytest
from playwright.sync_api import Page, expect, Browser
import re
import time # For delays

BASE_URL = "http://127.0.0.1:5000"

# Fixture to provide a Playwright page for each test
# Assumes a running Flask backend at BASE_URL
@pytest.fixture(scope="module", autouse=True)
def setup_teardown_browser(browser: Browser):
    # This fixture ensures a browser is launched and closed for the module
    yield

def test_save_load_game_flow(page: Page):
    # 1. Start a new game
    page.goto(BASE_URL)
    page.locator("button.option-btn.large[data-mode='design-your-own']").click()
    # Select theme, location, difficulty (using the first option for each)
    page.locator("#theme-options .option-btn").first.click()
    page.locator("#setup-step-theme button.action-btn[data-action='next']").click()
    page.locator("#location-options .option-btn").first.click()
    page.locator("#setup-step-location button.action-btn[data-action='next']").click()
    page.locator("#difficulty-options .option-btn").first.click()
    page.locator("#setup-step-difficulty button.action-btn[data-action='start']").click()

    # Verify redirection to /game/<session_id>
    expect(page).to_have_url(re.compile(f"{BASE_URL}/game/[0-9]+"))
    expect(page.locator("h2").first).to_be_visible() # Room name visible
    expect(page.locator("p#room-description")).to_be_visible() # Room description visible

    # Extract initial session ID
    initial_game_url = page.url
    initial_session_id = initial_game_url.split('/')[-1]
    unique_save_name = f"My E2E Test Save {initial_session_id}"

    # 2. Perform some action in the game (e.g., move to another room)
    # Click "Go north"
    page.locator("button:has-text('Go north')").click()
    time.sleep(1) # Wait for page to update
    # Verify current room has changed
    expect(page.locator("h2").first).not_to_have_text("Ancient Library") # Assuming start_room leads to Ancient Library, then north to Mysterious Observatory

    # 3. Save the game
    # Set up dialog handler *before* clicking the button that triggers the dialog
    def handle_save_dialog(dialog):
        dialog.accept(unique_save_name) # Accept the prompt with the unique save name
    page.on("dialog", handle_save_dialog)

    page.locator("#save-game-btn").click()
    
    # A short wait to ensure the dialog is handled and the save API call is made
    time.sleep(1)

    # 4. Go back to the main menu (navigate directly)
    page.goto(BASE_URL)
    expect(page).to_have_url(BASE_URL + "/")

    # 5. Load the game
    page.locator("button[data-mode='load-game']").click()
    time.sleep(1) # Wait for saved games to load
    page.locator(f"button.saved-game-btn:has-text('{unique_save_name}')").click()

    # Verify redirection to /game/<session_id>
    expect(page).to_have_url(re.compile(f"{BASE_URL}/game/[0-9]+"))
    # Ensure it's the same session ID as before the save operation
    assert initial_session_id in page.url
    # 6. Assert game state is restored (e.g., current room is the same as when saved)
    # The room name should be the changed room from step 2
    expect(page.locator("h2").first).not_to_have_text("Ancient Library") # Should be Mysterious Observatory or similar
