import speech_recognition as sr

class VoiceToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self):
        try:
            # Capture audio from the microphone
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = self.recognizer.listen(source)
            
            # Convert audio to text
            input_text = self.recognizer.recognize_google(audio)
            return input_text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError as e:
            return f"Error with Google Web Speech API: {e}"
