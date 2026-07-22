@echo off
chcp 65001 >nul
cd /d "D:\Gigbestcopilot_app\BuildPilot\BuildPilot"
echo [INFO] Running Manual Build...
python manual_build.py
pause
