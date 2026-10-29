@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set PID_FILE=%~dp0media_assets\telegram_bot.pid
set BOT_PID=

if exist "%PID_FILE%" (
    set /p BOT_PID=<"%PID_FILE%"
)

:: Self-healing: if PID_FILE was missing, search for running process
if not defined BOT_PID (
    for /f "tokens=2 delims=," %%i in ('wmic process where "CommandLine like '%%telegram_control_bot.py%%' and Name='python.exe'" get ProcessId /format:csv 2^>nul ^| findstr /r "[0-9]"') do (
        set BOT_PID=%%i
        if defined BOT_PID (
            echo !BOT_PID!>"%PID_FILE%"
        )
    )
)

set IS_RUNNING=0
if defined BOT_PID (
    for /f "tokens=1 delims=," %%p in ('tasklist /fi "PID eq !BOT_PID!" /fo csv /nh 2^>nul ^| findstr /i "python"') do (
        set IS_RUNNING=1
    )
)

echo ======================================================================
echo       🌿 هيلينج تاتش مصر - حالة مركز القيادة التفاعلي على تيليجرام
echo           Healing Touch Egypt - Telegram Bot Status Check
echo ======================================================================

if "%IS_RUNNING%"=="1" (
    echo   الحالة:             🟢 قيد التشغيل ونشط (ONLINE)
    echo   معرف العملية (PID): !BOT_PID!
    echo   المعرف:             @ArgentoSpeedaf_bot
    echo   المشرف المعتمد:     7692685242
    echo   الأوامر التفاعلية:  /start , /menu , /run , /products
    echo ======================================================================
    echo [+] البوت يستقبل الأوامر والقوائم التفاعلية والوسائط على مدار الساعة.
    echo.
    echo ======================================================================
    echo اضغط Enter أو أي زر لإغلاق هذه النافذة...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 0
) else (
    echo   الحالة:             🔴 متوقف حالياً (OFFLINE)
    echo ======================================================================
    echo [*] لتشغيل الخدمة: شغل ملف start_bot.bat
    echo.
    echo ======================================================================
    echo اضغط Enter أو أي زر لإغلاق هذه النافذة...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 1
)
