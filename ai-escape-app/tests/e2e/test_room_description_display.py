import pytest
from playwright.sync_api import Page, expect
import re # Import regex for pattern matching

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="function")
def page_with_game_session(page: Page):
    page.set_default_timeout(60000) # Increase timeout to 60 seconds

    # Start a new game session
    start_game_response = page.request.post(f"{BASE_URL}/start_game", data={"player_id": "test_e2e_player_desc", "theme": "mystery", "location": "ancient_library", "difficulty": "medium"})
    assert start_game_response.status == 201
    session_data = start_game_response.json()
    session_id = session_data["id"]

    # Navigate to the game page for the session
    page.goto(f"{BASE_URL}/game/{session_id}")
    page.wait_for_load_state("networkidle")
    return page, session_id


def test_dynamic_room_description_displayed(page_with_game_session):
    page, session_id = page_with_game_session

    # Initial room description should be present and not empty
    room_description_locator = page.locator("#room-description")
    expect(room_description_locator).not_to_be_empty()
    expect(room_description_locator).to_be_visible()

    # Get initial description text
    initial_description = room_description_locator.text_content()
    
    # Simulate moving to another room to trigger a new description
    # This involves calling the interact route to move the player
    game_session_data_response = page.request.get(f"{BASE_URL}/game_session/{session_id}")
    game_session_data = game_session_data_response.json()
    contextual_options = game_session_data["contextual_options"]
    
    go_north_index = -1
    for i, option_text in enumerate(contextual_options):
        if "Go north to Mysterious Observatory" in option_text:
            go_north_index = i
            break
    assert go_north_index != -1, "Go north option not found"

    interact_response = page.request.post(
        f"{BASE_URL}/game_session/{session_id}/interact", 
        data={"option_index": go_north_index}
    )
    assert interact_response.status == 200

    # After interaction, reload the page to get the updated UI with new description
    page.goto(f"{BASE_URL}/game/{session_id}")
    page.wait_for_load_state("networkidle")

    # Assert that the room description is updated and not empty
    expect(room_description_locator).not_to_be_empty()
    expect(room_description_locator).to_be_visible()
    
    # Assert that the new description is different from the initial one
    updated_description = room_description_locator.text_content()
    assert updated_description != initial_description, "Room description did not change after move"

    # You could add more sophisticated checks here,
    # e.g., using regex to check for keywords related to the new room,
    # or even mocking the AI service to return specific descriptions for assertion.
