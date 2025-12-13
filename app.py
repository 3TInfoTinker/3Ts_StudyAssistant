import os
import streamlit as st
from datetime import datetime
import json
from agent import Tutor
from quick_actbtns import render_sticky_buttons, process_quick_action
from record_manager import render_record_manager 


# ============================================================
#                     PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="3Ts Tutor",
    page_icon="images/3TinfoTinkerLogo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#                   DARK THEME CSS STYLING
# ============================================================
st.markdown("""
    <style>
    /* Balanced Dark Theme - Easy on the eyes */
    .stApp {
        background-color: #2b2d31;
        color: #dcddee;
    }
    
    .main-header {
        font-size: 2rem;
        color: #5865f2;
        text-align: center;
        padding: 1rem 0;
        text-shadow: 0 2px 10px rgba(88, 101, 242, 0.3);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .user-message {
        background-color: #404249;
        border-left-color: #5865f2;
        color: #ffffff;
    }
    
    .bot-message {
        background-color: #383a40;
        border-left-color: #57f287;
        color: #dcddde;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #5865f2;
        color: #ffffff;
        border: none;
        font-weight: 500;
        transition: all 0.2s;
    }

    .stButton>button:hover {
        background-color: #4752c4;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(88, 101, 242, 0.4);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e1f22;
    }
#--------------------------------------------------------------------
#       File Uploader Styling
#--------------------------------------------------------------------
    /* File uploader section - Dark theme */
    [data-testid="stFileUploader"] > div {
        background-color: #2b2d31;
        border: 2px dashed #4e5058;
        border-radius: 8px;
        padding: 1rem;
        transition: all 0.3s;
    }

    [data-testid="stFileUploader"] > div:hover {
        border-color: #5865f2;
        background-color: #383a40;
    }

    /* Drag and drop zone text color */
    [data-testid="stFileUploader"] label {
        color: #dcddde !important;
    }

    [data-testid="stFileUploader"] small {
        color: #b5bac1 !important;
    }
    

    /* Browse files button */
    [data-testid="stFileUploader"] button {
        background-color: #5865f2 !important;
        border: none !important;
        color: white !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #4752c4 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(88, 101, 242, 0.3) !important;
    }

    /* Process & Build Buttons in sidebar */
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        background-color: #5865f2;
        color: white;
        border: none;
        border-radius: 6px !important;         /* from 8px to 6px */
        padding: 0.35rem 0.6rem !important;   /* affects Buttons - from 0.6rem to 0.4rem, 1rem to 0.8rem */
        font-weight: 600;                    /*
        font-size: 0.85rem !important;      /* from 0.95rem to 0.85rem */
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #4752c4;
        transform: translateY(-1px) !important;        /* affects Buttons */
        box-shadow: 0 4px 8px rgba(88, 101, 242, 0.4);
        cursor: pointer !important;
    }

    /* Fix cursor on entire file upload area */
    [data-testid="stFileUploadDropzone"] {
        cursor: pointer !important;
        pointer-events: none !important;  /* ← Blocks all clicks on dropzone */
    }

    /* Uploaded files display - dark theme */
    [data-testid="stFileUploader"] section {
        background-color: #383a40 !important;
        border-radius: 6px;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }

    [data-testid="stFileUploader"] section div {
        color: #dcddde !important;
    }

        /* ===== FILE UPLOADER CURSOR FIX  ===== */

    /* Force default cursor on ALL file uploader elements */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] *,
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploadDropzone"] * {
        cursor: default !important;
    }

    /* ONLY the Browse files button gets pointer */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button * {
        cursor: pointer !important;
    }

    /* Browse files button styling */
    [data-testid="stFileUploader"] button {
        background-color: #5865f2 !important;
        border: none !important;
        color: white !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #4752c4 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(88, 101, 242, 0.3) !important;
    }
#--------------------------------------------------------------------
    section[data-testid="stSidebar"] > div {
        background-color: #1e1f22;
    }
    
    /* Input box styling */
    .stTextInput>div>div>input {
        background-color: #383a40;
        color: #dcddde;
        border: 2px solid #4e5058;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #5865f2;
        box-shadow: 0 0 0 2px rgba(88, 101, 242, 0.2);
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: #383a40;
        border: 2px solid #4e5058;
        border-radius: 0.5rem;
    }
    
    /* Headers */
    h3 {
        color: #ffffff;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #dcddde;
    }
    
    /* Dividers */
    hr {
        border-color: #4e5058;
    }
    
    </style>
""", unsafe_allow_html=True)

# ============================================================
#                   SESSION STATE INIT
# ============================================================
if 'tutor' not in st.session_state:
    st.session_state.tutor = Tutor()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'history_file' not in st.session_state:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    HISTORY_DIR = os.path.join(SCRIPT_DIR, "chat_history")
    os.makedirs(HISTORY_DIR, exist_ok=True)
    st.session_state.history_file = os.path.join(
        HISTORY_DIR, 
        f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# ============================================================
#                   HELPER FUNCTIONS
# ============================================================
def save_chat_history():
    """Save chat history to JSON file"""
    with open(st.session_state.history_file, 'w') as f:
        json.dump(st.session_state.chat_history, f, indent=2)

def load_previous_chats():
    """Load list of previous chat sessions"""
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    HISTORY_DIR = os.path.join(SCRIPT_DIR, "chat_history")
    
    if not os.path.exists(HISTORY_DIR):
        return []
    
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith('.json')]
    return sorted(files, reverse=True)

