from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.api import router
from .app.models import init_db
import sys
from pathlib import Path

from contextlib import asynccontextmanager
import sys
from pathlib import Path
import os # Import the os module

# Determine the project root and change the working directory
# This script is in 'backend/main.py', so parent.parent is the project root
project_root = Path(__file__).parent.parent.resolve()
os.chdir(project_root)
# print(f"INFO: Changed working directory to: {os.getcwd()}") # Removed after confirmation

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Initializes database on startup.
    """
    init_db()
    print("Database initialized successfully")
    print("BharatVox AI is ready to serve requests!")
    yield
    # Can add shutdown logic here if needed

# Initialize FastAPI app
app = FastAPI(
    title="BharatVox AI",
    description="AI-powered voice detection system for Indian languages",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins like "https://your-frontend-domain.vercel.app"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api", tags=["Voice Detection"])

@app.get("/api", tags=["Root"])
async def api_root_get():
    """API root endpoint - GET"""
    return {
        "message": "Welcome to BharatVox AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "voiceDetection": "/api/voice-detection"
    }


@app.post("/api", tags=["Root"])
async def api_root_post(request: dict):
    """
    API POST endpoint for direct voice detection.
    Accepts JSON body with: language, audio_format, audio_base64
    """
    from .app.models import VoiceDetectionRequest
    from .app.core import verify_api_key
    from .app.services import decode_base64_audio, validate_audio_format
    from ml_engine import get_classifier
    from sqlalchemy.orm import Session
    from .app.models import get_db, InferenceLog
    import time
    
    try:
        # Validate required fields
        required_fields = {"language", "audio_format", "audio_base64"}
        missing = required_fields - set(request.keys())
        if missing:
            return {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing)}",
                "code": 400
            }
        
        # Create structured request
        req_data = {
            "language": request["language"],
            "audioFormat": request.get("audio_format", "mp3"),
            "audioBase64": request["audio_base64"]
        }
        
        start_time = time.time()
        
        # Decode and validate audio
        audio_bytes = decode_base64_audio(req_data["audioBase64"])
        validate_audio_format(audio_bytes, req_data["audioFormat"])
        
        # Get classifier and predict
        classifier = get_classifier()
        classification, confidence_score, explanation = classifier.predict(audio_bytes)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "status": "success",
            "language": req_data["language"],
            "classification": classification,
            "confidenceScore": confidence_score,
            "explanation": explanation,
            "responseTimeMs": response_time_ms
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "code": 500
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
