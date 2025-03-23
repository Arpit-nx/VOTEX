import threading
import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
from queue import Queue
from googletrans import Translator
from gtts import gTTS
import pygame
import io

# Queue to communicate between threads
queue = Queue()

# Flag to stop the thread
stop_flag = threading.Event()

# Initialize Pygame
pygame.mixer.init()

# Language codes for text-to-speech
language_codes = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Urdu": "ur",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "English": "en"
}

def speech_recognition_thread():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)  # Adjust for ambient noise
        while not stop_flag.is_set():
            try:
                queue.put("mic_ready")
                audio = recognizer.listen(source, timeout=10)  # Set timeout to a reasonable value
                text = recognizer.recognize_google(audio, language="en-US")  # Default to English
                queue.put(text)
            except sr.UnknownValueError:
                queue.put("Could not understand audio")
            except sr.RequestError as e:
                queue.put(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.WaitTimeoutError:
                queue.put("Listening timed out, please try again.")
            except Exception as e:
                queue.put(f"An unexpected error occurred: {e}")

def translate_text(text, target_language):
    try:
        translator = Translator()
        result = translator.translate(text, dest=target_language)
        return result.text
    except Exception as e:
        return f"Error: {e}"

def speak_text(text, language_code='en'):
    try:
        tts = gTTS(text=text, lang=language_code)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        pygame.mixer.music.load(audio_fp, 'mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            root.update()  # Update GUI to ensure responsiveness
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert text to speech: {e}")

def update_gui():
    if not queue.empty():
        data = queue.get()

        if data == "mic_ready":
            mic_status_label.config(text="Mic is ready to accept input", fg="green")
            progress_bar.start()
        else:
            mic_status_label.config(text="Processing...", fg="orange")
            recognized_text_box.insert(tk.END, f"{data}\n")
            progress_bar.stop()

            # Translate the text
            translated_text = translate_text(data, output_language_var.get())
            translated_text_box.insert(tk.END, f"{translated_text}\n")
            reply_input.delete(0, tk.END)  # Clear the reply input field
            
            # Auto-scroll to the bottom
            recognized_text_box.yview(tk.END)
            translated_text_box.yview(tk.END)

    if not stop_flag.is_set():
        root.after(100, update_gui)

def start_listening():
    stop_flag.clear()
    thread = threading.Thread(target=speech_recognition_thread, daemon=True)
    thread.start()

def stop_listening():
    stop_flag.set()
    progress_bar.stop()
    mic_status_label.config(text="Stopped", fg="red")

def send_reply():
    reply_text = reply_input.get()
    if reply_text:
        # Translate the reply text to the selected output language
        translated_reply = translate_text(reply_text, output_language_var.get())
        
        # Display the translated reply in the Text box
        reply_text_box.insert(tk.END, f"{translated_reply}\n")
        reply_input.delete(0, tk.END)
        
        # Speak the translated reply text in English
        speak_text(translated_reply, 'en')
    else:
        messagebox.showwarning("Input Error", "Please enter a reply.")

# Create the main window
root = tk.Tk()
root.title("Speech-to-Text, Translation, and Voice Reply")

# Style the window background
root.configure(bg="#2c3e50")  # Dark background

# Mic status label
mic_status_label = tk.Label(root, text="Mic is not ready", font=("Arial", 14), bg="#2c3e50", fg="red")
mic_status_label.pack(pady=10)

# Output language dropdown
output_language_label = tk.Label(root, text="Select Output Language:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
output_language_label.pack(pady=5)

output_language_var = tk.StringVar(value="en")
output_language_menu = ttk.Combobox(root, textvariable=output_language_var, values=list(language_codes.keys()))
output_language_menu.pack()

# Recognized text box
recognized_text_box_label = tk.Label(root, text="Recognized Text:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
recognized_text_box_label.pack(pady=5)
recognized_text_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", height=5, width=50)
recognized_text_box.pack(padx=20, pady=10)

# Translated text box
translated_text_box_label = tk.Label(root, text="Translated Text:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
translated_text_box_label.pack(pady=5)
translated_text_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", height=5, width=50)
translated_text_box.pack(padx=20, pady=10)

# Reply input
reply_input_label = tk.Label(root, text="Type Your Reply:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
reply_input_label.pack(pady=5)
reply_input = tk.Entry(root, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", width=50)
reply_input.pack(pady=5)

# Send reply button
send_reply_button = ttk.Button(root, text="Send Reply", command=send_reply)
send_reply_button.pack(pady=10)

# Reply text box
reply_text_box_label = tk.Label(root, text="Reply Text:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
reply_text_box_label.pack(pady=5)
reply_text_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", height=5, width=50)
reply_text_box.pack(padx=20, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
progress_bar.pack(pady=20)

# Start and Stop buttons
start_button = ttk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(side=tk.LEFT, padx=10, pady=20)

stop_button = ttk.Button(root, text="Stop Listening", command=stop_listening)
stop_button.pack(side=tk.RIGHT, padx=10, pady=20)

# Start the GUI update loop
root.after(100, update_gui)

root.mainloop()