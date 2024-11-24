from fastapi import APIRouter
from despro_web.services.notification import update_oven_status

router = APIRouter()

# Status oven
oven_status = {"state": "OFF"}


@router.post("/voice-command/")
async def handle_command(intent: dict):
    global oven_status
    command = intent.get("intent", {}).get("name")

    if command == "TurnOnOven":
        oven_status["state"] = "ON"
        await update_oven_status(oven_status)
        return {"status": "success", "message": "Oven turned on"}
    elif command == "TurnOffOven":
        oven_status["state"] = "OFF"
        await update_oven_status(oven_status)
        return {"status": "success", "message": "Oven turned off"}
    else:
        return {"status": "error", "message": "Unknown command"}
