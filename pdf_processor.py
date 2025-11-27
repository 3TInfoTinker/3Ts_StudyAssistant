import os
import json
import PyPDF2
import pdfplumber
from PIL import Image
import io

class PDFProcessor:
    """
    Extract text from PDF files using multiple methods for best results
    """
    
    def __init__(self):
        self.page_mapping = self._load_page_mapping()
    
    def _load_page_mapping(self):
        """Load page number mapping from JSON file if it exists"""
        mapping_file = "./books/page_mapping.json"
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    mapping = json.load(f)
                    print(f"📖 Loaded page mapping for {len(mapping)} pages")
                    return mapping
            except Exception as e:
                print(f"⚠️  Could not load page mapping: {e}")
        return {}
    
    def extract_text_from_pdf(self, pdf_path, method='pdfplumber'):
        """
        Extract text from PDF using specified method
        
        Methods:
        - 'pdfplumber': Best for complex layouts, tables, equations (default)
        - 'pypdf2': Faster, good for simple text
        """
        try:
            if method == 'pdfplumber':
                return self._extract_with_pdfplumber(pdf_path)
            else:
                return self._extract_with_pypdf2(pdf_path)
        except Exception as e:
            print(f"❌ Error extracting from {pdf_path}: {e}")
            return []
    
    def _extract_with_pdfplumber(self, pdf_path):
        """Extract using pdfplumber (better for complex layouts)"""
        extracted_texts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"📄 Processing {total_pages} pages from PDF...")
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Get custom page number from mapping, or use sequential
                actual_page = self.page_mapping.get(f"page_{page_num}", page_num)
                
                print(f"  [{page_num}/{total_pages}] Page {actual_page}...", end=" ", flush=True)
                
                # Extract text
                text = page.extract_text()
                
                if text and text.strip():
                    extracted_texts.append({
                        'filename': f"{os.path.basename(pdf_path)}_page_{page_num}",
                        'text': text.strip(),
                        'page_number': actual_page,
                        'pdf_page': page_num
                    })
                    print("✅")
                else:
                    print("⚠️ (empty)")
        
        return extracted_texts
    
    def _extract_with_pypdf2(self, pdf_path):
        """Extract using PyPDF2 (faster, simpler)"""
        extracted_texts = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"📄 Processing {total_pages} pages from PDF...")
            
            for page_num in range(total_pages):
                actual_page = self.page_mapping.get(f"page_{page_num + 1}", page_num + 1)
                
                print(f"  [{page_num + 1}/{total_pages}] Page {actual_page}...", end=" ", flush=True)
                
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if text and text.strip():
                    extracted_texts.append({
                        'filename': f"{os.path.basename(pdf_path)}_page_{page_num + 1}",
                        'text': text.strip(),
                        'page_number': actual_page,
                        'pdf_page': page_num + 1
                    })
                    print("✅")
                else:
                    print("⚠️ (empty)")
        
        return extracted_texts
    
    def process_book_folder(self, folder_path, delay=0, resume=True):
        """
        Process all PDFs in the books folder
        Compatible with existing OCR processor interface
        """
        all_extracted = []
        
        # Get all PDF files
        pdf_files = [f for f in os.listdir(folder_path) 
                    if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("⚠️  No PDF files found in books/ folder")
            return []
        
        pdf_files.sort()
        
        print(f"🚀 Found {len(pdf_files)} PDF file(s)")
        print("⚡ Direct text extraction - Fast & accurate!\n")
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(folder_path, pdf_file)
            print(f"\n📚 [{idx}/{len(pdf_files)}] Processing: {pdf_file}")
            print("=" * 60)
            
            # Extract text from this PDF
            texts = self.extract_text_from_pdf(pdf_path, method='pdfplumber')
            all_extracted.extend(texts)
            
            print(f"✅ Extracted {len(texts)} pages from {pdf_file}")
        
        print(f"\n🎉 Total: Successfully processed {len(all_extracted)} pages!")
        return all_extracted

# Alias for drop-in replacement
OCRProcessor = PDFProcessor

if __name__ == "__main__":
    processor = PDFProcessor()
    texts = processor.process_book_folder("./books")
    
    if texts:
        print(f"\n--- Sample Output ---")
        print(f"First page preview:\n{texts[0]['text'][:500]}...")
        print(f"\nTotal pages extracted: {len(texts)}")