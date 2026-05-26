@echo off
setlocal

echo [SeedScope] Stopping local services on ports 8000 and 3000...

for %%P in (8000 3000) do (
  for /f "tokens=5" %%A in ('netstat -ano ^| findstr ":%%P" ^| findstr "LISTENING"') do (
    echo [SeedScope] Killing PID %%A on port %%P
    taskkill /PID %%A /F >nul 2>nul
  )
)

echo [SeedScope] Stop command completed.
pause
