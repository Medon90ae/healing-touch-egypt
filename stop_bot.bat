@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set "PID_FILE=%~dp0media_assets\telegram_bot.pid"

echo ======================================================================
echo       🌿 هيلينج تاتش مصر - إيقاف مركز القيادة التفاعلي على تيليجرام
echo           Healing Touch Egypt - Stop Telegram Bot Service
echo ======================================================================

set "KILLED=0"

:: Step 0: Stop scheduled task instance if running
schtasks /end /tn "HealingTouch_TelegramBot_Service" >nul 2>&1

:: Step 1: Kill process listening on exclusive port 48199
for /f "tokens=5" %%a in ('netstat -ano -p tcp 2^>nul ^| findstr "127.0.0.1:48199" ^| findstr /i "LISTENING"') do (
    echo [*] جاري إنهاء العملية النشطة على المنفذ 48199 - PID: %%a...
    taskkill /F /PID %%a /T >nul 2>&1
    set "KILLED=1"
)

:: Step 2: Kill via PID file if still exists
if exist "%PID_FILE%" (
    set /p BOT_PID=<"%PID_FILE%"
    if defined BOT_PID (
        taskkill /F /PID !BOT_PID! /T >nul 2>&1
        set "KILLED=1"
    )
    del "%PID_FILE%" >nul 2>&1
)

:: Step 3: Kill any lingering telegram_control_bot.py python processes
for /f "tokens=2 delims=," %%i in ('wmic process where "CommandLine like '%%telegram_control_bot.py%%' and (Name='python.exe' or Name='pythonw.exe')" get ProcessId /format:csv 2^>nul ^| findstr /r "[0-9]"') do (
    taskkill /F /PID %%i /T >nul 2>&1
    set "KILLED=1"
)

if "!KILLED!"=="1" (
    echo [+] تم إيقاف خدمة بوت تيليجرام بنجاح.
) else (
    echo [*] خدمة بوت تيليجرام متوقفة بالفعل (لا توجد عمليات جارية).
)

echo ======================================================================
if /i "%1"=="nopause" exit /b 0
if /i "%1"=="--nopause" exit /b 0
echo %cmdcmdline% | findstr /i /c:"/c """ >nul && pause >nul
exit /b 0
