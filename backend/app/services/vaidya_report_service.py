from app.ai.vaidya_service import analyze_medical_report

from app.ai.narration_service import (
    generate_english_narration,
    generate_hindi_narration,
)

from app.services.voice_service import generate_voice

import easyocr
from PIL import Image
import io


# Load OCR model once
reader = easyocr.Reader(["en"])


async def analyze_report(file):

    # Read uploaded image
    content = await file.read()

    image = Image.open(io.BytesIO(content))

    # Extract text using OCR
    ocr_result = reader.readtext(image)

    extracted_text = "\n".join([item[1] for item in ocr_result])

    print("========== OCR TEXT ==========")
    print(extracted_text)
    print("==============================")

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