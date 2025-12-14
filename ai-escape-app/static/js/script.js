let lastPage = 'start';
let loadingInterval;
let hintCooldownInterval;
let gameTimerInterval;
let selectedDifficulty = 'normal';
let selectedAmbianceText = 'mysterious'; // Default to mysterious
let selectedLocationText = ''; // To store the selected location name
const currentPlayerId = 'test_player_1'; // Placeholder for now

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
                used: [],
                budget: 5,
                cooldown: 15, // seconds
                isOnCooldown: false
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
            switch(difficulty) {
                case 'easy':
                    gameState.hints.budget = 8;
                    break;
                case 'hard':
                    gameState.hints.budget = 3;
                    break;
                case 'normal':
                default:
                    gameState.hints.budget = 5;
                    break;
            }
            gameState.hints.isOnCooldown = false;
            clearInterval(hintCooldownInterval);
            renderHint();
        }

        async function fetchAndRenderGameImmersive() {
            if (!currentSessionId) return;

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
                document.getElementById('objective-text').textContent = gameData.narrative_state.objective || tr("explore_and_find_clues");
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
                
                // Set initial client-side hint state based on backend difficulty
                initGameImmersive(gameData.difficulty);

            } catch (error) {
                console.error('Failed to fetch and render game immersive:', error);
                // Optionally, show an error message on the UI
            }
        }

        function renderHint() {
            const hintBox = document.getElementById('hint-box');
            const hintBudget = document.getElementById('hint-budget');
            const hintText = document.getElementById('hint-text');
            const hintCooldown = document.getElementById('hint-cooldown');

            if (!hintBox) return;

            hintBudget.textContent = `x${gameState.hints.budget}`;
            hintCooldown.textContent = '';
            hintBox.classList.remove('disabled');

            if (gameState.hints.budget === 0) {
                hintText.textContent = 'No more hints available.';
                hintBox.classList.add('disabled');
            }

            if (gameState.hints.isOnCooldown) {
                hintBox.classList.add('disabled');
            } else if(hintText.textContent !== 'Click for a hint' && gameState.hints.used.includes(hintText.textContent)) {
                // Do not reset text if a hint is being displayed
            }
            else {
                hintText.textContent = 'Click for a hint';
            }
        }

        async function requestHint() {
            if (gameState.hints.isOnCooldown || gameState.hints.budget === 0) {
                return; // Do nothing if on cooldown or no hints left
            }

            try {
                const response = await fetch(`/game_session/${currentSessionId}/hint`);
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Failed to fetch hint.');
                }
                const data = await response.json();
                
                const hintText = document.getElementById('hint-text');
                hintText.textContent = data.hint;
                gameState.hints.used.push(data.hint);
                gameState.hints.budget--;
                startHintCooldown();

            } catch (error) {
                console.error('Failed to request hint:', error);
                const hintText = document.getElementById('hint-text');
                hintText.textContent = "Could not retrieve a hint at this time.";
            }
        }

        function startHintCooldown() {
            gameState.hints.isOnCooldown = true;
            let timeLeft = gameState.hints.cooldown;
            const hintCooldownEl = document.getElementById('hint-cooldown');

            hintCooldownInterval = setInterval(() => {
                timeLeft--;
                hintCooldownEl.textContent = `(${timeLeft}s)`;
                if (timeLeft <= 0) {
                    clearInterval(hintCooldownInterval);
                    gameState.hints.isOnCooldown = false;
                    renderHint();
                }
            }, 1000);
            renderHint();
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
            const currentPage = document.querySelector('.mockup.active')?.id;
            if (currentPage && currentPage !== 'settings' && currentPage !== 'load-game') {
                lastPage = currentPage;
            }
            document.querySelectorAll('.mockup').forEach(mockup => mockup.classList.remove('active'));
            const targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('active');
            }
            
            if (pageId === 'design') {
                goToStep(1);
                // Ensure initial ambiance is selected for locations display
                const initialAmbianceButton = document.querySelector('#design-step-1 .design-options .option-btn.active');
                if (initialAmbianceButton) {
                    selectAmbiance(initialAmbianceButton.dataset.theme, initialAmbianceButton.dataset.ambianceCategory, initialAmbianceButton);
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
            }
        }

        function selectAmbiance(themeId, ambianceCategory, buttonElement) {
            console.log(`selectAmbiance called with: themeId=${themeId}, ambianceCategory=${ambianceCategory}`);
            const themeButtons = document.querySelector('#design-step-1 .design-options');
            themeButtons.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
            buttonElement.classList.add('active');
            selectedAmbianceText = themeId; // Store the ambiance theme ID
            
            document.querySelectorAll('.location-options').forEach(loc => loc.style.display = 'none');
            const locationContainer = document.getElementById('locations-' + ambianceCategory);
            if (locationContainer) {
                locationContainer.style.display = 'flex';
                
                // --- Automatically select default location ---
                // Clear any previously active location buttons in this category
                locationContainer.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));

                if (ROOM_DATA_JS && ROOM_DATA_JS[themeId]) {
                    const defaultLocationId = ROOM_DATA_JS[themeId].start_room;
                    const defaultLocationButton = locationContainer.querySelector(`[data-location="${defaultLocationId}"]`);
                    
                    if (defaultLocationButton) {
                        selectedLocationText = defaultLocationId;
                        defaultLocationButton.classList.add('active');
                        // Also ensure the selectedAmbianceText is updated based on the default location's themeId
                        // This might be redundant if themeId passed is always correct, but good for consistency
                        selectedAmbianceText = defaultLocationButton.dataset.themeId; 
                        console.log(`Default location selected: ${selectedLocationText} for theme: ${selectedAmbianceText}`);
                    } else {
                        // Fallback if start_room from ROOM_DATA_JS is not found among buttons
                        const firstLocationButton = locationContainer.querySelector('.option-btn');
                        if (firstLocationButton) {
                            selectedLocationText = firstLocationButton.dataset.location;
                            firstLocationButton.classList.add('active');
                            selectedAmbianceText = firstLocationButton.dataset.themeId;
                            console.log(`Fallback: First location selected: ${selectedLocationText} for theme: ${selectedAmbianceText}`);
                        } else {
                            selectedLocationText = ''; // No locations available
                            console.warn(`No location buttons found for ambiance category: ${ambianceCategory}`);
                        }
                    }
                } else {
                    selectedLocationText = ''; // No ROOM_DATA or theme found
                    console.warn(`ROOM_DATA_JS not available or themeId ${themeId} not found.`);
                }
            }
        }
        
        function selectLocation(locationElement) {
            console.log('selectLocation called');
            const optionsContainer = locationElement.parentElement;
            if (optionsContainer) {
                optionsContainer.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
                locationElement.classList.add('active');
                selectedLocationText = locationElement.dataset.location; // Store the location key
                // Update selectedAmbianceText based on the selected location's theme
                selectedAmbianceText = locationElement.dataset.themeId;
            }
        }

        function selectDifficulty(difficultyElement) {
            console.log('selectDifficulty called');
            document.querySelectorAll('#design-step-3 .option-btn').forEach(btn => btn.classList.remove('active'));
            difficultyElement.classList.add('active');
            selectedDifficulty = difficultyElement.textContent.toLowerCase();
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
            const messages = [
                tr("reticulating_splines"),
                tr("generating_narrative_paradoxes"),
                tr("hiding_keys_in_obvious_places"),
                tr("polishing_virtual_dust"),
                tr("teaching_ai_to_count_on_its_fingers"),
                tr("finalizing_your_impending_doom")
            ];
            let index = 0;
            const el = document.getElementById('loading-text');
            el.textContent = messages[index];
            loadingInterval = setInterval(() => {
                index = (index + 1) % messages.length;
                el.textContent = messages[index];
            }, 2000);
            setTimeout(() => {
                clearInterval(loadingInterval);
                startGame(); // Use the general startGame function
            }, 10000);
        }
        
        async function saveGame() {
            if (!currentSessionId) {
                alert('No active game to save.');
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
            await loadTranslations(currentLanguage); // Load translations first
            console.log('DOMContentLoaded fired.');

            // Language Select Initialization
            const languageSelect = document.getElementById('language-select');
            if (languageSelect) {
                languageSelect.value = currentLanguage;
            }

            // --- Music & Volume Initialization ---
            initAudio();

            // Update UI for music toggle and volume slider
            updateMusicToggleButton();
            updateSfxToggleButton();

            const volumeSlider = document.getElementById('volume-slider');
            if (volumeSlider) {
                volumeSlider.value = gameVolume * 100; // Set slider position (0-100)
                volumeSlider.addEventListener('input', (e) => setVolume(e.target.value));
            }

            const musicToggleButton = document.getElementById('music-toggle');
            if (musicToggleButton) {
                musicToggleButton.addEventListener('click', toggleMusic);
            }

            const sfxToggleButton = document.getElementById('sfx-toggle');
            if (sfxToggleButton) {
                sfxToggleButton.addEventListener('click', toggleSfx);
            }

            document.addEventListener('click', (e) => {
                if (e.target.matches('button')) {
                    playButtonClickSound();
                }
            });
            // --- End Music & Volume Initialization ---

            // Check if currentSessionId is defined (meaning we are on the /game/<session_id> page)
            if (typeof currentSessionId !== 'undefined' && currentSessionId !== null) {
                console.log('On immersive game page. currentSessionId:', currentSessionId);
                fetchAndRenderGameImmersive();
                // Attach event listener for dynamic immersive options
                document.querySelector('.immersive-options').addEventListener('click', async (e) => {
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

                document.getElementById('hint-box').addEventListener('click', requestHint);

                document.querySelectorAll('.retro-actions button').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const action = e.target.dataset.action;
                        const value = e.target.dataset.value;
                        console.log(`Retro action clicked: ${action}, Value: ${value}`);
                        if (action === 'showPage') {
                            if (value === 'start') {
                                window.location.href = '/'; // Redirect to home on quit
                            } else {
                                // This part might still be relevant for future in-game settings/load game modals
                                // If they are meant to show actual mockups, we would call showPage(value);
                                showPage(value);
                            }
                        } else if (action === 'saveGame') {
                            saveGame();
                        }
                    });
                });

                // Since we are on the game page, there are no initial mockups to show or hide,
                // the immersive mockup is already active via game.html.
                return; // Exit here as we are on the game immersive page.
            }

            // If currentSessionId is NOT defined, we are on the index.html page
            console.log('On index.html page.');
            showPage('start'); // Default to showing the start page initially.

            // Start Page buttons
            console.log('Attempting to attach event listeners to start menu buttons.');
            const startMenuButtons = document.querySelectorAll('.start-menu button');
            if (startMenuButtons.length > 0) {
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
            document.querySelectorAll('#game-mode .design-options .option-btn')[0].addEventListener('click', () => {
                console.log('DESIGN YOUR OWN button clicked');
                showPage('design');
            });
            document.querySelectorAll('#game-mode .design-options .option-btn')[1].addEventListener('click', () => {
                console.log('AI-DRIVEN button clicked');
                showPage('ai-prompt');
            });
            document.querySelector('#game-mode .design-actions .action-btn').addEventListener('click', () => {
                console.log('BACK button from game-mode clicked');
                showPage('start');
            });

            // AI Prompt buttons
            document.querySelector('#ai-prompt .design-actions .action-btn:nth-child(1)').addEventListener('click', () => {
                console.log('BACK button from ai-prompt clicked');
                showPage('game-mode');
            });
            document.querySelector('#ai-prompt .design-actions .action-btn.primary').addEventListener('click', () => {
                console.log('GENERATE button clicked');
                startLoading();
            });

            // Design Page - Ambiance
            document.querySelectorAll('#design-step-1 .design-options .option-btn').forEach(button => {
                button.addEventListener('click', (e) => {
                    console.log(`Ambiance button clicked: ${e.target.textContent}`);
                    selectAmbiance(e.target.dataset.theme, e.target.dataset.ambianceCategory, e.target);
                });
            });
            document.querySelector('#design-step-1 .design-actions .action-btn:nth-child(1)').addEventListener('click', () => {
                console.log('BACK button from design-step-1 clicked');
                showPage('game-mode');
            });
            document.querySelector('#design-step-1 .design-actions .action-btn.primary').addEventListener('click', () => {
                console.log('NEXT button from design-step-1 clicked');
                goToStep(2);
            });
            
            // Design Page - Location (event listeners already attached for each div)
            document.querySelectorAll('.location-options .option-btn').forEach(button => {
                button.addEventListener('click', () => {
                    console.log(`Location button clicked`);
                    selectLocation(button);
                });
            });
            document.querySelector('#design-step-2 .design-actions .action-btn:nth-child(1)').addEventListener('click', () => {
                console.log('BACK button from design-step-2 clicked');
                goToStep(1);
            });
            document.querySelector('#design-step-2 .design-actions .action-btn.primary').addEventListener('click', () => {
                console.log('NEXT button from design-step-2 clicked');
                goToStep(3);
            });

            // Design Page - Difficulty
            document.querySelectorAll('#design-step-3 .option-btn').forEach(button => {
                button.addEventListener('click', (e) => {
                    console.log(`Difficulty button clicked: ${e.target.textContent}`);
                    selectDifficulty(e.target);
                });
            });
            document.querySelector('#design-step-3 .design-actions .action-btn:nth-child(1)').addEventListener('click', () => {
                console.log('BACK button from design-step-3 clicked');
                goToStep(2);
            });
            document.querySelector('#design-step-3 .design-actions .action-btn.primary').addEventListener('click', () => {
                console.log('START ADVENTURE button clicked');
                startLoading(); // Changed to startLoading
            });

            // Settings buttons - These are the actual toggle buttons inside the modal, they don't open the modal
            document.getElementById('music-toggle').addEventListener('click', function() {
                this.classList.toggle('active');
                this.textContent = this.classList.contains('active') ? 'ON' : 'OFF';
                console.log(`Music toggle clicked, new state: ${this.textContent}`);
            });
            document.getElementById('sfx-toggle').addEventListener('click', function() {
                this.classList.toggle('active');
                this.textContent = this.classList.contains('active') ? 'ON' : 'OFF';
                console.log(`SFX toggle clicked, new state: ${this.textContent}`);
            });
            document.querySelector('#settings .design-actions .action-btn.primary').addEventListener('click', () => {
                console.log('CLOSE settings button clicked');
                closeSettings();
            });

            // Load Game buttons
            document.querySelector('#load-game .design-actions .action-btn').addEventListener('click', () => {
                console.log('BACK button from load-game clicked');
                showPage('start');
            });
        });