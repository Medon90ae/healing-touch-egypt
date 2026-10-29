@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set TASK_NAME=HealingTouch_TelegramBot_Service
set VBS_SCRIPT=%~dp0run_bot_silent.vbs

echo ======================================================================
echo    🌿 Healing Touch Egypt - Telegram Bot Service Persistence Setup
echo ======================================================================

:: Handle /uninstall or /remove flag
if /i "%1"=="/uninstall" goto REMOVE_TASK
if /i "%1"=="/remove" goto REMOVE_TASK
if /i "%1"=="--uninstall" goto REMOVE_TASK
if /i "%1"=="--remove" goto REMOVE_TASK

:: Handle /query or /status flag
if /i "%1"=="/query" goto QUERY_TASK
if /i "%1"=="/status" goto QUERY_TASK
if /i "%1"=="--status" goto QUERY_TASK

if not exist "%VBS_SCRIPT%" (
    echo [-] ERROR: Runner script not found: "%VBS_SCRIPT%"
    echo ======================================================================
    exit /b 1
)

echo [*] Target VBScript Launcher: "%VBS_SCRIPT%"
echo [*] Task Name: "%TASK_NAME%"
echo [*] Configuring Windows Scheduled Task for ONLOGON auto-start...

:: Attempt registration with /rl HIGHEST
schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%VBS_SCRIPT%\"" /sc ONLOGON /rl HIGHEST /f >nul 2>&1
if !errorlevel! equ 0 goto TASK_SUCCESS

:: If /rl HIGHEST failed (due to non-elevated prompt), retry standard registration
schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%VBS_SCRIPT%\"" /sc ONLOGON /f >nul 2>&1
if !errorlevel! equ 0 goto TASK_SUCCESS

echo [-] ERROR: Failed to register Windows Scheduled Task "%TASK_NAME%".
echo [-] Please run this script in an administrative command prompt.
echo ======================================================================
exit /b 1

:TASK_SUCCESS
echo [+] SUCCESS: Windows Scheduled Task "%TASK_NAME%" registered successfully^^!
echo.
echo Task Details:
echo ----------------------------------------------------------------------
schtasks /query /tn "%TASK_NAME%" /fo LIST
echo ----------------------------------------------------------------------
echo.
echo [+] Persistence is ACTIVE.
echo [+] Telegram Bot will automatically launch in silent background mode whenever the user logs on.
echo.
echo Management commands:
echo   Query status:      scripts\setup_bot_service.bat /query
echo   Uninstall service: scripts\setup_bot_service.bat /uninstall
echo ======================================================================
exit /b 0

:QUERY_TASK
schtasks /query /tn "%TASK_NAME%" /fo LIST 2^>nul
if %errorlevel% neq 0 (
    echo [*] Scheduled task "%TASK_NAME%" is NOT registered.
    exit /b 1
)
exit /b 0

:REMOVE_TASK
echo [*] Removing Scheduled Task "%TASK_NAME%"...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Scheduled task "%TASK_NAME%" removed successfully.
) else (
    echo [*] Task was not registered or already removed.
)
exit /b 0
