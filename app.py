import pytesseract
import shutil
import os
import random
from PIL import Image
from pdf2image import convert_from_bytes,convert_from_path
import io
import webbrowser
from io import BytesIO
import base64
import streamlit as st
from englisttohindi.englisttohindi import EngtoHindi
from googletrans import Translator
from textblob import TextBlob
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI

translator = Translator()

new_txt=""
# result = llm.invoke("Write a ballad about LangChain")
def apply_spell_check(extracted_text):
    try:
        text = TextBlob(extracted_text)
        corrected_text = str(text.correct())
        return corrected_text
    except Exception as e:
        print("Error during spell check:", e)
        return None

def create_download_link(text, filename):
    # Convert the text to bytes
    text_bytes = text.encode()

    # Encode the bytes to base64
    b64 = base64.b64encode(text_bytes).decode()

    # Create the download link
    download_link = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download text file</a>'

    return download_link
st.write("First clear cache before using for faster result")
butto=st.button("Clear Cache")
if butto:
    st.cache_data.clear()
    st.success("Cleared!")
    webbrowser.open("https://pdf-text-totxtconverter-xtpnypcj4tbm7f5tcnvtov.streamlit.app/", new=0)
file = st.file_uploader("Choose a PDF file", type="pdf")
key=st.text_input("Enter the key")
butt=st.button("Submit")

tx=""
original_txt=""

if file is not None and key and butt:
    # Convert the PDF to images
    #pdf-->bytes-->images
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=f"{key}")
    pop_path = r'poppler-24.02.0/Library/bin'
    images = convert_from_bytes(file.read())
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=f"{key}") 
    # Display the images
    for i, image in enumerate(images):
        # Convert the PIL image to a format that Streamlit can display
        img_bytes = BytesIO()


        image.save(img_bytes,format='PNG')
        #doing format=jpeg and reducing quality will make it a little faster
        img_bytes = img_bytes.getvalue()
        st.image(img_bytes, caption=f'Page {i+1}', use_column_width=True)
        img = Image.open(BytesIO(img_bytes))
        txt=pytesseract.image_to_string(img)
         
        result=llm.invoke(f"Translate this text separated by triple backticks delimiter(```) \n Text: \n ```\n {txt} \n ``` \n in Hindi without changing its meaning")
        tx+="\n ----- \n"+result+"\n ----- \n"
         
          # res=translator.translate(str(txt),dest='hi')
          # tx+="\n ----- \n"+str(res.text)+"\n ----- \n"
          # t=apply_spell_check(txt)
          # r=translator.translate(str(t),dest='hi')
          # st.write(len(t))
          # st.write(r)
    st.session_state.extracted_txt=tx
if "extracted_txt" in st.session_state and key:
  tx=st.session_state.extracted_txt  
  b=st.button("Download in txt format")
  if b:
    
    # download_link = create_download_link(tx, "output.txt")
    lnk2= create_download_link(tx, "output_gemini.txt") 
    
    st.markdown(lnk2, unsafe_allow_html=True)  
          
