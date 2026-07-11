@echo off
REM Crop Yield Bot - Quick Start Script for Windows

echo.
echo ========================================
echo   Crop Yield Bot - Quick Start
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Node.js found: 
node --version

echo ✓ Python found: 
python --version

echo.
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo Terminal 1 - Backend (Flask):
echo   cd backend
echo   python app.py
echo.
echo Terminal 2 - Frontend (React):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5000
echo.
echo For more information, see SETUP_GUIDE.md
echo.
pause
