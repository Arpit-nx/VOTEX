import tkinter as tk
from tkinter import messagebox
from My_project.Voice_to_text import VoiceToText
from My_project.Text_to_voice import TextToVoice
from My_project.database import DatabaseHandler
from googletrans import Translator

# Initialize classes
voice_to_text = VoiceToText()
text_to_voice = TextToVoice()
translator = Translator()
db_handler = DatabaseHandler()

# Ensure the translations table is created
db_handler.create_table()

# Common languages and their codes for the dropdown menu
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
}

def handle_voice_to_text():
    # Use VoiceToText class to convert speech to text
    input_text = voice_to_text.speech_to_text()
    recognized_text.set(input_text)

def handle_text_to_voice():
    target_lang = LANGUAGES[language.get()]
    
    if not target_lang:
        messagebox.showerror("Error", "Please select a target language.")
        return
    
    text = translated_text_var.get()
    
    if not text:
        messagebox.showerror("Error", "No text to convert to speech.")
        return
    
    # Use TextToVoice class to convert text to speech
    audio_file_path = text_to_voice.text_to_speech(text, target_lang)
    if audio_file_path:
        # Save the recognized, translated text, and audio file path to the database
        db_handler.insert_translation(recognized_text.get(), translated_text_var.get(), audio_file_path)
        messagebox.showinfo("Success", f"Speech saved as {audio_file_path}")

def handle_translation():
    target_lang = LANGUAGES[language.get()]
    
    if not target_lang:
        messagebox.showerror("Error", "Please select a target language.")
        return
    
    input_text = recognized_text.get()
    
    if not input_text:
        messagebox.showerror("Error", "No text to translate.")
        return
    
    # Translate the text
    try:
        translated = translator.translate(input_text, dest=target_lang)
        translated_text_var.set(translated.text)
    except Exception as e:
        messagebox.showerror("Error", f"Translation error: {e}")

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

tk.Button(root, text="Speak (Voice to Text)", command=handle_voice_to_text).pack(pady=10)
tk.Label(root, text="Recognized Text:").pack(pady=5)
tk.Label(root, textvariable=recognized_text, wraplength=400, bg="light yellow", width=50, height=5).pack(pady=5)

tk.Button(root, text="Translate", command=handle_translation).pack(pady=10)
tk.Label(root, text="Translated Text:").pack(pady=5)
tk.Label(root, textvariable=translated_text_var, wraplength=400, bg="light cyan", width=50, height=5).pack(pady=5)

tk.Button(root, text="Text to Speech", command=handle_text_to_voice).pack(pady=20)

# Close database connection when the app closes
def on_closing():
    db_handler.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
root.mainloop()
