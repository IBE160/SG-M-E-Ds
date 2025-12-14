let lastPage = 'start';
let loadingInterval;
let hintCooldownInterval;
let gameTimerInterval;
let selectedDifficulty = 'normal';
let selectedAmbianceText = 'mysterious'; // Default to mysterious
let selectedLocationText = ''; // To store the selected location name
let currentPlayerId = 'test_player_1'; // Placeholder for now - should be managed by backend/auth
let gameSetupOptions = {}; // Global to store fetched game setup options

// Hard-coded AMBIANCE_MAP for selectAmbiance function
const AMBIANCE_MAP = {
    "forgotten_library": { "start_room": "forgotten_library_entrance", "ambiance_category": "mysterious" },
    "sci-fi_hangar": { "start_room": "sci-fi_hangar_main", "ambiance_category": "sci-fi" }, // Assuming sci-fi is an ambiance category
    "underwater_lab": { "start_room": "underwater_lab_entrance", "ambiance_category": "underwater" }, // Assuming underwater is an ambiance category
    "abandoned_mansion": { "start_room": "mansion_foyer", "ambiance_category": "horror" }, // Assuming horror is an ambiance category
    "clown_funhouse": { "start_room": "clown_funhouse_entrance", "ambiance_category": "funny" },
    // Add other themes as needed based on data/rooms.py, for which default locations are desired
};

