import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import sqlite3
import os

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

def speech_to_text():
    try:
        # Capture audio from the microphone
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            messagebox.showinfo("Listening", "Please speak into the microphone.")
            audio = recognizer.listen(source)
        
        input_text = recognizer.recognize_google(audio)
        return input_text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Error with Google Web Speech API: {e}"

def translate_text(input_text, target_lang):
    try:
        # Translate the text
        translated = translator.translate(input_text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation error: {e}"

def text_to_speech(translated_text, target_lang):
    try:
        # Convert text to speech
        tts = gTTS(text=translated_text, lang=target_lang, slow=False)
        output_file = "translated_speech.mp3"
        tts.save(output_file)
        messagebox.showinfo("Success", f"Speech saved as {output_file}")
        return output_file
    except Exception as e:
        messagebox.showerror("Error", f"Text-to-speech error: {e}")
        return None

# Function to handle the translation and speech synthesis
def process_audio():
    try:
        target_lang = LANGUAGES[language.get()]
        
        if not target_lang:
            messagebox.showerror("Error", "Please select a target language.")
            return
        
        # Capture audio and convert it to text
        input_text = speech_to_text()
        recognized_text.set(input_text)
        
        if "error" not in input_text.lower():
            # Translate the text
            translated_text = translate_text(input_text, target_lang)
            translated_text_var.set(translated_text)
            
            # Convert translated text to speech
            if "error" not in translated_text.lower():
                audio_file_path = text_to_speech(translated_text, target_lang)
                if audio_file_path:
                    # Insert the recognized text, translated text, and file path into the database
                    insert_translation(input_text, translated_text, audio_file_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main application window
root = tk.Tk()
root.title("Speech Translator")
root.geometry("500x400")

# Variables for storing inputs and outputs
language = tk.StringVar(root)
language.set("Select Language")  # Default value for the dropdown
recognized_text = tk.StringVar()
translated_text_var = tk.StringVar()

# UI Components
tk.Label(root, text="Select Target Language:").pack(pady=10)
tk.OptionMenu(root, language, *LANGUAGES.keys()).pack(pady=5)  # Dropdown for language selection

tk.Button(root, text="Speak and Translate", command=process_audio).pack(pady=20)

tk.Label(root, text="Recognized Text:").pack(pady=5)
tk.Label(root, textvariable=recognized_text, wraplength=400, bg="light yellow", width=50, height=5).pack(pady=5)

tk.Label(root, text="Translated Text:").pack(pady=5)
tk.Label(root, textvariable=translated_text_var, wraplength=400, bg="light cyan", width=50, height=5).pack(pady=5)

# Initialize the database
init_db()

# Run the Tkinter event loop
root.mainloop()
