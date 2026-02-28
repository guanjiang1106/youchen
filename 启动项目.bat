@echo off
chcp 65001 >nul
title RuoYi-FastAPI ????
color 0A

echo.
echo ========================================
echo    RuoYi-FastAPI ????
echo ========================================
echo.

REM ????? Redis
echo [1/3] ?? Redis ??...
echo.

tasklist | find /i "redis-server.exe" >nul
if %errorlevel% equ 0 (
    echo [] Redis ???
    goto :start_backend
)

echo [!] Redis ????????...
echo.

pushd "D:\Program Files\Redis-x64-5.0.14.1"
if exist redis-server.exe (
    echo [] ?? Redis
    start "Redis ??" redis-server.exe
    popd
    timeout /t 3 /nobreak >nul
    
    tasklist | find /i "redis-server.exe" >nul
    if %errorlevel% equ 0 (
        echo [] Redis ????
    ) else (
        echo [] Redis ????
        pause
        exit /b 1
    )
) else (
    echo [] ??? Redis
    popd
    pause
    exit /b 1
)

:start_backend
echo.
echo ========================================
echo.

REM ????
echo [2/3] ??????...
echo.

start "????" cmd /k "cd /d %~dp0ruoyi-fastapi-backend && color 0E && python app.py --env=dev"

echo [] ?????????
echo     ????????15??...
timeout /t 15 /nobreak >nul

echo.
echo ========================================
echo.

REM ????
echo [3/3] ??????...
echo.

start "????" cmd /k "cd /d %~dp0ruoyi-fastapi-frontend && color 0B && npm run dev"

echo [] ?????????

echo.
echo ========================================
echo    ?????
echo ========================================
echo.
echo ??: http://localhost:80
echo ??: http://localhost:9099
echo ??: http://localhost:9099/docs
echo.
echo ??: admin / ??: admin123
echo.
pause
