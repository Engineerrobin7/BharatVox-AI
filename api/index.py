"""
BharatVox AI - Vercel FastAPI (DEBUG - No ML imports)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import traceback

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
def api_detect_voice(request: dict):
    try:
        required_fields = {"language", "audio_format", "audio_base64"}
        missing = required_fields - set(request.keys())
        if missing:
            return {
                "status": "error",
                "message": f"Missing: {', '.join(missing)}",
                "code": 400
            }
        
        language = request.get("language", "").lower()
        valid_langs = {"tamil", "english", "hindi", "malayalam", "telugu"}
        if language not in valid_langs:
            return {
                "status": "error",
                "message": f"Invalid language. Use: {', '.join(valid_langs)}",
                "code": 400
            }
        
        # MOCK RESPONSE
        return {
            "status": "success",
            "language": language,
            "classification": "HUMAN",
            "confidenceScore": 0.92,
            "explanation": "Mock response (ML model pending)",
            "responseTimeMs": 100,
            "testMode": True
        }
    except Exception as e:
        return {
            "status": "error",
            "code": 500,
                "message": f"Model inference failed: {str(ml_error)}",
            "error": str(type(e).__name__),
            "trace": str(traceback.format_exc())[:200]
            }
