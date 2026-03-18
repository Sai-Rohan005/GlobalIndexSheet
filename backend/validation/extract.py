
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from docx import Document
import io


from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')


# -------- TEXT EXTRACTION -------- #

def extract_text_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    # OCR fallback
    if not text.strip():
        images = convert_from_bytes(file_bytes)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text


def extract_text_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])


def extract_text_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image)


def extract_text_txt(file_bytes):
    return file_bytes.decode("utf-8")


def extract_text(filename, content):
    name = filename.lower()

    if name.endswith(".pdf"):
        return extract_text_pdf(content)

    elif name.endswith(".docx"):
        return extract_text_docx(content)

    elif name.endswith(".txt"):
        return extract_text_txt(content)

    elif name.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_image(content)

    return ""


def is_relevant(subject, text):
    subject_emb = model.encode(subject, convert_to_tensor=True)

    # Split into chunks
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    max_score = 0

    for chunk in chunks[:10]:  # limit for speed
        chunk_emb = model.encode(chunk, convert_to_tensor=True)
        score = util.cos_sim(subject_emb, chunk_emb).item()

        if score > max_score:
            max_score = score

    return max_score > 0.02, max_score





