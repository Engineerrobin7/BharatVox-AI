"""
BharatVox AI - Vercel-native FastAPI entry point
Routes all requests to the main FastAPI app
"""
import sys
from pathlib import Path

# Add backend to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.models import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    try:
        init_db()
        print("Database initialized successfully")
        print("BharatVox AI is ready to serve requests!")
    except Exception as e:
        print(f"Warning: Could not initialize database on startup: {e}")
    yield

# Initialize FastAPI app
app = FastAPI(
    title="BharatVox AI",
    description="AI-powered voice detection system for Indian languages",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - required for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api/v1", tags=["Voice Detection"])

@app.get("/api")
async def api_health():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "service": "BharatVox AI",
        "version": "1.0.0"
    }

@app.post("/api")
async def api_direct_detect(request: dict):
    """
    Direct voice detection endpoint.
    Accepts JSON body with: language, audio_format, audio_base64
    """
    import time
    from app.services import decode_base64_audio, validate_audio_format
    from ml_engine import get_classifier
    
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
        
        start_time = time.time()
        
        # Decode and validate audio
        audio_bytes = decode_base64_audio(request["audio_base64"])
        validate_audio_format(audio_bytes, request.get("audio_format", "mp3"))
        
        # Get classifier and predict
        classifier = get_classifier()
        classification, confidence_score, explanation = classifier.predict(audio_bytes)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "status": "success",
            "language": request["language"],
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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BharatVox AI",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api"
    }
