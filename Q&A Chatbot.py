from dotenv import load-dotenv
load_dotenv()

import streamlit as slt
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")
model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
  response=chat.send_message(question, stream=True)
  return response

slt.set_page_config(page_title="Q&A Demo")
slt.header("Gemini LLM Application")

if 'chat_history' not in session_state:
  slt.session_state['chat_history']=[]

input=slt.text_input("Input :", key="input")
submit=slt.button("Ask the question")

if submit and input:
  response=get_gemini_response(input)
  slt.session_state['chat_history'].append(("You",input))
  slt.subheader("The response is")
  for chunk in response:
    slt.write(chunk.text)
    slt.session_state['chat_history'].append(("Bot", chunk.text))
slt.subheader("The chat history is")

for role,text in slt.session_state['chat_history']:
  slt.write(f"{role}:{text}")
