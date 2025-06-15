import streamlit as st
from src.crew import create_crew_for_question

st.set_page_config(page_title="Planto.ai Chatbot", layout="centered")
st.title("🤖 Planto.ai Chatbot (Gemini 1.5 Flash)")

# Session chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask about Planto.ai", placeholder="e.g. What does it do?")

if st.button("Ask") and user_input:
    st.session_state.chat_history.append(("User", user_input))
    with st.spinner("Thinking..."):
        answer = create_crew_for_question(user_input)
        st.session_state.chat_history.append(("Bot", answer))

for role, message in st.session_state.chat_history:
    st.markdown(f"**{role}:** {message}")
