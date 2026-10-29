@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0"
set PID_FILE=%~dp0media_assets\telegram_bot.pid
set VBS_SCRIPT=%~dp0scripts\run_bot_silent.vbs

echo ======================================================================
echo       🌿 هيلينج تاتش مصر - تشغيل مركز القيادة التفاعلي على تيليجرام
echo           Healing Touch Egypt - Telegram Bot Background Service
echo ======================================================================

:: Step 1: Check if already running via PID file
if exist "%PID_FILE%" (
    set /p BOT_PID=<"%PID_FILE%"
    if defined BOT_PID (
        set IS_ALIVE=
        for /f "tokens=1 delims=," %%p in ('tasklist /fi "PID eq !BOT_PID!" /fo csv /nh 2^>nul ^| findstr /i "python"') do (
            set IS_ALIVE=%%p
        )
        if defined IS_ALIVE (
            echo [+] بوت تيليجرام التفاعلي يعمل بالفعل في الخلفية بنشاط! [PID: !BOT_PID!]
            echo [+] اسم البوت: @ArgentoSpeedaf_bot
            echo [+] يمكنك إرسال /start في الشات للتحكم الفوري.
            echo ======================================================================
            echo اضغط Enter أو أي زر لإغلاق هذه النافذة...
            echo ======================================================================
            echo %cmdcmdline% | find """" >nul && pause >nul
            exit /b 0
        ) else (
            echo [*] تم رصد سجل عملية قديم غير نشط [PID: !BOT_PID!] — جاري التنظيف وإعادة الإطلاق...
            del "%PID_FILE%" >nul 2>&1
        )
    )
)

:: Step 2: Also kill any lingering orphaned telegram_control_bot.py processes
for /f "tokens=2 delims=," %%i in ('wmic process where "CommandLine like '%%telegram_control_bot.py%%' and Name='python.exe'" get ProcessId /format:csv 2^>nul ^| findstr /r "[0-9]"') do (
    taskkill /F /PID %%i /T >nul 2>&1
)

:: Step 3: Launch silently via VBScript runner
echo [*] جاري تشغيل بوت تيليجرام كخدمة صامتة في الخلفية...
if not exist "%VBS_SCRIPT%" (
    echo [-] خطأ: ملف التشغيل الصامت غير موجود: "%VBS_SCRIPT%"
    echo ======================================================================
    echo اضغط Enter أو أي زر لإغلاق هذه النافذة...
    echo ======================================================================
    echo %cmdcmdline% | find """" >nul && pause >nul
    exit /b 1
)

start "" wscript.exe "%VBS_SCRIPT%"
ping -n 3 127.0.0.1 >nul

:: Step 4: Verify startup
if exist "%PID_FILE%" (
    set /p NEW_PID=<"%PID_FILE%"
    set IS_NEW_ALIVE=
    for /f "tokens=1 delims=," %%p in ('tasklist /fi "PID eq !NEW_PID!" /fo csv /nh 2^>nul ^| findstr /i "python"') do (
        set IS_NEW_ALIVE=%%p
    )
    if defined IS_NEW_ALIVE (
        echo [+] ✅ تم تشغيل بوت تيليجرام بنجاح كخدمة دائمة في الخلفية! [PID: !NEW_PID!]
        echo [+] تم إرسال رسالة الترحيب وقائمة التحكم إلى حسابك على تيليجرام فوراً.
        echo [+] المعرف: @ArgentoSpeedaf_bot
        echo ======================================================================
        echo اضغط Enter أو أي زر لإغلاق هذه النافذة...
        echo ======================================================================
        echo %cmdcmdline% | find """" >nul && pause >nul
        exit /b 0
    )
)

echo [!] تنبيه: جاري اكتمال إطلاق الخدمة. يرجى مراجعة حالة البوت عبر status_bot.bat
echo ======================================================================
echo اضغط Enter أو أي زر لإغلاق هذه النافذة...
echo ======================================================================
echo %cmdcmdline% | find """" >nul && pause >nul
exit /b 0
