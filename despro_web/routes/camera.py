from fastapi import APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from despro_web.services.camera_service import generate_frames, capture_and_predict
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Konfigurasi folder upload
UPLOAD_FOLDER = "despro_web/static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@router.get("/", response_class=HTMLResponse)
async def index():
    """
    Render the main HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": {}})


@router.get("/video_feed")
async def video_feed():
    """
    Video streaming endpoint.
    """
    return StreamingResponse(
        generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.post("/capture")
async def capture():
    """
    Capture a frame and predict whether it's a cat or a dog.
    """
    result = capture_and_predict(UPLOAD_FOLDER)

    # Jika ada error saat capture
    if "error" in result:
        return {"error": result["error"]}

    # Sesuaikan path untuk akses melalui "/static"
    img_path = result["file_path"].replace("despro_web/static", "/static")

    return {"prediction": result["label"], "img_path": img_path}
