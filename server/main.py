import asyncio
from binance_ws import binance_websocket
from server_ws import websocket_server

if __name__ == "__main__":
    symbol = "btcusdt"  # You can change this to any Binance symbol
    loop = asyncio.get_event_loop()

    # Run both Binance WebSocket handler and custom WebSocket server concurrently
    loop.run_until_complete(
        asyncio.gather(
            binance_websocket(symbol),
            websocket_server()
        )
    )
