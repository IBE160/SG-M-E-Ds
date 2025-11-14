# ibe160 UX Design Specification

_Created on Friday, 14 November 2025 by BIP_
_Generated using BMad Method - Create UX Design Workflow v1.0_

---

## Executive Summary

{{project_vision}}

---

## 1. Design System Foundation

### 1.1 Design System Choice

**System:** shadcn/ui
**Version:** Latest stable version
**Rationale:** Chosen for its balance of accessibility, developer control, and creative freedom, allowing for a unique visual identity for "AI Escape" without being locked into a prescriptive design language. It provides unstyled, accessible components that are highly customizable with Tailwind CSS.
**Provides:** A robust library of accessible, unstyled UI components (e.g., buttons, forms, modals, navigation elements).
**Customization Needs:** High, to achieve the unique, immersive game aesthetic and interaction patterns required for "AI Escape."

---

## 2. Core User Experience

### 2.1 Defining Experience

**Core Experience Principles:**

*   **Speed:** The standard game setup will be fast and intuitive. The "completely generate a new story" option will be intentionally slower to create a sense of anticipation and uniqueness.
*   **Guidance:** We'll provide clear choices during setup, but the puzzles themselves will be challenging with minimal hand-holding. The "Help" system will be a safety net, not a primary guide.
*   **Flexibility:** Players will have a high degree of control over the game's theme and location, but the AI will guide the narrative and puzzle progression within a structured framework to ensure coherence.
*   **Feedback:** Feedback will be rich and immersive, from a "delightful" loading screen to clear and satisfying feedback when solving puzzles.

### 2.2 Novel UX Patterns

**Pattern Name:** AI-Driven Replayability

**User Goal:** To start a new, unique adventure that feels fresh and compelling.

**Trigger:** A "New Game" button on the main menu.

**Interaction Flow:**
1.  User selects "New Game."
2.  User is presented with a choice of themes/feelings (e.g., "Mystery," "Sci-Fi," "Fantasy").
3.  User is presented with a choice of pre-defined locations based on the theme, OR an option to "Completely generate a new story and location."
4.  If the user chooses to generate, a loading screen appears with intriguing quotes, jokes, or hints, indicating that the AI is crafting a unique world.

**Visual Feedback:** The loading screen will visually communicate that a unique world is being built.

**States:**
*   **Default:** Main menu with "New Game," "Continue Game," "Load Game," "Options," and "Help."
*   **Loading:** A loading screen with quotes/jokes/hints.
*   **Success:** The game begins with the chosen or generated theme and location.
*   **Error:** If generation fails, a dialog appears with options to "Try Again" or "Go Back" to the selection screen.

**Platform Considerations:** The layout will adapt from horizontal on desktop/web to vertical on mobile web.

**Accessibility:** All buttons and choices will be keyboard-navigable and screen-reader compatible.

**Inspiration:** The setup flow is inspired by common patterns in many games, while the loading screen experience is inspired by *The Sims 4*. The "generate a new world" option is similar to using "seeds" in games like *Minecraft*.

---

## 3. Visual Foundation

### 3.1 Color System

**Theme:** Retro-Futuristic Grit (Dark Mode)
**Rationale:** Inspired by "The Oregon Trail" and adapted for a modern, AI-driven game, this theme evokes a sense of ruggedness, challenge, and technological mystery. The dark background enhances immersion and focus.

**Color Palette:**
*   **Primary:** `#F8F9FA` (Light Grey) - Used for primary text and key elements.
*   **Secondary:** `#8B4513` (Saddle Brown) - Used for secondary actions and earthy, historical accents.
*   **Accent:** `#D2691E` (Chocolate/Rust) - Used for subtle tech/futuristic highlights and interactive elements, evoking a weathered, adventurous feel.
*   **Success:** `#28A745` (Green) - Used for success messages and positive feedback.
*   **Warning:** `#FFC107` (Amber) - Used for warnings and cautionary messages.
*   **Error:** `#DC3545` (Red) - Used for error messages and destructive actions.
*   **Info:** `#17A2B8` (Info Blue) - Used for informational messages and hints.
*   **Background:** `#212529` (Darkest Grey) - The primary background color for the application.
*   **Borders:** `#343A40` (Darker Grey) - Used for borders and separators.

### 3.2 Typography

*   **Heading Font:** 'Press Start 2P', cursive - Provides a pixelated, retro feel for headings.
*   **Body Font:** 'Roboto Mono', monospace - Offers a clean, technical feel for body text and game commands, enhancing readability.
*   **Type Scale:** A standard, responsive type scale will be used for headings (h1-h6), body text, and smaller captions to ensure a clear visual hierarchy.

### 3.3 Spacing & Layout

*   **Base Unit:** 8px - All spacing and sizing will be based on an 8px grid for consistency.
*   **Spacing Scale:** A consistent spacing scale (e.g., 4px, 8px, 12px, 16px, 24px) will be used for margins, padding, and layout composition.
*   **Layout Grid:** A standard 12-column grid will be used for web and desktop layouts to ensure proper alignment and responsive behavior.

**Interactive Visualizations:**

- Color Theme Explorer: [ux-color-themes.html](./ux-color-themes.html)

