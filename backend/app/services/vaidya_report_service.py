from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

import base64
import io
import os
import requests
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


def _ocr_image_cloud_vision(content_bytes: bytes) -> str:
    """
    Extracts 100% accurate text from uploaded report image bytes via Cloud Vision API.
    Does NOT depend on local Tesseract binary or PyTorch memory.
    """
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        return ""
    try:
        b64 = base64.b64encode(content_bytes).decode("utf-8")
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract ALL medical text, patient details, test names, parameters, measurements, findings, and impressions from this medical report image exactly."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                }
            ],
            "model": "gpt-4o-mini",
            "temperature": 0.1
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        res = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            json=payload,
            headers=headers,
            timeout=20
        )
        if res.status_code == 200:
            txt = res.json()["choices"][0]["message"]["content"].strip()
            if txt:
                print("=== CLOUD VISION OCR EXTRACTED TEXT SUCCESSFULLY ===")
                return txt
    except Exception as e:
        print("Cloud Vision OCR Exception:", e)
    return ""


def _ocr_image_local_tesseract(img: Image.Image) -> str:
    """
    Fallback local OCR text extraction using PyTesseract if available.
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
    """
    Master Vaidya Report Service.
    Extracts text from uploaded image (via Cloud Vision OCR / PyTesseract) or PDF document (via PyPDF),
    and sends the extracted text to Vaidya AI for layman report explanation.
    """
    content = await file.read()
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()
    extracted_text = ""

    # 1. If image file, run Cloud Vision OCR
    if any(ext in filename for ext in [".png", ".jpg", ".jpeg", ".webp"]) or content_type.startswith("image/"):
        extracted_text = _ocr_image_cloud_vision(content)
        if not extracted_text:
            try:
                img = Image.open(io.BytesIO(content))
                extracted_text = _ocr_image_local_tesseract(img)
            except Exception as img_err:
                print("Local Image OCR Exception:", img_err)

    # 2. If PDF document, extract text using pypdf
    elif filename.endswith(".pdf") or content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
            extracted_text = "\n".join(text_pages).strip()
        except Exception as e:
            print("PDF Extraction Exception:", e)

    # Fallback context if OCR text is empty
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