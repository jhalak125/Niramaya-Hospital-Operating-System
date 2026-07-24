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
    Extracts text from uploaded images using PyTesseract OCR.
    """
    if not pytesseract:
        return ""
    try:
        extracted = []
        # Raw image pass
        try:
            raw_txt = pytesseract.image_to_string(img).strip()
            if raw_txt:
                extracted.append(raw_txt)
        except Exception:
            pass

        # Enhanced grayscale pass
        try:
            if img.mode not in ("L", "RGB"):
                img = img.convert("RGB")
            gray = img.convert("L")
            enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
            txt2 = pytesseract.image_to_string(enhanced).strip()
            if txt2:
                extracted.append(txt2)
        except Exception:
            pass

        return "\n".join(extracted).strip()
    except Exception:
        return ""


async def analyze_report(file):
    """
    Extracts text from uploaded image (via PyTesseract OCR) or PDF document (via PyPDF/OCR),
    and sends the extracted text to Vaidya AI for layman report explanation.
    """
    try:
        content = await file.read()
        filename = (file.filename or "").lower()
        content_type = (file.content_type or "").lower()

        extracted_text = ""

        # 1. Image OCR Processing (PNG, JPG, JPEG, WEBP)
        if any(ext in filename for ext in [".png", ".jpg", ".jpeg", ".webp"]) or content_type.startswith("image/"):
            try:
                image = Image.open(io.BytesIO(content))
                extracted_text = _ocr_image(image)
            except Exception as img_err:
                print("Image OCR Exception:", img_err)

        # 2. PDF Document Text Extraction (PyPDF + Embedded Image OCR Fallback)
        elif filename.endswith(".pdf") or content_type == "application/pdf":
            try:
                reader = PdfReader(io.BytesIO(content))
                text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                extracted_text = "\n".join(text_pages).strip()
            except Exception as pdf_err:
                print("PDF Text Extraction Exception:", pdf_err)

            if not extracted_text:
                try:
                    reader = PdfReader(io.BytesIO(content))
                    ocr_texts = []
                    for page in reader.pages:
                        for img_file in page.images:
                            img = Image.open(io.BytesIO(img_file.data))
                            txt = _ocr_image(img)
                            if txt:
                                ocr_texts.append(txt)
                    if ocr_texts:
                        extracted_text = "\n".join(ocr_texts).strip()
                except Exception as pdf_img_err:
                    print("PDF Image OCR Exception:", pdf_img_err)

        # Fallback context if OCR text is empty
        if not extracted_text.strip():
            clean_name = filename.split('.')[0].replace('_', ' ').replace('-', ' ').title() if filename else "Medical Diagnostic Report"
            extracted_text = f"Medical Diagnostic Document: {clean_name}"

        # Analyze report using Groq
        result = await analyze_medical_report(extracted_text)

        # Generate narrations
        english_text = await generate_english_narration(result)
        hindi_text = await generate_hindi_narration(result)

        result["english_text"] = english_text
        result["hindi_text"] = hindi_text
        result["english_voice"] = generate_voice(english_text, "en")
        result["hindi_voice"] = generate_voice(hindi_text, "hi")

        return result
    except Exception as master_report_err:
        print("analyze_report Master Exception:", master_report_err)
        return await analyze_medical_report("Medical Diagnostic Report")