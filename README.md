# PDF_Text_Extraction

This is a simple web application that converts PDF files and photos to text using Streamlit. The application offers an easy-to-use interface for file uploading, optical character recognition, and text extraction.

# Features
1. PDF to Text Conversion: Converts PDF files to text with options for OCR and language selection.
2. Image OCR: Extracts text from images using Tesseract OCR.
3. Text Output Options: Allows users to download the text as a single file or separate files for each page (stored in a ZIP file).
4. Clean UI: Provides a clean and responsive user interface for a seamless experience.

# Usage
**Installation:**
```python
pip install -r requirements.txt
```

**Running the Application:**

```python
streamlit run app.py
```

Open your browser and navigate to the provided URL.

**Upload Files:**

Upload PDF files or images using the file uploader.

**Customize Settings:**

- Enable OCR for scanned documents.
- Choose the language for OCR.
**Select Output Options:**

Choose between a single text file or a ZIP file with text files for each page.
**Download:**

Download the extracted text files or ZIP file based on your preferences.
# Dependencies
- Streamlit
- pdf2image
- pytesseract
- pdfminer.six

# Author
Jahnavi Sharma 
