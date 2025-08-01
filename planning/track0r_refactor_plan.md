# Track0r Refactor Plan: Data-Driven Architecture

## Overview

This document outlines a plan to refactor the current track0r system from individual HTML files per game to a unified, data-driven architecture. The goal is to eliminate code duplication, improve maintainability, and enable advanced features while preserving the current functionality and user experience.

## Current State Analysis

### Existing Structure
```
track0r/
├── html/
│   └── track0r_template.html (original template)
├── STALKER/
│   └── track0r_STALKER_v1.html (22KB, 412 lines)
├── SWU/
│   └── track0r_SWU.html
├── Wonderous_Creatures/
│   ├── track0r_WondrousCreatures.html
│   └── track0r_WonderousCreature_solo.html
└── track0r_creation_guide.md
```

### Code Duplication Issues
- **HTML Structure**: Navigation, tabs, containers, styling repeated across files
- **CSS Styling**: Same responsive design, visual hierarchy, mobile optimization
- **JavaScript Logic**: formatDetailText(), tab switching, keyboard navigation, selection tracking
- **Maintenance Burden**: Bug fixes and feature additions require changes to multiple files

### Current Features to Preserve
- Tab-based organization (Turn Flow, Setup, etc.)
- Keyboard navigation (arrow keys)
- Mobile-responsive design (iPhone landscape)
- Detailed rule references with page numbers
- Visual emphasis and formatting
- Offline functionality
- Self-contained files

## Proposed Architecture

### 1. Directory Structure
```
track0r/
├── view/
│   ├── track0r.html              # Universal template
│   ├── track0r.css               # Shared styles
│   ├── track0r.js                # Core functionality
│   └── README.md                 # Usage instructions
├── data/
│   ├── stalker.json              # STALKER game data
│   ├── star_wars_unlimited.json  # SWU game data
│   ├── wondrous_creatures.json   # Standard mode
│   ├── wondrous_creatures_solo.json # Solo mode
│   ├── schema.json               # Data structure definition
│   └── validation.js             # JSON schema validation
├── games/
│   ├── stalker.html              # Game-specific loader
│   ├── star_wars_unlimited.html  # Game-specific loader
│   ├── wondrous_creatures.html   # Game-specific loader
│   └── wondrous_creatures_solo.html # Game-specific loader
├── tools/
│   ├── converter.js              # HTML-to-JSON migration tool
│   ├── validator.js              # Data validation utility
│   └── generator.js              # Static file generator
├── legacy/
│   └── [current HTML files]     # Backup of original files
└── docs/
    ├── migration_guide.md        # Step-by-step migration
    ├── data_format_guide.md      # JSON structure documentation
    └── api_reference.md          # JavaScript API docs
```

### 2. Data Structure Design

#### JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "gameInfo": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        "rulebookReferences": {
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["title"]
    },
    "tabs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "steps": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {"type": "string"},
                "title": {"type": "string"},
                "detail": {"type": "string"},
                "substeps": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {"type": "string"},
                      "title": {"type": "string"},
                      "detail": {"type": "string"}
                    },
                    "required": ["id", "title", "detail"]
                  }
                }
              },
              "required": ["id", "title", "detail"]
            }
          }
        },
        "required": ["id", "name", "steps"]
      }
    },
    "formatting": {
      "type": "object",
      "properties": {
        "gameTerms": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Terms to emphasize with <em> tags"
        },
        "actionWords": {
          "type": "array", 
          "items": {"type": "string"},
          "description": "Action words to bold with <strong> tags"
        },
        "measurements": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Measurement patterns to bold"
        },
        "customRules": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "pattern": {"type": "string"},
              "replacement": {"type": "string"},
              "flags": {"type": "string"}
            }
          }
        }
      }
    },
    "styles": {
      "type": "object",
      "properties": {
        "primaryColor": {"type": "string"},
        "accentColor": {"type": "string"},
        "customCSS": {"type": "string"}
      }
    }
  },
  "required": ["gameInfo", "tabs"]
}
```

#### Example Game Data File (stalker.json)
```json
{
  "gameInfo": {
    "title": "STALKER",
    "subtitle": "Zone Survival",
    "version": "1.0",
    "description": "Turn order tracker for STALKER cooperative board game",
    "rulebookReferences": ["Rulebook", "Mission book"]
  },
  "tabs": [
    {
      "id": "turn-flow",
      "name": "Turn Flow", 
      "steps": [
        {
          "id": "1",
          "title": "Round Overview",
          "detail": "STALKER follows a structured round sequence where all players work together to survive the Zone. Each round consists of four main phases that must be completed in order. The game continues until the mission is completed or all Stalkers are eliminated. (Rulebook p. 18, 30, 35)",
          "substeps": []
        },
        {
          "id": "2",
          "title": "Event Phase",
          "detail": "Draw and read a new Event card to discover what is happening in the Zone and apply any Instant effects immediately. Event cards contain story narrative and may have immediate consequences or ongoing effects that last until the end of the round. This phase sets the conditions for the current round. (Rulebook p. 18)",
          "substeps": [
            {
              "id": "2.1",
              "title": "Draw Event Card and Apply Instant Effects",
              "detail": "Draw a new Event card from the top of the Event deck and read the story narrative aloud to set the atmospheric scene. If the card has any Instant effects marked with the lightning bolt symbol, resolve them immediately before proceeding. Place the Event card in the active Event slot next to the deck for reference during the round. (Rulebook p. 18)"
            }
          ]
        }
      ]
    },
    {
      "id": "setup",
      "name": "Setup",
      "steps": [
        {
          "id": "1", 
          "title": "Game Setup Overview",
          "detail": "STALKER setup involves preparing the Mission Map, distributing player components, setting up the Event deck, and placing initial Enemies and environmental elements. Setup varies based on the chosen Mission scenario. Follow the Mission book instructions for your specific scenario. (Rulebook p. varies by mission)",
          "substeps": [
            {
              "id": "1.1",
              "title": "Choose Mission and Set Up Map",
              "detail": "Choose a Mission from the Mission book and read its briefing. Each Mission has specific setup requirements, victory conditions, and special rules. Set up the Mission Map using the required Map tiles as shown in the Mission diagram. Place the Map in the center of the table where all players can reach it. (Mission book)"
            }
          ]
        }
      ]
    }
  ],
  "formatting": {
    "gameTerms": [
      "Event Phase", "Player Phase", "Enemies & Zone Phase", "End of Round",
      "Turn", "Action", "Stalker", "Enemy", "Activation", "Attention", 
      "Radiation", "Lead Stalker", "Alert", "Patrol", "High Attention", 
      "Low Attention", "Line of Sight", "LoS"
    ],
    "actionWords": [
      "must", "cannot", "may", "immediately", "exactly", "choose", 
      "perform", "resolve", "draw", "place", "discard", "activate", 
      "hunt", "investigate", "patrol"
    ],
    "measurements": [
      "\\d+\\s*Actions?", "\\d+\\s*Turns?", "\\d+\\s*HP", 
      "\\d+\\s*spaces?", "\\d+\\s*dice"
    ]
  },
  "styles": {
    "primaryColor": "#4a90e2",
    "accentColor": "#357abd"
  }
}
```

### 3. Universal HTML Template

#### view/track0r.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title id="game-title">Track0r</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="track0r.css">
</head>
<body>
  <div class="loading" id="loading">
    <p>Loading game data...</p>
  </div>
  
  <div class="app" id="app" style="display: none;">
    <div class="navigation">
      <button id="upButton">↑</button>
      <button id="downButton">↓</button>
    </div>
    
    <div class="tabs" id="tab-container">
      <!-- Tabs generated dynamically -->
    </div>
    
    <div class="content" id="content-container">
      <!-- Tab content generated dynamically -->
    </div>
  </div>
  
  <div class="error" id="error" style="display: none;">
    <h2>Error Loading Game</h2>
    <p id="error-message"></p>
  </div>
  
  <script src="track0r.js"></script>
  <script>
    // Initialize based on URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const gameId = urlParams.get('game');
    
    if (gameId) {
      initializeTracker(gameId);
    } else {
      showError('No game specified. Please provide a game parameter.');
    }
  </script>
</body>
</html>
```

