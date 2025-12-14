import { test, expect } from '../support/fixtures';

test.describe('Inventory and Interaction Functionality', () => {

  // Helper function to navigate and start a new game
  async function startNewGame(page: any, playerID: string, themeName: string, locationDataLocation: string) {
    console.log(`Navigating to / for player ${playerID}`); // Debug log
    await page.goto('/', { timeout: 90000, waitUntil: 'load' }); // Increased timeout and wait until 'load'
    console.log(`Page loaded for player ${playerID}`); // Debug log
    await page.waitForLoadState('networkidle'); // Wait for network to be idle
    await page.getByRole('button', { name: 'NEW GAME' }).click(); // Click NEW GAME on start screen
    await page.getByRole('button', { name: 'DESIGN YOUR OWN' }).click(); // Click DESIGN YOUR OWN
    
    // Step 1: Choose Ambiance (Theme)
    await page.getByRole('button', { name: themeName.toUpperCase() }).click(); // Select theme, e.g., 'MYSTERIOUS'
    await page.getByRole('button', { name: 'NEXT' }).click();

    // Step 2: Choose Location
    // Target the div with the correct data-location attribute
    await page.locator(`div.option-btn[data-location="${locationDataLocation}"]`).click(); 
    await page.getByRole('button', { name: 'NEXT' }).click();

    // Step 3: Select Difficulty (assuming 'NORMAL' for now)
    await page.getByRole('button', { name: 'NORMAL' }).click(); // Select difficulty
    await page.getByRole('button', { name: 'START ADVENTURE' }).click();

    // Awaiting "Current Room:" text as an indicator of game started
    await expect(page.getByText('Current Room:')).toBeVisible();
  }

  test('should allow picking up an item and adding it to inventory', async ({ page }) => {
    // Corrected locationDataLocation to match the data-location attribute
    await startNewGame(page, 'test_player_1', 'mysterious', 'forgotten_library_entrance'); 
    
    // Wait for options to load
    await page.waitForSelector('.immersive-options button');

    // Check if "Pick up Old Key" is an available option
    await expect(page.getByRole('button', { name: 'Pick up Old Key' })).toBeVisible();

    // Click to pick up the old_key
    await page.getByRole('button', { name: 'Pick up Old Key' }).click();

    // Expect a success message (if any) and that the item is in inventory
    await expect(page.getByText('You picked up the old key.')).toBeVisible(); // Assuming a message is shown

    // Verify inventory now contains 'old_key'
    await expect(page.locator('#inventory-list')).toContainText('Old Key');

    // Verify "Pick up Old Key" is no longer an option
    await expect(page.getByRole('button', { name: 'Pick up Old Key' })).toBeHidden();
  });

  test('should allow inspecting an interactable and provide feedback', async ({ page }) => {
    // Corrected locationDataLocation to match the data-location attribute
    await startNewGame(page, 'test_player_2', 'mysterious', 'forgotten_library_entrance'); 

    // Wait for options to load
    await page.waitForSelector('.immersive-options button');

    // Expect "Inspect Bookshelf" option
    await expect(page.getByRole('button', { name: 'Inspect Bookshelf' })).toBeVisible();

    // Click to inspect bookshelf
    await page.getByRole('button', { name: 'Inspect Bookshelf' }).click();

    // Expect feedback from AI
    // The actual text will depend on AI output, so this is a placeholder
    await expect(page.locator('.immersive-text-box')).toContainText('The bookshelf reveals'); // Partial text for robustness
  });

  test('should allow using an inventory item on a puzzle/interactable', async ({ page }) => {
    // Corrected locationDataLocation to match the data-location attribute
    await startNewGame(page, 'test_player_3', 'mysterious', 'forgotten_library_entrance'); 

    // Wait for options to load
    await page.waitForSelector('.immersive-options button');

    // Pick up the key first
    await page.getByRole('button', { name: 'Pick up Old Key' }).click();
    await expect(page.getByText('You picked up the old key.')).toBeVisible();

    // Go to study room where desk_puzzle is
    await page.getByRole('button', { name: /Go North to Forgotten Library Study/ }).click(); // Use regex for robust matching
    await expect(page.getByText('Current Room: Forgotten Library Study')).toBeVisible();

    // Wait for options to load
    await page.waitForSelector('.immersive-options button');

    // Expect "Use Old Key on Intricate Desk" option
    await expect(page.getByRole('button', { name: 'Use Old Key on Intricate Desk' })).toBeVisible();

    // Click to use key on desk
    await page.getByRole('button', { name: 'Use Old Key on Intricate Desk' }).click();

    // Expect feedback and puzzle state change
    // Placeholder AI feedback - actual text will vary
    await expect(page.locator('.immersive-text-box')).toContainText('The desk lock clicks open');
    // Also verify that the puzzle is now solved or has progressed
    // This would ideally involve checking a visual indicator or a message.
  });
});
