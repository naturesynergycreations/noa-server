import asyncio
import websockets
import wave
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def receive_audio(websocket):
    print("ESP32 Connected")

    filename = os.path.join(UPLOAD_DIR, "voice.wav")

    wav = wave.open(filename, "wb")
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(16000)

    try:
        async for message in websocket:

            if isinstance(message, bytes):
                wav.writeframes(message)

            elif message == "END":
                print("Recording Finished")
                break

    except websockets.exceptions.ConnectionClosed:
        print("ESP32 Disconnected")

    finally:
        wav.close()
        print("Saved:", filename)

async def main():
    print("Waiting for ESP32...")
    async with websockets.serve(receive_audio, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())