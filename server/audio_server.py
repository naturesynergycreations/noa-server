from flask import Flask, request
import wave
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "NOA Audio Server Running"

@app.route("/upload_audio", methods=["POST"])
def upload_audio():

    audio = request.data

    filename = os.path.join(UPLOAD_FOLDER, "voice.wav")

    with wave.open(filename, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)      # 16-bit
        wav.setframerate(16000)
        wav.writeframes(audio)

    return "Audio Saved Successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)