### 4. Core JavaScript Architecture

#### view/track0r.js
```javascript
class Track0r {
  constructor() {
    this.gameData = null;
    this.currentTab = null;
    this.selections = {}; // Per-tab selection tracking
    this.elements = {
      app: document.getElementById('app'),
      loading: document.getElementById('loading'),
      error: document.getElementById('error'),
      tabContainer: document.getElementById('tab-container'),
      contentContainer: document.getElementById('content-container'),
      upButton: document.getElementById('upButton'),
      downButton: document.getElementById('downButton')
    };
  }

  async loadGameData(gameId) {
    try {
      const response = await fetch(`../data/${gameId}.json`);
      if (!response.ok) {
        throw new Error(`Failed to load game data: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      throw new Error(`Error loading ${gameId}: ${error.message}`);
    }
  }

  async initialize(gameId) {
    try {
      this.showLoading();
      this.gameData = await this.loadGameData(gameId);
      this.validateGameData();
      this.setupGame();
      this.showApp();
    } catch (error) {
      this.showError(error.message);
    }
  }

  validateGameData() {
    // Validate required fields and structure
    if (!this.gameData.gameInfo || !this.gameData.tabs) {
      throw new Error('Invalid game data structure');
    }
  }

  setupGame() {
    // Set page title
    document.getElementById('game-title').textContent = 
      `${this.gameData.gameInfo.title} - Track0r`;
    
    // Apply custom styles if provided
    if (this.gameData.styles) {
      this.applyCustomStyles();
    }
    
    // Initialize selections for each tab
    this.gameData.tabs.forEach(tab => {
      this.selections[tab.id] = 0;
    });
    
    // Set first tab as current
    this.currentTab = this.gameData.tabs[0].id;
    
    // Render UI
    this.renderTabs();
    this.renderContent();
    this.bindEvents();
    this.updateSelection();
  }

  renderTabs() {
    const tabsHTML = this.gameData.tabs.map((tab, index) => 
      `<button class="tab ${index === 0 ? 'active' : ''}" 
               data-tab="${tab.id}">${tab.name}</button>`
    ).join('');
    
    this.elements.tabContainer.innerHTML = tabsHTML;
  }

  renderContent() {
    const contentHTML = this.gameData.tabs.map((tab, index) => {
      const stepsHTML = this.renderSteps(tab.steps);
      return `
        <div class="tab-content ${index === 0 ? 'active' : ''}" id="${tab.id}">
          <div class="container">
            <div class="selector" id="${tab.id}-list">
              ${stepsHTML}
            </div>
            <div class="details" id="${tab.id}-details">
              <h2>Details</h2>
              <p id="${tab.id}-detailText"></p>
            </div>
          </div>
        </div>
      `;
    }).join('');
    
    this.elements.contentContainer.innerHTML = contentHTML;
  }

  renderSteps(steps) {
    return steps.map((step, stepIndex) => {
      const substepsHTML = step.substeps ? step.substeps.map(substep => 
        `<div class="substep" data-detail="${this.escapeHtml(substep.detail)}">${substep.title}</div>`
      ).join('') : '';
      
      return `
        <div class="step ${stepIndex === 0 ? 'selected' : ''}" 
             data-detail="${this.escapeHtml(step.detail)}">${step.title}</div>
        ${substepsHTML}
      `;
    }).join('');
  }

  formatDetailText(text) {
    if (!this.gameData.formatting) return text;
    
    // Extract page reference
    const pageMatch = text.match(/\(([^)]*p\.\s*[^)]+)\)/);
    const pageRef = pageMatch ? 
      `<span class="page-ref">${pageMatch[1]}</span>` : '';
    const cleanText = text.replace(/\([^)]*p\.\s*[^)]+\)/, '').trim();
    
    // Check for explicit bullet points
    if (cleanText.includes('•')) {
      return this.formatBulletPoints(cleanText, pageRef);
    }
    
    // Apply formatting rules
    let formatted = cleanText;
    const formatting = this.gameData.formatting;
    
    // Apply game terms (italics)
    if (formatting.gameTerms) {
      const gameTermsPattern = new RegExp(
        `\\b(${formatting.gameTerms.join('|')})\\b`, 'g'
      );
      formatted = formatted.replace(gameTermsPattern, '<em>$1</em>');
    }
    
    // Apply action words (bold)
    if (formatting.actionWords) {
      const actionPattern = new RegExp(
        `\\b(${formatting.actionWords.join('|')})\\b`, 'gi'
      );
      formatted = formatted.replace(actionPattern, '<strong>$1</strong>');
    }
    
    // Apply measurements (bold)
    if (formatting.measurements) {
      formatting.measurements.forEach(pattern => {
        const regex = new RegExp(`\\b(${pattern})\\b`, 'g');
        formatted = formatted.replace(regex, '<strong>$1</strong>');
      });
    }
    
    // Apply custom rules
    if (formatting.customRules) {
      formatting.customRules.forEach(rule => {
        const regex = new RegExp(rule.pattern, rule.flags || 'g');
        formatted = formatted.replace(regex, rule.replacement);
      });
    }
    
    // Split into bullet points if multiple sentences
    const sentences = formatted.split(/(?<=[.!?])\s+(?=[A-Z])/);
    
    if (sentences.length <= 2) {
      return `<p>${formatted}</p>${pageRef}`;
    }
    
    const bulletPoints = sentences.map(sentence => 
      `<li>${sentence.trim()}</li>`
    ).join('');
    
    return `<ul>${bulletPoints}</ul>${pageRef}`;
  }

  formatBulletPoints(text, pageRef) {
    const parts = text.split('•').filter(part => part.trim());
    const introText = parts[0].trim();
    const bulletItems = parts.slice(1);
    
    const formattedIntro = this.applyBasicFormatting(introText);
    const bulletPoints = bulletItems.map(item => 
      `<li>${this.applyBasicFormatting(item.trim())}</li>`
    ).join('');
    
    return `<p>${formattedIntro}</p><ul>${bulletPoints}</ul>${pageRef}`;
  }

  applyBasicFormatting(text) {
    // Apply formatting without bullet point logic
    // Implementation similar to formatDetailText but simpler
    return text; // Simplified for brevity
  }

  // Event handling, tab switching, navigation, etc.
  bindEvents() {
    // Tab click handlers
    this.elements.tabContainer.addEventListener('click', (e) => {
      if (e.target.classList.contains('tab')) {
        this.switchTab(e.target.dataset.tab);
      }
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        this.navigate(e.key === 'ArrowUp' ? -1 : 1);
      }
    });
    
    // Button navigation
    this.elements.upButton.addEventListener('click', () => this.navigate(-1));
    this.elements.downButton.addEventListener('click', () => this.navigate(1));
  }

  // Additional methods for navigation, state management, etc.
  switchTab(tabId) { /* Implementation */ }
  navigate(direction) { /* Implementation */ }
  updateSelection() { /* Implementation */ }
  
  // Utility methods
  escapeHtml(text) { /* Implementation */ }
  showLoading() { /* Implementation */ }
  showApp() { /* Implementation */ }
  showError(message) { /* Implementation */ }
  applyCustomStyles() { /* Implementation */ }
}

