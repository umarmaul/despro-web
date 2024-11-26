from fastapi import APIRouter, Depends
from despro_web.services.oven_service import (
    save_history,
    turn_on_oven,
    turn_off_oven,
    get_latest_history,
)
from sqlalchemy.orm import Session
from despro_web.config import get_db


router = APIRouter()


@router.post("/turn-on")
async def turn_on(db: Session = Depends(get_db)):
    response = turn_on_oven()
    save_history(db, "TurnOnOven", response["message"])
    return response


@router.post("/turn-off")
async def turn_off(db: Session = Depends(get_db)):
    response = turn_off_oven()
    save_history(db, "TurnOffOven", response["message"])
    return response
