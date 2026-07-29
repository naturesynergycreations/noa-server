import asyncio
import edge_tts
import subprocess
import os

MP3_FILE = "reply.mp3"
WAV_FILE = "reply.wav"

async def generate(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"
    )

    await communicate.save(MP3_FILE)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        MP3_FILE,
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-ar",
        "16000",
        WAV_FILE
    ], check=True)

    print("reply.wav Created")

def speak(text):
    asyncio.run(generate(text))