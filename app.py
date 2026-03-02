from flask import Flask, request, jsonify, send_from_directory
from deep_translator import GoogleTranslator
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FOLDER = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Serve index.html from same folder
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

# Translation API
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text")
    dest = data.get("dest", "en")

    if not text:
        return jsonify({"error": "No text provided"})

    try:
        translated_text = GoogleTranslator(source='auto', target=dest).translate(text)

        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_FOLDER, filename)

        tts = gTTS(text=translated_text, lang=dest)
        tts.save(file_path)

        return jsonify({
            "translated_text": translated_text,
            "audio_url": f"/audio/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# Serve audio
@app.route("/audio/<filename>")
def get_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)