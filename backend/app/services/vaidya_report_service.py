from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

import io
from PIL import Image
from pypdf import PdfReader
from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

from app.services.voice_service import generate_voice


async def analyze_report(file):

    # Read uploaded file
    content = await file.read()
    filename = (file.filename or "").lower()
    extracted_text = ""

    # 1. If PDF document, extract text using lightweight pypdf
    if filename.endswith(".pdf") or file.content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
            extracted_text = "\n".join(text_pages)
        except Exception as e:
            print("PDF Extraction Exception:", e)

    # 2. Fallback for images or binary reports
    if not extracted_text.strip():
        try:
            image = Image.open(io.BytesIO(content))
            extracted_text = f"Medical Diagnostic Image (Format: {image.format}, Resolution: {image.size[0]}x{image.size[1]}px)"
        except Exception:
            extracted_text = "Medical Diagnostic Laboratory Report"

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

    # Add narration text (optional - useful for frontend)
    result["english_text"] = english_text
    result["hindi_text"] = hindi_text

    # Add audio URLs
    result["english_voice"] = english_audio
    result["hindi_voice"] = hindi_audio

    return result