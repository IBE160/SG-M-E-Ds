import pytest
from playwright.sync_api import Page, expect
from app import create_app # Import create_app from your main Flask app


BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="session")
def flask_app_url():
    # Start the Flask app in a separate thread or process for E2E tests
    # For simplicity, we assume the Flask app is already running or will be started externally
    # In a real CI/CD setup, you'd manage the Flask app lifecycle here.
    return BASE_URL


@pytest.fixture(scope="function")
def page_with_session(page: Page, flask_app_url):
    # This fixture starts a game session and navigates to the game page
    # You might want to mock the start_game POST request for faster tests
    # but for true E2E, we'll hit the actual endpoint.

    # Start a new game session
    start_game_response = page.request.post(f"{flask_app_url}/start_game", data={"player_id": "test_e2e_player", "theme": "mystery", "location": "mansion", "difficulty": "medium"})
    assert start_game_response.status == 201
    session_data = start_game_response.json()
    session_id = session_data["id"]

    # Navigate to the game page for the session
    page.goto(f"{flask_app_url}/game/{session_id}")
    page.wait_for_load_state("networkidle")
    return page, session_id


def test_room_background_image_display(page_with_session):
    page, session_id = page_with_session

    # Assuming the body or a specific container has the background image
    # We need to inspect the CSS properties to verify the image.
    # This might require some adjustments based on the actual CSS implementation.
    
    # Example: Check background-image style on the body element
    # This is a basic check. A more robust test might check a specific element
    # and compare the URL.

    # Check for Ancient Library background
    # Initial room for create_game_session in services/game_logic.py is "ancient_library"
    expect(page.locator("#background-image-container")).to_have_css("background-image", f'url("{BASE_URL}/static/images/ancient_library.jpg")')
    
    # Simulate moving to another room (e.g., mysterious_observatory)
    # This assumes there's a way to trigger interaction from the frontend, e.g., via a button click or API call
    # For now, we'll simulate the API call directly to advance the room.

    # Find the "Go north to Mysterious Observatory" option index
    game_session_data_response = page.request.get(f"{BASE_URL}/game_session/{session_id}")
    game_session_data = game_session_data_response.json()
    contextual_options = game_session_data["contextual_options"]
    
    go_north_index = -1
    for i, option_text in enumerate(contextual_options):
        if "Go north to Mysterious Observatory" in option_text:
            go_north_index = i
            break
    assert go_north_index != -1, "Go north option not found"


    # Interact to move north
    interact_response = page.request.post(
        f"{BASE_URL}/game_session/{session_id}/interact", 
        data={"option_index": go_north_index}
    )
    assert interact_response.status == 200

    # After interaction, reload the page to get the updated UI with new background
    page.goto(f"{BASE_URL}/game/{session_id}")
    page.wait_for_load_state("networkidle")

    # Check for Mysterious Observatory background
    expect(page.locator("#background-image-container")).to_have_css("background-image", f'url("{BASE_URL}/static/images/mysterious_observatory.jpg")')

    # Simulate moving to escape_chamber
    game_session_data_response = page.request.get(f"{BASE_URL}/game_session/{session_id}")
    game_session_data = game_session_data_response.json()
    contextual_options = game_session_data["contextual_options"]

    go_east_index = -1
    for i, option_text in enumerate(contextual_options):
        if "Go east to Escape Chamber" in option_text:
            go_east_index = i
            break
    assert go_east_index != -1, "Go east option not found"

    interact_response = page.request.post(
        f"{BASE_URL}/game_session/{session_id}/interact", 
        data={"option_index": go_east_index}
    )
    assert interact_response.status == 200

    page.goto(f"{BASE_URL}/game/{session_id}")
    page.wait_for_load_state("networkidle")

    # Check for Escape Chamber background
    expect(page.locator("#background-image-container")).to_have_css("background-image", f'url("{BASE_URL}/static/images/escape_chamber.jpg")')