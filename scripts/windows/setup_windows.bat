@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0..\.."

echo [SeedScope] Windows setup started.

where node >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Node.js is not installed or not in PATH.
  echo Download LTS from https://nodejs.org/ and run this script again.
  pause
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo [ERROR] npm is not available. Please reinstall Node.js LTS.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python is not installed or not in PATH.
  echo Download Python 3.11+ from https://www.python.org/downloads/ and enable "Add python.exe to PATH".
  pause
  exit /b 1
)

python -m pip --version >nul 2>nul
if errorlevel 1 (
  echo [ERROR] pip is not available for the current Python installation.
  pause
  exit /b 1
)

if not exist ".env" (
  if exist ".env.example" (
    copy ".env.example" ".env" >nul
    echo [SeedScope] Created .env from .env.example.
  ) else (
    echo [WARN] .env.example not found. Please create .env manually.
  )
) else (
  echo [SeedScope] .env already exists. Skipping copy.
)

if not exist ".venv\Scripts\python.exe" (
  echo [SeedScope] Creating Python virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create Python virtual environment.
    pause
    exit /b 1
  )
)

echo [SeedScope] Installing backend dependencies...
call ".venv\Scripts\python.exe" -m pip install -r apps/api/requirements.txt
if errorlevel 1 (
  echo [ERROR] Backend dependency installation failed.
  pause
  exit /b 1
)

echo [SeedScope] Installing frontend dependencies...
call npm --prefix apps/web install
if errorlevel 1 (
  echo [ERROR] Frontend dependency installation failed.
  pause
  exit /b 1
)

if not exist "logs" mkdir logs

echo.
echo [SeedScope] Setup completed.
echo Next steps:
echo   1. Optional: edit .env to configure LLM_PROVIDER and API Key.
echo   2. Run scripts\windows\check_env.bat to verify model settings.
echo   3. Run scripts\windows\start_windows.bat to start SeedScope.
echo   4. Open http://127.0.0.1:3000 if the browser does not open automatically.
echo.
pause
