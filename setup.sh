#!/bin/bash

# Crop Yield Bot - Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "   Crop Yield Bot - Quick Start"
echo "========================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"
echo "✓ Python found: $(python3 --version)"
echo ""

echo "Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install backend dependencies"
    exit 1
fi
cd ..

echo ""
echo "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install frontend dependencies"
    exit 1
fi
cd ..

echo ""
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 - Backend (Flask):"
echo "  cd backend"
echo "  python app.py"
echo ""
echo "Terminal 2 - Frontend (React):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:5173"
echo ""
echo "For more information, see SETUP_GUIDE.md"
echo ""
