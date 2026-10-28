@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set PID_FILE=%~dp0media_assets\telegram_bot.pid

echo ======================================================================
echo       🌿 هيلينج تاتش مصر - إيقاف مركز القيادة التفاعلي على تيليجرام
echo           Healing Touch Egypt - Stop Telegram Bot Service
echo ======================================================================

set KILLED=0
if exist "%PID_FILE%" (
    set /p BOT_PID=<"%PID_FILE%"
    if defined BOT_PID (
        echo [*] جاري إنهاء عملية بوت تيليجرام [PID: !BOT_PID!]...
        taskkill /F /PID !BOT_PID! /T >nul 2>&1
        set KILLED=1
    )
    del "%PID_FILE%" >nul 2>&1
)

:: Also kill any lingering telegram_control_bot.py python processes
for /f "tokens=2 delims=," %%i in ('wmic process where "CommandLine like '%%telegram_control_bot.py%%' and Name='python.exe'" get ProcessId /format:csv 2^>nul ^| findstr /r "[0-9]"') do (
    taskkill /F /PID %%i /T >nul 2>&1
    set KILLED=1
)

if "%KILLED%"=="1" (
    echo [+] ✅ تم إيقاف خدمة بوت تيليجرام بنجاح.
) else (
    echo [*] ℹ️ خدمة بوت تيليجرام متوقفة بالفعل (لا توجد عمليات جارية).
)

echo ======================================================================
exit /b 0
