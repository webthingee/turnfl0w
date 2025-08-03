#!/bin/bash

# Get the current directory
current_dir=$(pwd)
echo "Current directory: $current_dir"

# Find all PDF files in the current directory and subdirectories
find . -name "*.pdf" -type f | while read -r pdf_file; do
    echo "Processing: $pdf_file"
    
    # Create the output filename by replacing .pdf with .txt
    txt_file="${pdf_file%.pdf}.txt"
    
    echo "Converting to: $txt_file"
    
    # Convert PDF to text with layout preservation
    if pdftotext -layout "$pdf_file" "$txt_file"; then
        echo "✓ Successfully converted: $pdf_file -> $txt_file"
        
        # Show file sizes for comparison
        pdf_size=$(du -h "$pdf_file" | cut -f1)
        txt_size=$(du -h "$txt_file" | cut -f1)
        echo "  PDF size: $pdf_size, TXT size: $txt_size"
        
        # Show first few lines of the converted file
        echo "  Preview (first 3 lines):"
        head -3 "$txt_file" | sed 's/^/    /'
        echo ""
    else
        echo "✗ Failed to convert: $pdf_file"
        echo ""
    fi
done

echo "Conversion complete!"