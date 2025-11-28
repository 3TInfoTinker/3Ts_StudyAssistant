import os
import time
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class OCRProcessor:
    def __init__(self):
        # Using latest stable model
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    def extract_text_from_image(self, image_path):
        """Extract text from a single image using Gemini Vision"""
        try:
            img = Image.open(image_path)
            
            prompt = """Extract ALL text from this image exactly as it appears.
            Include headings, paragraphs, equations, tables, and any other text.
            Maintain the original structure and formatting as much as possible.
            If there are diagrams, briefly describe them in [brackets]."""
            
            response = self.model.generate_content([prompt, img])
            return response.text
        
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def process_book_folder(self, folder_path, delay=5, resume=True):
        """Process all images in the books folder with rate limiting and resume capability"""
        
        # Progress file to resume if interrupted
        progress_file = os.path.join(folder_path, ".ocr_progress.json")
        extracted_texts = []
        processed_files = set()
        
        # Load previous progress if resuming
        if resume and os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    data = json.load(f)
                    extracted_texts = data['extracted_texts']
                    processed_files = set(data['processed_files'])
                    print(f"📂 Resuming from previous session ({len(processed_files)} already done)")
            except:
                print("⚠️  Could not load progress, starting fresh")
        
        # Get all image files
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(image_extensions)]
        
        image_files.sort()  # Process in order
        
        # Filter out already processed files
        remaining_files = [f for f in image_files if f not in processed_files]
        
        if not remaining_files:
            print("✅ All files already processed!")
            return extracted_texts
        
        print(f"Found {len(remaining_files)} images to process (out of {len(image_files)} total)")
        print(f"⏱️  Rate limit protection: {delay}s delay between requests\n")
        
        for idx, filename in enumerate(remaining_files, 1):
            image_path = os.path.join(folder_path, filename)
            page_num = image_files.index(filename) + 1
            
            print(f"Processing [{idx}/{len(remaining_files)}] Page {page_num}: {filename}", end=" ")
            
            # Retry logic for rate limits
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    text = self.extract_text_from_image(image_path)
                    if text:
                        extracted_texts.append({
                            'filename': filename,
                            'text': text,
                            'page_number': page_num
                        })
                        processed_files.add(filename)
                        
                        # Save progress after each successful extraction
                        with open(progress_file, 'w') as f:
                            json.dump({
                                'extracted_texts': extracted_texts,
                                'processed_files': list(processed_files)
                            }, f)
                        
                        print("✅")
                    else:
                        print("⚠️ No text extracted")
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        wait_time = delay * (attempt + 1) * 2  # Exponential backoff
                        print(f"\n⏳ Rate limit hit! Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        if attempt == max_retries - 1:
                            print(f"❌ Failed after {max_retries} attempts")
                            print(f"💾 Progress saved! Run again to resume from here.")
                            return extracted_texts
                    else:
                        print(f"❌ Error: {e}")
                        break
            
            # Add delay between requests (except after last image)
            if idx < len(remaining_files):
                print(f"⏱️  Waiting {delay}s...", end="\r")
                time.sleep(delay)
        
        # Clean up progress file on completion
        if os.path.exists(progress_file):
            os.remove(progress_file)
        
        print(f"\n✅ Successfully processed {len(extracted_texts)}/{len(image_files)} images!")
        return extracted_texts

if __name__ == "__main__":
    # Test the OCR
    processor = OCRProcessor()
    texts = processor.process_book_folder("./books")
    
    if texts:
        print("\n--- Sample Output ---")
        print(f"First page text preview:\n{texts[0]['text'][:500]}...")