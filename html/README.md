# PDF Image Extractor Tool

A Python tool to extract images from PDF files using PyMuPDF.

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Extract all pages as images:
```bash
python pdf_image_extractor.py input.pdf
```

Extract embedded images only:
```bash
python pdf_image_extractor.py input.pdf -m embedded
```

### Advanced Usage

Extract specific page range:
```bash
python pdf_image_extractor.py input.pdf -p 0 5
```

Extract with custom DPI:
```bash
python pdf_image_extractor.py input.pdf -d 600
```

Extract to custom directory:
```bash
python pdf_image_extractor.py input.pdf -o my_images
```

### Options

- `-o, --output`: Output directory (default: extracted_images)
- `-m, --method`: Extraction method: 'all' (pages as images) or 'embedded' (embedded images only)
- `-p, --pages`: Page range to extract (0-indexed, e.g., 0 5)
- `-d, --dpi`: DPI for page-to-image conversion (default: 300)

## Examples

Extract all pages from LOTR LCG rulebook:
```bash
python pdf_image_extractor.py "LOTR LCG/lotr-lcg-rules.pdf" -o lotr_images
```

Extract only embedded images (icons, diagrams):
```bash
python pdf_image_extractor.py "LOTR LCG/lotr-lcg-rules.pdf" -m embedded -o lotr_icons
```

Extract pages 20-25 (timing diagrams):
```bash
python pdf_image_extractor.py "LOTR LCG/lotr-lcg-rules.pdf" -p 20 25 -o timing_diagrams
``` 