---

## 4. Design Direction

### 4.1 Chosen Design Approach

**Chosen Direction:** Direction 5: Immersive Adventure

**Description:** This direction combines a full-screen immersive background with an organized sidebar and a semi-transparent text overlay. It aims to provide both atmospheric immersion and clear, at-a-glance information.

**Key Features:**
*   Full-screen background image for deep immersion.
*   Semi-transparent dark text box overlay for story and options, ensuring readability without fully obscuring the background.
*   Right-side vertical sidebar for "Game Status" (Inventory, Objectives, Hint, Options, Save), providing quick access to critical information.
*   The accent color is used for interactive elements and highlights, maintaining the retro-futuristic grit theme.

**Interactive Mockups:**

- Design Direction Showcase: [ux-design-directions.html](./ux-design-directions.html)

---

## 5. Information Architecture

### 5.1 High-Level Structure

The application's information architecture is structured to provide intuitive navigation and access to core game functionalities and information.

**Main Menu:**
*   **New Game:** Initiates the AI-Driven Replayability flow, allowing users to start a fresh, unique adventure.
*   **Continue Game:** Resumes the last saved game session.
*   **Load Game:** Provides access to a list of saved game states for selection.
*   **Options:** Navigates to game settings (audio, display, controls, accessibility).
*   **Help:** Accesses in-game assistance, tutorials, and lore.

**In-Game Screen:**
*   **Immersive Main Area:** The primary display for the game's narrative, puzzles, and interactive choices. This area is dynamic and driven by the AI.
*   **Right Sidebar (Game Status):** A persistent vertical sidebar providing at-a-glance information and quick access to essential game features.
    *   **Inventory:** Displays items collected by the player.
    *   **Objectives:** Shows current goals and tasks.
    *   **Hint:** Provides contextual hints for puzzles (limited use).
    *   **Options:** Quick access to game settings without leaving the game screen.
    *   **Save:** Allows players to save their current game progress.

**Options Screen:**
*   **Audio Settings:** Volume controls for music, sound effects, and dialogue.
*   **Display Settings:** Resolution, full-screen/windowed mode, graphics quality.
*   **Controls:** Keybindings and input device settings.
*   **Accessibility:** Options for color blindness, text size, narration, etc.
*   **Save/Apply:** Confirms and applies changes.
*   **Back to Main Menu / Back to Game:** Returns to the previous screen.

**Help Screen:**
*   **How to Play:** Basic game instructions and mechanics.
*   **Game Mechanics:** Detailed explanations of puzzle types, interaction models, etc.
*   **Lore/Background:** Information about the game world and story.
*   **FAQ:** Frequently asked questions.
*   **Back to Main Menu / Back to Game:** Returns to the previous screen.

**Load/Save Game Screens:**
*   **List of Save Slots:** Displays available save files with details (e.g., date, location, progress).
*   **Save Button:** Saves the current game to a selected slot.
*   **Load Button:** Loads a selected game state.
*   **Delete Save:** Removes a selected save file.
*   **Back to Main Menu / Back to Game:** Returns to the previous screen.

---

## 6. Component Library

### 6.1 Component Strategy

{{component_library_strategy}}

---

## 7. UX Pattern Decisions

### 7.1 Consistency Rules

{{ux_pattern_decisions}}

---

## 8. Responsive Design & Accessibility

### 8.1 Responsive Strategy

{{responsive_accessibility_strategy}}

---

## 9. Implementation Guidance

### 9.1 Completion Summary

{{completion_summary}}

---

## Appendix

### Related Documents

- Product Requirements: `{{prd_file}}`
- Product Brief: `{{brief_file}}`
- Brainstorming: `{{brainstorm_file}}`

### Core Interactive Deliverables

This UX Design Specification was created through visual collaboration:

- **Color Theme Visualizer**: {{color_themes_html}}
  - Interactive HTML showing all color theme options explored
  - Live UI component examples in each theme
  - Side-by-side comparison and semantic color usage

- **Design Direction Mockups**: {{design_directions_html}}
  - Interactive HTML with 6-8 complete design approaches
  - Full-screen mockups of key screens
  - Design philosophy and rationale for each direction

### Optional Enhancement Deliverables

_This section will be populated if additional UX artifacts are generated through follow-up workflows._

<!-- Additional deliverables added here by other workflows -->

### Next Steps & Follow-Up Workflows

This UX Design Specification can serve as input to:

- **Wireframe Generation Workflow** - Create detailed wireframes from user flows
- **Figma Design Workflow** - Generate Figma files via MCP integration
- **Interactive Prototype Workflow** - Build clickable HTML prototypes
- **Component Showcase Workflow** - Create interactive component library
- **AI Frontend Prompt Workflow** - Generate prompts for v0, Lovable, Bolt, etc.
- **Solution Architecture Workflow** - Define technical architecture with UX context

### Version History

| Date     | Version | Changes                         | Author        |
| -------- | ------- | ------------------------------- | ------------- |
| Friday, 14 November 2025 | 1.0     | Initial UX Design Specification | BIP |

---

_This UX Design Specification was created through collaborative design facilitation, not template generation. All decisions were made with user input and are documented with rationale._
