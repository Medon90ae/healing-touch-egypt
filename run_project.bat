@echo off
chcp 65001 >nul
cd /d "%~dp0"
".venv\Scripts\python.exe" menu.py
if %errorlevel% neq 0 pause
