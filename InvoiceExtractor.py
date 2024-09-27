from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('google-1.5-flash')

def get_gemini_response(input,image):
    if input!="":
      response=model.generate_content([input,image])
    else:
      response=model.generate_content(image)
    return response.text
st.set_page_config(page_title='Multilingual Invoice Extractor')
st.header('Multilingual Invoice Extractor')
input="""
You are an expert in understanding the invoices. We will upload a image of invoice 
and you will have to answer any questions based on the uploaded invoice image
"""

uploaded_image = slt.file_uploader("Choose the image of invoice", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    slt.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
submit=slt.button("Tell me about the image")

if submit:
  response=get_gemini_response(input,image)
  slt.subheader("The respose is")
  slt.write(response)
  
