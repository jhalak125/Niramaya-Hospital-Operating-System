from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

import io
from PIL import Image, ImageEnhance, ImageOps
from pypdf import PdfReader
from app.services.voice_service import generate_voice
import shutil

try:
    import pytesseract
    tesseract_bin = shutil.which("tesseract") or "/usr/bin/tesseract" or "/usr/local/bin/tesseract" or "/opt/homebrew/bin/tesseract"
    if tesseract_bin:
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseract_bin
        except Exception:
            pass
except ImportError:
    pytesseract = None


def _ocr_image_preprocess(img):
    """
    High-precision multi-pass OCR image preprocessor.
    Applies image scaling, contrast sharpening, autocontrast, binarization, and rotation.
    """
    if not pytesseract:
        return ""
    try:
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")
        w, h = img.size
        if w < 2400:
            scale = 2400.0 / w
            img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

        gray = img.convert("L")
        enhanced = ImageEnhance.Contrast(gray).enhance(3.5)
        sharpened = ImageEnhance.Sharpness(enhanced).enhance(3.5)
        auto = ImageOps.autocontrast(gray)
        inverted = ImageOps.invert(gray)

        images_to_try = [gray, enhanced, sharpened, auto, inverted]
        extracted_lines = []

        for im in images_to_try:
            for config in ["--psm 3", "--psm 6", "--psm 4", "--psm 11", "--psm 1", ""]:
                try:
                    txt = pytesseract.image_to_string(im, config=config).strip()
                    if txt:
                        for line in txt.split("\n"):
                            line_clean = line.strip()
                            if line_clean and line_clean not in extracted_lines and len(line_clean) > 1:
                                extracted_lines.append(line_clean)
                except Exception:
                    pass

        # Rotation checks for sideways/upside-down camera photo scans
        if len(extracted_lines) < 3:
            for angle in [90, 180, 270]:
                try:
                    rot = img.rotate(angle, expand=True)
                    rot_gray = rot.convert("L")
                    txt = pytesseract.image_to_string(rot_gray, config="--psm 3").strip()
                    if txt:
                        for line in txt.split("\n"):
                            line_clean = line.strip()
                            if line_clean and line_clean not in extracted_lines:
                                extracted_lines.append(line_clean)
                except Exception:
                    pass

        return "\n".join(extracted_lines).strip()
    except Exception as e:
        print("Image Preprocessing OCR Exception:", e)
        return ""


async def analyze_report(file):
    """
    Extracts text from uploaded image (via multi-pass OCR) or PDF document (via PyPDF/OCR),
    and sends the exact extracted text to Vaidya AI for analysis.
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

        # Send exact OCR / PDF extracted text to Vaidya AI for analysis
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