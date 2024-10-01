import asyncio
import websockets
import json
from server_ws import push_to_client  # Import push_to_client from client_ws_server

BINANCE_WS_URL = "wss://fstream.binance.com/ws"

# Store the last processed bid and ask data
latest_data = {"b": None, "a": None}  # 'b' is best bid, 'a' is best ask


async def binance_websocket(symbol: str):
    url = f"{BINANCE_WS_URL}/{symbol.lower()}@bookTicker"

    async with websockets.connect(url) as websocket:
        print(f"Connected to Binance WebSocket: {url}")

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                best_bid = data["b"]
                best_ask = data["a"]

                # Compare with the previous data
                if best_bid != latest_data["b"] or best_ask != latest_data["a"]:
                    latest_data["b"] = best_bid
                    latest_data["a"] = best_ask

                    # If the data has changed, push it to clients
                    await push_to_client(data)

            except websockets.ConnectionClosed:
                print("Connection to Binance closed, reconnecting...")
                await asyncio.sleep(5)
                continue
