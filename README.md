<<<<<<< HEAD
# 📚 3Ts Study Assistant - Personal AI Study Assistant

AI-powered study assistant that helps students learn from their textbooks using RAG (Retrieval-Augmented Generation).

Deployed on Streamlit: https://3tinfotinker-3ts-studyassistant-app-lxdxcx.streamlit.app/

## ✨ Features

- 📤 Upload PDF or image-based textbooks
- 💬 Natural conversation with your books
- 📝 Generate practice quizzes
- 📖 Summarize topics/chapters
- 💡 Explain concepts simply
- 💾 Persistent chat history
- 📒 Record Management - Storage & Data
- 🎨 Dark mode UI
- video demo: https://youtu.be/QCcdvMNnWBc?si=t3Dl3utKpbOxpYKv

## 🛠️ Tech Stack

- **Frontend**  : Streamlit
- **LLM**       : Google Gemini 2.0 Flash
- **Vector DB** : FAISS
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **OCR**       : Tesseract + PyMuPDF

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/3TInfoTinker/3Ts_StudyAssistant
cd 3Ts_StudyAssistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

4. Run the app:
```bash
streamlit run web_app.py
```

## 📋 Requirements

See `requirements.txt` for full list. Main dependencies:
- streamlit
- google-generativeai
- faiss-cpu
- sentence-transformers
- pytesseract
- PyMuPDF
- python-dotenv

## 🎯 Usage

1. Upload your textbook (PDF/images) via sidebar
2. Click "Process & Build Index"
3. Use Quick Actions Dashboard or chat naturally
4. Get instant answers with page citations

## 🏗️ Architecture
```
web_app.py (UI) → agent.py (Logic) → vector_store.py (Search)
                                    → hybrid_processor.py (OCR)
```

## 📝 License

MIT License - Feel free to use for educational purposes

## 💝 Acknowledgments

Built for [Kaggle - Agents Intensive - Capstone Project]

Powered by:
- Google Gemini API
- FAISS (Meta AI)
- Sentence-Transformers
- Streamlit
- HuggingFace
=======
---
title: 3Ts Study Assistant
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: streamlit
app_file: app.py
pinned: false
---
>>>>>>> f90be87350c6c578659c9634392e374f03ba61f6
