"""
Write service scripts with exact Windows CRLF line endings.
"""
from pathlib import Path

BASE_DIR = Path(r"c:\followUPSHEET\healing_touch")
SCRIPTS_DIR = BASE_DIR / "scripts"
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

RUN_N8N_SILENT_VBS = """\
' =============================================================================
' 🌿 Healing Touch Egypt - n8n Silent Background Runner
' File: scripts/run_n8n_silent.vbs
' Executes npx n8n start with WindowStyle 0 (completely hidden)
' =============================================================================
Option Explicit

Dim fso, scriptDir, projectDir, WshShell, env, currentPath, runCmd

Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
projectDir = fso.GetParentFolderName(scriptDir)

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = projectDir

Set env = WshShell.Environment("PROCESS")

' Ensure Node.js and npm paths are available in PATH
currentPath = env("PATH")
If InStr(1, currentPath, "C:\\Program Files\\nodejs", vbTextCompare) = 0 Then
    env("PATH") = currentPath & ";C:\\Program Files\\nodejs;C:\\Users\\moga\\AppData\\Roaming\\npm"
End If

' Configure n8n environment variables
env("N8N_PORT") = "5678"
env("N8N_LISTEN_ADDRESS") = "0.0.0.0"
env("GENERIC_TIMEZONE") = "Africa/Cairo"
env("N8N_DEFAULT_BINARY_DATA_MODE") = "filesystem"
env("EXECUTIONS_DATA_PRUNE") = "true"
env("EXECUTIONS_DATA_MAX_AGE") = "168"
env("N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS") = "true"
env("N8N_DIAGNOSTICS_ENABLED") = "false"
env("N8N_VERSION_NOTIFICATIONS_ENABLED") = "false"
env("N8N_RUNNERS_ENABLED") = "false"

' Execute npx n8n start hidden (WindowStyle = 0, WaitOnReturn = False)
runCmd = "cmd.exe /d /s /c npx --prefer-offline --yes n8n start"
WshShell.Run runCmd, 0, False
"""

START_N8N_BAT = """\
@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set N8N_PORT=5678
set HEALTH_URL=http://localhost:%N8N_PORT%/healthz
set VBS_SCRIPT=%~dp0scripts\\run_n8n_silent.vbs

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
echo [*] Launching n8n background service silently via scripts\\run_n8n_silent.vbs...
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
"""

STOP_N8N_BAT = """\
@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set N8N_PORT=5678

echo ======================================================================
echo           Healing Touch Egypt - n8n Service Stopper
echo ======================================================================

set N8N_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
    set N8N_PID=%%a
)

if not defined N8N_PID (
    echo [i] No active listening process found on port %N8N_PORT%.
    
    :: Check if any node n8n processes are lingering
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*n8n*start*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1
    
    echo [+] Port %N8N_PORT% is clear. n8n service is stopped.
    echo ======================================================================
    exit /b 0
)

echo [*] Found active n8n process listening on port %N8N_PORT% [PID: !N8N_PID!].
echo [*] Terminating process tree gracefully...

taskkill /F /PID !N8N_PID! /T >nul 2>&1

:: Also terminate any child node processes executing n8n start
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*n8n*start*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1

:: Wait up to 5 seconds for port release
set /a ATTEMPTS=0
:VERIFY_STOP_LOOP
ping -n 2 127.0.0.1 >nul
set /a ATTEMPTS+=1

set REMAINING_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
    set REMAINING_PID=%%a
)

if not defined REMAINING_PID (
    echo [+] SUCCESS: n8n service on port %N8N_PORT% [PID: !N8N_PID!] successfully stopped.
    echo [+] Port %N8N_PORT% has been cleanly released.
    echo ======================================================================
    exit /b 0
)

if %ATTEMPTS% geq 5 (
    echo [!] Notice: Process was terminated, but port %N8N_PORT% is still clearing network sockets [PID: !REMAINING_PID!].
    echo ======================================================================
    exit /b 0
)

goto VERIFY_STOP_LOOP
"""

STATUS_N8N_BAT = """\
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
set TEMP_HEALTH=%TEMP%\\n8n_status_%RANDOM%.tmp
if exist "!TEMP_HEALTH!" del "!TEMP_HEALTH!" >nul 2>&1

for /f "tokens=*" %%c in ('curl.exe -s -m 3 -w "%%{http_code}" -o "!TEMP_HEALTH!" "%HEALTH_URL%" 2^>nul') do (
    set HTTP_CODE=%%c
)

if exist "!TEMP_HEALTH!" (
    for /f "usebackq delims=" %%h in ("!TEMP_HEALTH!") do set HEALTH_BODY=%%h
    del "!TEMP_HEALTH!" >nul 2>&1
)

if "%HTTP_CODE%"=="200" (
    set N8N_MEM=N/A
    if defined N8N_PID (
        for /f "usebackq tokens=*" %%m in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Write-Output (([math]::Round((Get-Process -Id %N8N_PID% -ErrorAction Stop).WorkingSet64 / 1MB, 1)).ToString() + ' MB') } catch { Write-Output 'N/A' }" 2^>nul`) do (
            set N8N_MEM=%%m
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
exit /b 1
"""

SETUP_N8N_SERVICE_BAT = """\
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
schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \\"%VBS_SCRIPT%\\"" /sc ONLOGON /rl HIGHEST /f >nul 2>&1
if !errorlevel! equ 0 goto TASK_SUCCESS

:: If /rl HIGHEST failed (due to non-elevated prompt), retry standard registration
schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \\"%VBS_SCRIPT%\\"" /sc ONLOGON /f >nul 2>&1
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
echo   Query status:      scripts\\setup_n8n_service.bat /query
echo   Uninstall service: scripts\\setup_n8n_service.bat /uninstall
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
"""

FILES = {
    SCRIPTS_DIR / "run_n8n_silent.vbs": RUN_N8N_SILENT_VBS,
    BASE_DIR / "start_n8n.bat": START_N8N_BAT,
    BASE_DIR / "stop_n8n.bat": STOP_N8N_BAT,
    BASE_DIR / "status_n8n.bat": STATUS_N8N_BAT,
    SCRIPTS_DIR / "setup_n8n_service.bat": SETUP_N8N_SERVICE_BAT,
}

for path, content in FILES.items():
    content_crlf = content.replace("\r\n", "\n").replace("\n", "\r\n")
    path.write_bytes(content_crlf.encode("utf-8"))
    print(f"Written: {path.relative_to(BASE_DIR)} ({len(content_crlf)} bytes CRLF)")
