from typing import List
from fastapi import WebSocket
from despro_web.services.oven_service import oven_status
from despro_web.models.history import CommandHistory
from sqlalchemy.orm import Session


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


websocket_manager = WebSocketManager()


async def update_oven_status():
    """
    Kirimkan status oven terbaru melalui WebSocket.
    """
    message = {
        "type": "status_update",
        "state": oven_status["state"],
        "mode": oven_status["mode"],
        "api_mode": oven_status["api_mode"],
        "time_remaining": oven_status["time_remaining"],
    }
    await websocket_manager.broadcast(message)


async def broadcast_history(db: Session):
    """
    Kirimkan data 10 history terbaru ke semua klien melalui WebSocket.
    """
    history = (
        db.query(CommandHistory)
        .order_by(CommandHistory.timestamp.desc())
        .limit(10)
        .all()
    )
    message = {
        "type": "history_update",
        "history": [
            {
                "command": h.command,
                "response": h.response,
                "timestamp": h.timestamp.isoformat(),
            }
            for h in history
        ],
    }
    await websocket_manager.broadcast(message)
