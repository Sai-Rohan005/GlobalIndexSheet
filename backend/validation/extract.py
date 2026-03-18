from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
import io
import google.generativeai as genai
import os


# -------- TEXT EXTRACTION -------- #

def extract_text_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    return text


def extract_text_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])


def extract_text_image(file_bytes):
    # OCR removed (deployment safe)
    return "Image text extraction not supported"


def extract_text_txt(file_bytes):
    try:
        return file_bytes.decode("utf-8")
    except:
        return ""


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


# -------- RELEVANCE CHECK (LIGHTWEIGHT) -------- #

def is_relevant(subject, text):
    try:
        if not text.strip():
            return False, 0.0

        # Configure Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("models/gemini-flash-latest")

        prompt = f"""
        Determine whether the following content is relevant to the given subject.

        Subject: {subject}

        Content:
        {text[:1000]}

        Respond with ONLY one word:
        Relevant OR Irrelevant
        """

        response = model.generate_content(prompt)
        result = response.text.strip().lower()

        if "relevant" in result:
            return True, 0.9
        else:
            return False, 0.1

    except Exception as e:
        print("Relevance check error:", e)
        return True, 0.5  # fallback (avoid blocking flow)