// Global initialization function
async function initializeTracker(gameId) {
  const tracker = new Track0r();
  await tracker.initialize(gameId);
}

function showError(message) {
  document.getElementById('loading').style.display = 'none';
  document.getElementById('app').style.display = 'none';
  document.getElementById('error').style.display = 'block';
  document.getElementById('error-message').textContent = message;
}
```

### 5. Game-Specific Loaders

#### games/stalker.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>STALKER - Track0r</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <script>
    // Redirect to universal tracker with game parameter
    window.location.href = '../view/track0r.html?game=stalker';
  </script>
  <noscript>
    <p>This application requires JavaScript. Please enable JavaScript and try again.</p>
    <p><a href="../view/track0r.html?game=stalker">Continue to STALKER tracker</a></p>
  </noscript>
</body>
</html>
```

### 6. Migration Tools

#### tools/converter.js
```javascript
/**
 * HTML to JSON Converter
 * Extracts game data from existing HTML files
 */

class HTMLToJSONConverter {
  convertFile(htmlFilePath) {
    // Parse HTML file
    // Extract game info from title, structure
    // Convert steps and substeps to JSON format
    // Extract data-detail attributes
    // Generate formatting rules based on content
    // Output JSON file
  }

  extractSteps(htmlContent) {
    // Parse .step and .substep elements
    // Extract titles and data-detail attributes
    // Build hierarchical structure
  }

  generateFormattingRules(content) {
    // Analyze existing formatDetailText patterns
    // Extract common terms and patterns
    // Generate formatting configuration
  }
}
```

