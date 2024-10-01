import asyncio
import websockets

async def listen_to_updates():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as websocket:
        print(f"Connected to WebSocket server at {url}")
        while True:
            message = await websocket.recv()
            print(f"Received update: {message}")

if __name__ == "__main__":
    asyncio.run(listen_to_updates())
