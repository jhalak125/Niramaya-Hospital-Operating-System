from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

import io
import os
import shutil
from PIL import Image, ImageEnhance
from pypdf import PdfReader

from app.services.voice_service import generate_voice

try:
    import pytesseract
    possible_paths = [
        shutil.which("tesseract"),
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
        "/opt/homebrew/bin/tesseract"
    ]
    for p in possible_paths:
        if p and os.path.exists(p) and os.access(p, os.X_OK):
            pytesseract.pytesseract.tesseract_cmd = p
            break
except ImportError:
    pytesseract = None


def _ocr_image(img):
    """
    Lightweight OCR text extraction using PyTesseract (0MB extra RAM).
    """
    if not pytesseract:
        return ""
    try:
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")
        gray = img.convert("L")
        enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
        return pytesseract.image_to_string(enhanced).strip()
    except Exception:
        return ""


async def analyze_report(file):

    content = await file.read()
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()
    extracted_text = ""

    # 1. If PDF document, extract text using pypdf
    if filename.endswith(".pdf") or content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
            extracted_text = "\n".join(text_pages).strip()
        except Exception as e:
            print("PDF Extraction Exception:", e)

    # 2. If image file or scanned document, run lightweight PyTesseract OCR
    if not extracted_text.strip():
        try:
            image = Image.open(io.BytesIO(content))
            extracted_text = _ocr_image(image)
        except Exception as img_err:
            print("Image OCR Exception:", img_err)

    # 3. Clean fallback context if OCR is empty
    if not extracted_text.strip():
        clean_name = filename.split('.')[0].replace('_', ' ').replace('-', ' ').title() if filename else "Medical Diagnostic Report"
        extracted_text = f"Medical Diagnostic Document: {clean_name}"

    print("========== EXTRACTED REPORT TEXT ==========")
    print(extracted_text[:300])
    print("===========================================")

    # Analyze report using Groq
    result = await analyze_medical_report(extracted_text)

    # Generate natural English narration
    english_text = await generate_english_narration(result)

    # Generate natural Hindi narration
    hindi_text = await generate_hindi_narration(result)

    # Convert narrations to speech
    english_audio = generate_voice(
        english_text,
        "en"
    )

    hindi_audio = generate_voice(
        hindi_text,
        "hi"
    )

    result["english_text"] = english_text
    result["hindi_text"] = hindi_text
    result["english_voice"] = english_audio
    result["hindi_voice"] = hindi_audio

    return result