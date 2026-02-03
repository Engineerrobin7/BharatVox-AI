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
        # Accept both snake_case and camelCase keys from testers
        language = (
            request.get("language")
            or request.get("Language")
            or request.get("lang")
            or request.get("Lang")
            or ""
        )
        audio_format = (
            request.get("audio_format")
            or request.get("audioFormat")
            or request.get("audio-format")
            or "mp3"
        )
        audio_b64 = (
            request.get("audio_base64")
            or request.get("audioBase64")
            or request.get("audio")
            or ""
        )

        # Required field validation (use normalized names)
        missing = []
        if not language:
            missing.append("language")
        if not audio_format:
            missing.append("audio_format")
        if not audio_b64:
            missing.append("audio_base64")
        if missing:
            return {"status": "error", "message": f"Missing: {', '.join(missing)}", "code": 400}

        language_norm = language.strip().lower()
        valid_langs = {"tamil", "english", "hindi", "malayalam", "telugu"}
        if language_norm not in valid_langs:
            return {
                "status": "error",
                "message": f"Invalid language. Use: {', '.join(valid_langs)}",
                "code": 400,
            }

        audio_format = audio_format.strip().lower()
        if audio_format not in {"mp3", "wav"}:
            return {"status": "error", "message": "Invalid audio format (mp3|wav expected)", "code": 400}

        # MOCK RESPONSE
        return {
            "status": "success",
            "language": language_norm,
            "classification": "HUMAN",
            "confidenceScore": 0.92,
            "explanation": "Mock response (ML model pending)",
            "responseTimeMs": 100,
            "testMode": True,
        }
    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"Internal error: {str(e)}",
            "error": str(type(e).__name__),
            "trace": str(traceback.format_exc())[:200]
            }


@app.get("/api/debug")
def api_debug():
    """Return minimal runtime info for debugging deployments on Vercel.
    WARNING: This exposes limited environment info — use only temporarily.
    """
    import platform, sys, os

    keys = ["VERCEL", "VERCEL_GIT_COMMIT_SHA", "PATH", "HOME"]
    env = {k: os.environ.get(k) for k in keys if os.environ.get(k) is not None}

    return {
        "status": "ok",
        "python_version": sys.version.splitlines()[0],
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "env_sample": env,
    }
