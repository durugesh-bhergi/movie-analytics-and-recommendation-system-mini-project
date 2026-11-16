@echo off
TITLE CinePulse - Movie Analytics & Recommendation System
echo ====================================================================
echo   CinePulse: Movie Analytics & Recommendation System (PES University)
echo ====================================================================
echo.
echo [1/3] Verifying and seeding SQLite / Relational Database...
python build_database_and_test.py
if %ERRORLEVEL% NEQ 0 (
    echo Database initialization failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Starting Python REST API & Vector Engine (Port 5000)...
start "CinePulse Backend API" cmd /k "python backend/server.py"

echo.
echo [3/3] Starting Next.js Production Web Server (Port 3000)...
cd frontend
start "CinePulse Next.js Frontend" cmd /k "npm run start"

timeout /t 3 >nul
echo.
echo ====================================================================
echo   All systems live! Opening http://localhost:3000 in your browser...
echo ====================================================================
start http://localhost:3000
pause
