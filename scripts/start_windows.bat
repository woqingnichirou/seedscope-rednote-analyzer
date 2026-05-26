@echo off
setlocal

cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
  echo [SeedScope] Python virtual environment not found.
  echo Please run the setup commands in docs\china_user_quickstart.md first.
  pause
  exit /b 1
)

if not exist "apps\web\node_modules" (
  echo [SeedScope] Frontend dependencies not found.
  echo Please run: npm --prefix apps/web install
  pause
  exit /b 1
)

echo [SeedScope] Starting API at http://127.0.0.1:8000
start "SeedScope API" cmd /k ".venv\Scripts\activate && python -m uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000"

echo [SeedScope] Starting Web at http://127.0.0.1:3000
start "SeedScope Web" cmd /k "npm --prefix apps/web run dev -- --hostname 127.0.0.1 --port 3000"

echo [SeedScope] Open http://127.0.0.1:3000 in your browser.
pause
