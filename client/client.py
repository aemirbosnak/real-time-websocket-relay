import asyncio
import websockets
import json


async def subscribe_to_coins(coins):
    async with websockets.connect("ws://localhost:8001") as websocket:
        # Send subscription message
        await websocket.send(json.dumps({"method": "SUBSCRIBE", "pairs": coins}))

        try:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        except Exception as e:
            print(f"Connection error: {e}")


async def main():
    # Simulate different clients subscribing to different coins
    client1 = asyncio.create_task(subscribe_to_coins(["BTCUSDT", "ETHUSDT"]))
    client2 = asyncio.create_task(subscribe_to_coins(["ETHUSDT", "BNBUSDT"]))
    client3 = asyncio.create_task(subscribe_to_coins(["BTCUSDT", "BNBUSDT"]))

    await asyncio.gather(client1, client2, client3)


if __name__ == "__main__":
    asyncio.run(main())
