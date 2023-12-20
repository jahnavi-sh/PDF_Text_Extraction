import streamlit as st
from zipfile import ZipFile
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import base64

# OCR
import pdf2image
import pytesseract

def images_to_txt(path, language):
    images = pdf2image.convert_from_bytes(path)
    all_text = []
    for i in images:
        pil_im = i
        text = pytesseract.image_to_string(pil_im, lang=language)
        all_text.append(text)
    return all_text, len(all_text)

def convert_pdf_to_txt_pages(path):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    size = 0
    c = 0
    file_pages = PDFPage.get_pages(path)
    nbPages = len(list(file_pages))
    
    for page in PDFPage.get_pages(path):
        interpreter.process_page(page)
        t = retstr.getvalue()
        if c == 0:
            texts.append(t)
        else:
            texts.append(t[size:])
        c = c + 1
        size = len(t)
    
    device.close()
    retstr.close()
    return texts, nbPages

def convert_pdf_to_txt_file(path):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    file_pages = PDFPage.get_pages(path)
    nbPages = len(list(file_pages))
    
    for page in PDFPage.get_pages(path):
        interpreter.process_page(page)
        t = retstr.getvalue()
    
    device.close()
    retstr.close()
    return t, nbPages

def save_pages(pages):
    files = []
    for page in range(len(pages)):
        filename = "page_" + str(page) + ".txt"
        with open("./file_pages/" + filename, 'w', encoding="utf-8") as file:
            file.write(pages[page])
            files.append(file.name)
    
    zipPath = './file_pages/pdf_to_txt.zip'
    with ZipFile(zipPath, 'w') as zipObj:
        for f in files:
            zipObj.write(f)
    
    return zipPath

def displayPDF(file):
    base64_pdf = base64.b64encode(file).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# UI
st.title("PDF to Text Converter")

pdf_file = st.file_uploader("Upload your PDF file", type=['pdf', 'png', 'jpg'])

if pdf_file:
    path = pdf_file.read()
    file_extension = pdf_file.name.split(".")[-1]
    
    if file_extension == "pdf":
        # OCR checkbox
        ocr_box = st.checkbox('Enable OCR (scanned document)')
        
        # Language selection
        option = st.selectbox('Select the document language', ['eng', 'fra', 'ara', 'spa'])
        
        # PDF to text options
        text_output = st.selectbox("Text Output Options", ['One text file (.txt)', 'Text file per page (ZIP)'])
        
        if text_output == 'One text file (.txt)':
            if ocr_box:
                texts, nb_pages = images_to_txt(path, option)
                total_pages = "Pages: " + str(nb_pages) + " in total"
                text_data_f = "\n\n".join(texts)
            else:
                text_data_f, nb_pages = convert_pdf_to_txt_file(path)
                total_pages = "Pages: " + str(nb_pages) + " in total"

            st.info(total_pages)
            st.download_button("Download txt file", text_data_f)
        
        else:
            if ocr_box:
                text_data, nb_pages = images_to_txt(path, option)
                total_pages = "Pages: " + str(nb_pages) + " in total"
            else:
                text_data, nb_pages = convert_pdf_to_txt_pages(path)
                total_pages = "Pages: " + str(nb_pages) + " in total"
            
            st.info(total_pages)
            zip_path = save_pages(text_data)
            
            with open(zip_path, "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP (txt)",
                    data=fp,
                    file_name="pdf_to_txt.zip",
                    mime="application/zip"
                )
    else:
        option = st.selectbox("What's the language of the text in the image?", ['eng', 'fra', 'ara', 'spa'])
        pil_image = Image.open(pdf_file)
        text = pytesseract.image_to_string(pil_image, lang=option)
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Display Image"):
                st.image(pdf_file)
        with col2:
            with st.expander("Display Text"):
                st.info(text)
        
        st.download_button("Download txt file", text)
