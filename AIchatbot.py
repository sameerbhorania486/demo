import streamlit as st
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()

# First try Streamlit Cloud Secrets
# If not available, try local .env
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please add it to Streamlit Secrets.")
    st.stop()


# =========================
# GROQ MODEL
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0
)


# =========================
# STREAMLIT PAGE
# =========================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Chatbot")


# =========================
# CHAT MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# DISPLAY OLD MESSAGES
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Type your message...")


if prompt:

    # =========================
    # SAVE USER MESSAGE
    # =========================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # =========================
    # DISPLAY USER MESSAGE
    # =========================

    with st.chat_message("user"):
        st.markdown(prompt)


    # =========================
    # CREATE CHAT HISTORY
    # =========================

    history = []


    # =========================
    # SYSTEM PROMPT
    # =========================

    history.append(
        SystemMessage(
            content="""
You are an AI chatbot created and developed by Sameer Ahemad Bhorania.

If the user asks:
- Who created you?
- Who made you?
- Who is your creator?
- Who developed you?
- Tumhe kisne banaya?
- Tumhe kisne create kiya?

Always answer:

"I was created and developed by Sameer Ahemad Bhorania."

Do not provide any other person's name as your creator.
"""
        )
    )


    # =========================
    # ADD PREVIOUS CONVERSATION
    # =========================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            history.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        else:

            history.append(
                AIMessage(
                    content=msg["content"]
                )
            )


    # =========================
    # GET AI RESPONSE
    # =========================

    try:

        response = llm.invoke(history)

        answer = response.content

    except Exception as e:

        answer = f"Error: {str(e)}"


    # =========================
    # SAVE AI RESPONSE
    # =========================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # =========================
    # DISPLAY AI RESPONSE
    # =========================

    with st.chat_message("assistant"):
        st.markdown(answer)
