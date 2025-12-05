@echo off
cd /d "%~dp0"

echo Starting DigiLife Backend...
start "DigiLife Backend" cmd /k "cd backend && uvicorn main:app --reload"

echo Waiting for backend to initialize...
timeout /t 3 >nul

echo Starting DigiLife Frontend...
start "DigiLife Frontend" cmd /k "cd frontend && npm run dev"

echo DigiLife started. 
echo Backend running on http://localhost:8000
echo Frontend running on http://localhost:5173
