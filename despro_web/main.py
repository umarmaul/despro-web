from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from despro_web.routes import api, websocket

import os
import uvicorn

app = FastAPI()

# Tambahkan CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfigurasi direktori static dan templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Register API dan WebSocket
app.include_router(api.router, prefix="/api")
app.include_router(websocket.router)


@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "status": "OFF"}
    )


# Jalankan aplikasi
def main() -> None:
    uvicorn.run("despro_web.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
