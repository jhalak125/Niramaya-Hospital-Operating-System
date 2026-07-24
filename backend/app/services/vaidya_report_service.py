from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

import io
import os
import shutil
from PIL import Image, ImageEnhance, ImageOps
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


def _ocr_image_preprocess(img):
    """
    High-precision multi-pass OCR image preprocessor.
    Safely executes pytesseract across original, contrast-enhanced, thresholded, and rotated images.
    """
    if not pytesseract:
        return ""
    try:
        extracted_lines = []

        # 1. Direct pass on raw original image (Fastest & most accurate for clear scans)
        try:
            raw_txt = pytesseract.image_to_string(img).strip()
            if raw_txt:
                for line in raw_txt.split("\n"):
                    l = line.strip()
                    if l and len(l) > 1:
                        extracted_lines.append(l)
        except Exception as e:
            print("Raw OCR pass exception:", e)

        # 2. Preprocessed passes (Grayscale, Contrast, Sharpness, Autocontrast, Inverted)
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")
        w, h = img.size
        if w < 2000:
            scale = 2000.0 / w
            img_scaled = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        else:
            img_scaled = img

        gray = img_scaled.convert("L")
        enhanced = ImageEnhance.Contrast(gray).enhance(2.5)
        sharpened = ImageEnhance.Sharpness(enhanced).enhance(2.5)
        auto = ImageOps.autocontrast(gray)

        images_to_try = [gray, enhanced, sharpened, auto]

        for im in images_to_try:
            for psm in ["--psm 3", "--psm 6", "--psm 4", "--psm 11", ""]:
                try:
                    txt = pytesseract.image_to_string(im, config=psm).strip()
                    if txt:
                        for line in txt.split("\n"):
                            line_clean = line.strip()
                            if line_clean and line_clean not in extracted_lines and len(line_clean) > 1:
                                extracted_lines.append(line_clean)
                except Exception:
                    pass

        # 3. Rotation passes for camera photo orientation issues
        if len(extracted_lines) < 3:
            for angle in [90, 180, 270]:
                try:
                    rot = img.rotate(angle, expand=True)
                    txt = pytesseract.image_to_string(rot.convert("L"), config="--psm 3").strip()
                    if txt:
                        for line in txt.split("\n"):
                            line_clean = line.strip()
                            if line_clean and line_clean not in extracted_lines:
                                extracted_lines.append(line_clean)
                except Exception:
                    pass

        return "\n".join(extracted_lines).strip()
    except Exception as master_ocr_err:
        print("Image Preprocessing OCR Exception:", master_ocr_err)
        return ""


async def analyze_report(file):
    """
    Extracts text from uploaded image (via multi-pass OCR) or PDF document (via PyPDF/OCR),
    and sends the exact extracted OCR text to Vaidya AI for layman report explanation.
    """
    try:
        content = await file.read()
        filename = (file.filename or "").lower()
        content_type = (file.content_type or "").lower()

        extracted_text = ""

        # 1. Image OCR Processing (PNG, JPG, JPEG, WEBP)
        if any(ext in filename for ext in [".png", ".jpg", ".jpeg", ".webp"]) or content_type.startswith("image/"):
            try:
                img = Image.open(io.BytesIO(content))
                extracted_text = _ocr_image_preprocess(img)
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
                            txt = _ocr_image_preprocess(img)
                            if txt:
                                ocr_texts.append(txt)
                    if ocr_texts:
                        extracted_text = "\n".join(ocr_texts).strip()
                except Exception as pdf_img_err:
                    print("PDF Image OCR Exception:", pdf_img_err)

        # Send exact OCR text to Vaidya AI prompt
        result = await analyze_medical_report(extracted_text, filename=file.filename or "")

        english_text = await generate_english_narration(result)
        hindi_text = await generate_hindi_narration(result)

        result["english_text"] = english_text
        result["hindi_text"] = hindi_text
        result["english_voice"] = generate_voice(english_text, "en")
        result["hindi_voice"] = generate_voice(hindi_text, "hi")

        return result
    except Exception as master_report_err:
        print("analyze_report Master Exception:", master_report_err)
        return await analyze_medical_report("", getattr(file, "filename", ""))