@echo off
setlocal

cd /d "%~dp0..\.."

if not exist "logs" mkdir logs

if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] Python virtual environment not found.
  echo Please run scripts\windows\setup_windows.bat first.
  pause
  exit /b 1
)

if not exist "apps\web\node_modules" (
  echo [ERROR] Frontend dependencies not found.
  echo Please run scripts\windows\setup_windows.bat first.
  pause
  exit /b 1
)

if not exist ".env" (
  if exist ".env.example" (
    copy ".env.example" ".env" >nul
    echo [SeedScope] Created .env from .env.example.
  )
)

echo [SeedScope] Checking model environment...
call "scripts\windows\check_env.bat" --no-pause

echo [SeedScope] Starting FastAPI backend at http://127.0.0.1:8000
start "SeedScope API" cmd /c ".venv\Scripts\activate && python -m uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000 > logs\api.log 2>&1"

echo [SeedScope] Starting Next.js frontend at http://127.0.0.1:3000
start "SeedScope Web" cmd /c "npm --prefix apps/web run dev -- --hostname 127.0.0.1 --port 3000 > logs\web.log 2>&1"

echo [SeedScope] Waiting for services...
timeout /t 5 /nobreak >nul

start "" "http://127.0.0.1:3000"

echo.
echo [SeedScope] Started.
echo   Web:  http://127.0.0.1:3000
echo   API:  http://127.0.0.1:8000
echo   Logs: logs\api.log and logs\web.log
echo.
echo To stop services, run scripts\windows\stop_windows.bat
pause
