from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
import asyncio
import json
import os
import subprocess
from main import Jarvis
from config import settings
import system_stats
from notifier import NotificationBridge

HISTORY_FILE = "conversation_history.json"
notif_bridge = NotificationBridge()

app = FastAPI(title="Jarvis Web API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Initialize Jarvis in a way that doesn't block the event loop
# Note: Since the original Jarvis is CLI-oriented, we'll wrap the logic
class JarvisWrapper:
    def __init__(self):
        self.jarvis = Jarvis(voice_mode=False)  # We'll handle voice in the browser or via backend triggers
        
    def get_response(self, text: str) -> str:
        low_text = text.lower()
        if "open" in low_text:
            if "chrome" in low_text:
                subprocess.Popen(["start", "chrome"], shell=True)
                return "Opening Chrome for you, Sir."
            elif "notepad" in low_text:
                subprocess.Popen(["notepad.exe"])
                return "Notepad is ready, Sir."
        
        return self.jarvis.brain.think(text, skills=self.jarvis.skills)

jarvis_ai = JarvisWrapper()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    action: Optional[str] = None
    status: str = "success"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_history(sender: str, text: str):
    history = load_history()
    history.append({"sender": sender, "text": text})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@app.on_event("startup")
async def startup_event():
    if await notif_bridge.initialize():
        # Start background polling
        async def poll_task():
            while True:
                await notif_bridge.poll_notifications()
                await asyncio.sleep(2)
        asyncio.create_task(poll_task())

@app.get("/api/notifications")
async def get_notifications():
    return notif_bridge.get_latest()

@app.get("/api/history")
async def get_history():
    return load_history()

@app.get("/api/system")
async def get_system_stats():
    return system_stats.get_system_stats()

@app.post("/api/tools/open")
async def open_app(request: dict):
    app_name = request.get("app")
    try:
        if app_name == "chrome":
            subprocess.Popen(["start", "chrome"], shell=True)
        elif app_name == "notepad":
            subprocess.Popen(["notepad.exe"])
        return {"status": "success", "message": f"Opening {app_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Log user message
        save_to_history("User", request.message)
        
        # Run the synchronous thinking process in a thread to avoid blocking FastAPI
        response = await asyncio.to_thread(jarvis_ai.get_response, request.message)
        
        # Log Jarvis response
        save_to_history("Jarvis", response)
        
        # Check for sensor trigger keywords
        action = None
        low_res = response.lower()
        if "visual scan" in low_res or "activating camera" in low_res:
            action = "open_camera"
        elif "coordinates" in low_res or "gps" in low_res or "location" in low_res:
            if "request" in low_res or "secure" in low_res:
                action = "request_location"
        
        return {"response": response, "status": "success", "action": action}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Mount static files (must be after API routes)
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
