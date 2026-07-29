from flask import Flask, request, jsonify
from ai.router import ask
from emotion import detect_emotion

app = Flask(__name__)


@app.route("/")
def home():
    return "Noa AI Server Running"


@app.route("/ping", methods=["POST"])
def ping():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "reply": "No JSON data received.",
                "emotion": "neutral"
            }), 400

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "status": "error",
                "reply": "Question is empty.",
                "emotion": "neutral"
            }), 400

        print("\n==============================")
        print("Question :", question)

        try:
            reply = ask(question)

        except Exception as e:
            print("AI Error:", e)
            reply = "Sorry, I couldn't process your request right now."

        try:
            emotion = detect_emotion(reply)

        except Exception as e:
            print("Emotion Error:", e)
            emotion = "neutral"

        print("Reply :", reply)
        print("Emotion :", emotion)
        print("==============================")

        return jsonify({
            "status": "success",
            "reply": reply,
            "emotion": emotion
        })

    except Exception as e:

        print("Server Error:", e)

        return jsonify({
            "status": "error",
            "reply": "Internal server error.",
            "emotion": "neutral"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )