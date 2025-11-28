import os
try:
    from .pdf_processor import PDFProcessor
    from .local_ocr_processor import LocalOCRProcessor
except ImportError:
    try:
        from pdf_processor import PDFProcessor
    except:
        PDFProcessor = None
    try:
        from local_ocr_processor import LocalOCRProcessor
    except:
        LocalOCRProcessor = None

class HybridProcessor:
    """
    Smart processor that automatically uses:
    - PDF processor if .pdf files found
    - OCR processor if only images found
    Priority: PDF first (better quality), then images
    """
    
    def __init__(self):
        self.pdf_processor = PDFProcessor() if PDFProcessor else None
        self.ocr_processor = LocalOCRProcessor() if LocalOCRProcessor else None
    
    def process_book_folder(self, folder_path, delay=0, resume=True):
        """Automatically detect and process PDFs or images"""
        
        # Check what files we have
        files = os.listdir(folder_path)
        
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        image_files = [f for f in files if f.lower().endswith(image_extensions)]
        
        # Decide what to process
        if pdf_files and self.pdf_processor:
            print(f"📚 Found {len(pdf_files)} PDF file(s) - Using PDF processor")
            print("✨ Direct text extraction (fast & accurate)\n")
            return self.pdf_processor.process_book_folder(folder_path)
        
        elif image_files and self.ocr_processor:
            print(f"🖼️  Found {len(image_files)} image file(s) - Using OCR processor")
            print("⚡ Local OCR processing\n")
            return self.ocr_processor.process_book_folder(folder_path, delay, resume)
        
        else:
            print("❌ No PDF or image files found in books/ folder!")
            print("   Please add either:")
            print("   - PDF files (recommended)")
            print("   - Image files (JPG, PNG, etc.)")
            return []

# Alias for drop-in replacement
OCRProcessor = HybridProcessor

if __name__ == "__main__":
    processor = HybridProcessor()
    texts = processor.process_book_folder("./books")
    print(f"\n✅ Total extracted: {len(texts)} pages")