import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate(
        text="Hello, I am Noa.",
        voice="en-US-AriaNeural"
    )
    await communicate.save("reply.mp3")

asyncio.run(main())

print("reply.mp3 created successfully!")