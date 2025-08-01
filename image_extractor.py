#!/usr/bin/env python3
"""
General Image Extractor and Processor Tool
Works with PDFs, JPGs, and other image formats.
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF for PDFs

def extract_from_pdf(pdf_path, output_dir, method='all', page_range=None, dpi=300):
    """Extract images from PDF file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        pdf_document = fitz.open(pdf_path)
        
        if method == 'embedded':
            image_count = 0
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    image_ext = base_image["ext"]
                    if image_ext == "jpeg":
                        image_ext = "jpg"
                    
                    image_filename = f"page_{page_num:03d}_img_{img_index:03d}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_bytes)
                    
                    image_count += 1
                    print(f"Extracted: {image_filename}")
            
            print(f"\nExtracted {image_count} embedded images")
            
        elif method == 'all':
            start_page = page_range[0] if page_range else 0
            end_page = page_range[1] if page_range else len(pdf_document)
            
            for page_num in range(start_page, min(end_page, len(pdf_document))):
                page = pdf_document[page_num]
                mat = fitz.Matrix(dpi/72, dpi/72)
                pix = page.get_pixmap(matrix=mat)
                
                image_filename = f"page_{page_num:03d}.png"
                image_path = os.path.join(output_dir, image_filename)
                pix.save(image_path)
                
                print(f"Extracted: {image_filename}")
            
            print(f"\nExtracted {end_page - start_page} pages as images")
        
        pdf_document.close()
        return True
        
    except Exception as e:
        print(f"Error extracting from PDF: {e}")
        return False

def process_image_file(image_path, output_dir, resize=None, crop=None, format='PNG'):
    """Process a single image file (JPG, PNG, etc.)."""
    try:
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if specified
            if resize:
                if 'x' in resize:
                    width, height = map(int, resize.split('x'))
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    size = int(resize)
                    img.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            # Crop if specified
            if crop:
                left, top, right, bottom = map(int, crop.split(','))
                img = img.crop((left, top, right, bottom))
            
            # Save processed image
            filename = Path(image_path).stem
            output_path = os.path.join(output_dir, f"{filename}.{format.lower()}")
            img.save(output_path, format=format)
            
            print(f"Processed: {output_path}")
            return True
            
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def process_image_directory(input_dir, output_dir, resize=None, crop=None, format='PNG'):
    """Process all images in a directory."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Input directory not found: {input_dir}")
        return False
    
    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    processed_count = 0
    for img_file in input_path.iterdir():
        if img_file.suffix.lower() in image_extensions:
            if process_image_file(img_file, output_dir, resize, crop, format):
                processed_count += 1
    
    print(f"\nProcessed {processed_count} images")
    return True

def main():
    parser = argparse.ArgumentParser(description='Extract and process images from various sources')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('-o', '--output', default='processed_images', 
                       help='Output directory (default: processed_images)')
    parser.add_argument('-t', '--type', choices=['pdf', 'image'], 
                       help='Input type (auto-detected if not specified)')
    parser.add_argument('-m', '--method', choices=['all', 'embedded'], default='all',
                       help='PDF extraction method: all (pages as images) or embedded (embedded images only)')
    parser.add_argument('-p', '--pages', nargs=2, type=int, metavar=('START', 'END'),
                       help='Page range to extract (0-indexed, PDF only)')
    parser.add_argument('-d', '--dpi', type=int, default=300,
                       help='DPI for PDF page-to-image conversion (default: 300)')
    parser.add_argument('-r', '--resize', 
                       help='Resize images: size (e.g., 100) or dimensions (e.g., 100x50)')
    parser.add_argument('-c', '--crop', 
                       help='Crop images: left,top,right,bottom (e.g., 10,10,90,90)')
    parser.add_argument('-f', '--format', default='PNG',
                       help='Output format: PNG, JPEG, etc. (default: PNG)')
    
    args = parser.parse_args()
    
    # Auto-detect input type
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input '{args.input}' not found")
        sys.exit(1)
    
    input_type = args.type
    if not input_type:
        if input_path.suffix.lower() == '.pdf':
            input_type = 'pdf'
        elif input_path.is_dir():
            input_type = 'image'
        else:
            input_type = 'image'
    
    success = False
    
    if input_type == 'pdf':
        success = extract_from_pdf(args.input, args.output, args.method, args.pages, args.dpi)
    elif input_type == 'image':
        if input_path.is_file():
            success = process_image_file(args.input, args.output, args.resize, args.crop, args.format)
        else:
            success = process_image_directory(args.input, args.output, args.resize, args.crop, args.format)
    
    if success:
        print(f"\nImages processed to: {args.output}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 