// Frontend helper function to convert snake_case to human readable
function formatSnakeCaseToHumanReadable(text) {
    if (typeof text !== 'string') {
        return text;
    }
    // Replace underscores with spaces, then capitalize the first letter of each word
    return text.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

// --- Music & Volume Globals ---
let backgroundMusic;
let buttonClickSound;
let isMusicEnabled = (localStorage.getItem('isMusicEnabled') === null) ? true : (localStorage.getItem('isMusicEnabled') === 'true');
let isSfxEnabled = (localStorage.getItem('isSfxEnabled') === null) ? true : (localStorage.getItem('isSfxEnabled') === 'true');
let gameVolume = parseFloat(localStorage.getItem('gameVolume')) || 0.5;

function initAudio() {
    try {
        backgroundMusic = new Howl({
            src: ["/static/audio/411867__ispeakwaves__mystery.mp3"],
            loop: true,
            volume: gameVolume,
            autoplay: isMusicEnabled,
            html5: true // Force HTML5 Audio to prevent Web Audio API issues
        });

        buttonClickSound = new Howl({
            src: ["/static/audio/342200__christopherderp__videogame-menu-button-click.wav"],
            volume: gameVolume,
            html5: true // Force HTML5 Audio
        });
        
        // Ensure initial play state
        if (isMusicEnabled) {
            backgroundMusic.play();
        } else {
            backgroundMusic.pause();
        }
    } catch (e) {
        console.error("Error initializing audio with Howler.js:", e);
    }
}
// --- End Music & Volume Globals ---

// --- Music & Volume Functions ---
function toggleMusic() {
    isMusicEnabled = !isMusicEnabled;
    if (backgroundMusic) {
        if (isMusicEnabled) {
            backgroundMusic.play();
        } else {
            backgroundMusic.pause();
        }
    }
    localStorage.setItem('isMusicEnabled', isMusicEnabled);
    updateMusicToggleButton();
}

function toggleSfx() {
    isSfxEnabled = !isSfxEnabled;
    localStorage.setItem('isSfxEnabled', isSfxEnabled);
    updateSfxToggleButton();
}

function setVolume(volumeLevel) { // volumeLevel is 0-100
    gameVolume = parseFloat(volumeLevel) / 100;
    if (typeof Howler !== 'undefined') { // Check if Howler is defined before using it
        Howler.volume(gameVolume);
    }
    localStorage.setItem('gameVolume', gameVolume);
}

function updateMusicToggleButton() {
    const musicToggleButton = document.getElementById('music-toggle');
    if (musicToggleButton) {
        // Reflect the actual playing state for the 'active' class
        if (backgroundMusic && backgroundMusic.playing()) {
            musicToggleButton.classList.add('active');
        } else {
            musicToggleButton.classList.remove('active');
        }
        // Reflect the stored preference for the text
        musicToggleButton.textContent = isMusicEnabled ? tr('on') : tr('off');
    }
}

function updateSfxToggleButton() {
    const sfxToggleButton = document.getElementById('sfx-toggle');
    if (sfxToggleButton) {
        if (isSfxEnabled) {
            sfxToggleButton.classList.add('active');
            sfxToggleButton.textContent = tr('on');
        } else {
            sfxToggleButton.classList.remove('active');
            sfxToggleButton.textContent = tr('off');
        }
    }
}

function playButtonClickSound() {
    if (isSfxEnabled && buttonClickSound) {
        buttonClickSound.play();
    }
}
// --- End Music & Volume Functions ---

// --- Translation Globals ---
let currentLanguage = localStorage.getItem('gameLanguage') || 'en'; // Default to 'en'
let translations = {}; // Stores the loaded translations for the current language
// --- End Translation Globals ---

// New: To store the current game session ID (declared in game.html)
        const gameState = {
            hints: {
                used: [], // Only track used hints on client-side
            }
        };


// --- Translation Functions ---
async function loadTranslations(lang) {
    try {
        const response = await fetch(`/static/translations/${lang}.json`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        translations = await response.json();
        console.log(`Translations loaded for ${lang}:`, translations);
        currentLanguage = lang;
        localStorage.setItem('gameLanguage', lang);
        applyTranslations();
    } catch (error) {
        console.error(`Failed to load translations for ${lang}:`, error);
        // Fallback to English if loading fails or requested lang is default
        if (lang !== 'en') {
            currentLanguage = 'en';
            loadTranslations('en');
        } else {
            // If even English fails, set translations to empty to prevent errors
            translations = {};
        }
    }
}

function tr(key, params = {}) {
    let text = translations[key] || key; // Use key as fallback
    for (const param in params) {
        text = text.replace(`{${param}}`, params[param]);
    }
    return text;
}

function applyTranslations() {
    // Translate direct text content
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        // Handle specific cases like game timer, current location subtext etc.
        if (element.classList.contains('game-timer')) {
            // Game timer text is dynamic, don't override here
            return;
        }
        if (element.classList.contains('current-location-subtext')) {
             // current location subtext is dynamic
             return;
        }
        element.textContent = tr(key);
    });

    // Translate placeholder attributes
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (element.placeholder) {
            element.placeholder = tr(key);
        }
    });

    // Handle numbered immersive options
    document.querySelectorAll('.immersive-options .immersive-option').forEach((element, index) => {
        const key = element.getAttribute('data-i18n');
        if (key) {
            element.textContent = `${index + 1}. ${tr(key)}`;
        }
    });

    // Translate document title (which doesn't have data-i18n)
    document.title = tr('app_title');

    // Ensure the music toggle button text is updated correctly after language change
    updateMusicToggleButton();
    updateSfxToggleButton();

    // The language select options themselves don't need translation,
    // as their text content is static (English, Norsk, etc.) and
    // the label for it is handled by data-i18n
}
// --- End Translation Functions ---

        function formatTime(seconds) {
            const d = new Date(null);
            d.setSeconds(seconds);
            return d.toISOString().substr(11, 8);
        }

        // This initGame is for the immersive screen's client-side state (like hints)
        // Actual game state (rooms, inventory, objective) comes from the backend.
        function initGameImmersive(difficulty = 'normal') {
            // Client-side initGameImmersive no longer handles hint state.
            // Hint state is now driven directly by backend gameData.
            // This function might be removed or repurposed later if no other client-side init is needed.
        }

        async function fetchAndRenderGameImmersive() {
            // Extract sessionId from URL pathname
            const pathParts = window.location.pathname.split('/');
            const currentSessionId = pathParts[pathParts.length - 1]; // Assumes URL is /game/<sessionId>

            if (!currentSessionId || isNaN(parseInt(currentSessionId))) {
                console.error("No valid currentSessionId found in URL.");
                return;
            }

            try {
                const response = await fetch(`/game_session/${currentSessionId}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const gameData = await response.json();
                console.log('Game data received:', gameData);

                if (gameTimerInterval) clearInterval(gameTimerInterval);
                const timerInitialOffset = Date.now(); // Store the time when the timer actually starts running
                gameTimerInterval = setInterval(() => {
                    const nowMs = Date.now();
                    const elapsedSeconds = Math.floor((nowMs - timerInitialOffset) / 1000); // Calculate elapsed from when this interval started
                    const timerElement = document.querySelector('.game-timer');
                    if (timerElement) {
                        timerElement.textContent = `TIME: ${formatTime(elapsedSeconds)}`;
                    }
                }, 1000);
                
                // Update narrative and options
                const immersiveTextBox = document.querySelector('.immersive-text-box');
                if (immersiveTextBox) {
                    immersiveTextBox.querySelector('h3').textContent = gameData.current_room_name;
                    immersiveTextBox.querySelector('p').textContent = gameData.current_room_description;
                    const immersiveOptions = immersiveTextBox.querySelector('.immersive-options');
                    immersiveOptions.innerHTML = '';
                    gameData.contextual_options.forEach((option, index) => {
                        const div = document.createElement('div');
                        div.classList.add('immersive-option');
                        // Use tr() for options if they are translatable keys, otherwise display directly
                        div.textContent = `${index + 1}. ${option}`; // Options are dynamic from backend, not directly translatable keys
                        div.dataset.optionIndex = index; // Store index for interaction
                        immersiveOptions.appendChild(div);
                    });
                }

                // Update game status (objective, inventory)
                document.getElementById('objective-text').textContent = gameData.objective_display_text;
                document.querySelector('.current-location-subtext').innerHTML = `${tr('current_location')}: ${gameData.current_room_name}`;
                
                const inventoryList = document.getElementById('inventory-list');
                if (inventoryList) {
                    inventoryList.innerHTML = '';
                    if (gameData.inventory && gameData.inventory.length > 0) {
                        gameData.inventory.forEach(item => {
                            const li = document.createElement('li');
                            li.textContent = item;
                            inventoryList.appendChild(li);
                        });
                    } else {
                        inventoryList.innerHTML = '<li>Empty</li>';
                    }
                }

                // Update background image
                const backgroundContainer = document.getElementById('background-container');
                if (backgroundContainer && gameData.current_room_image) {
                    backgroundContainer.style.backgroundImage = `url(${gameData.current_room_image})`;
                } else if (backgroundContainer) {
                    backgroundContainer.style.backgroundImage = "url('/static/images/start_page_image_2.jpg')"; // Fallback
                }
                
                // Render hint state based on backend data
                renderHint(gameData);
                if (gameData.remaining_hint_cooldown > 0) {
                    startHintCooldown(gameData.remaining_hint_cooldown);
                }

            } catch (error) {
                console.error('Failed to fetch and render game immersive:', error);
                // Optionally, show an error message on the UI
            }
        }

        function renderHint(gameData) { // Now accepts gameData
            const hintBox = document.getElementById('hint-box');
            const hintBudget = document.getElementById('hint-budget');
            const hintText = document.getElementById('hint-text');
            const hintCooldown = document.getElementById('hint-cooldown');

            if (!hintBox) return;

            const hintsRemaining = gameData.hints_remaining;
            const remainingCooldown = gameData.remaining_hint_cooldown;

            hintBudget.textContent = `x${hintsRemaining}`;
            
            hintBox.classList.remove('disabled');

            hintText.textContent = gameData.hint_status_display_text;

            if (remainingCooldown > 0) {
                hintCooldown.textContent = `(${remainingCooldown}s)`;
                hintBox.classList.add('disabled');
            } else {
                hintCooldown.textContent = '';
            }
        }

        async function requestHint() {
            // Extract sessionId from URL pathname
            const pathParts = window.location.pathname.split('/');
            const currentSessionId = pathParts[pathParts.length - 1]; // Assumes URL is /game/<sessionId>

            if (!currentSessionId || isNaN(parseInt(currentSessionId))) {
                console.error("No valid currentSessionId found in URL for requestHint.");
                return;
            }
            // Check hint availability and cooldown based on *current UI state* derived from backend
            const hintsRemaining = parseInt(document.getElementById('hint-budget').textContent.replace('x', ''));
            const hintCooldownText = document.getElementById('hint-cooldown').textContent;
            const hintTextElement = document.getElementById('hint-text'); // Get hint text element

            // If a hint is currently displayed, don't request another one immediately.
            // This prevents spamming requests if the user clicks fast.
            // Also if there's text in hintCooldownText, it means we're on cooldown.
            if (hintsRemaining <= 0 || hintCooldownText.includes('s)')) {
                return; // Do nothing if on cooldown or no hints left
            }

            // Temporarily disable hint button to prevent multiple rapid clicks
            const hintBox = document.getElementById('hint-box');
            if (hintBox) hintBox.classList.add('disabled');
            if (hintTextElement) hintTextElement.textContent = tr('requesting_hint'); // Show requesting state
            
            try {
                const response = await fetch(`/game_session/${currentSessionId}/hint`);
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Failed to fetch hint.');
                }
                const data = await response.json(); // Data contains hint, hints_remaining, remaining_hint_cooldown, hint_status_display_text
                
                // Display the received hint message directly
                if (hintTextElement) {
                    hintTextElement.textContent = data.hint; // This is the actual hint content
                }
                // Add the hint to the client-side used list, if it's a new hint.
                if (data.hint && !gameState.hints.used.includes(data.hint)) {
                    gameState.hints.used.push(data.hint);
                }

                // Update hint budget and status based on new data from backend
                const hintBudget = document.getElementById('hint-budget');
                if (hintBudget) hintBudget.textContent = `x${data.hints_remaining}`;
                
                // If there's a cooldown, start the client-side countdown
                if (data.remaining_hint_cooldown > 0) {
                    startHintCooldown(data.remaining_hint_cooldown);
                } else {
                    // If no cooldown, ensure hint box is re-enabled if budget allows
                    const hintBox = document.getElementById('hint-box');
                    if (hintBox) hintBox.classList.remove('disabled');
                    // Also update the status message to 'Click for a hint' if not on cooldown and budget > 0
                    if (hintTextElement && data.hints_remaining > 0) {
                        hintTextElement.textContent = "Click for a hint"; // Hardcoded English
                    } else if (hintTextElement && data.hints_remaining <= 0) {
                        hintTextElement.textContent = "No more hints available."; // Hardcoded English
                    }
                }

                // After displaying the hint and updating status, we don't immediately re-render
                // the entire game immersive. The hint is displayed, and cooldown started if needed.
                // The main game state will be updated on next interaction or cooldown expiry.
                // For a consistent UI state after interaction that does not block the current hint,
                // we should let the cooldown handle the full refresh.

            } catch (error) {
                console.error('Failed to request hint:', error);
                if (hintTextElement) hintTextElement.textContent = "Could not retrieve a hint at this time."; // Hardcoded English
            }
        }

        function startHintCooldown(remainingSeconds) { // Now accepts remainingSeconds
            clearInterval(hintCooldownInterval); // Clear any existing interval
            
            let timeLeft = remainingSeconds;
            const hintCooldownEl = document.getElementById('hint-cooldown');
            const hintBox = document.getElementById('hint-box');

            hintBox.classList.add('disabled');
            hintCooldownEl.textContent = `(${timeLeft}s)`;
            
            hintCooldownInterval = setInterval(() => {
                timeLeft--;
                hintCooldownEl.textContent = `(${timeLeft}s)`;
                if (timeLeft <= 0) {
                    clearInterval(hintCooldownInterval);
                    fetchAndRenderGameImmersive(); // Refresh state from backend
                }
            }, 1000);
        }

        async function fetchAndRenderSavedGames() {
            const savedGamesList = document.querySelector('.saved-games-list');
            savedGamesList.innerHTML = ''; // Clear existing items

            try {
                // Assuming currentPlayerId is available globally or passed appropriately
                const response = await fetch(`/saved_games?player_id=${currentPlayerId}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const savedGames = await response.json();

                if (savedGames.length === 0) {
                    savedGamesList.innerHTML = '<p>No saved games found.</p>';
                } else {
                    savedGames.forEach(game => {
                        const gameItem = document.createElement('div');
                        gameItem.classList.add('saved-game-item');
                        gameItem.dataset.sessionId = game.session_id; // Store session_id for loading
                        gameItem.dataset.saveId = game.id; // Store save_id for loading
                        
                        const savedDate = new Date(game.saved_at);
                        const formattedDate = savedDate.toLocaleDateString();
                        const formattedTime = savedDate.toLocaleTimeString();

                        gameItem.innerHTML = `
                            <p>${game.save_name} - ${game.game_state.location}</p>
                            <small>Date: ${formattedDate} | Time: ${formattedTime}</small>
                        `;
                        gameItem.addEventListener('click', async () => {
                            console.log('savedGameItem clicked directly:', gameItem);
                            const saveId = gameItem.dataset.saveId;
                            console.log('Loading game with saveId:', saveId);

                            try {
                                const response = await fetch(`/load_game/${saveId}`);
                                console.log('Fetch response for /load_game:', response);
                                if (!response.ok) {
                                    const errorData = await response.json();
                                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                                }
                                const data = await response.json();
                                const sessionId = data.id; // The loaded session's ID
                                console.log('Game loaded, new session ID:', sessionId);
                                window.location.href = `/game/${sessionId}`; // Redirect to the game page
                            } catch (error) {
                                console.error('Failed to load game:', error);
                                alert('Failed to load game: ' + error.message);
                            }
                        });
                        savedGamesList.appendChild(gameItem);
                    });
                }
            } catch (error) {
                console.error('Failed to fetch saved games:', error);
                savedGamesList.innerHTML = '<p>Error loading saved games.</p>';
            }
        }

        function showPage(pageId) {
            console.log(`showPage called with: ${pageId}`);
            // Find current active page (if any) and store its ID for 'lastPage'
            const currentPageElement = document.querySelector('.mockup.active');
            const currentPageId = currentPageElement ? currentPageElement.id : null;

            if (currentPageId && currentPageId !== 'settings' && currentPageId !== 'load-game') {
                lastPage = currentPageId;
            }
            
            // Deactivate all mockups
            document.querySelectorAll('.mockup').forEach(mockup => mockup.classList.remove('active'));
            
            // Activate the target page
            const targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('active');
            } else {
                console.error(`Error: Target page with ID '${pageId}' not found.`);
                return; // Prevent further execution if target page doesn't exist
            }
            
            if (pageId === 'design') {
                goToStep(1);
                // Ensure initial ambiance is selected for locations display
                // Null-safe access for the initialAmbianceButton
                const initialAmbianceButton = document.querySelector('#design-step-1 .design-options .option-btn.active');
                if (initialAmbianceButton) {
                    selectAmbiance(initialAmbianceButton.dataset.theme, initialAmbianceButton.dataset.ambianceCategory, initialAmbianceButton);
                } else {
                    console.warn('No active ambiance button found on design-step-1 on page load.');
                    // Fallback to a default ambiance if none is active
                    const defaultAmbianceButton = document.querySelector('#design-step-1 .design-options .option-btn[data-theme="mysterious"]');
                    if (defaultAmbianceButton) {
                         selectAmbiance(defaultAmbianceButton.dataset.theme, defaultAmbianceButton.dataset.ambianceCategory, defaultAmbianceButton);
                    }
                }
            } else if (pageId === 'load-game') {
                fetchAndRenderSavedGames(); // Call to load saved games
            }
        }

        function closeSettings() {
            showPage(lastPage);
        }

        function closeLoadGame() {
            showPage('start');
        }

        async function startGame() {
            console.log('startGame called');
            // Use the selected ambiance, location, and difficulty to start a new game
            const gameData = {
                player_id: currentPlayerId, // Using the placeholder player ID
                theme: selectedAmbianceText,
                location: selectedLocationText,
                difficulty: selectedDifficulty
            };
            console.log('Game Data:', gameData);

            try {
                const response = await fetch('/start_game', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(gameData),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                const sessionId = data.session_id;
                console.log('Game started, session ID:', sessionId);

                // Redirect to the game page
                window.location.href = `/game/${sessionId}`;

            } catch (error) {
                console.error('Failed to start game:', error);
                alert('Failed to start game: ' + error.message);
                // Optionally, show an error message on the UI
            }
        }

        function goToStep(stepNumber) {
            console.log(`goToStep called with: ${stepNumber}`);
            document.querySelectorAll('.design-step').forEach(step => step.classList.remove('active'));
            const targetStep = document.getElementById('design-step-' + stepNumber);
            if (targetStep) {
                targetStep.classList.add('active');
            } else {
                console.error(`Error: Design step with ID 'design-step-${stepNumber}' not found.`);
            }
        }

        function selectAmbiance(themeId, ambianceCategory, buttonElement) {
            console.log(`selectAmbiance called with: themeId=${themeId}, ambianceCategory=${ambianceCategory}`);
            const themeButtonsContainer = document.querySelector('#design-step-1 .design-options');
            if (themeButtonsContainer) { // Null-safe check
                themeButtonsContainer.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
            }
            if (buttonElement) { // Null-safe check
                buttonElement.classList.add('active');
            }
            selectedAmbianceText = themeId; // Store the ambiance theme ID
            
            document.querySelectorAll('.location-options').forEach(loc => loc.style.display = 'none');
            const locationContainer = document.getElementById('locations-' + ambianceCategory);
            if (locationContainer) {
                locationContainer.style.display = 'flex';
                
                // --- Automatically select default location ---
                // Clear any previously active location buttons in this category
                locationContainer.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));

                // Use the hard-coded AMBIANCE_MAP
                const ambianceData = AMBIANCE_MAP[themeId];

                if (ambianceData && ambianceData.start_room) {
                    const defaultLocationId = ambianceData.start_room;
                    const defaultLocationButton = locationContainer.querySelector(`[data-location="${defaultLocationId}"]`);
                    
                    if (defaultLocationButton) {
                        selectedLocationText = defaultLocationId;
                        defaultLocationButton.classList.add('active');
                        // selectedAmbianceText is already themeId, no need to update from dataset
                        console.log(`Default location selected: ${selectedLocationText} for theme: ${selectedAmbianceText}`);
                    } else {
                        // Fallback if start_room from AMBIANCE_MAP is not found among buttons
                        const firstLocationButton = locationContainer.querySelector('.option-btn');
                        if (firstLocationButton) {
                            selectedLocationText = firstLocationButton.dataset.location;
                            firstLocationButton.classList.add('active');
                            selectedAmbianceText = firstLocationButton.dataset.themeId; // Fallback to dataset
                            console.log(`Fallback: First location selected: ${selectedLocationText} for theme: ${selectedAmbianceText}`);
                        } else {
                            selectedLocationText = ''; // No locations available
                            console.warn(`No location buttons found for ambiance category: ${ambianceCategory}`);
                        }
                    }
                } else {
                    selectedLocationText = ''; // No ambianceData or start_room found in AMBIANCE_MAP
                    console.warn(`start_room not available for themeId ${themeId} in AMBIANCE_MAP. Falling back to first available location.`);
                     // Fallback to first available location if theme not in AMBIANCE_MAP or missing start_room
                    const firstLocationButton = locationContainer.querySelector('.option-btn');
                    if (firstLocationButton) {
                        selectedLocationText = firstLocationButton.dataset.location;
                        firstLocationButton.classList.add('active');
                        selectedAmbianceText = firstLocationButton.dataset.themeId;
                        console.log(`Fallback: First location selected: ${selectedLocationText} for theme: ${selectedAmbianceText}`);
                    } else {
                        console.warn(`No location buttons found for ambiance category: ${ambianceCategory}`);
                    }
                }
            } else {
                console.warn(`Location container for ambiance category '${ambianceCategory}' not found.`);
            }
        }
        
        function selectLocation(locationElement) {
            console.log('selectLocation called');
            if (!locationElement) { // Null-safe check
                console.error('selectLocation called with null or undefined element.');
                return;
            }
            const optionsContainer = locationElement.parentElement;
            if (optionsContainer) {
                optionsContainer.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
                locationElement.classList.add('active');
                selectedLocationText = locationElement.dataset.location; // Store the location key
                // Update selectedAmbianceText based on the selected location's theme
                selectedAmbianceText = locationElement.dataset.themeId;
            } else {
                console.warn('Parent container for location element not found.');
            }
        }

        function selectDifficulty(difficultyElement) {
            console.log('selectDifficulty called');
            // Null-safe check for querySelectorAll result and each button
            document.querySelectorAll('#design-step-3 .option-btn').forEach(btn => {
                if (btn) btn.classList.remove('active');
            });
            if (difficultyElement) { // Null-safe check
                difficultyElement.classList.add('active');
                selectedDifficulty = difficultyElement.textContent.toLowerCase();
            } else {
                console.error('selectDifficulty called with null or undefined element.');
            }
        }

        function startLoading() {
            console.log('startLoading called');

            // --- Frontend Validation ---
            if (!selectedAmbianceText) {
                alert(tr('please_select_theme'));
                return;
            }
            if (!selectedLocationText) {
                alert(tr('please_select_location'));
                return;
            }
            if (!selectedDifficulty) { // Although it defaults, explicit check for safety
                alert(tr('please_select_difficulty'));
                return;
            }
            // --- End Frontend Validation ---

            showPage('loading');
            // Fetch translated loading messages from API
            fetch('/api/loading_messages')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(messages => { // These messages are now hardcoded English strings
                    let index = 0;
                    const el = document.getElementById('loading-text');
                    if (el) { // Null-safe check
                        el.textContent = messages[index];
                        loadingInterval = setInterval(() => {
                            index = (index + 1) % messages.length;
                            el.textContent = messages[index];
                        }, 2000);
                    } else {
                        console.error('Loading text element not found.');
                        // Fallback to directly starting game if loading text element is missing
                        clearInterval(loadingInterval);
                        startGame();
                        return;
                    }
                    
                    setTimeout(() => {
                        clearInterval(loadingInterval);
                        startGame(); // Use the general startGame function
                    }, 10000);
                })
                .catch(error => {
                    console.error('Failed to fetch loading messages:', error);
                    // Fallback to static messages if API fails
                    const messages = [
                        "Reticulating splines...",
                        "Generating narrative paradoxes...",
                        "Hiding keys in obvious places...",
                        "Polishing virtual dust...",
                        "Teaching AI to count on its fingers...",
                        "Finalizing your impending doom..."
                    ];
                    let index = 0;
                    const el = document.getElementById('loading-text');
                    if (el) {
                        el.textContent = messages[index];
                        loadingInterval = setInterval(() => {
                            index = (index + 1) % messages.length;
                            el.textContent = messages[index];
                        }, 2000);
                    }
                    setTimeout(() => {
                        clearInterval(loadingInterval);
                        startGame();
                    }, 10000);
                });
        }
        
        async function saveGame() {
            // Extract sessionId from URL pathname
            const pathParts = window.location.pathname.split('/');
            const currentSessionId = pathParts[pathParts.length - 1]; // Assumes URL is /game/<sessionId>
            
            if (!currentSessionId || isNaN(parseInt(currentSessionId))) {
                alert(tr('no_active_game_to_save'));
                return;
            }
            const saveName = prompt("Enter a name for your saved game:");
            if (!saveName) {
                alert("Save operation cancelled.");
                return;
            }

            try {
                const response = await fetch('/save_game', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ session_id: currentSessionId, save_name: saveName }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }

                alert(`Game saved successfully as "${saveName}"!`);
            } catch (error) {
                console.error('Failed to save game:', error);
                alert('Failed to save game: ' + error.message);
            }
        }

        document.addEventListener('DOMContentLoaded', async () => {
                        console.log('DOMContentLoaded fired.');
            
                        // Language Select Initialization
                        const languageSelect = document.getElementById('language-select');
                        if (languageSelect) { // Null-safe check
                            languageSelect.value = currentLanguage;
                            languageSelect.addEventListener('change', (e) => loadTranslations(e.target.value)); // Add event listener for language change
                        }
            
                        // --- Music & Volume Initialization ---
                        initAudio();
            
                        // Update UI for music toggle and volume slider
                        updateMusicToggleButton();
                        updateSfxToggleButton();
            
                        const volumeSlider = document.getElementById('volume-slider');
                        if (volumeSlider) { // Null-safe check
                            volumeSlider.value = gameVolume * 100; // Set slider position (0-100)
                            volumeSlider.addEventListener('input', (e) => setVolume(e.target.value));
                        }
            
                        const musicToggleButton = document.getElementById('music-toggle');
                        if (musicToggleButton) { // Null-safe check
                            musicToggleButton.addEventListener('click', toggleMusic);
                        }
            
                        const sfxToggleButton = document.getElementById('sfx-toggle');
                        if (sfxToggleButton) { // Null-safe check
                            sfxToggleButton.addEventListener('click', toggleSfx);
                        }
            
                        document.addEventListener('click', (e) => {
                            if (e.target.matches('button, .option-btn')) { // Include .option-btn for wider click detection
                                playButtonClickSound();
                            }
                        });
                        // --- End Music & Volume Initialization ---
            
                                    // Determine currentSessionId based on URL
                                    const pathParts = window.location.pathname.split('/');
                                    let currentSessionId = null;
                                    if (pathParts.length === 3 && pathParts[1] === 'game' && !isNaN(parseInt(pathParts[2]))) {
                                        currentSessionId = parseInt(pathParts[2]);
                                    }
                                    
                                    // Check if we are on the /game/<session_id> page
                                    if (currentSessionId !== null) {
                                        console.log('On immersive game page. currentSessionId:', currentSessionId);
                                        fetchAndRenderGameImmersive(); // This function now handles getting currentSessionId
                                        // Attach event listener for dynamic immersive options using event delegation
                                        const immersiveOptionsContainer = document.querySelector('.immersive-options');                            if (immersiveOptionsContainer) { // Null-safe check
                                immersiveOptionsContainer.addEventListener('click', async (e) => {
                                    if (e.target.classList.contains('immersive-option')) {
                                        console.log('Immersive option clicked');
                                        const optionIndex = e.target.dataset.optionIndex;
                                        const chosenOptionText = e.target.textContent.substring(e.target.textContent.indexOf('.') + 2); // Extract option text without number
                                        let playerAttempt = "";
            
                                        if (chosenOptionText.startsWith("Solve ")) {
                                            playerAttempt = prompt("What is your solution to the puzzle?");
                                            if (playerAttempt === null) { // User cancelled the prompt
                                                return;
                                            }
                                        }
            
                                        try {
                                            const response = await fetch(`/game_session/${currentSessionId}/interact`, {
                                                method: 'POST',
                                                headers: {
                                                    'Content-Type': 'application/json',
                                                },
                                                body: JSON.stringify({
                                                    option_index: parseInt(optionIndex),
                                                    player_attempt: playerAttempt // Include player attempt
                                                }),
                                            });
                                            if (!response.ok) {
                                                const errorData = await response.json();
                                                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                                            }
                                            const data = await response.json();
                                            if (data.game_over) {
                                                alert(data.message); // Show game over message
                                                window.location.href = '/'; // Go back to start page
                                            } else {
                                                fetchAndRenderGameImmersive(); // Re-render immersive screen with new state
                                            }
                                        } catch (error) {
                                            console.error('Failed to interact:', error);
                                            alert('Failed to interact: ' + error.message);
                                        }
                                    }
                                });
                            }
            
                            const hintBox = document.getElementById('hint-box');
                            if (hintBox) { // Null-safe check
                                hintBox.addEventListener('click', requestHint);
                            }
            
                            document.querySelectorAll('.retro-actions button').forEach(button => {
                                if (button) { // Null-safe check for each button
                                    button.addEventListener('click', (e) => {
                                        const action = e.target.dataset.action;
                                        const value = e.target.dataset.value;
                                        console.log(`Retro action clicked: ${action}, Value: ${value}`);
                                        if (action === 'showPage') {
                                            if (value === 'start') {
                                                window.location.href = '/'; // Redirect to home on quit
                                            } else {
                                                showPage(value);
                                            }
                                        } else if (action === 'saveGame') {
                                            saveGame();
                                        }
                                    });
                                }
                            });
            
                            return; // Exit here as we are on the game immersive page.
                        }
            
                        // If currentSessionId is NOT defined, we are on the index.html page
                        console.log('On index.html page.');
                        showPage('start'); // Default to showing the start page initially.
            
                        // Start Page buttons
                        console.log('Attempting to attach event listeners to start menu buttons.');
                        const startMenuButtons = document.querySelectorAll('.start-menu button');
                        if (startMenuButtons.length > 0) { // Null-safe check for the NodeList
                            console.log(`Found ${startMenuButtons.length} start menu buttons.`);
                            startMenuButtons[0].addEventListener('click', () => {
                                console.log('NEW GAME button clicked.');
                                showPage('game-mode');
                            });
                            startMenuButtons[1].addEventListener('click', () => {
                                console.log('LOAD GAME button clicked.');
                                showPage('load-game');
                            });
                            startMenuButtons[2].addEventListener('click', () => {
                                console.log('SETTINGS button clicked.');
                                showPage('settings');
                            });
                            console.log('Start menu button event listeners attached.');
                        } else {
                            console.error('No start menu buttons found to attach listeners.');
                        }
            
                        // Game Mode Selection buttons
                        const gameModeDesignBtn = document.querySelectorAll('#game-mode .design-options .option-btn')[0];
                        if (gameModeDesignBtn) { // Null-safe check
                            gameModeDesignBtn.addEventListener('click', () => {
                                console.log('DESIGN YOUR OWN button clicked');
                                showPage('design');
                            });
                        }
                        const gameModeAiBtn = document.querySelectorAll('#game-mode .design-options .option-btn')[1];
                        if (gameModeAiBtn) { // Null-safe check
                            gameModeAiBtn.addEventListener('click', () => {
                                console.log('AI-DRIVEN button clicked');
                                showPage('ai-prompt');
                            });
                        }
                        const gameModeBackBtn = document.querySelector('#game-mode .design-actions .action-btn');
                        if (gameModeBackBtn) { // Null-safe check
                            gameModeBackBtn.addEventListener('click', () => {
                                console.log('BACK button from game-mode clicked');
                                showPage('start');
                            });
                        }
            
                        // AI Prompt buttons
                        const aiPromptBackBtn = document.querySelector('#ai-prompt .design-actions .action-btn:nth-child(1)');
                        if (aiPromptBackBtn) { // Null-safe check
                            aiPromptBackBtn.addEventListener('click', () => {
                                console.log('BACK button from ai-prompt clicked');
                                showPage('game-mode');
                            });
                        }
                        const aiPromptGenerateBtn = document.querySelector('#ai-prompt .design-actions .action-btn.primary');
                        if (aiPromptGenerateBtn) { // Null-safe check
                            aiPromptGenerateBtn.addEventListener('click', () => {
                                console.log('GENERATE button clicked');
                                startLoading();
                            });
                        }
            
                        // Design Page - Ambiance
                        document.querySelectorAll('#design-step-1 .design-options .option-btn').forEach(button => {
                            if (button) { // Null-safe check for each button
                                button.addEventListener('click', (e) => {
                                    console.log(`Ambiance button clicked: ${e.target.textContent}`);
                                    selectAmbiance(e.target.dataset.theme, e.target.dataset.ambianceCategory, e.target);
                                });
                            }
                        });
                        const designStep1BackBtn = document.querySelector('#design-step-1 .design-actions .action-btn:nth-child(1)');
                        if (designStep1BackBtn) { // Null-safe check
                            designStep1BackBtn.addEventListener('click', () => {
                                console.log('BACK button from design-step-1 clicked');
                                showPage('game-mode');
                            });
                        }
                        const designStep1NextBtn = document.querySelector('#design-step-1 .design-actions .action-btn.primary');
                        if (designStep1NextBtn) { // Null-safe check
                            designStep1NextBtn.addEventListener('click', () => {
                                console.log('NEXT button from design-step-1 clicked');
                                goToStep(2);
                            });
                        }
                        
                        // Design Page - Location (event listeners attached via delegation in selectAmbiance or direct below)
                        // It's better to delegate this to a parent that always exists if possible, or add null checks here.
                        // selectAmbiance already handles dynamic attachment/selection, but initial setup needs care.
                        document.querySelectorAll('.location-options').forEach(locationOptionContainer => {
                            if (locationOptionContainer) { // Null-safe check
                                locationOptionContainer.addEventListener('click', (e) => {
                                    if (e.target.closest('.option-btn')) { // Use closest to handle clicks on child elements of the button
                                        console.log(`Location button clicked`);
                                        selectLocation(e.target.closest('.option-btn'));
                                    }
                                });
                            }
                        });
            
                        const designStep2BackBtn = document.querySelector('#design-step-2 .design-actions .action-btn:nth-child(1)');
                        if (designStep2BackBtn) { // Null-safe check
                            designStep2BackBtn.addEventListener('click', () => {
                                console.log('BACK button from design-step-2 clicked');
                                goToStep(1);
                            });
                        }
                        const designStep2NextBtn = document.querySelector('#design-step-2 .design-actions .action-btn.primary');
                        if (designStep2NextBtn) { // Null-safe check
                            designStep2NextBtn.addEventListener('click', () => {
                                console.log('NEXT button from design-step-2 clicked');
                                goToStep(3);
                            });
                        }
            
                        // Design Page - Difficulty
                        document.querySelectorAll('#design-step-3 .option-btn').forEach(button => {
                            if (button) { // Null-safe check for each button
                                button.addEventListener('click', (e) => {
                                    console.log(`Difficulty button clicked: ${e.target.textContent}`);
                                    selectDifficulty(e.target);
                                });
                            }
                        });
                        const designStep3BackBtn = document.querySelector('#design-step-3 .design-actions .action-btn:nth-child(1)');
                        if (designStep3BackBtn) { // Null-safe check
                            designStep3BackBtn.addEventListener('click', () => {
                                console.log('BACK button from design-step-3 clicked');
                                goToStep(2);
                            });
                        }
                        const designStep3StartAdventureBtn = document.querySelector('#design-step-3 .design-actions .action-btn.primary');
                        if (designStep3StartAdventureBtn) { // Null-safe check
                            designStep3StartAdventureBtn.addEventListener('click', () => {
                                console.log('START ADVENTURE button clicked');
                                startLoading(); // Changed to startLoading
                            });
                        }
            
                        // Settings buttons - These are the actual toggle buttons inside the modal, they don't open the modal
                        const musicToggleBtn = document.getElementById('music-toggle');
                        if (musicToggleBtn) { // Null-safe check
                            musicToggleBtn.addEventListener('click', function() {
                                this.classList.toggle('active');
                                this.textContent = this.classList.contains('active') ? tr('on') : tr('off'); // Use tr()
                                console.log(`Music toggle clicked, new state: ${this.textContent}`);
                            });
                        }
                        const sfxToggleBtn = document.getElementById('sfx-toggle');
                        if (sfxToggleBtn) { // Null-safe check
                            sfxToggleBtn.addEventListener('click', function() {
                                this.classList.toggle('active');
                                this.textContent = this.classList.contains('active') ? tr('on') : tr('off'); // Use tr()
                                console.log(`SFX toggle clicked, new state: ${this.textContent}`);
                            });
                        }
                        const settingsCloseBtn = document.querySelector('#settings .design-actions .action-btn.primary');
                        if (settingsCloseBtn) { // Null-safe check
                            settingsCloseBtn.addEventListener('click', () => {
                                console.log('CLOSE settings button clicked');
                                closeSettings();
                            });
                        }
            
                        // Load Game buttons
                        const loadGameBackBtn = document.querySelector('#load-game .design-actions .action-btn');
                        if (loadGameBackBtn) { // Null-safe check
                            loadGameBackBtn.addEventListener('click', () => {
                                console.log('BACK button from load-game clicked');
                                showPage('start');
                            });
                        }
                    });
            
                    // Function definitions follow...
                    // ... (remaining functions like formatTime, initGameImmersive, etc. are already updated or don't need changes)
                    