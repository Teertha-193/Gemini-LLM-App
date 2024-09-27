import streamlit as slt
from PyPDF2 import PdfReader
from langchain.text.splitter import RecursiveCharacterTextSplitter
import os

from langchain.google.genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.google_genai import ChatGoogleGeneratieAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
  text=""
  for pdf in pdf_docs:
    pdf_reader=PdfReader(pdf)
    for page in pdf_reader.pages:
      text+=page.extract_text()
    return text

def get_text_chunks(text):
  text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
  chunks=text_splitter.split_text(text)
  return chunks

def get_vector_store(text_chunks):
  embeddings=GoogleGenerativeAIEmbeddings("model/embedding-001")
  vector_store=FAISS.from_texts(text_chunks,embedding=embeddings)
  vector_store.save_local("faiss_index")

def get_coversational_chain():
  prompt_template="""
  Answer the following question as detailed as possible from provided context. Make sure to provide
  all the details. if the answer is not in context, just say,"answer is not in context". Don't provide the answer \n
  Context:\n {context}\n
  Question:\n {question}\n

  Answer:
  """
  model=ChatGoogleGenerativeAI(model='gemini-pro',temperature=0.3)
  PromptTemplate(template=prompt_template,input_variables=["context","question"])
  chain=load_qa_chain(model, chain_type="stuff",prompt=prompt)
  return chain

def user_input(user_question):
  embeddings = GoogleGenerativeAIEmbeddings(model="models/embeddings-001")
  new_db = FAISS.load_local("faiss_index",embeddings)
  docs = new_db.similarity_search(user_question)
  chain=get_conversational_chain()
  response=chain(
    {"input_documents":docs, "question":user_question},
    return_only_outputs=True)
  print(response)
  slt.write("Reply:", response["output_text"])

def main():
  slt.set_page_config("Chat With Multiple PDFs")
  slt.header("Chat with multiple PDFs using Gemini")
  user_question = slt.text_input("Ask a question from the PDF Files")
  if user_question:
    user_input(user_question)
  with slt.sidebar:
    slt.title("Menu:")
    pdf_docs = slt.file_uploader("Upload your PDF Files and click on the submit")
    if slt.button("Submit & Process"):
      with slt.spinner("Processing..."):
        raw_text = get_pdf_text(pdf_docs)
        text_chunks=get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        slt.success("Done")




           



  

      