#### tools/validator.js
```javascript
/**
 * JSON Data Validator
 * Validates game data files against schema
 */

const Ajv = require('ajv');

class DataValidator {
  constructor() {
    this.ajv = new Ajv();
    this.schema = require('../data/schema.json');
  }

  validateFile(jsonFilePath) {
    // Load and validate JSON against schema
    // Check for required fields
    // Validate data integrity
    // Generate validation report
  }

  validateAllGames() {
    // Validate all JSON files in data directory
    // Generate comprehensive report
  }
}
```

### 7. Migration Strategy

#### Phase 1: Foundation (Week 1)
1. **Setup Infrastructure**
   - Create directory structure
   - Implement schema.json
   - Create universal HTML template
   - Develop core Track0r class

2. **Convert One Game**
   - Choose STALKER as pilot (most recently updated)
   - Extract data to stalker.json
   - Test universal template with STALKER data
   - Validate functionality matches original

#### Phase 2: Migration (Week 2)
1. **Convert Remaining Games**
   - Star Wars Unlimited → star_wars_unlimited.json
   - Wondrous Creatures → wondrous_creatures.json + wondrous_creatures_solo.json
   - Validate each conversion

2. **Develop Migration Tools**
   - HTML-to-JSON converter
   - Data validation utilities
   - Automated testing framework

#### Phase 3: Enhancement (Week 3)
1. **Advanced Features**
   - Game selection interface
   - Search functionality
   - Bookmark system
   - Improved mobile experience

2. **Developer Tools**
   - JSON editor interface
   - Live preview system
   - Data validation dashboard

#### Phase 4: Deployment (Week 4)
1. **Testing & QA**
   - Cross-browser testing
   - Mobile device testing
   - Performance optimization
   - Accessibility improvements

2. **Documentation**
   - Migration guide
   - API documentation
   - Data format guide
   - Contribution guidelines

### 8. Benefits Analysis

#### Development Benefits
- **Single Source of Truth**: One codebase for all games
- **Faster Development**: New games require only JSON files
- **Easier Maintenance**: Bug fixes apply to all games
- **Consistent Features**: All games get same functionality
- **Version Control**: Content changes tracked separately from code

#### User Benefits
- **Consistent Experience**: Same interface across all games
- **Better Performance**: Optimized shared codebase
- **Advanced Features**: Search, bookmarks, game comparison
- **Accessibility**: Centralized accessibility improvements
- **Mobile Experience**: Unified responsive design

