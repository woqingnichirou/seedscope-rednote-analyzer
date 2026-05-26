@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0..\.."

set NO_PAUSE=0
if "%~1"=="--no-pause" set NO_PAUSE=1

if not exist ".env" (
  echo [ERROR] .env not found. Run scripts\windows\setup_windows.bat first.
  if "%NO_PAUSE%"=="0" pause
  exit /b 1
)

set LLM_PROVIDER=
set OPENAI_API_KEY=
set DEEPSEEK_API_KEY=
set QWEN_API_KEY=
set KIMI_API_KEY=
set ZHIPU_API_KEY=

for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
  set KEY=%%A
  set VALUE=%%B
  if /i "!KEY!"=="LLM_PROVIDER" set LLM_PROVIDER=!VALUE!
  if /i "!KEY!"=="OPENAI_API_KEY" set OPENAI_API_KEY=!VALUE!
  if /i "!KEY!"=="DEEPSEEK_API_KEY" set DEEPSEEK_API_KEY=!VALUE!
  if /i "!KEY!"=="QWEN_API_KEY" set QWEN_API_KEY=!VALUE!
  if /i "!KEY!"=="KIMI_API_KEY" set KIMI_API_KEY=!VALUE!
  if /i "!KEY!"=="ZHIPU_API_KEY" set ZHIPU_API_KEY=!VALUE!
)

if "%LLM_PROVIDER%"=="" (
  echo [WARN] LLM_PROVIDER is not configured. Recommended: LLM_PROVIDER=mock for first run.
  if "%NO_PAUSE%"=="0" pause
  exit /b 0
)

echo [SeedScope] LLM_PROVIDER=%LLM_PROVIDER%

if /i "%LLM_PROVIDER%"=="mock" (
  echo [OK] Mock provider selected. No API Key is required.
  if "%NO_PAUSE%"=="0" pause
  exit /b 0
)

if /i "%LLM_PROVIDER%"=="openai" set REQUIRED_KEY=%OPENAI_API_KEY%
if /i "%LLM_PROVIDER%"=="deepseek" set REQUIRED_KEY=%DEEPSEEK_API_KEY%
if /i "%LLM_PROVIDER%"=="qwen" set REQUIRED_KEY=%QWEN_API_KEY%
if /i "%LLM_PROVIDER%"=="kimi" set REQUIRED_KEY=%KIMI_API_KEY%
if /i "%LLM_PROVIDER%"=="zhipu" set REQUIRED_KEY=%ZHIPU_API_KEY%

if "%REQUIRED_KEY%"=="" (
  echo [WARN] API Key for provider "%LLM_PROVIDER%" is not configured.
  echo SeedScope can still start, and backend will fall back to rule/mock behavior when model calls fail.
  if "%NO_PAUSE%"=="0" pause
  exit /b 0
)

echo [OK] API Key appears to be configured for %LLM_PROVIDER%.
if "%NO_PAUSE%"=="0" pause
