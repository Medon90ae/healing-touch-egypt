@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set N8N_PORT=5678

echo ======================================================================
echo           Healing Touch Egypt - n8n Service Stopper
echo ======================================================================

:: Identify listening process PID on port 5678
set N8N_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":%N8N_PORT%.*LISTENING" 2^>nul') do (
    set N8N_PID=%%a
)

if not defined N8N_PID (
    echo [*] n8n service is NOT running on port %N8N_PORT% (no listening process found).
    echo ======================================================================
    echo Press Enter or any key to close this window...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 0
)

echo [*] Found n8n service listening on port %N8N_PORT% [PID: !N8N_PID!]
echo [*] Terminating process tree for PID !N8N_PID!...
taskkill /F /PID !N8N_PID! /T >nul 2>&1

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
    echo Press Enter or any key to close this window...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 0
)

if %ATTEMPTS% geq 5 (
    echo [!] Notice: Process was terminated, but port %N8N_PORT% is still clearing network sockets [PID: !REMAINING_PID!].
    echo ======================================================================
    echo Press Enter or any key to close this window...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 0
)

goto VERIFY_STOP_LOOP
