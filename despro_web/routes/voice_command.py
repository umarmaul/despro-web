from fastapi import APIRouter, Depends
from despro_web.services.oven_service import (
    set_manual_mode,
    set_auto_mode,
    turn_on_oven,
    turn_off_oven,
    save_history,
)
from despro_web.services.notification import update_oven_status, broadcast_history
from sqlalchemy.orm import Session
from despro_web.routes.api import get_db

router = APIRouter()

# Pemetaan nilai slot dari kata ke angka
MODE_MAPPING = {"satu": 1, "dua": 2, "tiga": 3}
DURATION_MAPPING = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5}


def map_slot_to_number(slot_value: str, mapping: dict) -> int:
    """
    Mengonversi nilai slot dari kata (satu, dua, tiga) ke angka menggunakan pemetaan.
    """
    if slot_value not in mapping:
        raise ValueError(f"Invalid slot value: {slot_value}")
    return mapping[slot_value]


@router.post("/voice-command/")
async def handle_command(intent: dict, db: Session = Depends(get_db)):
    """
    Endpoint untuk menangani perintah suara dari Rhasspy.
    Menggunakan intent dan slots untuk mengatur mode oven atau mengontrolnya.
    """
    # Ambil nama command dan slot dari request intent
    command = intent.get("intent", {}).get("name")
    slots = intent.get("slots", {})
    response = {"status": "error", "message": "Unknown command"}

    try:
        if command == "TurnOnOven":
            # Nyalakan oven
            response = turn_on_oven()

        elif command == "TurnOffOven":
            # Matikan oven
            response = turn_off_oven()

        elif command == "SetManualMode":
            # Set mode manual
            mode_raw = slots.get("mode", None)
            duration_raw = slots.get("duration", None)

            if not mode_raw or not duration_raw:
                response = {
                    "status": "error",
                    "message": "Mode and duration are required for manual mode",
                }
            else:
                # Pemetaan nilai slot
                mode = map_slot_to_number(mode_raw, MODE_MAPPING)
                duration = map_slot_to_number(duration_raw, DURATION_MAPPING)

                response = set_manual_mode(mode, duration)

        elif command == "SetAutoMode":
            # Set mode otomatis
            response = set_auto_mode()

        else:
            response = {"status": "error", "message": "Invalid command"}

        # Simpan command dan respons ke database
        save_history(db, command, response["message"])

        # Update oven status dan broadcast history melalui WebSocket
        await update_oven_status()
        await broadcast_history(db)

    except ValueError as ve:
        # Tangani error parsing slot
        response = {"status": "error", "message": str(ve)}
    except Exception as e:
        # Tangani error lainnya
        response = {"status": "error", "message": str(e)}

    return response
