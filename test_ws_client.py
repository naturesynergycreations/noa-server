import asyncio
import websockets

async def test():
    uri = "ws://192.168.0.101:8765"

    async with websockets.connect(uri) as ws:
        print("Connected")

        # Send fake audio bytes
        await ws.send(b'\x01\x02\x03\x04' * 1000)

        # Tell server recording is finished
        await ws.send("END")

asyncio.run(test())