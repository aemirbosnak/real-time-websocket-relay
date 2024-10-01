import asyncio
import concurrent.futures
from binance_ws import start_binance_websocket
from server_ws import start_websocket_server
from config import DEFAULT_COINS, WEBSOCKET_SERVER_HOST, WEBSOCKET_SERVER_PORT

async def main():
    # Start the Binance WebSocket fetchers in separate threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for symbol in DEFAULT_COINS:
            tasks.append(loop.run_in_executor(executor, start_binance_websocket, symbol))

        # Start the WebSocket server for client connections
        await start_websocket_server(WEBSOCKET_SERVER_HOST, WEBSOCKET_SERVER_PORT)

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())