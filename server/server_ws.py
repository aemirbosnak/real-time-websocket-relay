import asyncio
import json

import websockets

clients = set()

async def register_client(ws):
    """Register a new client to the WebSocket."""
    clients.add(ws)
    print(f"New client connected: {ws.remote_address}")
    try:
        await ws.wait_closed()
    finally:
        clients.remove(ws)

async def broadcast(data):
    """Send updated data to all connected clients."""
    message = json.dumps(data)
    if clients:
        await asyncio.wait([client.send(message) for client in clients])

async def websocket_server():
    """Start the WebSocket server for clients to subscribe to."""
    async with websockets.serve(client_handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

async def client_handler(ws):
    """Handle incoming connections from clients."""
    await register_client(ws)

async def push_to_client(data):
    """Push the new data to our clients via our custom WebSocket server."""
    await broadcast(data)
    print(f"Pushed updated data to clients: {data}")
