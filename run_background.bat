@echo off
:: 1. Start Backend (Hidden)
cd backend
start /b py -m uvicorn main:app --reload > nul 2>&1

:: 2. Start Frontend (Hidden)
cd ../frontend
start /b npm run dev > nul 2>&1

:: 3. Wait and Open Browser
timeout /t 5 /nobreak >nul
start http://localhost:5173
