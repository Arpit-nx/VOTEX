from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from deep_translator import GoogleTranslator 
from gtts import gTTS
import os
from pymongo import MongoClient
from pydub import AudioSegment

app = Flask(__name__)
translator = GoogleTranslator(source='auto', target='en')
recognizer = sr.Recognizer()

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'audio')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr",
    "German": "de", "Hindi": "hi", "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja"
}

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
mongo_db = client["votex_db"]
translations_collection = mongo_db["translations"]

def convert_webm_to_wav(input_path):
    output_path = input_path.replace(".webm", ".wav")
    audio = AudioSegment.from_file(input_path, format="webm")
    audio.export(output_path, format="wav")
    return output_path

def speech_to_text(audio_file_path):
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
        return recognizer.recognize_google(audio)

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        if 'audio' not in request.files or 'language' not in request.form:
            return jsonify({'error': "Missing 'audio' file or 'language' parameter"}), 400

        audio_data = request.files['audio']
        target_lang = request.form['language']

        if target_lang not in LANGUAGES.values():
            return jsonify({'error': f"Unsupported language code: {target_lang}"}), 400

        temp_path = os.path.join(UPLOAD_FOLDER, audio_data.filename)
        audio_data.save(temp_path)

        if temp_path.endswith(".webm"):
            wav_path = convert_webm_to_wav(temp_path)
        else:
            wav_path = temp_path

        recognized_text = speech_to_text(wav_path)
        translated = translator.translate(recognized_text, target_lang)

        translated_audio_path = os.path.join(UPLOAD_FOLDER, f"translated_{os.path.basename(wav_path)}.mp3")
        tts = gTTS(translated, lang=target_lang)
        tts.save(translated_audio_path)

        # Store translation data in MongoDB
        translation_data = {
            "recognized_text": recognized_text,
            "translated_text": translated,
            "audio_file_path": f"/static/audio/{os.path.basename(translated_audio_path)}"
        }
        translations_collection.insert_one(translation_data)

        return jsonify({
            'recognized_text': recognized_text,
            'translated_text': translated,
            'audio_file': translation_data['audio_file_path']
        })

    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
