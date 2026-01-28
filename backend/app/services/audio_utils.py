import base64
from typing import Tuple
from fastapi import HTTPException, status


def decode_base64_audio(audio_base64: str) -> bytes:
    """
    Decode base64 audio string to bytes
    
    Args:
        audio_base64: Base64 encoded audio string
        
    Returns:
        Decoded audio bytes
        
    Raises:
        HTTPException: If base64 decoding fails
    """
    try:
        # Remove data URL prefix if present
        if ',' in audio_base64:
            audio_base64 = audio_base64.split(',')[1]
        
        audio_bytes = base64.b64decode(audio_base64)
        
        # Validate minimum size (should be at least a few KB for valid audio)
        if len(audio_bytes) < 1000:
            raise ValueError("Audio data too small to be valid")
        
        return audio_bytes
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid base64 audio data: {str(e)}"
        )


def validate_audio_format(audio_bytes: bytes, expected_format: str = "mp3") -> bool:
    """
    Validate audio format by checking file signature
    
    Args:
        audio_bytes: Audio file bytes
        expected_format: Expected audio format (currently only mp3)
        
    Returns:
        True if format is valid
        
    Raises:
        HTTPException: If format is invalid
    """
    # MP3 file signatures
    mp3_signatures = [
        b'\xff\xfb',  # MPEG-1 Layer 3
        b'\xff\xf3',  # MPEG-2 Layer 3
        b'\xff\xf2',  # MPEG-2.5 Layer 3
        b'ID3',       # ID3v2 tag
    ]
    
    if expected_format.lower() == "mp3":
        is_valid = any(audio_bytes.startswith(sig) for sig in mp3_signatures)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid MP3 format. Please provide a valid MP3 audio file."
            )
        
        return True
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported audio format: {expected_format}. Only MP3 is supported."
    )
