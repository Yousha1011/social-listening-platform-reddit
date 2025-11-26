@echo off
setlocal EnableDelayedExpansion
echo ===================================================
echo   Social Listening Platform - One-Time Setup
echo ===================================================

echo.
echo 1. Installing Backend (Python) libraries...
cd backend
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python libraries. Is Python installed?
    pause
    exit /b
)

echo.
echo 2. Installing Frontend (Node.js) libraries...
cd ../frontend
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js libraries. Is Node.js installed?
    pause
    exit /b
)

echo.
echo 3. Setting up API Keys...
cd ../backend

if exist .env (
    echo [.env] file already exists. Skipping key setup.
) else (
    echo.
    echo We need to create your configuration file.
    echo Please enter your API Keys when prompted.
    echo.
    
    set /p REDDIT_ID="Enter Reddit Client ID: "
    set /p REDDIT_SECRET="Enter Reddit Client Secret: "
    set /p GEMINI_KEY="Enter Gemini API Key: "
    
    echo REDDIT_CLIENT_ID=!REDDIT_ID!> .env
    echo REDDIT_CLIENT_SECRET=!REDDIT_SECRET!>> .env
    echo REDDIT_USER_AGENT=SocialListeningApp/1.0>> .env
    echo GEMINI_API_KEY=!GEMINI_KEY!>> .env
    
    echo.
    echo [.env] file created successfully!
)

echo.
echo ===================================================
echo   Setup Complete!
echo ===================================================
echo.
echo You can now run "start_hidden.vbs" to launch the app.
echo.
pause