def add_to_chat(role, content):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    })
    save_chat_history()

def clear_input():
    """Clear input by incrementing key"""
    st.session_state.input_key += 1

# ============================================================
#                       SIDEBAR
# ============================================================
with st.sidebar:
    # Display logo
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    #logo_path = os.path.join(SCRIPT_DIR, "images", "3T_AnimLogo_L.gif")
    logo_path = os.path.join(SCRIPT_DIR, "images", "3TinfoTinkerLogo.png")
    
    if os.path.exists(logo_path):
        # New Eddition
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(logo_path, width='stretch') # For - use_container_width=True, use:- width='stretch'. For use_container_width=False, use:- width='content'`.
    else:
        st.warning("⚠️ Logo not found. Place it in: Tutor/images/3T_AnimLogo_L.gif")
    
    st.markdown("---")
    st.markdown("### 📚 Book Management")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload Books (PDF/Images)",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload your textbooks"
    )
    
    if uploaded_files:
        if st.button("🔨 Process & Build Index"):
            with st.spinner("Processing books... This may take a few minutes."):
                try:
                    # Create uploads directory
                    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
                    UPLOAD_DIR = os.path.join(SCRIPT_DIR, "uploads")
                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    
                    # Save uploaded files
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    st.info("📖 Extracting text from books...")
                    # Build knowledge base
                    st.session_state.tutor.build_knowledge_base(UPLOAD_DIR)
                    st.success("✅ Books processed successfully!")
                    
                    # Show sample of extracted text for verification
                    st.info("💡 Try asking questions about the book content now!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error processing books: {e}")
                    st.warning("⚠️ If OCR failed, check your hybrid_processor.py configuration")
    
    st.markdown("---")
    st.markdown("### 💾 Chat History")
    
    # Load previous chats
    previous_chats = load_previous_chats()
    if previous_chats:
        selected_chat = st.selectbox(
            "Load Previous Session",
            ["Current Session"] + previous_chats
        )
        
        if selected_chat != "Current Session" and st.button("Load"):
            SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            HISTORY_DIR = os.path.join(SCRIPT_DIR, "chat_history")
            with open(os.path.join(HISTORY_DIR, selected_chat), 'r') as f:
                st.session_state.chat_history = json.load(f)
            st.rerun()
    
    if st.button("🗑️ Clear Current Chat"):
        st.session_state.chat_history = []
        save_chat_history()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔧 Debug Info")
    if st.checkbox("Show Index Status"):
        try:
            num_chunks = len(st.session_state.tutor.vector_store.chunks)
            st.success(f"✅ Index loaded: {num_chunks} chunks")
            if st.button("Show Sample Text"):
                if num_chunks > 0:
                    st.code(st.session_state.tutor.vector_store.chunks[0][:300])
        except:
            st.error("❌ No index found - please build first")
            
    render_record_manager()
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    **3Ts Tutor v1.0**
    
    AI-powered Study Assistant.
    
    Features:
    - 💬 Natural conversation
    - 📝 Quiz generation
    - 📖 Topic summaries
    - 🎯 Concept explanations
    """)

# ============================================================
#                      MAIN CONTENT
# ============================================================
st.markdown('<h1 class="main-header">📚 3Ts Tutor - Your Personal Study Assistant</h1>', 
            unsafe_allow_html=True)

render_sticky_buttons()

process_quick_action()

# Display chat history
chat_container = st.container()
with chat_container:
    for idx, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {message['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Tutor:</strong><br>
                    {message['content'].replace(chr(10), '<br>')}
                </div>
            """, unsafe_allow_html=True)
            
            # # Add copy button for bot messages
            # if st.button(f"📋 Copy", key=f"copy_{idx}"):
            #     st.code(message['content'], language=None)

# Chat input
st.markdown("---")
st.markdown("### 💬 Ask me anything!")

user_input = st.text_input(
    "Type your question here...",
    placeholder="e.g., What is Newton's first law? or Give me a quiz on vectors",
    key=f"main_input_{st.session_state.input_key}"
)

if st.button("Send 🚀") and user_input:
    # Add user message
    add_to_chat('user', user_input)
    
    # Get tutor response
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.tutor.chat(user_input)
            add_to_chat('assistant', response)
            clear_input()  # Clear the input box
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Make sure you've built the knowledge base first!")

# ============================================================
#                      FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #b5b5b5; padding: 1rem;'>
    <h3>| Built with ❤️ for Students and Learning enthusiasts |</h3><small> Powered by Google Gemini & FAISS</small>
</div>
""", unsafe_allow_html=True)