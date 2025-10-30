@echo off
echo ----------------------------
echo NGROK HELPER - Start tunnel to local server port 5000
echo ----------------------------

:: Check for ngrok in PATH
where ngrok >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: ngrok not found in PATH.
    echo Download and install ngrok from: https://ngrok.com/download
    echo After installing, either put ngrok.exe in your PATH or place it in this folder.
    echo
    pause
    exit /b 1
)

necho Starting ngrok tunnel on port 5000...
echo (Press Ctrl+C in this window to stop ngrok)

ngrok http 5000

nexit /b 0
