from gtts import gTTS
import tempfile
import os

def create_tts_audio_bytes(text: str, lang: str = "en"):
    """
    Returns audio bytes (MP3) for Streamlit's st.audio.
    """
    if not text:
        return None
    # Save to a temporary file, read bytes, and remove
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(tmp.name)
        with open(tmp.name, "rb") as f:
            data = f.read()
        return data
    finally:
        try:
            os.remove(tmp.name)
        except OSError:
                pass
