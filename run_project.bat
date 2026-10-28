@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================================
echo         🌿 هيلينج تاتش مصر - محرك التشغيل والنشر السريري الموحد (2026)
echo              Healing Touch Egypt - Master Control Center
echo ======================================================================
echo.
echo   [1] التشغيل الشامل بضغطة واحدة (Single-Click Master Pipeline)
echo   [2] معاينة وتجهيز الأصول واللاندنج بيدج بدون نشر (Dry Run)
echo   [3] فحص حالة خدمة n8n الخلفية الدائمة (n8n Service Status)
echo   [4] فتح صندوق الاستقبال manual_inbox وملف البرومبتات
echo   [5] تحديث الموسوعة وخريطة السيو ورفع التحديثات لـ GitHub Pages
echo   [6] فحص ومزامنة سجل العملاء المحلي مع Google Sheet
echo   [7] فتح أحدث حزمة نشر جاهزة للمنصات (Ready-to-Publish Pack)
echo   [8] لوحة التحكم التفاعلية الشاملة (menu.py)
echo.
echo ======================================================================
set choice=1
set /p choice="اختر رقم العملية المطلوبة (اضغط Enter لاختيار 1 للتشغيل الشامل): "

if "%choice%"=="1" goto opt1
if "%choice%"=="2" goto opt2
if "%choice%"=="3" goto opt3
if "%choice%"=="4" goto opt4
if "%choice%"=="5" goto opt5
if "%choice%"=="6" goto opt6
if "%choice%"=="7" goto opt7
if "%choice%"=="8" goto opt8
goto opt1

:opt1
echo.
echo [*] [1/1] جاري تشغيل المسار الرئيسي الموحد (Single-Click Master Pipeline)...
".venv\Scripts\python.exe" single_click_master_pipeline.py
if %errorlevel% equ 0 (
    echo.
    echo [+] ✅ تم تنفيذ المسار الشامل بنجاح!
) else (
    echo.
    echo [!] ❌ حدث خطأ أثناء تنفيذ المسار (كود الخطأ: %errorlevel%)
)
goto end

:opt2
echo.
echo [*] جاري تشغيل المعاينة الكاملة بدون نشر شبكي (Dry Run Mode)...
".venv\Scripts\python.exe" single_click_master_pipeline.py --dry-run
goto end

:opt3
echo.
echo [*] جاري فحص حالة خدمة n8n الدائمة في الخلفية...
call status_n8n.bat
goto end

:opt4
echo.
echo [*] فتح مجلد manual_inbox وملف البرومبتات...
if not exist "media_assets\manual_inbox" mkdir "media_assets\manual_inbox"
explorer "media_assets\manual_inbox"
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt5
echo.
echo [*] [1/3] جاري تحديث صفحات الموقع ومقالات السيو وخريطة الموقع...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/3] جاري تجميع تطبيق البوابة التفاعلية...
call npm --prefix "portal_app" run build
if exist "portal_app\dist" (
    xcopy /E /Y /I "portal_app\dist\*" "docs\portal\" >nul
)
echo.
echo [*] [3/3] جاري رفع التحديثات إلى GitHub Pages...
git add -A
git commit -m "feat(deploy): live site, portal, and seo sync"
git push origin main
goto end

:opt6
echo.
echo [*] فحص ومزامنة قاعدة بيانات العملاء المحلية وسجل SQLite مع Google Sheet...
".venv\Scripts\python.exe" scripts\crm_sync_engine.py --sync
".venv\Scripts\python.exe" scripts\crm_sync_engine.py --stats
goto end

:opt7
echo.
echo [*] فتح أحدث حزمة نشر مفرزة للمنصات (Ready-to-Publish Pack)...
".venv\Scripts\python.exe" -c "import menu; menu.run_option_4()"
goto end

:opt8
echo.
echo [*] فتح لوحة التحكم التفاعلية الشاملة (menu.py)...
".venv\Scripts\python.exe" menu.py
goto end

:end
echo.
echo ======================================================================
echo انتهت العملية. اضغط أي زر للمتابعة...
echo ======================================================================
pause
