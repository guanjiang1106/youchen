@echo off
title RuoYi-FastAPI Project
color 0A

echo.
echo ========================================
echo    RuoYi-FastAPI Startup
echo ========================================
echo.

REM Check Redis
echo [1/3] Checking Redis...
echo.

tasklist | find /i "redis-server.exe" >nul
if %errorlevel% equ 0 (
    echo [OK] Redis is running
    goto :start_backend
)

echo [!] Redis not running, starting...
echo.

REM Try common Redis paths
set "REDIS_PATH="
if exist "D:\Program Files\Redis-x64-5.0.14.1\redis-server.exe" set "REDIS_PATH=D:\Program Files\Redis-x64-5.0.14.1"
if exist "C:\Program Files\Redis\redis-server.exe" set "REDIS_PATH=C:\Program Files\Redis"
if exist "C:\Redis\redis-server.exe" set "REDIS_PATH=C:\Redis"

if "%REDIS_PATH%"=="" (
    echo [ERROR] Redis not found. Please install Redis or start it manually.
    echo.
    echo Continue without Redis? Backend will fail if Redis is required.
    pause
    goto :start_backend
)

pushd "%REDIS_PATH%"
echo [OK] Starting Redis from: %REDIS_PATH%
start "Redis Service" redis-server.exe
popd
timeout /t 3 /nobreak >nul

tasklist | find /i "redis-server.exe" >nul
if %errorlevel% equ 0 (
    echo [OK] Redis started successfully
) else (
    echo [ERROR] Redis failed to start
    pause
    exit /b 1
)

:start_backend
echo.
echo ========================================
echo.

REM Start Backend
echo [2/3] Starting Backend...
echo.

start "Backend Service" cmd /k "cd /d %~dp0ruoyi-fastapi-backend && color 0E && python app.py --env=dev"

echo [OK] Backend starting...
echo     Wait for initialization (about 15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo ========================================
echo.

REM Start Frontend
echo [3/3] Starting Frontend...
echo.

start "Frontend Service" cmd /k "cd /d %~dp0ruoyi-fastapi-frontend && color 0B && npm run dev"

echo [OK] Frontend starting...

echo.
echo ========================================
echo    Startup Complete!
echo ========================================
echo.
echo Frontend: http://localhost:80
echo Backend:  http://localhost:9099
echo API Docs: http://localhost:9099/docs
echo.
echo Account: admin / Password: admin123
echo.
pause
