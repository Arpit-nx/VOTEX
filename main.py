from flask import Flask, render_template, request, jsonify, send_from_directory
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import sqlite3
from pydub import AudioSegment

app = Flask(__name__)
translator = Translator()
recognizer = sr.Recognizer()

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'audio')
TEMP_FOLDER = os.path.join(UPLOAD_FOLDER, 'temp_files')
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr",
    "German": "de", "Hindi": "hi", "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja"
}

def init_db():
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS translations (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          recognized_text TEXT,
                          translated_text TEXT,
                          audio_file_path TEXT)''')
    conn.commit()
    conn.close()

def insert_translation(recognized_text, translated_text, audio_file_path):
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO translations (recognized_text, translated_text, audio_file_path) VALUES (?, ?, ?)",
                   (recognized_text, translated_text, audio_file_path))
    conn.commit()
    conn.close()

def convert_to_wav(input_file_path, output_file_path):
    audio = AudioSegment.from_file(input_file_path)
    audio.export(output_file_path, format="wav")
    return output_file_path

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

        with tempfile.NamedTemporaryFile(delete=False, dir=TEMP_FOLDER, suffix=".wav") as temp_audio:
            audio_data.save(temp_audio.name)
            input_audio_path = temp_audio.name

        with tempfile.NamedTemporaryFile(delete=False, dir=TEMP_FOLDER, suffix=".wav") as temp_converted:
            converted_audio_path = convert_to_wav(input_audio_path, temp_converted.name)

        recognized_text = speech_to_text(converted_audio_path)
        translated = translator.translate(recognized_text, dest=target_lang).text

        with tempfile.NamedTemporaryFile(delete=False, dir=UPLOAD_FOLDER, suffix=".mp3") as temp_translated_audio:
            tts = gTTS(translated, lang=target_lang)
            tts.save(temp_translated_audio.name)
            translated_audio_path = temp_translated_audio.name

        insert_translation(recognized_text, translated, os.path.basename(translated_audio_path))
        os.remove(input_audio_path)
        os.remove(converted_audio_path)

        return jsonify({
            'recognized_text': recognized_text,
            'translated_text': translated,
            'audio_file': f'/static/audio/{os.path.basename(translated_audio_path)}'
        })

    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
