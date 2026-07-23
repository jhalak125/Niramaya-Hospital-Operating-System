from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

from app.services.voice_service import generate_voice

from PIL import Image
import io

try:
    import easyocr
    reader = easyocr.Reader(["en"])
except Exception:
    reader = None


async def analyze_report(file):

    # Read uploaded image
    content = await file.read()
    extracted_text = ""

    if reader:
        try:
            image = Image.open(io.BytesIO(content))
            ocr_result = reader.readtext(image)
            extracted_text = "\n".join([item[1] for item in ocr_result])
        except Exception:
            extracted_text = "Medical Report File"
    else:
        try:
            extracted_text = content.decode("utf-8", errors="ignore")
            if not extracted_text.strip():
                extracted_text = "Medical Diagnostic Report"
        except Exception:
            extracted_text = "Medical Diagnostic Report"

    print("========== REPORT TEXT ==========")
    print(extracted_text[:200])
    print("=================================")

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