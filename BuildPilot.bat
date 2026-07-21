@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM ============================================
REM BuildPilot Launcher
REM Runs auto_updater.py or manual_build.py
REM ============================================

cd /d "D:\Gigbestcopilot_app\BuildPilot\BuildPilot"

if "%1"=="auto" goto run_auto
if "%1"=="manual" goto run_manual
if "%1"=="" goto menu

echo.
echo Invalid argument: %1
echo.
goto help

:menu
echo.
echo ============================================
echo     BuildPilot Launcher
echo ============================================
echo.
echo  [1] Run Auto Updater (continuous monitoring)
echo  [2] Run Manual Build (one-time build + upload)
echo  [3] Install dependencies
echo  [4] Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto run_auto
if "%choice%"=="2" goto run_manual
if "%choice%"=="3" goto install_deps
if "%choice%"=="4" goto end

echo Invalid choice!
goto menu

:run_auto
echo.
echo [INFO] Starting Auto Updater...
echo [INFO] Press Ctrl+C to stop
echo.
python auto_updater.py
if errorlevel 1 (
    echo [ERROR] Auto updater crashed!
    pause
)
goto end

:run_manual
echo.
echo [INFO] Starting Manual Build...
echo.
python manual_build.py
if errorlevel 1 (
    echo [ERROR] Manual build failed!
    pause
) else (
    echo [INFO] Build completed successfully!
    pause
)
goto end

:install_deps
echo.
echo [INFO] Installing required packages...
pip install requests python-dotenv
echo [INFO] Done!
pause
goto menu

:help
echo Usage: BuildPilot.bat [auto ^| manual]
echo.
echo   auto    - Run continuous update checker
echo   manual  - Run one-time build and upload
echo.
echo Without arguments, shows interactive menu.
pause

:end
endlocal
