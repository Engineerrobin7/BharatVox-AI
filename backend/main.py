from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.models import init_db
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

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BharatVox AI",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/voice-detection"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
