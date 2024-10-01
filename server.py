import asyncio
import websockets
import json
import time

# Binance Futures WebSocket API endpoint
BINANCE_WS_URL = "wss://fstream.binance.com/ws"

# Set the time limit to control message processing rate (100 ms = 10 messages per second)
RATE_LIMIT_INTERVAL = 0.1


async def binance_websocket(symbol: str):
    url = f"{BINANCE_WS_URL}/{symbol.lower()}@bookTicker"

    async with websockets.connect(url) as websocket:
        print(f"Connected to {url}")
        last_message_time = 0

        while True:
            try:
                message = await websocket.recv()
                current_time = time.time()

                # Ensure we don't process messages faster than 10 per second (i.e., 100 ms apart)
                if current_time - last_message_time >= RATE_LIMIT_INTERVAL:
                    data = json.loads(message)

                    # Extracting relevant fields
                    output = {
                        "e": data['e'],  # Event type
                        "u": data['u'],  # Order book updateId
                        "E": data['E'],  # Event time
                        "T": data['T'],  # Transaction time
                        "s": data['s'],  # Symbol
                        "b": data['b'],  # Best bid price
                        "B": data['B'],  # Best bid quantity
                        "a": data['a'],  # Best ask price
                        "A": data['A'],  # Best ask quantity
                    }

                    # Pretty print the dictionary
                    print(json.dumps(output, indent=4))

                    last_message_time = current_time
                else:
                    await asyncio.sleep(RATE_LIMIT_INTERVAL - (current_time - last_message_time))

            except websockets.ConnectionClosed:
                print("Connection closed, reconnecting...")
                await asyncio.sleep(5)
                continue


if __name__ == "__main__":
    # Run the WebSocket connection
    coin_symbol = "btcusdt"  # You can change this symbol as needed
    asyncio.run(binance_websocket(coin_symbol))
