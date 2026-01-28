# 🚀 BharatVox AI - Quick Start Guide

Welcome to **BharatVox AI**! This guide will get you up and running in minutes.

---

## ⚡ 3-Step Quick Start

### Step 1: Install Dependencies ✅

The installation is currently running. Once complete, you'll see:
```
Successfully installed fastapi uvicorn pydantic librosa...
```

### Step 2: Create Demo Model

```bash
# Activate virtual environment (if not already active)
.\venv\Scripts\activate

# Create demo model for testing
cd ml_engine
python create_demo_model.py
cd ..
```

This creates a basic model so you can test the system immediately.

### Step 3: Start the Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Database initialized successfully
BharatVox AI is ready to serve requests!
```

---

## 🎨 Using the Frontend

1. **Open the frontend**
   - Navigate to `frontend` folder
   - Open `index.html` in your web browser
   - Or serve it: `python -m http.server 3000` (from frontend folder)

2. **Test the system**
   - Select a language (e.g., "English")
   - Upload an MP3 file
   - Enter API key (configured in your .env file)
   - Click "Analyze Voice"

3. **View results**
   - Classification: AI_GENERATED or HUMAN
   - Confidence score with visual bar
   - Detailed explanation

---

## 🧪 Quick API Test

### Using cURL

```bash
# First, convert an MP3 to base64
# On Windows PowerShell:
$bytes = [System.IO.File]::ReadAllBytes("path\to\audio.mp3")
$base64 = [Convert]::ToBase64String($bytes)
echo $base64

# Then test the API:
curl -X POST "http://localhost:8000/api/voice-detection" ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: YOUR_API_KEY_FROM_ENV" ^
  -d "{\"language\":\"English\",\"audioFormat\":\"mp3\",\"audioBase64\":\"YOUR_BASE64_HERE\"}"
```

### Using Python

Create `test.py`:
```python
import requests
import base64

# Read MP3 file
with open("test_audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    "http://localhost:8000/api/voice-detection",
    json={
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    },
    headers={"x-api-key": "YOUR_API_KEY_FROM_ENV"}
)

print(response.json())
```

Run: `python test.py`

---

## 📊 What's Next?

### For Testing (Using Demo Model)
✅ You're ready! The demo model works for immediate testing.

### For Production (Train Custom Model)

1. **Collect Training Data**
   ```
   data/training_data/
   ├── human/          # Add 50+ human voice MP3s
   └── ai_generated/   # Add 50+ AI voice MP3s
   ```

2. **Train the Model**
   ```bash
   cd ml_engine
   python train_model.py
   ```

3. **Restart Backend**
   - The new model will be loaded automatically

---

## 🔍 Verify Everything Works

### 1. Check Backend Health
```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "BharatVox AI",
  "version": "1.0.0"
}
```

### 2. Check API Documentation
Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test Voice Detection
Use the frontend or cURL examples above.

---

## 🎯 Current Status

✅ **Project Structure**: Complete  
✅ **Backend Code**: Ready  
✅ **Frontend Code**: Ready  
✅ **ML Engine**: Ready  
✅ **Documentation**: Complete  
⏳ **Dependencies**: Installing...  
⏳ **Demo Model**: Next step  
⏳ **Backend Running**: After model creation  

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.env` | API key configuration |
| `backend/main.py` | FastAPI server |
| `ml_engine/create_demo_model.py` | Demo model generator |
| `ml_engine/train_model.py` | Real model training |
| `frontend/index.html` | Web interface |
| `README.md` | Full documentation |
| `API_TESTING.md` | API testing guide |

---

## 🆘 Troubleshooting

### Installation Issues
```bash
# If pip install fails, try:
pip install --upgrade pip
pip install -r backend/requirements.txt --no-cache-dir
```

### Model Not Found
```bash
# Create demo model:
cd ml_engine
python create_demo_model.py
```

### Port Already in Use
```bash
# Change port in backend/main.py (line 58):
uvicorn.run("main:app", host="0.0.0.0", port=8001)  # Use 8001
```

### API Key Issues
- Check your .env file and ensure API_KEY matches the header value
- Use same key in frontend/API requests

---

## 🎓 Learning Resources

1. **API Documentation**: http://localhost:8000/docs (after starting backend)
2. **README.md**: Comprehensive project documentation
3. **API_TESTING.md**: Testing examples in multiple languages
4. **PROJECT_SUMMARY.md**: Complete project overview

---

## 🏆 Hackathon Features

✅ **5 Languages**: Tamil, English, Hindi, Malayalam, Telugu  
✅ **AI Detection**: Binary classification with confidence  
✅ **REST API**: FastAPI with authentication  
✅ **Modern UI**: Responsive web interface  
✅ **ML Pipeline**: 40 audio features  
✅ **Database**: Inference logging  
✅ **Docker**: Production deployment  
✅ **Documentation**: Complete guides  

---

## 💡 Pro Tips

1. **Demo Model**: Good for testing, but train with real data for accuracy
2. **API Key**: Change the default key in `.env` for security
3. **Training Data**: More diverse samples = better accuracy
4. **File Size**: Keep MP3 files under 10MB for best performance
5. **Languages**: The language field is for validation/logging (model is language-agnostic)

---

## 📞 Next Commands

Once installation completes, run these in order:

```bash
# 1. Create demo model
cd ml_engine
python create_demo_model.py
cd ..

# 2. Start backend
cd backend
python main.py

# 3. In another terminal, test API
curl http://localhost:8000/api/health

# 4. Open frontend
# Open frontend/index.html in browser
```

---

**You're almost ready! Just waiting for dependencies to finish installing...** ⏳

Once you see "Successfully installed...", proceed to create the demo model! 🚀
