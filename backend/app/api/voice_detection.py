from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from datetime import datetime
import time
from pathlib import Path

from app.models import (
    VoiceDetectionRequest,
    VoiceDetectionResponse,
    ErrorResponse,
    InferenceLog,
    get_db
)
from app.core import verify_api_key
from app.services import decode_base64_audio, validate_audio_format
from ml_engine import get_classifier

router = APIRouter()


@router.post(
    "/voice-detection",
    response_model=VoiceDetectionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Detect AI-generated or human voice",
    description="Analyzes an MP3 audio file to determine if it's AI-generated or human voice"
)
async def detect_voice(
    request: VoiceDetectionRequest,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Voice Detection Endpoint
    
    Accepts a base64-encoded MP3 audio file and returns classification results.
    
    - **language**: One of Tamil, English, Hindi, Malayalam, Telugu
    - **audioFormat**: Must be "mp3"
    - **audioBase64**: Base64 encoded MP3 audio data
    
    Returns classification, confidence score, and explanation.
    """
    start_time = time.time()
    
    try:
        # Decode base64 audio
        audio_bytes = await run_in_threadpool(decode_base64_audio, request.audioBase64)
        
        # Validate audio format
        await run_in_threadpool(validate_audio_format, audio_bytes, request.audioFormat.value)
        
        # Get classifier and perform inference
        classifier = get_classifier()
        classification, confidence_score, explanation = await run_in_threadpool(classifier.predict, audio_bytes)
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Log inference to database
        try:
            log_entry = InferenceLog(
                language=request.language.value,
                classification=classification,
                confidence_score=confidence_score,
                response_time_ms=response_time_ms
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_error:
            # Don't fail the request if logging fails
            print(f"Database logging error: {str(db_error)}")
        
        # Return response
        return VoiceDetectionResponse(
            language=request.language.value,
            classification=classification,
            confidenceScore=confidence_score,
            explanation=explanation
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health", summary="Health check endpoint")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "service": "BharatVox AI",
        "version": "1.0.0"
    }
