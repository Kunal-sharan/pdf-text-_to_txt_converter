import pytesseract
import shutil
import os
import random
from PIL import Image
from pdf2image import convert_from_bytes
import io
import base64
import streamlit as st
from englisttohindi.englisttohindi import EngtoHindi
from googletrans import Translator
from textblob import TextBlob
translator = Translator()
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

file = st.file_uploader("Choose a PDF file", type="pdf")
tx=""
if file is not None:
    # Convert the PDF to images
    #pdf-->bytes-->images
    pop_path = r'poppler-24.02.0/Library/bin'
    images = convert_from_path(file,poppler_path=pop_path)

    # Display the images
    for i, image in enumerate(images):
        # Convert the PIL image to a format that Streamlit can display
        img_bytes = io.BytesIO()


        image.save(img_bytes, format='JPEG',quality=50)
        img_bytes = img_bytes.getvalue()
        st.image(img_bytes, caption=f'Page {i+1}', use_column_width=True)
        img = Image.open(io.BytesIO(img_bytes))
        txt=pytesseract.image_to_string(img)
        tx+="\n ----- \n"+txt+"\n ----- \n"
        if i>0:
          res=translator.translate(str(txt),dest='hi')
          tx+="\n ----- \n"+str(res.text)+"\n ----- \n"
          # t=apply_spell_check(txt)
          # r=translator.translate(str(t),dest='hi')
          # st.write(len(t))
          # st.write(r)
    if tx:
      b=st.button("Download in txt format")
      if b:
        download_link = create_download_link(tx, "output.txt")
        st.markdown(download_link, unsafe_allow_html=True)          


