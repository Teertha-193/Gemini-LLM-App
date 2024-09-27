from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('google-1.5-flash')

def get_gemini_response(input_prompt, image):
    try:
        response = model.generate_content(input_prompt, image)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def handle_uploaded_image(uploaded_image):
    if uploaded_image is not None:
        allowed_types = ["jpg", "jpeg", "png"]
        if uploaded_image.type not in allowed_types:
            st.error(f"Invalid file type. Please upload a jpg, jpeg, or png image.")
            return None

        try:
            return Image.open(uploaded_image)
        except Exception as e:
            st.error(f"Error opening image: {e}")
            return None
    else:
        return None

st.set_page_config(page_title='Multilingual Invoice Extractor')
st.header('Multilingual Invoice Extractor')

input_prompt = """
You are an expert in understanding the invoices. We will upload a image of invoice 
and you will have to answer any questions based on the uploaded invoice image
"""

# input_text = st.text_input("Input Prompt:", key='input')
uploaded_image = st.file_uploader("Choose the image of invoice ", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = handle_uploaded_image(uploaded_image)
    if image is not None:
        st.image(uploaded_image, caption='Uploaded Invoice', use_column_width=True)
submit = st.button("Tell me about the invoice")

if submit:
    response = get_gemini_response(input_prompt, image)
    if response:
        st.subheader('The response is')
        st.write(response)
