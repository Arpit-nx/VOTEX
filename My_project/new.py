from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import sqlite3
import os

app = Flask(__name__)

# Initialize the translator and speech recognizer
translator = Translator()
recognizer = sr.Recognizer()

# Expanded list of languages including Indian languages and their codes for the dropdown menu
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS translations
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
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

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate_audio():
    try:
        # Check if the audio file is provided
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        # Save the audio file
        audio_file = request.files['audio']
        audio_file_path = os.path.join('uploads', audio_file.filename)
        os.makedirs('uploads', exist_ok=True)
        audio_file.save(audio_file_path)

        # Recognize speech
        with sr.AudioFile(audio_file_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
        input_text = recognizer.recognize_google(audio)

        # Translate the recognized text
        target_language = request.form.get('language')
        if target_language not in LANGUAGES.values():
            return jsonify({'error': 'Invalid target language selected'}), 400

        translated_text = translator.translate(input_text, dest=target_language).text

        # Convert the translated text to speech
        tts = gTTS(text=translated_text, lang=target_language)
        output_file_path = os.path.join('outputs', 'translated_speech.mp3')
        os.makedirs('outputs', exist_ok=True)
        tts.save(output_file_path)

        # Save the result to the database
        insert_translation(input_text, translated_text, output_file_path)

        return jsonify({
            'input_text': input_text,
            'translated_text': translated_text,
            'audio_file': output_file_path
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
