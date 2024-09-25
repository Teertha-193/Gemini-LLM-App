from dotenv import load_dotenv
load_dotenv()

import streamlit as slt
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv(key="GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-pro")

def get_gemini_response(question):
    response=model.generate_content(question)
    return response

slt.set_page_config(page_title="Q&A Demo")
slt.header("Gemini LLM Application")
input=slt.text_input("Input :", key='input')
submit=slt.button("Ask the question")

if submit:
    response=get_gemini_response(input)
    slt.subheader('The response is')
    slt.write(response)
    
