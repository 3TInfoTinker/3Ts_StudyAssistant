"""
Record Manager Module for 3Ts Tutor
Handles clearing books, indexes, and storage management
"""

import os
import shutil
import streamlit as st

# ============================================================
#                   STORAGE UTILITIES
# ============================================================

def get_storage_info():
    """Get current storage information"""
    info = {
        'num_chunks': 0,
        'num_books': 0,
        'has_index': False
    }
    
    try:
        # Get chunk count from loaded index
        if hasattr(st.session_state.tutor, 'vector_store'):
            info['num_chunks'] = len(st.session_state.tutor.vector_store.chunks)
            info['has_index'] = info['num_chunks'] > 0
    except:
        pass
    
    try:
        # Count books in books directory
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        BOOKS_DIR = os.path.join(SCRIPT_DIR, "books")
        
        if os.path.exists(BOOKS_DIR):
            books = [f for f in os.listdir(BOOKS_DIR) if not f.startswith('.')]
            info['num_books'] = len(books)
    except:
        pass
    
    return info


def clear_all_storage():
    """Clear all books, indexes, and uploaded files"""
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Directories to clear
    dirs_to_clear = [
        os.path.join(SCRIPT_DIR, "books"),
        os.path.join(SCRIPT_DIR, "index"),
        os.path.join(SCRIPT_DIR, "uploads"),
        os.path.join(SCRIPT_DIR, "images")  # Only temp images, not logo
    ]
    
    success = True
    
    for dir_path in dirs_to_clear:
        try:
            if os.path.exists(dir_path):
                # Special handling for images - keep logo files
                if "images" in dir_path:
                    for file in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file)
                        # Keep logo files, delete everything else
                        if not file.lower().startswith(('logo', '3t_', '.gitkeep')):
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                else:
                    # For other directories, clear everything
                    shutil.rmtree(dir_path)
                    os.makedirs(dir_path)
                    
                    # Recreate .gitkeep
                    gitkeep_path = os.path.join(dir_path, ".gitkeep")
                    open(gitkeep_path, 'a').close()
        except Exception as e:
            st.error(f"Error clearing {dir_path}: {e}")
            success = False
    
    return success


# ============================================================
#                   UI COMPONENT
# ============================================================

def render_record_manager():
    """
    Render record management UI in sidebar
    Call this from web_app.py sidebar
    """
    st.markdown("---")
    st.markdown("### 🗑️ Record Management")
    
    # Get current storage info
    info = get_storage_info()
    
    # Display storage status
    if info['has_index']:
        st.info(f"""
        **📊 Current Records:**
        - 📚 {info['num_books']} book(s) uploaded
        - 📄 {info['num_chunks']} text chunks indexed
        - 💾 Index size: ~{info['num_chunks'] * 0.5:.1f} KB
        """)
    else:
        st.info("📊 No books or index stored yet")
    
    # Initialize confirmation state
    if 'confirm_clear' not in st.session_state:
        st.session_state.confirm_clear = False
    
    # Two-step clear process
    if not st.session_state.confirm_clear:
        # Step 1: Initial button
        if st.button("🗑️ Clear All Books & Index", use_container_width=True, type="secondary"):
            st.session_state.confirm_clear = True
            st.rerun()
    else:
        # Step 2: Confirmation
        st.warning("⚠️ **This will permanently delete:**")
        st.markdown("""
        - All uploaded books
        - Vector index
        - Temporary files
        
        Chat history will be preserved.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(" Yes, Clear", use_container_width=True, type="primary"):
                with st.spinner("Clearing storage..."):
                    if clear_all_storage():
                        # Reset tutor state
                        st.session_state.tutor.vector_store.index = None
                        st.session_state.tutor.vector_store.chunks = []
                        st.session_state.tutor.vector_store.metadata = []
                        
                        st.session_state.confirm_clear = False
                        st.success("👷 All data cleared! Ready for new books.")
                        st.rerun()
                    else:
                        st.error("🙎 Some files couldn't be cleared. Check permissions.")
                        st.session_state.confirm_clear = False
        
        with col2:
            if st.button("🙅 Cancel", use_container_width=True, type="secondary"):
                st.session_state.confirm_clear = False
                st.rerun()
    
    # Helpful tip
    if not info['has_index']:
        st.info("💡 Upload books above to get started!")


# ============================================================
#                   OPTIONAL: INDIVIDUAL ACTIONS
# ============================================================

def clear_chat_history_only():
    """Clear only chat history, keep books and index"""
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    HISTORY_DIR = os.path.join(SCRIPT_DIR, "chat_history")
    
    try:
        if os.path.exists(HISTORY_DIR):
            shutil.rmtree(HISTORY_DIR)
            os.makedirs(HISTORY_DIR)
            
            # Recreate .gitkeep
            gitkeep_path = os.path.join(HISTORY_DIR, ".gitkeep")
            open(gitkeep_path, 'a').close()
        
        st.session_state.chat_history = []
        return True
    except Exception as e:
        st.error(f"Error clearing chat history: {e}")
        return False


def get_detailed_storage_stats():
    """Get detailed storage statistics (for advanced users)"""
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    stats = {
        'books': {'count': 0, 'size_mb': 0, 'files': []},
        'index': {'exists': False, 'size_mb': 0},
        'uploads': {'count': 0, 'size_mb': 0},
        'chat_history': {'count': 0, 'size_mb': 0}
    }
    
    # Check books
    books_dir = os.path.join(SCRIPT_DIR, "books")
    if os.path.exists(books_dir):
        for file in os.listdir(books_dir):
            if not file.startswith('.'):
                file_path = os.path.join(books_dir, file)
                size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                stats['books']['files'].append({'name': file, 'size_mb': size})
                stats['books']['size_mb'] += size
                stats['books']['count'] += 1
    
    # Check index
    index_dir = os.path.join(SCRIPT_DIR, "index")
    if os.path.exists(index_dir):
        index_file = os.path.join(index_dir, "faiss.index")
        if os.path.exists(index_file):
            stats['index']['exists'] = True
            stats['index']['size_mb'] = os.path.getsize(index_file) / (1024 * 1024)
    
    # Check uploads
    uploads_dir = os.path.join(SCRIPT_DIR, "uploads")
    if os.path.exists(uploads_dir):
        for file in os.listdir(uploads_dir):
            if not file.startswith('.'):
                file_path = os.path.join(uploads_dir, file)
                stats['uploads']['size_mb'] += os.path.getsize(file_path) / (1024 * 1024)
                stats['uploads']['count'] += 1
    
    # Check chat history
    history_dir = os.path.join(SCRIPT_DIR, "chat_history")
    if os.path.exists(history_dir):
        for file in os.listdir(history_dir):
            if file.endswith('.json'):
                file_path = os.path.join(history_dir, file)
                stats['chat_history']['size_mb'] += os.path.getsize(file_path) / (1024 * 1024)
                stats['chat_history']['count'] += 1
    
    return stats