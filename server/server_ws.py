import asyncio
import websockets
import json

connected_clients = {}
subscriptions = {}

async def websocket_handler(websocket):
    client_id = id(websocket)
    connected_clients[client_id] = websocket
    subscriptions[client_id] = []

    try:
        async for message in websocket:
            await handle_message(websocket, message)
    finally:
        # Clean up on disconnect
        del connected_clients[client_id]
        del subscriptions[client_id]

async def handle_message(websocket, message):
    data = json.loads(message)
    if data["method"] == "SUBSCRIBE":
        subscriptions[id(websocket)] = data["pairs"]
        print(f"Client {id(websocket)} subscribed to: {data['pairs']}")

async def broadcast(data):
    for client_id, websocket in connected_clients.items():
        if data["s"] in subscriptions[client_id]:
            try:
                await websocket.send(json.dumps(data))
                print(f"Sent update to client {client_id}: {data}")
            except Exception as e:
                print(f"Error sending message to client {client_id}: {e}")

async def start_websocket_server(host_ip, host_port):
    async with websockets.serve(websocket_handler, host_ip, host_port):
        print("WebSocket server started")
        await asyncio.Future()
