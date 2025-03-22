import pytesseract
from pdf2image import convert_from_path

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = " "
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_text += text + "\n"
    return extracted_text.strip()