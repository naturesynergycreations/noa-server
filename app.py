from flask import Flask, request
import os
import wave
from flask import send_file
from speech.speech_to_text import listen
from ai.router import ask
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

        import time

        filename = os.path.join(
                UPLOAD_FOLDER,
                f"voice_{int(time.time())}.wav"
            )

        print("Saving to:", filename)

        with wave.open(filename, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(audio)

        print("\n✅ Voice received.")

        # Speech to Text
        question = listen(filename)
        print("You :", repr(question))

        # AI Response
        reply = ask(question)
        print("Noa :", reply)

        
        # Generate reply.mp3
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