from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "BharatVox AI running"}

@app.post("/api")
def post_api(payload: dict):
    return {
        "message": "POST working",
        "data": payload
    }
@app.get("/api")
def get_api():
    return {
        "message": "GET working"
    }

@app.put("/api")
def put_api():
    return {
        "message": "PUT working"
    }

@app.delete("/api")
def delete_api():
    return {
        "message": "DELETE working"
    }

@app.patch("/api")
def patch_api():
    return {
        "message": "PATCH working"
    }

@app.options("/api")
def options_api():
    return {
        "message": "OPTIONS working"
    }

@app.head("/api")
def head_api():
    return {
        "message": "HEAD working"
    }

@app.trace("/api")
def trace_api():
    return {
        "message": "TRACE working"
    }

@app.connect("/api")
def connect_api():
    return {
        "message": "CONNECT working"
    }

@app.websocket("/api")
def websocket_api():
    return {
        "message": "WEBSOCKET working"
    }

@app.middleware("/api")
def middleware_api():
    return {
        "message": "MIDDLEWARE working"
    }