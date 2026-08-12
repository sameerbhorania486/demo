from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found in .env")


# =========================
# LOAD TXT FILES
# =========================

text_loader = DirectoryLoader(
    path="books",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

text_docs = text_loader.load()

print("TXT files loaded:", len(text_docs))


# =========================
# COMBINE DOCUMENTS
# =========================

knowledge = "\n\n".join(
    doc.page_content for doc in text_docs
)


# =========================
# LLM
# =========================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=api_key
)


# =========================
# ASK QUESTION
# =========================

def ask_question(question):

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using the information
provided in the knowledge base below.

If the answer is present in the knowledge base,
give a clear answer.

If the answer is not present, say:
"I don't have this information in the knowledge base."

Knowledge Base:
{knowledge}

User Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content
