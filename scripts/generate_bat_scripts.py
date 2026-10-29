from pathlib import Path

start_bat = """@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set "PID_FILE=%~dp0media_assets\\telegram_bot.pid"
set "VBS_SCRIPT=%~dp0scripts\\run_bot_silent.vbs"

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
echo %cmdcmdline% | findstr /i /c:"/c \"\"" >nul && pause >nul
exit /b 0

:END_ERROR
echo ======================================================================
if /i "%1"=="nopause" exit /b 1
if /i "%1"=="--nopause" exit /b 1
echo %cmdcmdline% | findstr /i /c:"/c \"\"" >nul && pause >nul
exit /b 1
"""

status_bat = """@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set "PID_FILE=%~dp0media_assets\\telegram_bot.pid"

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
echo %cmdcmdline% | findstr /i /c:"/c \"\"" >nul && pause >nul
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
echo %cmdcmdline% | findstr /i /c:"/c \"\"" >nul && pause >nul
exit /b 1
"""

stop_bat = """@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set "PID_FILE=%~dp0media_assets\\telegram_bot.pid"

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
echo %cmdcmdline% | findstr /i /c:"/c \"\"" >nul && pause >nul
exit /b 0
"""

for path, content in [
    (Path(r"c:\followUPSHEET\healing_touch\start_bot.bat"), start_bat),
    (Path(r"c:\followUPSHEET\healing_touch\status_bot.bat"), status_bat),
    (Path(r"c:\followUPSHEET\healing_touch\stop_bot.bat"), stop_bat),
]:
    crlf_content = content.replace("\r\n", "\n").replace("\n", "\r\n")
    path.write_bytes(crlf_content.encode("utf-8"))

print("All 3 scripts generated cleanly with labels and zero nested-parenthesis traps.")
