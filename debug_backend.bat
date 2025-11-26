@echo off
echo ===================================================
echo   DEBUG MODE: Starting Backend Server
echo ===================================================
cd backend
echo Current Directory: %CD%
echo Running command: py -m uvicorn main:app --reload
py -m uvicorn main:app --reload
echo.
echo ===================================================
echo   SERVER CRASHED OR STOPPED
echo   Please take a screenshot of any errors above.
echo ===================================================
pause
