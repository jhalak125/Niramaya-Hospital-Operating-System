from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

import io
import os
import numpy as np
from PIL import Image
from pypdf import PdfReader

from app.services.voice_service import generate_voice

try:
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
except Exception as err:
    print("EasyOCR init exception:", err)
    reader = None


def _ocr_image(img):
    """
    Extracts text from uploaded images using EasyOCR (pure Python PyTorch OCR).
    Does NOT use Tesseract binary.
    """
    if not reader:
        return ""
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img_np = np.array(img)
        results = reader.readtext(img_np)
        lines = [res[1] for res in results if len(res[1].strip()) > 1]
        return "\n".join(lines).strip()
    except Exception as e:
        print("EasyOCR extraction exception:", e)
        return ""


async def analyze_report(file):

    # Read uploaded file
    content = await file.read()
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()
    extracted_text = ""

    # 1. If image file, extract text using EasyOCR (pure Python PyTorch OCR)
    if any(ext in filename for ext in [".png", ".jpg", ".jpeg", ".webp"]) or content_type.startswith("image/"):
        try:
            image = Image.open(io.BytesIO(content))
            extracted_text = _ocr_image(image)
        except Exception as img_err:
            print("Image OCR Exception:", img_err)

    # 2. If PDF document, extract text using lightweight pypdf + EasyOCR fallback for scanned pages
    elif filename.endswith(".pdf") or content_type == "application/pdf":
        try:
            reader_pdf = PdfReader(io.BytesIO(content))
            text_pages = [page.extract_text() for page in reader_pdf.pages if page.extract_text()]
            extracted_text = "\n".join(text_pages).strip()
        except Exception as e:
            print("PDF Extraction Exception:", e)

        if not extracted_text:
            try:
                reader_pdf = PdfReader(io.BytesIO(content))
                ocr_texts = []
                for page in reader_pdf.pages:
                    for img_file in page.images:
                        img = Image.open(io.BytesIO(img_file.data))
                        txt = _ocr_image(img)
                        if txt:
                            ocr_texts.append(txt)
                if ocr_texts:
                    extracted_text = "\n".join(ocr_texts).strip()
            except Exception as pdf_img_err:
                print("PDF Image OCR Exception:", pdf_img_err)

    # Fallback description if OCR text is blank
    if not extracted_text.strip():
        clean_title = filename.split('.')[0].replace('_', ' ').replace('-', ' ').title() if filename else "Medical Report"
        extracted_text = f"Medical Diagnostic Document: {clean_title}"

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

    # Add narration text
    result["english_text"] = english_text
    result["hindi_text"] = hindi_text

    # Add audio URLs
    result["english_voice"] = english_audio
    result["hindi_voice"] = hindi_audio

    return result