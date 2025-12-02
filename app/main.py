# app/main.py

import json
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import create_db_and_tables, get_session
from app.services.conversation_engine import ConversationEngine
from app.models.chat_models import ChatClientMessage

# ✅ ADD THIS IMPORT:
from app.router import router   # <-- Here

from sqlmodel import Session

# ✅ CREATE THE APP:
app = FastAPI(title="Real Estate AI Assistant")

# ✅ REGISTER THE ROUTER IMMEDIATELY AFTER APP CREATION:
app.include_router(router)      # <-- Here

# Static & Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

conversation_engine = ConversationEngine()

# -------------------------------------------------------------
# STARTUP EVENT → INIT DB
# -------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# -------------------------------------------------------------
# HOME PAGE (Modern Chat UI)
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------------------------
# ADMIN UI (optional)
# -------------------------------------------------------------
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


# -------------------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------------------------------------
# WEBSOCKET CHAT
# -------------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    session_id = str(uuid.uuid4())

    try:
        while True:
            raw = await ws.receive_text()
            try:
                data = json.loads(raw)
                msg = ChatClientMessage(**data)
            except:
                msg = ChatClientMessage(text=raw)

            # Use thread-safe DB session
            with next(get_session()) as db:
                bot_response = conversation_engine.handle(
                    session_id=session_id,
                    message=msg,
                    db=db
                )

            await ws.send_text(bot_response.model_dump_json())

    except WebSocketDisconnect:
        print(f"Client disconnected → session {session_id} closed.")
