import asyncio
from despro_web.services.oven_service import oven_status
from despro_web.services.notification import websocket_manager


async def countdown_timer():
    while True:
        if oven_status["state"] == "ON" and oven_status["time_remaining"] > 0:
            await asyncio.sleep(1)
            oven_status["time_remaining"] -= 1
            await websocket_manager.broadcast(oven_status)

        elif oven_status["time_remaining"] == 0 and oven_status["state"] == "ON":
            oven_status.update({"state": "OFF", "mode": None, "api_mode": None})
            await websocket_manager.broadcast(oven_status)

        await asyncio.sleep(1)
