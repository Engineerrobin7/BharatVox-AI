@echo off
REM BharatVox AI - Quick Setup Script for Windows

echo ========================================
echo BharatVox AI - Quick Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - Please edit it to set your API key
) else (
    echo .env file already exists
)

echo [5/5] Creating demo model for testing...
cd ml_engine
python create_demo_model.py
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and set your API_KEY
echo 2. (Optional) Add training data and run: python ml_engine\train_model.py
echo 3. Start the backend: cd backend ^&^& python main.py
echo 4. Open frontend\index.html in your browser
echo.
echo For detailed instructions, see README.md
echo ========================================
pause
