"""
mode for converting text to speech.
"""
from playsound import playsound
import tempfile
import os
from gtts import gTTS

def convert_text_to_speech(text: str):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang="en")
            tts.save(fp.name)
            temp_name = fp.name
            # playsound(fp.name)
        # Now the file is closed, safe to play
        playsound(temp_name)

        # Optionally, delete the file after playback
        os.remove(temp_name)
    except Exception as e:
        print("Error occured while converting text to speech: ", e)
        return