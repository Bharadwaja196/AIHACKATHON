import streamlit as st
from core_logic.chat_engine import ChatEngine
from core_logic.emotion_analyzer import EmotionAnalyzer
from core_logic.memory_manager import MemoryManager

st.set_page_config(page_title="🧠 AGI Chat Dashboard", layout="wide")

# Initialize core components
chat_engine = ChatEngine()
emotion_analyzer = EmotionAnalyzer()
memory_manager = MemoryManager()

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🤖 AGI Core Chat")
st.markdown("Talk to your AGI and watch it think.")

# Chat UI
user_input = st.text_input("🗣️ You:", placeholder="Type your message and press Enter...")
if user_input:
    # Retrieve memory
    retrieved, _ = zip(*memory_manager.retrieve_similar(user_input)) if memory_manager else ([], [])

    # Get response
    agi_response = chat_engine.generate_response(user_input, list(retrieved))

    # Analyze emotion
    emotion = emotion_analyzer.detect_emotion(user_input)

    # Store memory
    memory_manager.store_memory(user_input, agi_response)

    # Save to session history
    st.session_state.history.append({
        "user": user_input,
        "agi": agi_response,
        "emotion": emotion,
        "memory": list(retrieved)
    })

# Display chat history
for chat in reversed(st.session_state.history):
    with st.chat_message("🧑 You"):
        st.markdown(chat["user"])
    with st.chat_message("🤖 AGI"):
        st.markdown(chat["agi"])
        st.caption(f"Emotion: `{chat['emotion']}`")
        if chat["memory"]:
            with st.expander("📚 Recalled Memories", expanded=False):
                for mem in chat["memory"]:
                    st.markdown(f"- {mem}")
