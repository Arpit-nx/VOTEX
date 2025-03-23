from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    r = sr.Recognizer()
    
    # Check if the request contains an audio file
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided.'}), 400
    
    audio_file = request.files['audio']
    
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        # Recognize speech using Google Web Speech API
        input_text = r.recognize_google(audio)
        
        # Translate the recognized text to the target language
        target_lang = request.form['language']
        translated = translator.translate(input_text, dest=target_lang)
        translated_text = translated.text
        
        # Convert the translated text to speech
        tts = gTTS(text=translated_text, lang=target_lang, slow=False)
        
        # Save the audio file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        
        return jsonify({'input_text': input_text, 'translated_text': translated_text, 'audio_file': temp_file.name})
    
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio.'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Could not request results; {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
