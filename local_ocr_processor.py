import os
import pytesseract
from PIL import Image

class LocalOCRProcessor:
    """CPU-based OCR using Tesseract - No API limits!"""
    
    def extract_text_from_image(self, image_path):
        """Extract text using local Tesseract OCR"""
        try:
            img = Image.open(image_path)
            
            # Use config for better accuracy with textbooks
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
            
            return text.strip() if text else None
        
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def process_book_folder(self, folder_path, delay=0, resume=True):
        """Process all images - NO RATE LIMITS! 
        Parameters match OCRProcessor for drop-in replacement"""
        extracted_texts = []
        
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(image_extensions)]
        
        image_files.sort()
        
        print(f"🚀 Processing {len(image_files)} images with local OCR...")
        print("⚡ No rate limits! Processing at full speed!\n")
        
        for idx, filename in enumerate(image_files, 1):
            image_path = os.path.join(folder_path, filename)
            print(f"[{idx}/{len(image_files)}] {filename}...", end=" ", flush=True)
            
            text = self.extract_text_from_image(image_path)
            if text:
                extracted_texts.append({
                    'filename': filename,
                    'text': text,
                    'page_number': idx
                })
                print("✅")
            else:
                print("⚠️")
        
        print(f"\n✅ Processed {len(extracted_texts)} images!")
        return extracted_texts

# Alias for drop-in replacement
OCRProcessor = LocalOCRProcessor

if __name__ == "__main__":
    processor = LocalOCRProcessor()
    texts = processor.process_book_folder("./books")
    
    if texts:
        print(f"\n--- Sample Output ---")
        print(f"First page: {texts[0]['text'][:300]}...")