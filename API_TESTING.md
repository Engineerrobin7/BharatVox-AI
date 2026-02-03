# API Testing Guide

## Quick Test Examples

### 1. Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "BharatVox AI",
  "version": "1.0.0"
}
```

---

### 2. API POST Endpoint (Direct Voice Detection)

```bash
curl -X POST "http://localhost:8000/api" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audio_format": "mp3",
    "audio_base64": "YOUR_BASE64_ENCODED_MP3_HERE"
  }'
```

Expected success response:
```json
{
  "status": "success",
  "language": "English",
  "classification": "HUMAN",
  "confidenceScore": 0.92,
  "explanation": "Detected human voice with natural spectral variation...",
  "responseTimeMs": 245
}
```

Expected error response (missing fields):
```json
{
  "status": "error",
  "message": "Missing required fields: audio_base64",
  "code": 400
}
```

---

### 3. Voice Detection Request

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_secret_api_key_here" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "YOUR_BASE64_ENCODED_MP3_HERE"
  }'
```

### Using Python

```python
import requests
import base64

# Read and encode MP3 file
with open("test_audio.mp3", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Make request
url = "http://localhost:8000/api/voice-detection"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "your_secret_api_key_here"
}
payload = {
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": audio_base64
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Using JavaScript (Node.js)

```javascript
const fs = require('fs');
const axios = require('axios');

// Read and encode MP3 file
const audioBuffer = fs.readFileSync('test_audio.mp3');
const audioBase64 = audioBuffer.toString('base64');

// Make request
axios.post('http://localhost:8000/api/voice-detection', {
    language: 'Hindi',
    audioFormat: 'mp3',
    audioBase64: audioBase64
}, {
    headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'your_secret_api_key_here'
    }
})
.then(response => {
    console.log(response.data);
})
.catch(error => {
    console.error(error.response.data);
});
```

---

## Expected Responses

### Success Response

```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "HUMAN",
  "confidenceScore": 0.92,
  "explanation": "Detected human voice with natural spectral variation, organic pitch fluctuations, natural voice modulation (confidence: 92%)"
}
```

### Error Responses

#### Missing API Key (401)
```json
{
  "status": "error",
  "message": "Missing API key. Please provide x-api-key header."
}
```

#### Invalid API Key (401)
```json
{
  "status": "error",
  "message": "Invalid API key"
}
```

#### Invalid Language (422)
```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "value is not a valid enumeration member; permitted: 'Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu'",
      "type": "type_error.enum"
    }
  ]
}
```

#### Invalid Base64 (400)
```json
{
  "status": "error",
  "message": "Invalid base64 audio data: ..."
}
```

#### Invalid Audio Format (400)
```json
{
  "status": "error",
  "message": "Invalid MP3 format. Please provide a valid MP3 audio file."
}
```

---

## Testing with Postman

1. **Create New Request**
   - Method: POST
   - URL: `http://localhost:8000/api/voice-detection`

2. **Set Headers**
   - `Content-Type`: `application/json`
   - `x-api-key`: `your_secret_api_key_here`

3. **Set Body** (raw JSON)
   ```json
   {
     "language": "English",
     "audioFormat": "mp3",
     "audioBase64": "YOUR_BASE64_STRING"
   }
   ```

4. **Send Request**

---

## Testing All Languages

```bash
# Tamil
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_key" \
  -d '{"language": "Tamil", "audioFormat": "mp3", "audioBase64": "..."}'

# English
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_key" \
  -d '{"language": "English", "audioFormat": "mp3", "audioBase64": "..."}'

# Hindi
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_key" \
  -d '{"language": "Hindi", "audioFormat": "mp3", "audioBase64": "..."}'

# Malayalam
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_key" \
  -d '{"language": "Malayalam", "audioFormat": "mp3", "audioBase64": "..."}'

# Telugu
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_key" \
  -d '{"language": "Telugu", "audioFormat": "mp3", "audioBase64": "..."}'
```

---

## Performance Testing

### Measure Response Time

```python
import time
import requests
import base64

with open("test_audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

start_time = time.time()

response = requests.post(
    "http://localhost:8000/api/voice-detection",
    json={
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    },
    headers={"x-api-key": "your_key"}
)

end_time = time.time()
response_time_ms = (end_time - start_time) * 1000

print(f"Response time: {response_time_ms:.2f} ms")
print(f"Result: {response.json()}")
```

---

## Automated Testing Script

Save as `test_api.py`:

```python
import requests
import base64
import sys
import os # Import the os module

API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = os.environ.get("API_KEY", "your_secret_api_key_here")

def test_voice_detection(audio_file, language):
    """Test voice detection API"""
    try:
        # Read and encode audio
        with open(audio_file, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Make request
        response = requests.post(
            API_URL,
            json={
                "language": language,
                "audioFormat": "mp3",
                "audioBase64": audio_base64
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            }
        )
        
        # Print results
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS")
            print(f"   Language: {result['language']}")
            print(f"   Classification: {result['classification']}")
            print(f"   Confidence: {result['confidenceScore']:.2%}")
            print(f"   Explanation: {result['explanation']}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"   {response.json()}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_api.py <audio_file.mp3> <language>")
        print("Languages: Tamil, English, Hindi, Malayalam, Telugu")
        sys.exit(1)
    
    test_voice_detection(sys.argv[1], sys.argv[2])
```

Run with:
```bash
python test_api.py test_audio.mp3 English
```

---

## Interactive API Documentation

Visit these URLs when the server is running:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing
  - Try out requests directly in browser
  - See request/response schemas

- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable documentation
  - Detailed schema information

---

## Troubleshooting

### Server Not Running
```bash
# Check if server is running
curl http://localhost:8000/

# Expected: {"message": "Welcome to BharatVox AI", ...}
```

### Model Not Found
```
Error: Model files not found. Please train the model first.
```
**Solution**: Run `python ml_engine/create_demo_model.py` or train with real data

### Invalid API Key
```
Error: Invalid API key
```
**Solution**: Check your `.env` file and ensure API_KEY matches the header value

---

**Happy Testing! 🚀**
