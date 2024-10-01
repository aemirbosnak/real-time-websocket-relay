# Binance WebSocket URL for book ticker
BINANCE_WS_URL_TEMPLATE = "wss://fstream.binance.com/ws/{symbol}@bookTicker"

# WebSocket server settings
WEBSOCKET_SERVER_HOST = "0.0.0.0"
WEBSOCKET_SERVER_PORT = 8001

# List of coin symbols to subscribe to (can be modified)
DEFAULT_COINS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

# Maximum number of concurrent clients
MAX_CLIENTS = 100
