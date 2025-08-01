#!/usr/bin/env python3
"""
Markdown Image Injector Tool
Injects PNG images into markdown files based on filename matching.
"""

import os
import sys
import argparse
import re
import base64
from pathlib import Path
from PIL import Image
import io

def encode_image_to_base64(image_path):
    """Convert image to base64 string for inline embedding."""
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            encoded = base64.b64encode(image_data).decode('utf-8')
            
            # Determine image format
            img = Image.open(image_path)
            format_name = img.format.lower()
            
            return f"data:image/{format_name};base64,{encoded}"
    except Exception as e:
        print(f"Error encoding {image_path}: {e}")
        return None

def inject_images_into_markdown(md_file_path, images_dir, output_file=None, 
                               pattern_type='exact', image_size='small', 
                               position='inline', encoding='base64'):
    """
    Inject images into markdown file based on filename matching.
    
    Args:
        md_file_path (str): Path to markdown file
        images_dir (str): Directory containing PNG images
        output_file (str): Output file path (if None, overwrites original)
        pattern_type (str): 'exact', 'contains', 'regex'
        image_size (str): 'small', 'medium', 'large' or custom size like '100x50'
        position (str): 'inline', 'above', 'below'
        encoding (str): 'base64' or 'file'
    """
    
    # Read markdown file
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return False
    
    # Get list of available images
    images_dir = Path(images_dir)
    if not images_dir.exists():
        print(f"Images directory not found: {images_dir}")
        return False
    
    available_images = {}
    for img_file in images_dir.glob("*.png"):
        available_images[img_file.stem] = img_file
    
    print(f"Found {len(available_images)} images in {images_dir}")
    
    # Process content line by line
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        
        # Look for potential image injection points
        # Common patterns: [icon], {icon}, <icon>, or just icon names
        potential_icons = re.findall(r'\[([^\]]+)\]|\{([^}]+)\}|<([^>]+)>|(\b\w+_icon\b|\bicon_\w+\b)', line)
        
        for match in potential_icons:
            icon_name = next((name for name in match if name), None)
            if not icon_name:
                continue
            
            # Try to find matching image
            matching_image = None
            
            if pattern_type == 'exact':
                if icon_name in available_images:
                    matching_image = available_images[icon_name]
            
            elif pattern_type == 'contains':
                for img_name, img_path in available_images.items():
                    if icon_name.lower() in img_name.lower() or img_name.lower() in icon_name.lower():
                        matching_image = img_path
                        break
            
            elif pattern_type == 'regex':
                for img_name, img_path in available_images.items():
                    if re.search(icon_name, img_name, re.IGNORECASE):
                        matching_image = img_path
                        break
            
            if matching_image:
                # Generate image markdown
                if encoding == 'base64':
                    base64_data = encode_image_to_base64(matching_image)
                    if base64_data:
                        if position == 'inline':
                            # Replace the icon reference with inline image
                            img_markdown = f"![{icon_name}]({base64_data})"
                            new_lines[-1] = line.replace(f"[{icon_name}]", img_markdown)
                            new_lines[-1] = new_lines[-1].replace(f"{{{icon_name}}}", img_markdown)
                            new_lines[-1] = new_lines[-1].replace(f"<{icon_name}>", img_markdown)
                        else:
                            # Add image above or below the line
                            img_markdown = f"![{icon_name}]({base64_data})"
                            if position == 'above':
                                new_lines.insert(len(new_lines) - 1, img_markdown)
                            else:  # below
                                new_lines.append(img_markdown)
                
                elif encoding == 'file':
                    # Use relative file path
                    relative_path = matching_image.relative_to(Path(md_file_path).parent)
                    img_markdown = f"![{icon_name}]({relative_path})"
                    
                    if position == 'inline':
                        new_lines[-1] = line.replace(f"[{icon_name}]", img_markdown)
                        new_lines[-1] = new_lines[-1].replace(f"{{{icon_name}}}", img_markdown)
                        new_lines[-1] = new_lines[-1].replace(f"<{icon_name}>", img_markdown)
                    else:
                        if position == 'above':
                            new_lines.insert(len(new_lines) - 1, img_markdown)
                        else:  # below
                            new_lines.append(img_markdown)
                
                print(f"Injected image: {matching_image.name} for '{icon_name}'")
    
    # Write output
    output_path = output_file if output_file else md_file_path
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"Updated markdown saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Inject PNG images into markdown files')
    parser.add_argument('markdown_file', help='Path to the markdown file')
    parser.add_argument('images_dir', help='Directory containing PNG images')
    parser.add_argument('-o', '--output', help='Output file path (default: overwrite original)')
    parser.add_argument('-p', '--pattern', choices=['exact', 'contains', 'regex'], default='contains',
                       help='Matching pattern type (default: contains)')
    parser.add_argument('-s', '--size', default='small',
                       help='Image size: small, medium, large, or custom like 100x50')
    parser.add_argument('-pos', '--position', choices=['inline', 'above', 'below'], default='inline',
                       help='Image position relative to text (default: inline)')
    parser.add_argument('-e', '--encoding', choices=['base64', 'file'], default='base64',
                       help='Image encoding method (default: base64)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.markdown_file):
        print(f"Error: Markdown file '{args.markdown_file}' not found")
        sys.exit(1)
    
    success = inject_images_into_markdown(
        args.markdown_file,
        args.images_dir,
        args.output,
        args.pattern,
        args.size,
        args.position,
        args.encoding
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 