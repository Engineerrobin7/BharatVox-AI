from fastapi import Header, HTTPException, status
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "your_secret_api_key_here")


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from request headers
    
    Args:
        x_api_key: API key from x-api-key header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide x-api-key header."
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return x_api_key
