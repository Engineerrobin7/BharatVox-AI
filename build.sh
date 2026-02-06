#!/bin/bash
# Build script for Render deployment
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Generating ML model if not present..."
python ml_engine/create_demo_model.py

echo "Build complete!"
