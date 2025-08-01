#!/usr/bin/env python3
"""
Icon Extractor Tool
Automatically detects and extracts individual icons from larger images.
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
import cv2

def detect_icons(image_path, output_dir, min_size=20, max_size=200, 
                threshold=0.8, padding=5, method='contour'):
    """
    Detect and extract individual icons from an image.
    
    Args:
        image_path (str): Path to image containing multiple icons
        output_dir (str): Directory to save extracted icons
        min_size (int): Minimum icon size in pixels
        max_size (int): Maximum icon size in pixels
        threshold (float): Detection threshold (0-1)
        padding (int): Padding around detected icons
        method (str): Detection method ('contour', 'template', 'grid')
    """
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return False
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if method == 'contour':
            icons = detect_by_contours(gray, min_size, max_size, threshold, padding)
        elif method == 'grid':
            icons = detect_by_grid(gray, min_size, max_size, padding)
        elif method == 'template':
            icons = detect_by_template_matching(gray, min_size, max_size, threshold, padding)
        else:
            print(f"Unknown method: {method}")
            return False
        
        # Extract and save icons
        extracted_count = 0
        for i, (x, y, w, h) in enumerate(icons):
            # Add padding
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)
            
            # Extract icon
            icon = image[y1:y2, x1:x2]
            
            # Save icon
            icon_filename = f"icon_{i:03d}.png"
            icon_path = os.path.join(output_dir, icon_filename)
            cv2.imwrite(icon_path, icon)
            
            print(f"Extracted: {icon_filename} ({w}x{h}) at ({x},{y})")
            extracted_count += 1
        
        print(f"\nExtracted {extracted_count} icons")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def detect_by_contours(gray, min_size, max_size, threshold, padding):
    """Detect icons using contour detection."""
    # Apply threshold to create binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    icons = []
    for contour in contours:
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter by size
        if min_size <= w <= max_size and min_size <= h <= max_size:
            # Calculate contour area ratio to filter out noise
            area = cv2.contourArea(contour)
            rect_area = w * h
            if rect_area > 0 and area / rect_area > threshold:
                icons.append((x, y, w, h))
    
    return icons

def detect_by_grid(gray, min_size, max_size, padding):
    """Detect icons using grid-based approach."""
    height, width = gray.shape
    
    # Estimate grid size based on image dimensions
    grid_size = min(width, height) // 4  # Assume 4x4 grid
    
    icons = []
    for row in range(4):
        for col in range(4):
            x = col * grid_size
            y = row * grid_size
            w = min(grid_size, width - x)
            h = min(grid_size, height - y)
            
            if w >= min_size and h >= min_size:
                icons.append((x, y, w, h))
    
    return icons

def detect_by_template_matching(gray, min_size, max_size, threshold, padding):
    """Detect icons using template matching (placeholder)."""
    # This would require template images to match against
    # For now, return empty list
    return []

def auto_detect_grid_size(image_path):
    """Automatically detect grid size from image."""
    image = cv2.imread(image_path)
    if image is None:
        return 4, 4  # Default
    
    height, width = image.shape[:2]
    
    # Simple heuristic: assume square grid
    # Look for common grid sizes
    for grid_size in [2, 3, 4, 5, 6]:
        if width % grid_size == 0 and height % grid_size == 0:
            return grid_size, grid_size
    
    # Fallback: estimate based on image size
    avg_size = min(width, height) // 4
    return 4, 4

def main():
    parser = argparse.ArgumentParser(description='Extract individual icons from larger images')
    parser.add_argument('image_path', help='Path to image containing multiple icons')
    parser.add_argument('-o', '--output', default='extracted_icons', 
                       help='Output directory (default: extracted_icons)')
    parser.add_argument('-m', '--method', choices=['contour', 'grid', 'template'], default='contour',
                       help='Detection method (default: contour)')
    parser.add_argument('--min-size', type=int, default=20,
                       help='Minimum icon size in pixels (default: 20)')
    parser.add_argument('--max-size', type=int, default=200,
                       help='Maximum icon size in pixels (default: 200)')
    parser.add_argument('-t', '--threshold', type=float, default=0.8,
                       help='Detection threshold 0-1 (default: 0.8)')
    parser.add_argument('-p', '--padding', type=int, default=5,
                       help='Padding around detected icons (default: 5)')
    parser.add_argument('--auto-grid', action='store_true',
                       help='Automatically detect grid size')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file '{args.image_path}' not found")
        sys.exit(1)
    
    success = detect_icons(
        args.image_path,
        args.output,
        args.min_size,
        args.max_size,
        args.threshold,
        args.padding,
        args.method
    )
    
    if success:
        print(f"\nIcons extracted to: {args.output}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 