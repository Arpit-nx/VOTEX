from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from google.cloud import translate_v2 as translate
import os

app = Flask(__name__)
translator = translate.Client()

@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()

    # Gather the language input
    gather = Gather(num_digits=1, action="/gather_language")
    gather.say("Press 1 for English to Spanish translation. Press 2 for English to French translation.")
    response.append(gather)

    return str(response)

@app.route("/gather_language", methods=['POST'])
def gather_language():
    response = VoiceResponse()
    digit_pressed = request.form['Digits']
    
    if digit_pressed == '1':
        response.say("You selected English to Spanish translation.")
        response.redirect("/translate?lang=es")
    elif digit_pressed == '2':
        response.say("You selected English to French translation.")
        response.redirect("/translate?lang=fr")
    else:
        response.say("Invalid choice. Please try again.")
        response.redirect("/voice")

    return str(response)

@app.route("/translate", methods=['POST'])
def translate_text():
    lang = request.args.get('lang')
    response = VoiceResponse()

    # Gather speech input
    gather = Gather(input='speech', action=f"/handle_speech?lang={lang}")
    gather.say("Please say the sentence you want to translate.")
    response.append(gather)

    return str(response)

@app.route("/handle_speech", methods=['POST'])
def handle_speech():
    lang = request.args.get('lang')
    speech_result = request.form.get('SpeechResult')
    
    # Translate the speech input
    translation = translator.translate(speech_result, target_language=lang)
    
    response = VoiceResponse()
    response.say(f"The translation is: {translation['translatedText']}")
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)