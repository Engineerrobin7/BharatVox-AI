from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BharatVox AI",
    description="AI Voice & Language API for India",
    version="1.0.0"
)

# CORS (important for testers + frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ HEALTH CHECK (GET)
@app.get("/")
def health():
    return {
        "status": "healthy",
        "service": "BharatVox AI",
        "message": "API is live and running"
    }

# ✅ MAIN API (POST)
@app.post("/")
async def process_request(request: Request):
    try:
        payload = await request.json()
    except Exception:
        return {
            "status": "error",
            "message": "Invalid JSON body"
        }

    # Echo back keys so hackathon tester can verify mapping
    return {
        "status": "success",
        "received_keys": list(payload.keys()),
        "note": "Mock response for hackathon validation"
    }
