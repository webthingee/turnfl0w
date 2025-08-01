#!/usr/bin/env python3
"""
PDF Image Extractor Tool
Extracts images from PDF files using various methods.
"""

import os
import sys
import argparse
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_pdf(pdf_path, output_dir, method='all', page_range=None, dpi=300):
    """
    Extract images from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted images
        method (str): 'all' for all pages as images, 'embedded' for embedded images only
        page_range (tuple): (start_page, end_page) for specific pages (0-indexed)
        dpi (int): Resolution for page-to-image conversion
    """
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Open PDF
        pdf_document = fitz.open(pdf_path)
        
        if method == 'embedded':
            # Extract embedded images
            image_count = 0
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Determine image format
                    image_ext = base_image["ext"]
                    if image_ext == "jpeg":
                        image_ext = "jpg"
                    
                    # Save image
                    image_filename = f"page_{page_num:03d}_img_{img_index:03d}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_bytes)
                    
                    image_count += 1
                    print(f"Extracted: {image_filename}")
            
            print(f"\nExtracted {image_count} embedded images")
            
        elif method == 'all':
            # Convert pages to images
            start_page = page_range[0] if page_range else 0
            end_page = page_range[1] if page_range else len(pdf_document)
            
            for page_num in range(start_page, min(end_page, len(pdf_document))):
                page = pdf_document[page_num]
                
                # Create transformation matrix for desired DPI
                mat = fitz.Matrix(dpi/72, dpi/72)
                pix = page.get_pixmap(matrix=mat)
                
                # Save as PNG
                image_filename = f"page_{page_num:03d}.png"
                image_path = os.path.join(output_dir, image_filename)
                pix.save(image_path)
                
                print(f"Extracted: {image_filename}")
            
            print(f"\nExtracted {end_page - start_page} pages as images")
        
        pdf_document.close()
        
    except Exception as e:
        print(f"Error extracting images: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Extract images from PDF files')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', default='extracted_images', 
                       help='Output directory (default: extracted_images)')
    parser.add_argument('-m', '--method', choices=['all', 'embedded'], default='all',
                       help='Extraction method: all (pages as images) or embedded (embedded images only)')
    parser.add_argument('-p', '--pages', nargs=2, type=int, metavar=('START', 'END'),
                       help='Page range to extract (0-indexed)')
    parser.add_argument('-d', '--dpi', type=int, default=300,
                       help='DPI for page-to-image conversion (default: 300)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file '{args.pdf_path}' not found")
        sys.exit(1)
    
    success = extract_images_from_pdf(
        args.pdf_path, 
        args.output, 
        args.method, 
        args.pages, 
        args.dpi
    )
    
    if success:
        print(f"\nImages extracted to: {args.output}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 