from sqlalchemy.orm import Session
from despro_web.models.history import CommandHistory
from datetime import datetime


oven_status = {"state": "OFF", "mode": None, "api_mode": None, "time_remaining": 0}


def save_history(db: Session, command: str, response: str):
    history = CommandHistory(
        command=command, response=response, timestamp=datetime.utcnow()
    )
    db.add(history)
    db.commit()


def get_latest_history(db: Session, limit: int = 10):
    return (
        db.query(CommandHistory)
        .order_by(CommandHistory.timestamp.desc())
        .limit(limit)
        .all()
    )


def set_manual_mode(api_mode: int, duration: int):
    oven_status.update(
        {"mode": api_mode, "api_mode": api_mode, "time_remaining": duration * 60}
    )
    return {"status": "success", "message": "Manual mode set"}


def set_auto_mode():
    oven_status.update({"mode": "AUTO", "api_mode": 3, "time_remaining": 300})
    return {"status": "success", "message": "Auto mode set"}


def turn_on_oven():
    if oven_status["mode"] is None or oven_status["api_mode"] is None:
        return {"status": "error", "message": "Set mode and timer first"}
    oven_status["state"] = "ON"
    return {"status": "success", "message": "Oven turned on"}


def turn_off_oven():
    oven_status.update(
        {"state": "OFF", "mode": None, "api_mode": None, "time_remaining": 0}
    )
    return {"status": "success", "message": "Oven turned off"}
