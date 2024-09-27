from dotenv import load_dotenv
load_dotenv()

import streamlit as slt
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key='GOOGLE_API_KEY')

model=genai.GenerativeModel('google-1.5-flash')

def get_gemini_response(input,image,prompt):
  response=model.generate_content(input,image[0], prompt)
  return response.text

def input_image_setup(uploaded_image):
  if uploaded_image is not None:
    byte_data = uploaded_image.getvalue()
    image_parts = [
      {
        "mime_type": uploaded_image.type,
        "data" : byte_data
      }
    ]
    return image_parts
  else:
    raise FileNotFoundError("No file uploaded")

slt.set_page_config(page_title='Multilingual Invoice Extractor')
slt.header('Multilingual Invoice Extractor')

input = slt.text_input("Input Prompt: ", key='input')
uploaded_image = slt.file_uploader("Choose the image of invoice ", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    slt.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
submit=slt.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding the invoices. We will upload a image of invoice 
and you will have to answer any questions based on the uploaded invoice image
"""
if submit:
  image_data=input_image-details(uploaded_image)
  response=get_gemini_response(input_prompt, image_data, input)
  slt.subheader('The response is')
  slt.write(response)

