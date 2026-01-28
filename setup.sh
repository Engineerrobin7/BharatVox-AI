#!/bin/bash
# BharatVox AI - Quick Setup Script for Linux/Mac

echo "========================================"
echo "BharatVox AI - Quick Setup"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - Please edit it to set your API key"
else
    echo ".env file already exists"
fi

echo "[5/5] Creating demo model for testing..."
cd ml_engine
python create_demo_model.py
cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and set your API_KEY"
echo "2. (Optional) Add training data and run: python ml_engine/train_model.py"
echo "3. Start the backend: cd backend && python main.py"
echo "4. Open frontend/index.html in your browser"
echo ""
echo "For detailed instructions, see README.md"
echo "========================================"
