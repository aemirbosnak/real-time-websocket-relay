import asyncio
import websockets
import json
from server_ws import broadcast

latest_data = {}

async def fetch_binance_data(symbol: str):
    url = f"wss://fstream.binance.com/ws/{symbol.lower()}@bookTicker"

    async with websockets.connect(url) as websocket:
        while True:
            try:
                data = await websocket.recv()
                data = json.loads(data)
                await process_data(data)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                break

async def process_data(data):
    symbol = data["s"]
    # Only store the necessary fields
    new_data = {
        "e": data["e"],
        "s": symbol,
        "b": data["b"],
        "a": data["a"],
    }

    # Check if the data has changed
    if symbol not in latest_data or latest_data[symbol]["b"] != new_data["b"] or latest_data[symbol]["a"] != new_data["a"]:
        latest_data[symbol] = new_data
        print(f"Updated data for {symbol}: {new_data}")
        # Here you would push the update to subscribed clients
        await push_to_client(new_data)

async def push_to_client(data):
    await broadcast(data)

def start_binance_websocket(symbol):
    asyncio.run(fetch_binance_data(symbol))