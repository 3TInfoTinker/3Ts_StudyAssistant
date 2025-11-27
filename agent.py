import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Handle both relative and absolute imports
try:
    from .vector_store import VectorStore
    from .hybrid_processor import OCRProcessor
except ImportError:
    from vector_store import VectorStore
    from hybrid_processor import OCRProcessor

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ============================================================
#                  PATH CONFIGURATION
# ============================================================
# Get the directory where THIS script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(SCRIPT_DIR, "books")
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
INDEX_DIR = os.path.join(SCRIPT_DIR, "index")

# Prompts separated into Text files
PROMPTS_DIR = os.path.join(SCRIPT_DIR, "prompts")


# ============================================================
#                   PROMPT LOADER UTILITY
# ============================================================
def load_prompt(filename):
    """Load prompt template from file"""
    prompt_path = os.path.join(PROMPTS_DIR, filename)
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Warning: Prompt file not found: {prompt_path}")
        return None

# ============================================================
#                     TUTOR AGENT
# ============================================================

class Tutor:
    def __init__(self):
        self.vector_store = VectorStore()
        self.ocr_processor = OCRProcessor()
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        # Load prompt templates
        self.system_prompt_template = load_prompt("system_prompt.txt")
        self.quiz_prompt_template = load_prompt("quiz_prompt.txt")
        self.summarize_prompt_template = load_prompt("summarize_prompt.txt")
        self.explain_prompt_template = load_prompt("explain_prompt.txt")

        # Load existing index
        if not self.vector_store.load_index():
            print("\n⚠️  No index found. You need to process your books first!")
            print("Run: python agent.py --build\n")

    # ------------------------------------------------------------
    #                   BUILD KNOWLEDGE BASE
    # ------------------------------------------------------------
    def build_knowledge_base(self, books_folder=None):
        """Process PDFs or images and build searchable index"""
        # Use configured BOOKS_DIR if no folder specified
        if books_folder is None:
            books_folder = BOOKS_DIR
            
        print(f"\n📚 Building Knowledge Base from: {books_folder}")

        extracted_texts = self.ocr_processor.process_book_folder(books_folder)

        if not extracted_texts:
            print("❌ No texts extracted! Check your books folder.")
            return

        self.vector_store.build_index(extracted_texts)
        print("\n✅ Knowledge base ready!")

    # ------------------------------------------------------------
    #               NATURAL LANGUAGE INTENT DETECTION
    # ------------------------------------------------------------
    def detect_intent(self, user_input):
        """Detect type of request: quiz, summarize, explain, or normal ask"""
        text = user_input.lower()

        # Quiz request
        if any(w in text for w in ["quiz", "test", "practice", "mcq", "questions"]):
            topic = user_input
            for w in ["quiz", "test", "practice", "on", "about", "give", "me", "create"]:
                topic = topic.lower().replace(w, "").strip()
            return ("quiz", topic if topic else user_input)

        # Summarize request
        if any(w in text for w in ["summarize", "summary", "brief", "overview", "tldr"]):
            topic = user_input
            for w in ["summarize", "summary", "brief", "give", "me", "a", "of", "about"]:
                topic = topic.lower().replace(w, "").strip()
            return ("summarize", topic if topic else user_input)

        # Explain request
        if any(w in text for w in ["explain", "how does", "why does", "help me understand"]):
            return ("explain", user_input)

        # Default - Ask a question
        return ("ask", user_input)

    # ------------------------------------------------------------
    #                   CHAT HANDLER (MAIN PIPELINE)
    # ------------------------------------------------------------
    def chat(self, user_input):
        """Natural conversation handler - detects intent and responds"""
        intent, content = self.detect_intent(user_input)

        if intent == "quiz":
            return self.generate_quiz(content)

        if intent == "summarize":
            return self.summarize_topic(content)

        if intent == "explain":
            return self.explain_concept(content)

        # Default - Answer question using RAG
        result = self.answer_question(content)
        return f"{result['answer']}\n\n📖 Sources: Pages {[s['page_number'] for s in result['sources']]}"

    # ------------------------------------------------------------
    #                        RAG ANSWER
    # ------------------------------------------------------------
    def answer_question(self, question):
        """Answer using Retrieval-Augmented Generation"""
        results = self.vector_store.search(question, top_k=3)

        context = "\n\n---\n\n".join([
            f"[Page {r['metadata']['page_number']}]: {r['chunk']}" for r in results
        ])

         # Use external prompt template
        if self.system_prompt_template:
            prompt = self.system_prompt_template.format(
                context=context,
                question=question
            )
        else:
            # Fallback prompt if file not found
            prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"

        response = self.model.generate_content(prompt)

        return {
            "answer": response.text,
            "sources": [r["metadata"] for r in results]
        }


    # ------------------------------------------------------------
    #                       QUIZ GENERATOR
    # ------------------------------------------------------------
    def generate_quiz(self, topic, num_questions=5):
        """Generate practice quiz on a topic"""
        results = self.vector_store.search(topic, top_k=5)
        context = "\n\n".join([r["chunk"] for r in results])

        # Use external prompt template
        if self.quiz_prompt_template:
            prompt = self.quiz_prompt_template.format(
                topic=topic,
                num_questions=num_questions,
                context=context
            )
        else:
            # Fallback prompt
            prompt = f"Create {num_questions} questions about {topic} from: {context}"

        response = self.model.generate_content(prompt)
        return response.text

    # ------------------------------------------------------------
    #                           SUMMARY GENERATOR
    # ------------------------------------------------------------
    def summarize_topic(self, topic):
        """Generate topic summary from textbook"""
        results = self.vector_store.search(topic, top_k=5)
        context = "\n\n".join([r["chunk"] for r in results])

        # Use external prompt template
        if self.summarize_prompt_template:
            prompt = self.summarize_prompt_template.format(
                topic=topic,
                context=context
            )
        else:
            # Fallback prompt
            prompt = f"Summarize {topic} from: {context}"

        response = self.model.generate_content(prompt)
        return response.text

    # ------------------------------------------------------------
    #                       EXPLANATION GENERATOR
    # ------------------------------------------------------------
    def explain_concept(self, concept):
        """Explain concept in simple terms"""
        results = self.vector_store.search(concept, top_k=3)
        context = "\n\n".join([r["chunk"] for r in results])

        # Use external prompt template
        if self.explain_prompt_template:
            prompt = self.explain_prompt_template.format(
                concept=concept,
                context=context
            )
        else:
            # Fallback prompt
            prompt = f"Explain {concept} simply from: {context}"

        response = self.model.generate_content(prompt)
        return response.text

# ============================================================
#              CLI MODE APP ~ (python agent.py)
# ============================================================
def main():
    """Command-line interface for the tutor"""
    tutor = Tutor()

    # Build mode
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        tutor.build_knowledge_base()
        return

    # Interactive chat mode
    print("\n" + "="*60)
    print("📚 3Ts TUTOR - Your Personal Study Assistant")
    print("="*60)
    print("\n💬 Chat naturally! Examples:")
    print("  • What is Newton's first law?")
    print("  • Give me a quiz on vectors")
    print("  • Summarize chapter 1")
    print("  • Explain momentum simply")
    print("\nType 'quit' or 'q' to exit")
    print("="*60 + "\n")

    while True:
        try:
            user = input("🙋Student: ").strip()

            if not user:
                continue

            if user.lower() in ["quit", "exit", "bye", "q"]:
                print("\n👋 Happy studying! Time is Life, Learn to save it!")
                break

            reply = tutor.chat(user)
            print(f"\n🤖 Tutor:\n{reply}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Happy studying!")
            break
        except Exception as e:
            print(f"\n❌ Oops! Something went wrong: {e}")
            print("Try rephrasing your question or check if the index is built.\n")


if __name__ == "__main__":
    main()