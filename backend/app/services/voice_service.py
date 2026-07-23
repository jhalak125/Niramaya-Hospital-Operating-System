from gtts import gTTS
import uuid
import os

AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)


def generate_voice(text, lang):

    filename = f"{uuid.uuid4()}.mp3"

    filepath = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(
        text=text,
        lang=lang,
        slow=False
    )

    tts.save(filepath)

    return f"/audio/{filename}"