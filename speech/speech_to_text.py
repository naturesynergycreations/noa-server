import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def listen():
    print("Uploading voice.wav to Groq...")

    with open("uploads/voice.wav", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            response_format="verbose_json",
            language="en",
        )

    text = transcription.text
    print(text)
    return text