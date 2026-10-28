@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set N8N_PORT=5678
set HEALTH_URL=http://localhost:%N8N_PORT%/healthz
set VBS_SCRIPT=%~dp0scripts\run_n8n_silent.vbs

echo ======================================================================
echo           Healing Touch Egypt - n8n Service Starter
echo ======================================================================

:: Step 1: Check if n8n is already listening and healthy
set HTTP_CODE=000
for /f "tokens=*" %%c in ('curl.exe -s -m 2 -w "%%{http_code}" -o nul "%HEALTH_URL%" 2^>nul') do (
    set HTTP_CODE=%%c
)

if "%HTTP_CODE%"=="200" (
    set N8N_PID=
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
        set N8N_PID=%%a
    )
    echo [+] n8n is ALREADY RUNNING and HEALTHY on port %N8N_PORT% [PID: !N8N_PID!]
    echo [+] Health check: %HEALTH_URL% -^> HTTP 200 OK
    echo [+] Web Editor UI: http://localhost:%N8N_PORT%
    echo ======================================================================
    exit /b 0
)

:: Step 2: Check if port 5678 is occupied by a stale/unresponsive process
set STALE_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
    set STALE_PID=%%a
)

if defined STALE_PID (
    echo [!] Warning: Port %N8N_PORT% is occupied by PID !STALE_PID! but /healthz is unresponsive.
    echo [*] Terminating stale process tree...
    taskkill /F /PID !STALE_PID! /T >nul 2>&1
    ping -n 3 127.0.0.1 >nul
)

:: Step 3: Launch n8n silently via VBScript runner
echo [*] Launching n8n background service silently via scripts\run_n8n_silent.vbs...
if not exist "%VBS_SCRIPT%" (
    echo [-] ERROR: Silent runner script not found: "%VBS_SCRIPT%"
    echo ======================================================================
    exit /b 1
)

wscript.exe "%VBS_SCRIPT%"

:: Step 4: Wait for http://localhost:5678/healthz to respond with HTTP 200 (timeout: 60s)
echo [*] Waiting for n8n service to initialize on port %N8N_PORT%...
set /a ATTEMPTS=0
set MAX_ATTEMPTS=60

:WAIT_HEALTH_LOOP
ping -n 2 127.0.0.1 >nul
set /a ATTEMPTS+=1

set CHECK_CODE=000
for /f "tokens=*" %%c in ('curl.exe -s -m 2 -w "%%{http_code}" -o nul "%HEALTH_URL%" 2^>nul') do (
    set CHECK_CODE=%%c
)

if "%CHECK_CODE%"=="200" goto N8N_STARTED_SUCCESS

if %ATTEMPTS% geq %MAX_ATTEMPTS% goto N8N_START_TIMEOUT

echo [*] Initializing n8n service... [!ATTEMPTS!/%MAX_ATTEMPTS%s]
goto WAIT_HEALTH_LOOP

:N8N_STARTED_SUCCESS
set NEW_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
    set NEW_PID=%%a
)

echo ======================================================================
echo [+] SUCCESS: n8n service is ONLINE and HEALTHY^^!
echo   Listening Port:  %N8N_PORT%
echo   Process PID:     !NEW_PID!
echo   Health Endpoint: %HEALTH_URL% [HTTP 200 OK]
echo   Web Editor UI:   http://localhost:%N8N_PORT%
echo ======================================================================
exit /b 0

:N8N_START_TIMEOUT
echo ======================================================================
echo [-] ERROR: Timed out waiting for n8n service to respond on %HEALTH_URL% after %MAX_ATTEMPTS% seconds.
echo [-] Please inspect logs or run 'status_n8n.bat' to verify status.
echo ======================================================================
exit /b 1
