@echo off
echo ===================================================
echo   Starting Social Listening Platform...
echo ===================================================

:: 1. Start Backend in a new window
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && py -m uvicorn main:app --reload"

:: 2. Start Frontend in a new window
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

:: 3. Wait for servers to spin up (5 seconds)
echo Waiting for servers to initialize...
timeout /t 5 /nobreak >nul

:: 4. Open Browser
echo Opening Application in Browser...
start http://localhost:5173

echo ===================================================
echo   App is running! 
echo   Close the popup windows to stop the servers.
echo ===================================================
pause
