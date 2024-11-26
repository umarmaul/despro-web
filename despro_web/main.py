import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from despro_web.routes import api, websocket, voice_command, web
from despro_web.tasks.countdown import countdown_timer
from despro_web.config import Base, engine
import os

# Buat tabel database
Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins. Replace "*" with specific IP if needed for security.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(api.router, prefix="/api")
app.include_router(websocket.router)
app.include_router(voice_command.router)
app.include_router(web.router)

app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static"
)


# Jalankan background task untuk countdown timer
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(countdown_timer())


def main():
    uvicorn.run("despro_web.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
