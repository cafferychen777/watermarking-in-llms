import os
from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import numpy as np
import logging
from tqdm import tqdm
import time
from datetime import datetime

class PDFProcessor:
    def __init__(self):
        self.papers_dir = Path('papers')
        self.output_dir = Path('data/text')
        self.log_dir = Path('logs')
        
        # Create necessary directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.log_dir / f'pdf_processing_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def convert_pdf_to_text(self, pdf_path):
        """Convert PDF to text using PyMuPDF (text) and Tesseract (for images)"""
        try:
            doc = fitz.open(pdf_path)
            text_content = []
            
            # Show progress for pages within each PDF
            for page_num in tqdm(range(len(doc)), 
                               desc=f"Processing pages in {pdf_path.name}",
                               leave=False):
                page = doc[page_num]
                
                # Get text
                text = page.get_text()
                
                # If page has no text, might be scanned, try OCR
                if not text.strip():
                    self.logger.info(f"No text found in page {page_num+1}, attempting OCR")
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img)
                
                text_content.append(text)
            
            doc.close()
            return '\n'.join(text_content)
            
        except Exception as e:
            self.logger.error(f"Error processing {pdf_path}: {str(e)}")
            return None

    def process_all_pdfs(self):
        """Process all PDFs in the papers directory"""
        pdf_files = list(self.papers_dir.glob('*.pdf'))
        self.logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Create progress bar for all PDFs
        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            start_time = time.time()
            self.logger.info(f"Starting to process: {pdf_file.name}")
            
            # Convert PDF to text
            text_content = self.convert_pdf_to_text(pdf_file)
            
            if text_content:
                # Save text to output file
                output_file = self.output_dir / f"{pdf_file.stem}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                
                processing_time = time.time() - start_time
                self.logger.info(f"Successfully converted {pdf_file.name} to text "
                               f"(Processing time: {processing_time:.2f}s)")
            else:
                self.logger.error(f"Failed to convert {pdf_file.name}")

def main():
    processor = PDFProcessor()
    
    # Log start time
    start_time = time.time()
    processor.logger.info("Starting PDF processing")
    
    # Process PDFs
    processor.process_all_pdfs()
    
    # Log completion
    total_time = time.time() - start_time
    processor.logger.info(f"PDF processing completed. Total time: {total_time:.2f}s")

if __name__ == "__main__":
    main() 