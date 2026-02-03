from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
import platform
import os

"""
Minimal BharatVox AI FastAPI app for Vercel deployments.
Provides basic /api health and POST endpoints and a debug endpoint.
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to BharatVox AI"}


@app.get("/api")
def api_health():
    return {"status": "healthy", "service": "BharatVox AI"}


@app.post("/api")
async def api_post(request: Request):
    """Accept arbitrary JSON and echo received keys (mock behavior)."""
    try:
        payload = await request.json()
    except Exception:
        return {"status": "error", "message": "Invalid JSON body", "code": 400}

    # Return success and the keys received so tester can confirm payload mapping
    return {"status": "success", "received_keys": list(payload.keys())}


@app.get("/api/debug")
def api_debug():
    """Return minimal runtime info for debugging deployments on Vercel.
    Use temporarily to inspect environment.
    """
    keys = ["VERCEL", "VERCEL_GIT_COMMIT_SHA", "PATH", "HOME"]
    env = {k: os.environ.get(k) for k in keys if os.environ.get(k) is not None}

    return {
        "status": "ok",
        "python_version": sys.version.splitlines()[0],
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "env_sample": env,
    }
