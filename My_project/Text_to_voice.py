from gtts import gTTS
import os

class TextToVoice:
    def __init__(self):
        pass

    def text_to_speech(self, text, lang="en"):
        try:
            # Convert text to speech
            tts = gTTS(text=text, lang=lang, slow=False)
            output_file = "translated_speech.mp3"
            tts.save(output_file)
            print(f"Speech saved as {output_file}")
            return output_file
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return None
