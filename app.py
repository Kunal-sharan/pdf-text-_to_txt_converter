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
from textblob import TextBlob
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_google_genai import GoogleGenerativeAI
# import streamlit_scrollable_textbox as stx
import PyPDF2
from gtts import gTTS
from langchain_groq import ChatGroq
def text_speech(text):
    tts = gTTS(text=text, lang='hi')
    speech_bytes = io.BytesIO()
    tts.write_to_fp(speech_bytes)
    speech_bytes.seek(0)

    # Convert speech to base64 encoding
    
    return speech_bytes.read()
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
def convert_pdf_to_images(pdf_bytes, start_page=0, end_page=None):
    # Create a PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    # Get the number of pages
    num_pages = len(pdf_reader.pages)

    # Set the end_page to the last page if it's not provided
    if end_page is None:
        end_page = num_pages

    # Convert each page to an image and store them in a list
    images = []
    for i in range(start_page, end_page):
        # Convert the page to an image
        page_images = convert_from_bytes(pdf_bytes, first_page=i+1, last_page=i+1)
        # images.extend(page_images)
        for image in page_images:
            yield image

    # return images
def create_download_link(text, filename):
    # Convert the text to bytes
    text_bytes = text.encode()

    # Encode the bytes to base64
    b64 = base64.b64encode(text_bytes).decode()

    # Create the download link
    download_link = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download text file</a>'

    return download_link
# st.set_page_config(layout="wide")   
st.write("First clear cache before using for faster result")
butto=st.button("Clear Cache")
if butto:
    st.cache_data.clear()
    st.success("Cleared!")
    webbrowser.open("https://pdf-text-totxtconverter-xtpnypcj4tbm7f5tcnvtov.streamlit.app/", new=0)
file = st.file_uploader("Choose a PDF file", type="pdf")
Lang=st.text_input("Enter The Language You want to translate your document into ")
key=st.secrets["GENAI_API_KEY"]
butt=st.button("Submit")

tx=""
original_txt=""

if file is not None and key and butt and Lang:
    # Convert the PDF to images
    #pdf-->bytes-->images
    # llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=f"{key}")
    llm = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key=key # https://console.groq.com/keys
)
    # pop_path = r'poppler-24.02.0/Library/bin'
    # images = convert_pdf_to_images(file.read())
    # Display the images
    i=0
    for image in convert_pdf_to_images(file.read()):
        # Convert the PIL image to a format that Streamlit can display
        img_bytes = BytesIO()


        image.save(img_bytes,format='PNG')
        #doing format=jpeg and reducing quality will make it a little faster
        img_bytes = img_bytes.getvalue()
        i=i+1
        st.image(img_bytes, caption=f'Page {i}', use_column_width=True)
        img = Image.open(BytesIO(img_bytes))
        txt=pytesseract.image_to_string(img)
        result=llm.invoke(f"Translate this text separated by triple backticks delimiter(```) \n Text: \n ```\n {txt} \n ``` \n in {Lang} without changing its meaning")
        result=result.content
        if result:
            with st.container(border=True,height=400):
                st.markdown(result)
            b=result.replace("```"," ")
            st.audio(text_speech(str(b)))
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
          
