@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set N8N_PORT=5678
set HEALTH_URL=http://localhost:%N8N_PORT%/healthz
set N8N_PID=

:: Find listening PID on port 5678 (supports both IPv4 and IPv6)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
    set N8N_PID=%%a
)

:: Query healthz endpoint via curl
set HTTP_CODE=000
set HEALTH_BODY=
set TEMP_HEALTH=%TEMP%\n8n_status_%RANDOM%.tmp
if exist "%TEMP_HEALTH%" del "%TEMP_HEALTH%" >nul 2>&1

for /f "tokens=*" %%c in ('curl.exe -s -m 3 -w "%%{http_code}" -o "%TEMP_HEALTH%" "%HEALTH_URL%" 2^>nul') do (
    set HTTP_CODE=%%c
)

if exist "%TEMP_HEALTH%" (
    for /f "usebackq delims=" %%h in ("%TEMP_HEALTH%") do set HEALTH_BODY=%%h
    del "%TEMP_HEALTH%" >nul 2>&1
)

if "%HTTP_CODE%"=="200" (
    set N8N_MEM=N/A
    if defined N8N_PID (
        for /f "tokens=5* delims=," %%m in ('tasklist /fi "PID eq !N8N_PID!" /fo csv /nh 2^>nul') do (
            if not "%%n"=="" (
                set RAW_MEM=%%m,%%n
                set N8N_MEM=!RAW_MEM:"=!
            ) else (
                set N8N_MEM=%%~m
            )
        )
    )

    echo ======================================================================
    echo           Healing Touch Egypt - n8n Service Status
    echo ======================================================================
    echo   Status:           ONLINE [HEALTHY]
    echo   Health Endpoint:  %HEALTH_URL%
    echo   HTTP Status:      200 OK
    echo   Health Response:  !HEALTH_BODY!
    echo   Listening Port:   %N8N_PORT%
    echo   Process PID:      !N8N_PID!
    echo   Process Name:     node.exe
    echo   Memory Usage:     !N8N_MEM!
    echo   Web Editor UI:    http://localhost:%N8N_PORT%
    echo ======================================================================
    echo Press Enter or any key to close this window...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 0
)

if defined N8N_PID (
    echo ======================================================================
    echo           Healing Touch Egypt - n8n Service Status
    echo ======================================================================
    echo   Status:           UNHEALTHY / INITIALIZING
    echo   Listening Port:   %N8N_PORT% [Occupied by PID: !N8N_PID!]
    echo   Health Endpoint:  %HEALTH_URL% [HTTP !HTTP_CODE!]
    echo ======================================================================
    echo   The port is listening but /healthz is not returning HTTP 200.
    echo   Run 'stop_n8n.bat' followed by 'start_n8n.bat' to restart.
    echo ======================================================================
    echo Press Enter or any key to close this window...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 2
)

echo ======================================================================
echo           Healing Touch Egypt - n8n Service Status
echo ======================================================================
echo   Status:           OFFLINE [STOPPED]
echo   Listening Port:   %N8N_PORT% [Not listening]
echo   Health Endpoint:  %HEALTH_URL% [Unreachable]
echo ======================================================================
echo   To start the n8n background service, run:
echo     start_n8n.bat
echo ======================================================================
echo Press Enter or any key to close this window...
echo ======================================================================
echo %cmdcmdline% | find """" >nul && pause >nul
exit /b 1
