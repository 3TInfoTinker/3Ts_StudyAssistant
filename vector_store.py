import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ============================================================
#                  PATH CONFIGURATION
# ============================================================
# Get the directory where THIS script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INDEX_DIR = os.path.join(SCRIPT_DIR, "index")


class VectorStore:
    def __init__(self, index_dir=None):
        # Use script-relative path if none provided
        if index_dir is None:
            index_dir = DEFAULT_INDEX_DIR
            
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        
        # Use a good free embedding model
        print("Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2
        
        self.index = None
        self.chunks = []
        self.metadata = []
    
    def chunk_text(self, text, chunk_size=500, overlap=100):
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def build_index(self, extracted_texts):
        """Build FAISS index from extracted texts"""
        print(f"\n🔨 Building vector index in: {self.index_dir}")
        
        all_chunks = []
        all_metadata = []
        
        for item in extracted_texts:
            chunks = self.chunk_text(item['text'])
            
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'filename': item['filename'],
                    'page_number': item['page_number'],
                    'chunk_id': chunk_idx
                })
        
        print(f"Created {len(all_chunks)} text chunks")
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedder.encode(all_chunks, show_progress_bar=True)
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
        self.chunks = all_chunks
        self.metadata = all_metadata
        
        print(f"✅ Index built with {len(all_chunks)} chunks!")
        
        # Save index
        self.save_index()
    
    def save_index(self):
        """Save FAISS index and metadata"""
        index_path = os.path.join(self.index_dir, "faiss.index")
        chunks_path = os.path.join(self.index_dir, "chunks.pkl")
        metadata_path = os.path.join(self.index_dir, "metadata.pkl")
        
        faiss.write_index(self.index, index_path)
        
        with open(chunks_path, 'wb') as f:
            pickle.dump(self.chunks, f)
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"💾 Index saved to {self.index_dir}/")
    
    def load_index(self):
        """Load existing FAISS index"""
        index_path = os.path.join(self.index_dir, "faiss.index")
        chunks_path = os.path.join(self.index_dir, "chunks.pkl")
        metadata_path = os.path.join(self.index_dir, "metadata.pkl")
        
        if not all(os.path.exists(p) for p in [index_path, chunks_path, metadata_path]):
            print(f"⚠️  Index not found in: {self.index_dir}")
            return False
        
        self.index = faiss.read_index(index_path)
        
        with open(chunks_path, 'rb') as f:
            self.chunks = pickle.load(f)
        
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        
        print(f"✅ Loaded index from {self.index_dir} with {len(self.chunks)} chunks")
        return True
    
    def search(self, query, top_k=5):
        """Search for relevant chunks"""
        if self.index is None:
            raise ValueError("Index not loaded! Build or load an index first.")
        
        # Embed query
        query_embedding = self.embedder.encode([query])
        
        # Search FAISS
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            top_k
        )
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                'chunk': self.chunks[idx],
                'metadata': self.metadata[idx],
                'distance': float(dist)
            })
        
        return results

if __name__ == "__main__":
    # Test vector store
    try:
        from .ocr_processor import OCRProcessor
    except ImportError:
        from ocr_processor import OCRProcessor
    
    processor = OCRProcessor()
    texts = processor.process_book_folder("../books")
    
    store = VectorStore()
    store.build_index(texts)
    
    # Test search
    results = store.search("What is Newton's first law?")
    print("\n--- Search Test ---")
    for r in results[:2]:
        print(f"\nPage {r['metadata']['page_number']}: {r['chunk'][:200]}...")