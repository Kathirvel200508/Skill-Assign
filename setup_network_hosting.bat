@echo off
echo.
echo ================================================
echo    NETWORK HOSTING SETUP
echo ================================================
echo.
echo Step 1: Finding your IP address...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    set IP=!IP: =!
    goto :found
)

:found
echo Your IP Address: %IP%
echo.
echo ================================================
echo    CONFIGURATION NEEDED
echo ================================================
echo.
echo Please update these files with your IP: %IP%
echo.
echo 1. mobile\config.js
echo    Change: export const API_BASE_URL = 'http://%IP%:8000';
echo.
echo 2. web\src\config.js (if needed)
echo    Change: export const API_BASE_URL = 'http://%IP%:8000';
echo.
echo ================================================
echo    STARTING SERVERS
echo ================================================
echo.
echo Press any key to start backend on network...
pause >nul

cd backend
start cmd /k "echo Backend running on http://%IP%:8000 && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo Backend started!
echo.
echo Press any key to start web app...
pause >nul

cd ..\web
start cmd /k "echo Web app running on http://%IP%:3000 && npm run dev -- --host"

echo.
echo Web app starting...
echo.
echo Press any key to start mobile app...
pause >nul

cd ..\mobile
start cmd /k "echo Mobile app running on http://%IP%:8082 && npm start"

echo.
echo ================================================
echo    ALL SERVERS STARTING!
echo ================================================
echo.
echo Share these URLs with jury:
echo    Web:    http://%IP%:3000
echo    Mobile: http://%IP%:8082
echo    API:    http://%IP%:8000/docs
echo.
echo Make sure all devices are on the SAME WiFi network!
echo.
echo Press any key to exit...
pause >nul
