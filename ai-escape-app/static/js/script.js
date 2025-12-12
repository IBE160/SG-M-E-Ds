let lastPage = 'start';
let loadingInterval;
let hintCooldownInterval;
let gameTimerInterval;
let selectedDifficulty = 'normal';
let selectedAmbianceText = 'mysterious'; // Default to mysterious
let selectedLocationText = ''; // To store the selected location name
const currentPlayerId = 'test_player_1'; // Placeholder for now
// New: To store the current game session ID (declared in game.html)
        const gameState = {
            hints: {
                used: [],
                budget: 5,
                cooldown: 15, // seconds
                isOnCooldown: false
            }
        };

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
                        div.textContent = `${index + 1}. ${option}`;
                        div.dataset.optionIndex = index; // Store index for interaction
                        immersiveOptions.appendChild(div);
                    });
                }

                // Update game status (objective, inventory)
                document.getElementById('objective-text').textContent = gameData.narrative_state.objective || "Explore and find clues.";
                document.querySelector('.current-location-subtext').textContent = `Current Location: ${gameData.current_room_name}`;
                
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
                    selectAmbiance(initialAmbianceButton.textContent.toLowerCase(), initialAmbianceButton);
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

        function selectAmbiance(ambiance, buttonElement) {
            console.log(`selectAmbiance called with: ${ambiance}`);
            const themeButtons = document.querySelector('#design-step-1 .design-options');
            themeButtons.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
            buttonElement.classList.add('active');
            selectedAmbianceText = ambiance; // Store the ambiance text
            document.querySelectorAll('.location-options').forEach(loc => loc.style.display = 'none');
            const locationContainer = document.getElementById('locations-' + ambiance);
            if (locationContainer) {
                locationContainer.style.display = 'flex';
                // Set the default selected location image for the ambiance
                const firstLocation = locationContainer.querySelector('.option-btn');
                if (firstLocation) {
                    selectedLocationText = firstLocation.dataset.location; // Store default location key
                    // Also visually activate the first location
                    firstLocation.classList.add('active');
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
            showPage('loading');
            const messages = ["Reticulating splines...", "Generating narrative paradoxes...", "Hiding keys in obvious places...", "Polishing virtual dust...", "Teaching AI to count on its fingers...", "Finalizing your impending doom..."];
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

        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOMContentLoaded fired');
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
            document.querySelectorAll('.start-menu button')[0].addEventListener('click', () => {
                console.log('NEW GAME button clicked');
                showPage('game-mode');
            });
            document.querySelectorAll('.start-menu button')[1].addEventListener('click', () => {
                console.log('LOAD GAME button clicked');
                showPage('load-game');
            });
            document.querySelectorAll('.start-menu button')[2].addEventListener('click', () => {
                console.log('SETTINGS button clicked');
                showPage('settings');
            });

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
                    selectAmbiance(e.target.textContent.toLowerCase(), e.target);
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