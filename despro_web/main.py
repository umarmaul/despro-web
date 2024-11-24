import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect, Request
import os

app = FastAPI()

# Mount static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Templates setup
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Oven state
oven_status = {"state": "OFF"}
connected_clients = []


@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "status": oven_status["state"]})


@app.post("/voice-command/")
async def handle_command(intent: dict):
    command = intent.get("intent", {}).get("name")
    global oven_status

    if command == "TurnOnOven":
        oven_status["state"] = "ON"
        await notify_clients()
        return {"status": "success", "message": "Oven turned on"}
    elif command == "TurnOffOven":
        oven_status["state"] = "OFF"
        await notify_clients()
        return {"status": "success", "message": "Oven turned off"}
    else:
        return {"status": "error", "message": "Unknown command"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def notify_clients():
    for client in connected_clients:
        await client.send_json({"oven_status": oven_status["state"]})


def main() -> None:
    uvicorn.run("despro_web.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
