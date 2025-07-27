# Track0r Creation Guide

A comprehensive guide for AI agents to create turn order tracking applications from game rulebooks.

## Overview

Track0rs are HTML-based turn tracking applications that help players navigate complex game sequences step-by-step. They provide detailed, rule-referenced guidance for each phase of gameplay.

## Table of Contents

1. [Rulebook Analysis Phase](#rulebook-analysis-phase)
2. [Structure Design](#structure-design)
3. [Content Creation](#content-creation)
4. [Implementation](#implementation)
5. [Quality Assurance](#quality-assurance)
6. [Examples & Templates](#examples--templates)

## Rulebook Analysis Phase

### Step 1: Initial Rulebook Assessment

**Goal**: Understand the game's core mechanics and turn structure.

**Actions**:
1. **Read overview sections** to understand basic gameplay flow
2. **Identify key phases** - look for terms like "round", "turn", "phase", "step"
3. **Search for turn structure** - use grep/search for terms:
   - `turn|phase|round|step|sequence`
   - `player.*turn|active.*player`
   - `begin|start|end|finish`

**Questions to Answer**:
- Is this a turn-based or phase-based game?
- How many players take actions simultaneously vs. sequentially?
- What are the main phases of a game round?
- Are there setup phases separate from gameplay?

### Step 2: Deep Dive Analysis

**Goal**: Map out the complete game flow with precise rule references.

**Actions**:
1. **Extract exact phase names** and their order
2. **Identify sub-steps** within each phase
3. **Note rule page references** for each step
4. **Find decision points** where players must choose actions
5. **Identify simultaneous vs. sequential actions**

**Key Areas to Focus On**:
- **Setup procedures** (deck building, initial placement, resource allocation)
- **Action selection** (what choices do players have?)
- **Turn passing** (when does control switch between players?)
- **Phase transitions** (what triggers moving to the next phase?)
- **End conditions** (how does the game/round end?)

### Step 3: Player Action Mapping

**Goal**: Understand when and how players make decisions.

**Questions to Answer**:
- When do players play cards/take actions?
- What are the available action types?
- How do players know whose turn it is?
- What happens when players pass?
- Are there mandatory vs. optional actions?

## Structure Design

### Core Principles

1. **Player-Centric Flow**: Structure should reflect actual player decision points
2. **Clear Action Points**: Make it obvious when players need to do something
3. **Logical Grouping**: Related actions should be grouped together
4. **Progressive Detail**: Main phases → sub-phases → specific actions

### Phase Organization Patterns

#### Pattern 1: Sequential Phases (like STALKER)
```
1. Event Phase
   1.1 Draw Event
   1.2 Apply Effects
2. Player Phase
   2.1 Player 1 Turn
   2.2 Player 2 Turn
3. Cleanup Phase
   3.1 Remove Tokens
   3.2 Ready Cards
```

#### Pattern 2: Alternating Actions (like Star Wars Unlimited)
```
1. Action Phase
   1.1 Start of Phase
   1.2 Active Player Takes Action
   1.3 Switch Active Player
   1.4 Continue Until Both Pass
   1.5 End of Phase
2. Regroup Phase
   2.1 Draw Cards
   2.2 Resource Cards
   2.3 Ready Cards
```

#### Pattern 3: Simultaneous + Sequential Hybrid
```
1. Planning Phase (Simultaneous)
   1.1 All Players Choose Actions
   1.2 Reveal Simultaneously
2. Resolution Phase (Sequential)
   2.1 Resolve in Initiative Order
   2.2 Apply Effects
```

### Tab Structure Decision Tree

**Use Separate Tabs When**:
- Setup is complex (5+ steps)
- Setup is only done once per game
- Different game modes exist
- Rules reference is needed

**Common Tab Structures**:
- **Setup + Turn Flow** (most common)
- **Setup + Turn Flow + Reference**
- **Basic + Advanced Rules**

## Content Creation

### Writing Effective Step Descriptions

#### Main Step (Phase Level)
```
Format: "Brief overview of what happens in this phase. Key player actions or decisions. Overall purpose and timing. (Rule Reference)"

Example: "The action phase is where players take turns playing cards, attacking, and using abilities. The player with the initiative counter takes the first action. Players alternate taking one action at a time until both players pass consecutively. This is the main gameplay phase where most strategic decisions happen. (Comprehensive Rules 5.4)"
```

#### Sub-Step (Action Level)
```
Format: "Specific action to take. Who does it and when. Clear instructions on execution. Important timing or sequencing notes. (Rule Reference)"

Example: "The player with the initiative counter becomes the active player and takes the first action. They must choose one of five actions: Play a Card (pay cost, put unit/upgrade into play or resolve event), Attack With a Unit (exhaust unit to attack enemy unit or base), Use an Action Ability (pay cost and resolve effect), Take the Initiative (gain initiative, end your actions for the round), or Pass (do nothing, opponent becomes active player). (Comprehensive Rules 5.4.1.b)"
```

#### Enhancing Clarity: Breaking Down Long Descriptions

**Problem**: Single long sentences reduce readability and make it hard to scan options quickly.

**Solution**: Break down complex actions into separate, clear statements.

**Bad Example:**
```
"Choose exactly one of the four Basic Actions: Place a Crew Member (deploy worker to gather resources/cards), Play a Card(s) (play up to 2 cards from hand by paying costs), Complete an Achievement (claim achievement slot for rewards), or Recharge (return all crew when all 3 deployed)."
```

**Good Example:**
```
"Choose exactly one of the four Basic Actions available to you on your turn. Place a Crew Member: deploy a worker on the map to gather resources or cards from adjacent Habitats. Play a Card(s): play up to 2 cards from your hand by paying their resource costs. Complete an Achievement: claim an available achievement slot for immediate rewards and end-game points. Recharge: return all 3 crew members to your board when they're all deployed on the map."
```

**Why This Works:**
- The formatting function automatically creates bullet points from separate sentences
- Each option gets its own clear explanation
- Players can quickly scan available choices
- Information is easier to digest during gameplay

#### Advanced Formatting: Explicit Bullet Points

For complex choice lists, use explicit bullet points (•) to ensure proper visual hierarchy.

**When to Use:**
- Multiple distinct options that players must choose between
- Action lists where each item needs clear separation
- Any time readability would benefit from obvious visual structure

**Implementation:**
```
"Introductory explanation that sets context. • First Option: detailed explanation of what this choice does. • Second Option: detailed explanation of the alternative. • Third Option: additional choice with clear description."
```

**Enhanced JavaScript Support:**
The formatting function should detect explicit bullet points and create proper HTML structure:
```javascript
// Check for explicit bullet points first
if (cleanText.includes('•')) {
  let parts = cleanText.split('•').filter(part => part.trim());
  let introText = parts[0].trim();
  let bulletItems = parts.slice(1);
  
  // Format intro as paragraph, bullet items as <li> elements
  return `<p>${formattedIntro}</p><ul>${bulletPoints}</ul>${pageRef}`;
}
```

**Visual Result:**
- Intro text appears as a normal paragraph
- Each bullet item gets proper indentation and spacing
- Players can quickly scan available options
- Clear visual hierarchy improves decision-making speed

### Rule Reference Format

**For Comprehensive Rules**: `(Comprehensive Rules X.Y.Z)`
**For Rulebook Pages**: `(Rulebook p. XX)`
**For Quick Reference**: `(Quick Rules p. XX)`
**For Multiple Sources**: `(Rulebook p. 30, 35)`

### Content Formatting Guidelines

#### Text Enhancement Patterns
```javascript
// Game-specific terms (italics)
.replace(/\b(initiative counter|active player|action phase)\b/g, '<em>$1</em>')

// Important mechanics (bold)
.replace(/\b(immediately|must|cannot|may|exhaust|ready)\b/gi, '<strong>$1</strong>')

// Numbers and quantities (bold)
.replace(/\b(\d+\s*HP|\d+\s*cards?|\d+\s*damage)\b/g, '<strong>$1</strong>')
```

#### Key Terms to Emphasize
- **Game phases**: action phase, regroup phase, cleanup phase
- **Player states**: active player, initiative, exhausted, ready
- **Action types**: play card, attack, pass, activate ability
- **Timing words**: immediately, must, may, cannot, before, after
- **Quantities**: numbers with units (3 damage, 2 cards, 30 HP)

## Implementation

### Technical Stack

**Required Files**:
- `track0r_[GAME].html` - Main application
- `[game]_rules.txt` - Processed rulebook text (if needed)

**Technologies**:
- HTML5 semantic structure
- CSS3 with responsive design
- Vanilla JavaScript (no dependencies)

### HTML Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Game Name] - Round Order</title>
  <style>
    /* Base styles + responsive design */
  </style>
</head>
<body>
  <div class="navigation">
    <button id="upButton">↑</button>
    <button id="downButton">↓</button>
  </div>
  
  <!-- Tabs (if needed) -->
  <div class="tabs">
    <button class="tab active" data-tab="turn-flow">Turn Flow</button>
    <button class="tab" data-tab="setup">Setup</button>
  </div>
  
  <!-- Content containers -->
  <div class="tab-content active" id="turn-flow">
    <div class="container">
      <div class="selector" id="list">
        <!-- Steps go here -->
      </div>
      <div class="details" id="details">
        <h2>Details</h2>
        <p id="detailText"></p>
      </div>
    </div>
  </div>
  
  <script>
    /* Navigation and formatting logic */
  </script>
</body>
</html>
```

### CSS Requirements

#### Core Layout
- **Flexbox-based responsive design**
- **50/50 split** between step list and details
- **Mobile optimization** for iPhone landscape (max-width: 926px)
- **Consistent spacing** and typography

#### Visual Hierarchy
```css
.step {
  /* Main phase styling */
  font-size: 1rem;
  padding: 8px 15px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 0 3px rgba(0,0,0,0.1);
}

.substep {
  /* Sub-action styling */
  font-size: 0.8rem;
  margin-left: 15px;
  padding: 6px 12px;
  background: #f8f8f8;
  border-radius: 4px;
}

.selected {
  /* Active selection */
  background-color: #4a90e2;
  color: white;
  font-weight: bold;
}
```

### JavaScript Functionality

#### Required Features
1. **Keyboard navigation** (arrow keys)
2. **Button navigation** (up/down arrows)
3. **Text formatting** (automatic bullet points, emphasis)
4. **Smooth scrolling** for selected items
5. **Tab switching** (if multiple tabs)

#### Core Functions Template
```javascript
function updateSelection() {
  // Update visual selection
  // Format detail text
  // Scroll to selected item
}

function formatDetailText(text) {
  // Extract rule references
  // Split into sentences
  // Apply emphasis patterns
  // Return formatted HTML
}

// Event handlers for navigation
// Tab switching logic (if needed)
```

## Quality Assurance

### Content Validation Checklist

**Structure Review**:
- [ ] Does the flow match actual gameplay?
- [ ] Are decision points clear?
- [ ] Is the player action sequence obvious?
- [ ] Are simultaneous vs. sequential actions distinguished?

**Detail Quality**:
- [ ] Every step has a rule reference
- [ ] Descriptions are action-oriented ("Do X" not "X happens")
- [ ] Game-specific terminology is used correctly
- [ ] Important mechanics are emphasized

**Usability Testing**:
- [ ] Can a new player follow the steps?
- [ ] Are setup and gameplay clearly separated?
- [ ] Do navigation controls work smoothly?
- [ ] Is mobile layout functional?

### Common Issues to Avoid

1. **Passive Voice**: "Cards are drawn" → "Each player draws 2 cards"
2. **Vague Timing**: "During this phase" → "Starting with the active player"
3. **Missing Decisions**: Not showing what choices players have
4. **Unclear Transitions**: Not explaining when phases end
5. **Abstract Steps**: "Process effects" → "Resolve each triggered ability"
6. **Long Sentence Lists**: Break down complex option lists into separate sentences for better bullet point formatting
7. **Cramped Information**: When describing multiple choices, give each option its own clear explanation rather than parenthetical notes
8. **Poor Visual Hierarchy**: Use explicit bullet points (•) for choice lists instead of relying on sentence splitting
9. **Missing JavaScript Support**: Ensure formatting functions can handle both automatic sentence splitting and explicit bullet points

## Examples & Templates

### Sample Step Formats

#### Setup Step
```html
<div class="substep" data-detail="Each player shuffles their 50-card deck thoroughly. Draw 6 cards from your deck to form your starting hand. Keep your deck face-down in easy reach - you'll draw from it during the game. (Quickstart Rules p. 3)">1.4 Shuffle Deck & Draw Starting Hand</div>
```

#### Action Selection Step
```html
<div class="substep" data-detail="The player with the initiative counter becomes the active player and takes the first action. They must choose one of five actions: Play a Card (pay cost, put unit/upgrade into play or resolve event), Attack With a Unit (exhaust unit to attack enemy unit or base), Use an Action Ability (pay cost and resolve effect), Take the Initiative (gain initiative, end your actions for the round), or Pass (do nothing, opponent becomes active player). (Comprehensive Rules 5.4.1.b)">1.2 Active Player Takes Action</div>
```

#### Cleanup Step
```html
<div class="substep" data-detail="Remove all Radiation (☢️) and Light (🔦) tokens from the Mission Map. These represent temporary environmental effects that dissipate over time. This cleanup step prepares the map for the next round. (Rulebook p. 35)">3.3 Discard all ☢️ and 🔦 from the Map</div>
```

### Game Type Templates

#### Card Game Template
1. **Setup Phase** (separate tab)
   - Deck preparation
   - Initial hand
   - Starting resources
2. **Action Phase**
   - Player turns with action choices
   - Card play timing
   - Attack sequences
3. **Cleanup/End Phase**
   - Resource management
   - Card draw
   - Status updates

#### Board Game Template
1. **Setup Phase** (separate tab)
   - Board setup
   - Component placement
   - Player initialization
2. **Round Phases**
   - Planning/Selection
   - Action resolution
   - Movement/Combat
3. **Maintenance Phase**
   - Cleanup
   - Preparation for next round

### Formatting Pattern Examples

```javascript
// Card game terms
.replace(/\b(hand|deck|discard|graveyard|battlefield)\b/g, '<em>$1</em>')
.replace(/\b(draw|play|cast|activate)\b/gi, '<strong>$1</strong>')

// Board game terms  
.replace(/\b(board|hex|space|zone|area)\b/g, '<em>$1</em>')
.replace(/\b(move|place|remove|rotate)\b/gi, '<strong>$1</strong>')

// General game terms
.replace(/\b(turn|phase|round|step)\b/g, '<em>$1</em>')
.replace(/\b(must|may|cannot|immediately)\b/gi, '<strong>$1</strong>')
```

## Success Metrics

A successful track0r should:

1. **Reduce cognitive load** - Players can focus on strategy, not rules lookup
2. **Eliminate rule disputes** - Clear references resolve questions quickly  
3. **Speed up gameplay** - No more flipping through rulebooks mid-game
4. **Lower learning curve** - New players can join games faster
5. **Work on mobile** - Functional during tabletop play

## Final Notes

- **Start simple** - Basic structure first, then enhance
- **Test with actual gameplay** - Walk through real scenarios
- **Prioritize clarity** over completeness in early versions
- **Use consistent terminology** from the official rules
- **Include strategic tips** sparingly, focus on procedures

The goal is to create a digital assistant that makes complex games more accessible while maintaining rule accuracy and providing a smooth user experience. 