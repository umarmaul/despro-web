from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from despro_web.services.oven_service import get_latest_history
from despro_web.config import get_db
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))


@router.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    history = get_latest_history(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "history": history}
    )