#### Content Creator Benefits
- **Non-Developer Friendly**: JSON easier than HTML for game designers
- **Validation**: Schema validation prevents errors
- **Modularity**: Easy to update specific parts of games
- **Reusability**: Common patterns shared across games
- **Community Contributions**: Lower barrier to entry

### 9. Risk Mitigation

#### Technical Risks
- **JavaScript Dependency**: Fallback to static generation
- **Loading Performance**: Implement caching and optimization
- **Browser Compatibility**: Progressive enhancement approach
- **Data Corruption**: Validation and backup systems

#### Migration Risks
- **Feature Loss**: Comprehensive testing against originals
- **User Disruption**: Parallel deployment strategy
- **Data Integrity**: Automated validation throughout process
- **Rollback Plan**: Keep legacy files as backup

#### Maintenance Risks
- **Complexity**: Clear documentation and modular design
- **Developer Onboarding**: Comprehensive guides and examples
- **Schema Evolution**: Versioning and migration strategies
- **Community Adoption**: Clear contribution guidelines

### 10. Success Metrics

#### Technical Metrics
- **Code Reduction**: Target 80% reduction in duplicate code
- **Load Time**: Sub-500ms game data loading
- **Bundle Size**: Optimized for mobile bandwidth
- **Error Rate**: Zero game data loading failures

#### User Experience Metrics
- **Feature Parity**: 100% functionality preservation
- **Mobile Usability**: iPhone landscape optimization maintained
- **Accessibility**: WCAG 2.1 compliance
- **Performance**: Smooth 60fps navigation

#### Development Metrics
- **New Game Time**: Under 2 hours for complete setup
- **Bug Fix Propagation**: Single fix applies to all games
- **Feature Development**: 50% faster implementation
- **Content Updates**: Non-developer content modification

### 11. Future Roadmap

#### Short Term (3-6 months)
- Game selection dashboard
- Advanced search across all games
- Export/import custom game configurations
- Community game sharing platform

#### Medium Term (6-12 months)
- Visual game data editor
- Real-time multiplayer synchronization
- Rule enforcement automation
- Integration with digital game platforms

#### Long Term (1+ years)
- AI-powered rule interpretation
- Automated game tracker generation from rulebooks
- Cross-platform mobile app
- Board game publisher partnerships

### 12. Implementation Checklist

#### Pre-Implementation
- [ ] Review and approve architecture plan
- [ ] Set up development environment
- [ ] Create backup of existing files
- [ ] Establish testing criteria

#### Phase 1 Tasks
- [ ] Create directory structure
- [ ] Implement JSON schema
- [ ] Build universal HTML template
- [ ] Develop core JavaScript classes
- [ ] Convert STALKER to JSON format
- [ ] Test functionality parity
- [ ] Document any issues or deviations

#### Phase 2 Tasks
- [ ] Convert remaining games to JSON
- [ ] Build migration tools
- [ ] Implement validation system
- [ ] Create automated tests
- [ ] Update documentation

#### Phase 3 Tasks
- [ ] Add advanced features
- [ ] Build developer tools
- [ ] Optimize performance
- [ ] Improve accessibility

#### Phase 4 Tasks
- [ ] Comprehensive testing
- [ ] Deploy new system
- [ ] Monitor for issues
- [ ] Gather user feedback
- [ ] Plan next iterations

---

## Conclusion

This refactor plan provides a comprehensive roadmap for transforming the track0r system into a maintainable, scalable, and feature-rich platform. The data-driven approach will eliminate code duplication, improve development velocity, and enable advanced features while preserving the current user experience.

The phased migration strategy minimizes risk while ensuring continuous functionality. The proposed architecture balances simplicity with extensibility, making it accessible to both developers and content creators.

**Next Steps**: Review this plan, approve the approach, and begin Phase 1 implementation with the STALKER game conversion. 