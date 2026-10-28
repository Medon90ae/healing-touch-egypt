@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set TASK_NAME=HealingTouch_n8n_Service
set VBS_SCRIPT=%~dp0run_n8n_silent.vbs

echo ======================================================================
echo       Healing Touch Egypt - n8n Service Persistence Setup
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
echo [-] Please run this script in an administrative command prompt or check Task Scheduler permissions.
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
echo [+] n8n will automatically launch in silent background mode whenever the user logs on.
echo.
echo Management commands:
echo   Query status:      scripts\setup_n8n_service.bat /query
echo   Uninstall service: scripts\setup_n8n_service.bat /uninstall
echo   Start service:     start_n8n.bat
echo   Stop service:      stop_n8n.bat
echo   Service status:    status_n8n.bat
echo ======================================================================
exit /b 0

:REMOVE_TASK
echo [*] Removing Windows Scheduled Task "%TASK_NAME%"...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
if !errorlevel! equ 0 (
    echo [+] Scheduled task "%TASK_NAME%" was successfully deleted.
    echo ======================================================================
    exit /b 0
) else (
    echo [i] Task "%TASK_NAME%" does not exist or was already removed.
    echo ======================================================================
    exit /b 0
)

:QUERY_TASK
schtasks /query /tn "%TASK_NAME%" /fo LIST 2>&1
exit /b !errorlevel!
