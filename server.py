from flask import Flask, request
import wave
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():

    filename = os.path.join(UPLOAD_FOLDER, "voice.wav")

    with wave.open(filename, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)      # 16-bit PCM
        wav.setframerate(16000)  # 16 kHz
        wav.writeframes(request.data)

    print("✅ voice.wav saved")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)