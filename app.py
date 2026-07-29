from flask import Flask, request
import os
import wave
from flask import send_file
from speech.speech_to_text import listen
from ai.groq_ai import ask_ai
from speech.text_to_speech import speak

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "NOA Server Running"


@app.route("/upload", methods=["POST"])
def upload():
    try:
        audio = request.data

        filename = os.path.join(UPLOAD_FOLDER, "voice.wav")

        with wave.open(filename, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(audio)

        print("\n✅ Voice received.")

        # Speech to Text
        question = listen()
        print("You :", question)

        # AI Response
        reply = ask_ai(question)
        print("Noa :", reply)


        # Generate reply.mp3
        reply = "Testing"
        speak(reply)

        return {
            "status": "success",
            "question": question,
            "reply": reply
        }

    except Exception as e:
        print("Server Error:", e)
        return {
            "status": "error",
            "message": str(e)
        }, 500

@app.route("/reply", methods=["GET"])
def reply_audio():
    return send_file(
        "reply.wav",
        mimetype="audio/wav"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)