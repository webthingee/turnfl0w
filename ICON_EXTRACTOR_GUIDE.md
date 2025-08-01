# Icon Extractor Tool Guide

This tool automatically detects and extracts individual icons from larger images that contain multiple icons.

## **Installation**

Install the additional dependencies:
```bash
/usr/bin/python3 -m pip install opencv-python numpy
```

## **How It Works**

The tool uses computer vision to automatically detect where individual icons are located in your image and extract them as separate files.

### **Detection Methods:**

1. **Contour Detection** (Default): Finds distinct shapes/objects in the image
2. **Grid Detection**: Assumes icons are arranged in a regular grid
3. **Template Matching**: Matches against known icon templates

## **Usage Examples**

### **Basic Usage:**
```bash
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg -o extracted_icons
```

### **With Custom Settings:**
```bash
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg \
  -o extracted_icons \
  -m contour \
  --min-size 30 \
  --max-size 150 \
  -t 0.7 \
  -p 10
```

### **Grid-based Detection:**
```bash
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg \
  -o extracted_icons \
  -m grid
```

## **Parameters Explained:**

- `-o, --output`: Where to save extracted icons
- `-m, --method`: Detection method (contour, grid, template)
- `--min-size`: Minimum icon size in pixels (default: 20)
- `--max-size`: Maximum icon size in pixels (default: 200)
- `-t, --threshold`: Detection sensitivity 0-1 (default: 0.8)
- `-p, --padding`: Extra pixels around each icon (default: 5)

## **What You'll Get:**

If your `StalkerIcons.jpg` contains multiple icons, you'll get:
```
extracted_icons/
├── icon_000.png  (first detected icon)
├── icon_001.png  (second detected icon)
├── icon_002.png  (third detected icon)
└── ... (more icons)
```

## **Troubleshooting:**

### **If it detects too many small objects:**
```bash
# Increase minimum size
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg --min-size 50
```

### **If it misses some icons:**
```bash
# Lower the threshold (more sensitive)
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg -t 0.6
```

### **If icons are arranged in a grid:**
```bash
# Use grid detection
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg -m grid
```

### **If you need more padding around icons:**
```bash
# Add more padding
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg -p 15
```

## **Complete Workflow:**

```bash
# 1. Extract individual icons
/usr/bin/python3 icon_extractor.py StalkerIcons.jpg -o extracted_icons

# 2. Rename them to match your references
mv extracted_icons/icon_000.png extracted_icons/willpower_icon.png
mv extracted_icons/icon_001.png extracted_icons/attack_icon.png
mv extracted_icons/icon_002.png extracted_icons/defense_icon.png

# 3. Inject into markdown
/usr/bin/python3 markdown_image_injector.py tracker.md extracted_icons/ -p contains
```

## **Tips for Best Results:**

1. **Clear Background**: Icons should have good contrast with the background
2. **Consistent Sizing**: Icons should be roughly the same size
3. **Good Spacing**: Icons should be well-separated from each other
4. **High Quality**: Use high-resolution images for better detection

## **Example Output:**

```
Extracted: icon_000.png (64x64) at (10,10)
Extracted: icon_001.png (64x64) at (80,10)
Extracted: icon_002.png (64x64) at (150,10)
Extracted: icon_003.png (64x64) at (10,80)
Extracted: icon_004.png (64x64) at (80,80)
Extracted: icon_005.png (64x64) at (150,80)

Extracted 6 icons
```

This should give you exactly what you wanted - automatic detection and extraction of individual icons from your larger image! 