
        let lastPage = 'start';
        let loadingInterval;
        let hintCooldownInterval;
        let selectedDifficulty = 'normal';
        let selectedLocationImg = ''; // To store the selected ambiance and location image

        const gameState = {
            objective: "",
            inventory: [],
            hints: {
                available: [
                    "The inscription on the sarcophagus seems important.",
                    "Perhaps the torch can be used for something other than light.",
                    "The key might not be for the door you think it is."
                ],
                used: [],
                budget: 5,
                cooldown: 15, // seconds
                isOnCooldown: false
            }
        };

        function initGame(difficulty = 'normal') {
            // Reset state for a new game
            gameState.objective = "Find a way to open the stone door.";
            gameState.inventory = ["Rusty Key", "Crumpled Note"];
            
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

            renderAll();
        }

        function renderAll() {
            renderObjective();
            renderInventory();
            renderHint();
        }

        function renderObjective() {
            const objectiveElement = document.getElementById('objective-text');
            if (objectiveElement) {
                objectiveElement.textContent = gameState.objective;
            }
        }

        function renderInventory() {
            const inventoryList = document.getElementById('inventory-list');
            if (inventoryList) {
                inventoryList.innerHTML = '';
                gameState.inventory.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item;
                    inventoryList.appendChild(li);
                });
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
            hintText.textContent = 'Click for a hint';
            hintBox.classList.remove('disabled');

            if (gameState.hints.budget === 0) {
                hintText.textContent = 'No more hints available.';
                hintBox.classList.add('disabled');
            }

            if (gameState.hints.isOnCooldown) {
                hintBox.classList.add('disabled');
                hintText.textContent = 'Hint on cooldown...';
            }
        }

        function updateObjective(newObjective) {
            gameState.objective = newObjective;
            renderObjective();
        }

        function addItem(item) {
            if (!gameState.inventory.includes(item)) {
                gameState.inventory.push(item);
                renderInventory();
            }
        }

        function removeItem(item) {
            gameState.inventory = gameState.inventory.filter(i => i !== item);
            renderInventory();
        }

        function requestHint() {
            if (gameState.hints.isOnCooldown || gameState.hints.budget === 0) {
                return; // Do nothing if on cooldown or no hints left
            }

            const availableHints = gameState.hints.available;
            if (availableHints.length > 0) {
                const hint = availableHints.shift(); // Get the first available hint
                gameState.hints.used.push(hint);
                gameState.hints.budget--;
                
                const hintText = document.getElementById('hint-text');
                hintText.textContent = hint;

                startHintCooldown();
            } else {
                const hintText = document.getElementById('hint-text');
                hintText.textContent = "No new hints at the moment.";
            }
            renderHint();
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

        function showPage(pageId) {
            const currentPage = document.querySelector('.mockup.active')?.id;
            if (currentPage && currentPage !== 'settings' && currentPage !== 'load-game') {
                lastPage = currentPage;
            }
            document.querySelectorAll('.mockup').forEach(mockup => mockup.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
            
            if (pageId === 'design') {
                goToStep(1);
            }
        }

        function closeSettings() {
            showPage(lastPage);
        }

        function startGame() {
            initGame(selectedDifficulty);
                        // Set the background of the immersive main content area
                        const immersiveMain = document.querySelector('#immersive .immersive-main');
                        if (immersiveMain && selectedLocationImg) {
                            immersiveMain.style.backgroundImage = selectedLocationImg;
                        } else if (immersiveMain) {
                            // Fallback if no location is selected (e.g., direct navigation)
                            immersiveMain.style.backgroundImage = "url('images/Abandiond Mansion.jpg')";
                        }
                        showPage('immersive');        }

        function goToStep(stepNumber) {
            document.querySelectorAll('.design-step').forEach(step => step.classList.remove('active'));
            document.getElementById('design-step-' + stepNumber).classList.add('active');
        }

        function selectAmbiance(ambiance, buttonElement) {
            const themeButtons = document.querySelector('#design-step-1 .design-options');
            themeButtons.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
            buttonElement.classList.add('active');
            document.querySelectorAll('.location-options').forEach(loc => loc.style.display = 'none');
            const locationContainer = document.getElementById('locations-' + ambiance);
            locationContainer.style.display = 'flex';
            // Set the default selected location image for the ambiance
            const firstLocation = locationContainer.querySelector('.option-btn');
            if (firstLocation) {
                selectedLocationImg = firstLocation.style.backgroundImage;
                // Also visually activate the first location
                firstLocation.classList.add('active');
            }
        }
        
        function selectLocation(locationElement) {
            const optionsContainer = locationElement.parentElement;
            optionsContainer.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('active'));
            locationElement.classList.add('active');
            selectedLocationImg = locationElement.style.backgroundImage;
        }

        function selectDifficulty(difficultyElement) {
            document.querySelectorAll('#design-step-3 .option-btn').forEach(btn => btn.classList.remove('active'));
            difficultyElement.classList.add('active');
            selectedDifficulty = difficultyElement.textContent.toLowerCase();
        }

        function startLoading() {
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
        
        function saveGame() {
            alert('Game Saved!');
        }

        document.addEventListener('DOMContentLoaded', () => {
            // Responsive Toggle
            const responsiveToggleBtn = document.getElementById('responsive-toggle');
            if (responsiveToggleBtn) {
                responsiveToggleBtn.addEventListener('click', () => {
                    document.body.classList.toggle('mobile-view');
                    if (document.body.classList.contains('mobile-view')) {
                        responsiveToggleBtn.textContent = 'Desktop View (Click for Mobile)';
                    } else {
                        responsiveToggleBtn.textContent = 'Mobile View (Click for Desktop)';
                    }
                });
            }

            // Start Page buttons
            document.querySelectorAll('.start-menu button')[0].addEventListener('click', () => showPage('game-mode'));
            document.querySelectorAll('.start-menu button')[1].addEventListener('click', () => showPage('load-game'));
            document.querySelectorAll('.start-menu button')[2].addEventListener('click', () => showPage('settings'));

            // Game Mode Selection buttons
            document.querySelectorAll('#game-mode .design-options .option-btn')[0].addEventListener('click', () => showPage('design'));
            document.querySelectorAll('#game-mode .design-options .option-btn')[1].addEventListener('click', () => showPage('ai-prompt'));
            document.querySelector('#game-mode .design-actions .action-btn').addEventListener('click', () => showPage('start'));

            // AI Prompt buttons
            document.querySelector('#ai-prompt .design-actions .action-btn:nth-child(1)').addEventListener('click', () => showPage('game-mode'));
            document.querySelector('#ai-prompt .design-actions .action-btn.primary').addEventListener('click', startLoading);

            // Design Page - Ambiance
            document.querySelectorAll('#design-step-1 .design-options .option-btn').forEach(button => {
                button.addEventListener('click', (e) => selectAmbiance(e.target.textContent.toLowerCase(), e.target));
            });
            document.querySelector('#design-step-1 .design-actions .action-btn:nth-child(1)').addEventListener('click', () => showPage('game-mode'));
            document.querySelector('#design-step-1 .design-actions .action-btn.primary').addEventListener('click', () => goToStep(2));
            
            // Design Page - Location (event listeners already attached for each div)
            document.querySelectorAll('.location-options .option-btn').forEach(button => {
                button.addEventListener('click', () => selectLocation(button));
            });
            document.querySelector('#design-step-2 .design-actions .action-btn:nth-child(1)').addEventListener('click', () => goToStep(1));
            document.querySelector('#design-step-2 .design-actions .action-btn.primary').addEventListener('click', () => goToStep(3));

            // Design Page - Difficulty
            document.querySelectorAll('#design-step-3 .design-options .option-btn').forEach(button => {
                button.addEventListener('click', (e) => selectDifficulty(e.target));
            });
            document.querySelector('#design-step-3 .design-actions .action-btn:nth-child(1)').addEventListener('click', () => goToStep(2));
            document.querySelector('#design-step-3 .design-actions .action-btn.primary').addEventListener('click', startGame);

            // Settings buttons - These are the actual toggle buttons inside the modal, they don't open the modal
            document.getElementById('music-toggle').addEventListener('click', function() { this.classList.toggle('active'); this.textContent = this.classList.contains('active') ? 'ON' : 'OFF'; });
            document.getElementById('sfx-toggle').addEventListener('click', function() { this.classList.toggle('active'); this.textContent = this.classList.contains('active') ? 'ON' : 'OFF'; });
            document.querySelector('#settings .design-actions .action-btn.primary').addEventListener('click', closeSettings);

            // Load Game buttons
            document.querySelectorAll('.saved-game-item').forEach(item => item.addEventListener('click', () => showPage('immersive')));
            document.querySelector('#load-game .design-actions .action-btn').addEventListener('click', () => showPage('start'));

            // Immersive page buttons (using data attributes for actions)
            document.querySelectorAll('.immersive-options .immersive-option').forEach(option => {
                option.addEventListener('click', (e) => {
                    const action = e.target.dataset.action;
                    const value = e.target.dataset.value;
                    if (action === 'updateObjective') {
                        updateObjective(value);
                    } else if (action === 'addItem') {
                        addItem(value);
                    } else if (action === 'removeItem') {
                        removeItem(value);
                    }
                    // For now, any click on an immersive option will refresh hints
                    renderHint(); 
                });
            });

            document.getElementById('hint-box').addEventListener('click', requestHint);

            document.querySelectorAll('.retro-actions button').forEach(button => {
                button.addEventListener('click', (e) => {
                    const action = e.target.dataset.action;
                    const value = e.target.dataset.value;
                    if (action === 'showPage') {
                        showPage(value);
                    } else if (action === 'saveGame') {
                        saveGame();
                    }
                });
            });

            // Set initial state for ambiance selection
            // This ensures selectedLocationImg is initialized even if user doesn't click ambiance first
            // const initialAmbianceButton = document.querySelector('#design-step-1 .design-options .option-btn.active');
            // if (initialAmbianceButton) {
            //     selectAmbiance(initialAmbianceButton.textContent.toLowerCase(), initialAmbianceButton);
            // }
             // Initialize game on page load for testing
            // initGame();
        });
    
