import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def listen(filename):
    with open(filename, "rb") as audio_file:
        print("Uploading voice.wav to Groq...")

    with open("uploads/voice.wav", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=("voice.wav", audio_file),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            language="en",
            temperature=0
        )

    text = transcription.text.strip()
    print("Whisper:", repr(text))
    return text