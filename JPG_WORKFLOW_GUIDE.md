# Working with JPG Files - Complete Guide

Yes, you can absolutely work with JPG files! Here are all the options:

## **Option 1: Direct JPG Processing (Recommended)**

Use the new `image_extractor.py` tool I just created:

### **Process Individual JPG Files:**
```bash
# Process a single JPG file
python image_extractor.py icon.jpg -o processed_icons

# Resize and convert to PNG
python image_extractor.py icon.jpg -r 100x100 -f PNG -o processed_icons

# Crop a specific area
python image_extractor.py icon.jpg -c 10,10,90,90 -o processed_icons
```

### **Process Directory of JPGs:**
```bash
# Process all JPGs in a directory
python image_extractor.py icons_folder/ -o processed_icons

# Resize all to 50x50 pixels
python image_extractor.py icons_folder/ -r 50x50 -o processed_icons

# Convert all to PNG format
python image_extractor.py icons_folder/ -f PNG -o processed_icons
```

## **Option 2: Convert JPGs to PNGs First**

If you have JPG icons and want to use them with the markdown injector:

```bash
# Convert JPG to PNG
python image_extractor.py icon.jpg -f PNG -o png_icons

# Convert entire directory
python image_extractor.py jpg_icons/ -f PNG -o png_icons
```

## **Option 3: Manual Conversion**

You can also use standard tools:

```bash
# Using ImageMagick (if installed)
convert icon.jpg icon.png

# Using sips (macOS built-in)
sips -s format png icon.jpg --out icon.png

# Batch convert with sips
for file in *.jpg; do sips -s format png "$file" --out "${file%.jpg}.png"; done
```

## **Complete JPG Workflow Example:**

### **Scenario: You have JPG icons from a rulebook**

```bash
# 1. Process your JPG icons
python image_extractor.py rulebook_icons/ -r 32x32 -f PNG -o processed_icons

# 2. Rename them to match your references
mv processed_icons/icon1.png processed_icons/willpower_icon.png
mv processed_icons/icon2.png processed_icons/attack_icon.png
mv processed_icons/icon3.png processed_icons/defense_icon.png

# 3. Inject into markdown
python markdown_image_injector.py tracker_description.md processed_icons/ -p contains
```

## **JPG vs PNG Considerations:**

### **JPG Advantages:**
- Smaller file sizes
- Good for photographs
- Widely supported

### **PNG Advantages:**
- Lossless compression
- Better for icons and graphics
- Supports transparency
- Better for web use

### **For Icons:**
- **PNG is usually better** for icons because:
  - Icons are usually graphics, not photos
  - PNG preserves sharp edges
  - PNG supports transparency
  - Smaller file sizes for simple graphics

## **Advanced JPG Processing:**

### **Resize Options:**
```bash
# Resize to specific dimensions
python image_extractor.py icon.jpg -r 100x50

# Resize maintaining aspect ratio (max dimension)
python image_extractor.py icon.jpg -r 100

# Resize to square
python image_extractor.py icon.jpg -r 64x64
```

### **Cropping Options:**
```bash
# Crop specific area (left,top,right,bottom)
python image_extractor.py icon.jpg -c 10,10,90,90

# Crop to center
python image_extractor.py icon.jpg -c 25,25,75,75
```

### **Format Conversion:**
```bash
# JPG to PNG
python image_extractor.py icon.jpg -f PNG

# PNG to JPG
python image_extractor.py icon.png -f JPEG

# Convert with quality settings
python image_extractor.py icon.png -f JPEG -o high_quality/
```

## **Real-World Example:**

### **You have JPG icons from a rulebook scan:**

```bash
# 1. Extract and process the JPGs
python image_extractor.py rulebook_scan.jpg -r 32x32 -f PNG -o icons

# 2. The tool will create: icons/rulebook_scan.png

# 3. Rename to match your references
mv icons/rulebook_scan.png icons/willpower_icon.png

# 4. Create markdown with references
echo "Willpower strength [willpower_icon] represents questing contribution." > tracker.md

# 5. Inject the icons
python markdown_image_injector.py tracker.md icons/ -p contains

# 6. Result: tracker.md now contains the embedded icon
```

## **Supported Formats:**

The tools support:
- **Input:** JPG, JPEG, PNG, BMP, TIFF, WEBP, PDF
- **Output:** PNG, JPEG, BMP, TIFF, WEBP

## **Tips for JPG Icons:**

1. **Use PNG for output** - Better for icons and web use
2. **Resize appropriately** - 32x32 or 64x64 for small icons
3. **Maintain aspect ratio** - Use square dimensions for consistent icons
4. **Consider transparency** - PNG supports transparent backgrounds
5. **Test quality** - Make sure icons are clear at small sizes

## **Quick Start with JPGs:**

```bash
# 1. Process your JPG icons
python image_extractor.py your_icons.jpg -r 32x32 -f PNG -o processed

# 2. Rename to match your needs
mv processed/your_icons.png processed/willpower_icon.png

# 3. Inject into your markdown
python markdown_image_injector.py your_tracker.md processed/ -p contains
```

This gives you the same workflow as PDFs, but starting with JPG files! 