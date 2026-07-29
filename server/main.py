from flask import Flask, request
import wave
import os

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():

    audio = request.data

    filename = "uploads/voice.wav"

    with wave.open(filename, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(audio)

    print("Saved voice.wav")

    return "OK"

app.run(host="0.0.0.0", port=5000)