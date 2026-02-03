"""
BharatVox AI - Vercel-native FastAPI entry point
Minimal, production-safe endpoint for voice detection
"""
import sys
import os
from pathlib import Path
import time
import base64

# Add backend to path so we can import app modules
backend_path = str(Path(__file__).parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="BharatVox AI",
    description="AI-powered voice detection system for Indian languages",
    version="1.0.0",
)

# CORS middleware - required for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BharatVox AI",
        "version": "1.0.0",
        "status": "ok"
    }

@app.get("/api")
async def api_health():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "service": "BharatVox AI",
        "version": "1.0.0"
    }

@app.post("/api")
async def api_detect_voice(request: dict):
    """
    Direct voice detection endpoint.
    Accepts JSON body with: language, audio_format, audio_base64
    
    Returns JSON with classification result or error.
    """
    try:
        # Step 1: Validate required fields
        required_fields = {"language", "audio_format", "audio_base64"}
        missing = required_fields - set(request.keys())
        if missing:
            return {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing)}",
                "code": 400
            }
        
        start_time = time.time()
        language = request.get("language", "").strip()
        audio_format = request.get("audio_format", "mp3").strip().lower()
        audio_b64 = request.get("audio_base64", "").strip()
        
        # Step 2: Validate language
        valid_languages = {"tamil", "english", "hindi", "malayalam", "telugu"}
        if language.lower() not in valid_languages:
            return {
                "status": "error",
                "message": f"Invalid language '{language}'. Must be one of: {', '.join(valid_languages)}",
                "code": 400
            }
        
        # Step 3: Validate audio format
        if audio_format not in {"mp3", "wav"}:
            return {
                "status": "error",
                "message": f"Invalid audio format '{audio_format}'. Must be 'mp3' or 'wav'",
                "code": 400
            }
        
        # Step 4: Decode base64
        try:
            audio_bytes = base64.b64decode(audio_b64)
            if len(audio_bytes) < 100:
                return {
                    "status": "error",
                    "message": "Audio data too small (likely invalid base64)",
                    "code": 400
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Invalid base64 encoding: {str(e)}",
                "code": 400
            }
        
        # Step 5: Try to load the classifier and run inference
        try:
            from ml_engine import get_classifier
            
            classifier = get_classifier()
            classification, confidence_score, explanation = classifier.predict(audio_bytes)
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                "status": "success",
                "language": language,
                "classification": classification,
                "confidenceScore": float(confidence_score),
                "explanation": explanation,
                "responseTimeMs": response_time_ms
            }
        except Exception as ml_error:
            # If ML model fails, still return valid JSON with error
            return {
                "status": "error",
                "message": f"Model inference failed: {str(ml_error)}",
                "code": 500,
                "hint": "Check that ml_engine is properly trained"
            }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Internal server error: {str(e)}",
            "code": 500
        }
