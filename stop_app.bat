@echo off
echo Stopping Social Listening Platform...
echo.
echo Killing Node.js (Frontend)...
taskkill /f /im node.exe
echo.
echo Killing Python (Backend)...
taskkill /f /im python.exe
echo.
echo Done! All servers stopped.
pause
