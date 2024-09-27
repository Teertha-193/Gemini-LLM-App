from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, chat_history):
    response = chat.send_message(question, stream=True, context=chat_history)
    return response

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input:")
submit = st.button("Ask the question")

if submit and input_text:
    try:
        response = get_gemini_response(input_text, st.session_state['chat_history'])
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The response is:")
        for chunk in response:
            st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
        st.session_state['chat_history'] = st.session_state['chat_history'][-5:]  # Keep only the last 5 messages
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.subheader("The chat history is:")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
