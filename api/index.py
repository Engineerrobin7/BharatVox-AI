from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
import platform
import os

# Vercel requires the app to be named "app"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "BharatVox AI root"}

@app.get("/api")
def api_health():
    return {"status": "healthy", "service": "BharatVox AI"}

@app.post("/api")
async def api_post(request: Request):
    payload = await request.json()
    return {
        "status": "success",
        "received_keys": list(payload.keys())
    }

@app.get("/api/debug")
def api_debug():
    return {
        "status": "ok",
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": os.getcwd()
    }
