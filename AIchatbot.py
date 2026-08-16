import streamlit as st
from dotenv import load_dotenv
import os
import io

from gtts import gTTS

from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)


# =========================
# TEXT TO SPEECH FUNCTION
# =========================

def text_to_speech(text):

    tts = gTTS(text=text, lang="en")

    audio_bytes = io.BytesIO()

    tts.write_to_fp(audio_bytes)

    audio_bytes.seek(0)

    return audio_bytes


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")


# =========================
# GROQ MODEL
# =========================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
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
# SIDEBAR - VOICE TOGGLE
# =========================

with st.sidebar:

    st.subheader("Settings")

    voice_enabled = st.checkbox("🔊 Voice reply (Text to Speech)", value=True)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


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

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)


    # =========================
    # CREATE CHAT HISTORY
    # =========================

    history = []

    # System Prompt
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


    # Add previous conversation
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

    response = llm.invoke(history)

    answer = response.content


    # =========================
    # SAVE AI RESPONSE
    # =========================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(answer)

        # =========================
        # TEXT TO SPEECH
        # =========================

        if voice_enabled:

            try:
                audio_bytes = text_to_speech(answer)
                st.audio(audio_bytes, format="audio/mp3")

            except Exception as e:
                st.warning(f"Voice generation failed: {e}")
