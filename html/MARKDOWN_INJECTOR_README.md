# Markdown Image Injector Tool

Automatically inject PNG images into markdown files based on filename matching.

## Features

- **Multiple matching patterns**: exact, contains, regex
- **Flexible positioning**: inline, above, below text
- **Two encoding methods**: base64 (embedded) or file paths
- **Smart icon detection**: recognizes `[icon]`, `{icon}`, `<icon>`, or icon names

## Installation

Uses the same dependencies as the PDF extractor:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Inject images using contains matching (default):
```bash
python markdown_image_injector.py document.md images/
```

### Advanced Options

```bash
python markdown_image_injector.py document.md images/ \
  -p contains \           # Pattern type: exact, contains, regex
  -pos inline \          # Position: inline, above, below
  -e base64 \            # Encoding: base64, file
  -o output.md           # Output file
```

## Pattern Types

### 1. Contains (Default)
Matches if icon name is contained in filename or vice versa:
- Icon: `[willpower]` → matches `willpower_icon.png`
- Icon: `[attack]` → matches `attack_strength.png`

### 2. Exact
Exact filename match:
- Icon: `[willpower_icon]` → matches `willpower_icon.png`

### 3. Regex
Regular expression matching:
- Icon: `[w.*power]` → matches `willpower_icon.png`

## Icon Reference Formats

The tool recognizes these patterns in your markdown:

```markdown
# These will be replaced with images:
[willpower_icon]
{attack_icon}
<defense_icon>
willpower_icon
icon_attack
```

## Examples

### Example 1: LOTR LCG Icons

If you have these images:
- `willpower_icon.png`
- `attack_icon.png` 
- `defense_icon.png`
- `threat_icon.png`

And your markdown contains:
```markdown
Willpower strength (Ò) represents a character's contribution to questing.
Attack strength (Û) represents damage dealt in combat.
Defense strength (Ú) represents damage reduction.
```

Run:
```bash
python markdown_image_injector.py lotr_rules.md icons/ -p contains
```

Result:
```markdown
Willpower strength ![willpower_icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...) represents a character's contribution to questing.
Attack strength ![attack_icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...) represents damage dealt in combat.
Defense strength ![defense_icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...) represents damage reduction.
```

### Example 2: Game Phase Icons

Images: `resource_phase.png`, `planning_phase.png`, `quest_phase.png`

Markdown:
```markdown
## Game Phases

1. [resource_phase] - Gain resources and draw cards
2. [planning_phase] - Play ally and attachment cards  
3. [quest_phase] - Commit characters to quest
```

### Example 3: Action Window Icons

Images: `action_window.png`, `response_window.png`

Markdown:
```markdown
During {action_window} players can play cards and use abilities.
{response_window} abilities can be triggered after specific events.
```

## Use Cases for Trackers

### 1. Icon Integration in HTML Trackers

Extract icons from rulebooks, then inject them into your tracker descriptions:

```bash
# Extract icons from rulebook
python pdf_image_extractor.py rulebook.pdf -m embedded -o icons

# Inject into tracker markdown
python markdown_image_injector.py tracker_description.md icons/ -p contains
```

### 2. Enhanced Rule References

Add visual icons to rule explanations:

```markdown
# Before injection:
The Ò symbol indicates willpower strength.

# After injection:
The ![willpower_icon](data:image/png;base64,...) symbol indicates willpower strength.
```

### 3. Phase-Specific Icons

Add phase icons to turn trackers:

```markdown
# Before:
## Resource Phase
Gain 1 resource per hero.

# After:
## ![resource_phase](data:image/png;base64,...) Resource Phase
Gain 1 resource per hero.
```

## Command Line Options

```bash
python markdown_image_injector.py <markdown_file> <images_dir> [options]

Options:
  -o, --output FILE     Output file path (default: overwrite original)
  -p, --pattern TYPE    Matching pattern: exact, contains, regex (default: contains)
  -s, --size SIZE       Image size: small, medium, large, or custom like 100x50
  -pos, --position POS  Image position: inline, above, below (default: inline)
  -e, --encoding ENC    Encoding method: base64, file (default: base64)
```

## Integration with PDF Extractor

Complete workflow:

```bash
# 1. Extract images from rulebook
python pdf_image_extractor.py rulebook.pdf -m embedded -o extracted_icons

# 2. Manually crop/rename icons as needed
# (rename to match your icon references)

# 3. Inject icons into markdown
python markdown_image_injector.py tracker_description.md extracted_icons/ -p contains

# 4. Use the enhanced markdown in your trackers
```

## Tips

1. **Naming Convention**: Use descriptive filenames like `willpower_icon.png`, `attack_strength.png`

2. **Icon References**: Use consistent patterns like `[icon_name]` or `{icon_name}`

3. **Base64 vs Files**: 
   - Use `base64` for self-contained documents
   - Use `file` for web applications with proper file structure

4. **Positioning**:
   - `inline` for small icons next to text
   - `above`/`below` for larger explanatory images 