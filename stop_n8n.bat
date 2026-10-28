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
