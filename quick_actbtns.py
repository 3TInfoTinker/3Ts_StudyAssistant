"""
Quick Actions Module for 3Ts Tutor
Handles the 4 sticky dashboard buttons.
"""

import streamlit as st

# ============================================================
#                   STICKY BUTTON STYLING
# ============================================================

def render_sticky_css():
    """Add CSS to make buttons sticky at top"""
    st.markdown("""
        <style>
        /* Sticky Quick Actions Dashboard */
        .sticky-dashboard {
            position: sticky;
            top: 0;
            z-index: 999;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            margin: -1rem -1rem 1.5rem -1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            border-radius: 0 0 12px 12px;
        }
        
        .sticky-dashboard h3 {
            color: white;
            margin: 0 0 0.8rem 0;
            text-align: center;
            font-size: 1.2rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* Dashboard buttons styling */
        .sticky-dashboard .stButton button {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            font-weight: 600;
            padding: 0.6rem;
            transition: all 0.3s;
            border-radius: 8px;
        }
        
        .sticky-dashboard .stButton button:hover {
            background-color: rgba(255, 255, 255, 0.35);
            border-color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

# ============================================================
#                   QUICK ACTION HANDLERS
# ============================================================

def handle_quiz_action():
    """Show quiz input form and generate quiz"""
    st.markdown("### 📝 Generate Quiz")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "Enter topic for quiz:",
            key=f"quiz_topic_{st.session_state.input_key}",
            placeholder="e.g., Newton's Laws, Photosynthesis, etc."
        )
    
    with col2:
        num_q = st.number_input(
            "Questions",
            min_value=3,
            max_value=10,
            value=5,
            key="num_quiz"
        )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
    
    with col_btn1:
        if st.button("✅ Generate", width='stretch'):
            if topic:
                # Generate quiz
                with st.spinner("Creating quiz..."):
                    try:
                        quiz_result = st.session_state.tutor.generate_quiz(topic, num_q)
                        
                        # Add to chat
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': f"Generate a {num_q}-question quiz on {topic}",
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': quiz_result,
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        
                        # Clear action and increment key
                        if 'quick_action' in st.session_state:
                            del st.session_state.quick_action
                        st.session_state.input_key += 1
                        st.success("✅ Quiz generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please enter a topic!")
    
    with col_btn2:
        if st.button("❌ Cancel", width='stretch'):
            if 'quick_action' in st.session_state:
                del st.session_state.quick_action
            st.rerun()


def handle_summarize_action():
    """Show summary input form and generate summary"""
    st.markdown("### 📖 Summarize Topic")
    
    topic = st.text_input(
        "Enter topic to summarize:",
        key=f"summary_topic_{st.session_state.input_key}",
        placeholder="e.g., Chapter 5, Cell Biology, etc."
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
    
    with col_btn1:
        if st.button("✅ Summarize", width='stretch'):
            if topic:
                with st.spinner("Creating summary..."):
                    try:
                        summary_result = st.session_state.tutor.summarize_topic(topic)
                        
                        # Add to chat
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': f"Summarize {topic}",
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': summary_result,
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        
                        # Clear action
                        if 'quick_action' in st.session_state:
                            del st.session_state.quick_action
                        st.session_state.input_key += 1
                        st.success("✅ Summary generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please enter a topic!")
    
    with col_btn2:
        if st.button("❌ Cancel", width='stretch', key="cancel_summary"):
            if 'quick_action' in st.session_state:
                del st.session_state.quick_action
            st.rerun()


def handle_explain_action():
    """Show explain input form and generate explanation"""
    st.markdown("### 💡 Explain Concept")
    
    concept = st.text_input(
        "Enter concept to explain:",
        key=f"explain_concept_{st.session_state.input_key}",
        placeholder="e.g., What is osmosis? How does gravity work?"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
    
    with col_btn1:
        if st.button("✅ Explain", width='stretch'):
            if concept:
                with st.spinner("Preparing explanation..."):
                    try:
                        explain_result = st.session_state.tutor.explain_concept(concept)
                        
                        # Add to chat
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': f"Explain {concept}",
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': explain_result,
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        
                        # Clear action
                        if 'quick_action' in st.session_state:
                            del st.session_state.quick_action
                        st.session_state.input_key += 1
                        st.success("✅ Explanation ready!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please enter a concept!")
    
    with col_btn2:
        if st.button("❌ Cancel", width='stretch', key="cancel_explain"):
            if 'quick_action' in st.session_state:
                del st.session_state.quick_action
            st.rerun()


def handle_ask_action():
    """Show ask question form and get answer"""
    st.markdown("### ❓ Ask a Question")
    
    question = st.text_area(
        "Type your question:",
        key=f"ask_question_{st.session_state.input_key}",
        placeholder="e.g., What is the difference between speed and velocity?",
        height=100
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
    
    with col_btn1:
        if st.button("✅ Ask", width='stretch'):
            if question:
                with st.spinner("Finding answer..."):
                    try:
                        answer_result = st.session_state.tutor.chat(question)
                        
                        # Add to chat
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': question,
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': answer_result,
                            'timestamp': st.session_state.get('timestamp', '')
                        })
                        
                        # Clear action
                        if 'quick_action' in st.session_state:
                            del st.session_state.quick_action
                        st.session_state.input_key += 1
                        st.success("✅ Answer ready!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please enter a question!")
    
    with col_btn2:
        if st.button("❌ Cancel", width='stretch', key="cancel_ask"):
            if 'quick_action' in st.session_state:
                del st.session_state.quick_action
            st.rerun()

# ============================================================
#                   MAIN ROUTER FUNCTION
# ============================================================

def render_sticky_buttons():
    """
    Render the sticky quick action buttons at the top
    Call this right after the header in web_app.py
    """
    # Add sticky CSS
    render_sticky_css()
    
    # Create sticky container
    st.markdown('<div class="sticky-dashboard">', unsafe_allow_html=True)
    st.markdown("### 🎯 Quick Actions Dashboard")
    
    # Button row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Generate Quiz", width='stretch', key="btn_quiz"):
            st.session_state.quick_action = "quiz"
            st.rerun()
    
    with col2:
        if st.button("📖 Summarize Topic", width='stretch', key="btn_summary"):
            st.session_state.quick_action = "summarize"
            st.rerun()
    
    with col3:
        if st.button("💡 Explain Concept", width='stretch', key="btn_explain"):
            st.session_state.quick_action = "explain"
            st.rerun()
    
    with col4:
        if st.button("❓ Ask Question", width='stretch', key="btn_ask"):
            st.session_state.quick_action = "ask"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def process_quick_action():
    """
    Check if a quick_action is set and display the appropriate form
    Call this AFTER the buttons and BEFORE chat display
    """
    if 'quick_action' in st.session_state:
        action = st.session_state.quick_action
        
        st.markdown("---")
        
        if action == "quiz":
            handle_quiz_action()
        elif action == "summarize":
            handle_summarize_action()
        elif action == "explain":
            handle_explain_action()
        elif action == "ask":
            handle_ask_action()
        
        st.markdown("---")