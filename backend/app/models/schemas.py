from pydantic import BaseModel, Field, validator
from typing import Literal
from enum import Enum


class Language(str, Enum):
    """Supported languages for voice detection"""
    TAMIL = "Tamil"
    ENGLISH = "English"
    HINDI = "Hindi"
    MALAYALAM = "Malayalam"
    TELUGU = "Telugu"


class AudioFormat(str, Enum):
    """Supported audio formats"""
    MP3 = "mp3"


class Classification(str, Enum):
    """Voice classification types"""
    AI_GENERATED = "AI_GENERATED"
    HUMAN = "HUMAN"


class VoiceDetectionRequest(BaseModel):
    """Request model for voice detection API"""
    language: Language = Field(..., description="Language of the audio")
    audioFormat: AudioFormat = Field(..., description="Format of the audio file")
    audioBase64: str = Field(..., description="Base64 encoded audio data")

    @validator('audioBase64')
    def validate_base64(cls, v):
        if not v or len(v) < 100:
            raise ValueError("Invalid or too short base64 audio data")
        return v


class VoiceDetectionResponse(BaseModel):
    """Success response model for voice detection"""
    status: Literal["success"] = "success"
    language: str
    classification: Classification
    confidenceScore: float = Field(..., ge=0.0, le=1.0)
    explanation: str


class ErrorResponse(BaseModel):
    """Error response model"""
    status: Literal["error"] = "error"
    message: str
