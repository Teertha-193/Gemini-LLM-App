from dotenv import load_dotenv
load_dotenv()

import streamlit as slt
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv(key="GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input,image):
    if input!="":
      response=model.generate_content([input,image])
    else:
      response=model.generate_content(image)
    return response.text

slt.set_page_config(page_title="Gemini Image Demo")
slt.header("Gemini LLM Application")
input=slt.text_input("Input :", key='input')
uploaded_image = slt.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    slt.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
submit=slt.button("Tell me about the image")

if submit:
  response=get_gemini_response(input,image)
  slt.subheader("The respose is")
  slt.write(response)
  
