@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set "PID_FILE=%~dp0media_assets\telegram_bot.pid"
set "VBS_SCRIPT=%~dp0scripts\run_bot_silent.vbs"

echo ======================================================================
echo       🌿 هيلينج تاتش مصر - تشغيل مركز القيادة التفاعلي على تيليجرام
echo           Healing Touch Egypt - Telegram Bot Background Service
echo ======================================================================

:: Step 1: Check if already running via exclusive localhost port 48199
set "PORT_PID="
for /f "tokens=5" %%a in ('netstat -ano -p tcp 2^>nul ^| findstr "127.0.0.1:48199" ^| findstr /i "LISTENING"') do (
    set "PORT_PID=%%a"
)

if defined PORT_PID goto ALREADY_RUNNING

:: Step 2: Clean up any lingering orphaned telegram_control_bot.py processes
for /f "tokens=2 delims=," %%i in ('wmic process where "CommandLine like '%%telegram_control_bot.py%%' and (Name='python.exe' or Name='pythonw.exe')" get ProcessId /format:csv 2^>nul ^| findstr /r "[0-9]"') do (
    taskkill /F /PID %%i /T >nul 2>&1
)
if exist "%PID_FILE%" del "%PID_FILE%" >nul 2>&1

:: Step 3: Launch via Scheduled Task or Silent VBScript
echo [*] جاري تشغيل بوت تيليجرام كخدمة صامتة في الخلفية...

set "LAUNCHED_VIA_TASK=0"
schtasks /query /tn "HealingTouch_TelegramBot_Service" >nul 2>&1
if !errorlevel! equ 0 (
    schtasks /run /tn "HealingTouch_TelegramBot_Service" >nul 2>&1
    if !errorlevel! equ 0 set "LAUNCHED_VIA_TASK=1"
)

if "!LAUNCHED_VIA_TASK!"=="0" (
    if not exist "%VBS_SCRIPT%" goto RUNNER_NOT_FOUND
    start "" wscript.exe "%VBS_SCRIPT%"
)

:: Wait for socket binding
ping -n 3 127.0.0.1 >nul

:: Step 4: Verify startup via port 48199
set "VERIFIED_PID="
for /f "tokens=5" %%a in ('netstat -ano -p tcp 2^>nul ^| findstr "127.0.0.1:48199" ^| findstr /i "LISTENING"') do (
    set "VERIFIED_PID=%%a"
)

if defined VERIFIED_PID goto LAUNCH_SUCCESS
goto LAUNCH_PENDING

:ALREADY_RUNNING
echo [+] بوت تيليجرام التفاعلي يعمل بالفعل في الخلفية بنشاط - PID: !PORT_PID!
echo [+] المنفذ الداخلي المؤمن: 127.0.0.1:48199
echo [+] اسم البوت: @ArgentoSpeedaf_bot
echo [+] يمكنك إرسال /start في الشات للتحكم الفوري.
goto END_SUCCESS

:LAUNCH_SUCCESS
echo !VERIFIED_PID!>"%PID_FILE%"
echo [+] تم تشغيل بوت تيليجرام التفاعلي بنجاح - PID: !VERIFIED_PID!
echo [+] اسم البوت: @ArgentoSpeedaf_bot
echo [+] المشرف المعتمد: 7692685242
echo [+] المنفذ المؤمن: 127.0.0.1:48199
echo [+] يمكنك الآن فتح تيليجرام وإرسال /start أو النقر على الأزرار التفاعلية.
goto END_SUCCESS

:LAUNCH_PENDING
echo [-] تنبيه: جاري بدء الخدمة في الخلفية... يمكنك فحص الحالة عبر status_bot.bat
goto END_SUCCESS

:RUNNER_NOT_FOUND
echo [-] خطأ: ملف التشغيل الصامت غير موجود: "%VBS_SCRIPT%"
goto END_ERROR

:END_SUCCESS
echo ======================================================================
if /i "%1"=="nopause" exit /b 0
if /i "%1"=="--nopause" exit /b 0
echo %cmdcmdline% | findstr /i /c:"/c """ >nul && pause >nul
exit /b 0

:END_ERROR
echo ======================================================================
if /i "%1"=="nopause" exit /b 1
if /i "%1"=="--nopause" exit /b 1
echo %cmdcmdline% | findstr /i /c:"/c """ >nul && pause >nul
exit /b 1
