from typing import List
from fastapi import WebSocket
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        logging.info(f"Broadcasting message: {message}")
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logging.error(f"Error sending message: {e}")


websocket_manager = WebSocketManager()


async def update_oven_status(oven_status: dict):
    message = {"oven_status": oven_status["state"]}
    await websocket_manager.broadcast(message)
