@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set "PID_FILE=%~dp0media_assets\telegram_bot.pid"

:: Step 1: Detect running instance via dedicated localhost port 48199
set "BOT_PID="
for /f "tokens=5" %%a in ('netstat -ano -p tcp 2^>nul ^| findstr "127.0.0.1:48199" ^| findstr /i "LISTENING"') do (
    set "BOT_PID=%%a"
)

echo ======================================================================
echo       🌿 هيلينج تاتش مصر - حالة مركز القيادة التفاعلي على تيليجرام
echo           Healing Touch Egypt - Telegram Bot Status Check
echo ======================================================================

if defined BOT_PID goto STATE_ONLINE
goto STATE_OFFLINE

:STATE_ONLINE
echo !BOT_PID!>"%PID_FILE%"
echo   الحالة:             ONLINE [قيد التشغيل ونشط]
echo   معرف العملية (PID): !BOT_PID!
echo   المنفذ الداخلي:     127.0.0.1:48199 (حماية ضد التكرار نشطة)
echo   المعرف:             @ArgentoSpeedaf_bot
echo   المشرف المعتمد:     7692685242
echo   الأوامر التفاعلية:  /start , /menu , /run , /products
echo ======================================================================
echo [+] البوت يستقبل الأوامر والقوائم التفاعلية والوسائط على مدار الساعة.
echo.
echo ======================================================================
if /i "%1"=="nopause" exit /b 0
if /i "%1"=="--nopause" exit /b 0
echo %cmdcmdline% | findstr /i /c:"/c """ >nul && pause >nul
exit /b 0

:STATE_OFFLINE
if exist "%PID_FILE%" del "%PID_FILE%" >nul 2>&1
echo   الحالة:             OFFLINE [متوقف حالياً]
echo ======================================================================
echo [*] لتشغيل الخدمة: شغل ملف start_bot.bat
echo.
echo ======================================================================
if /i "%1"=="nopause" exit /b 1
if /i "%1"=="--nopause" exit /b 1
echo %cmdcmdline% | findstr /i /c:"/c """ >nul && pause >nul
exit /b 1
