from gtts import gTTS
import uuid
import os

from app.config import settings

AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)


def generate_voice(text, lang):
    try:
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        tts = gTTS(
            text=text,
            lang=lang,
            slow=False
        )

        tts.save(filepath)

        base = settings.BASE_URL.rstrip("/")
        return f"{base}/audio/{filename}"
    except Exception as e:
        print("gTTS Voice Generation Exception:", e)
        return ""