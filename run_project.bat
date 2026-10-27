@echo off
chcp 65001 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo        🌿 هيلينج تاتش مصر - محرك النشر والتعافي السريري الموحد (2026)
echo =====================================================================
echo.
echo   [1] التشغيل الشامل والنشر الفوري (قراءة manual_inbox + بناء LPs + النشر لسوشيال وGitHub)
echo   [2] تجهيز حملة اليوم والبرومبتات باختيار المنتج (Pomelli + Deep Research + NotebookLM)
echo   [3] معاينة وتجهيز الأصول واللاندنج بيدج بدون نشر (Dry Run)
echo   [4] فتح صندوق الاستقبال manual_inbox وملف البرومبتات الجاهزة للنسخ
echo   [5] تحديث الموقع وتطبيق البوابة ونشر التغييرات مباشرة إلى GitHub Pages
echo   [6] استعراض وفحص سجل العملاء وحجوزات الاستشارات في Google Sheet
echo   [7] ربط وتفعيل حساب Reddit تلقائياً (لمرة واحدة فقط)
echo   [8] فتح أحدث منشور تم نشره على فيسبوك في المتصفح
echo.
echo =====================================================================
set choice=1
set /p choice="اختر رقم العملية المطلوبة (اضغط Enter لاختيار 1 للتشغيل والنشر الشامل): "

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
echo [*] [1/5] جاري فحص manual_inbox وتوليد صفحات الهبوط متعددة الزوايا (Multi-Angle LPs)...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode auto-daily
echo.
echo [*] [2/5] جاري إعادة بناء الموقع وخريطة السيو sitemap.xml ومقالات التعافي...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [3/5] جاري بناء وتجميع تطبيق البوابة التفاعلية (Clinical Portal App)...
call npm --prefix "portal_app" run build
xcopy /E /Y /I "portal_app\dist\*" "docs\portal\"
echo.
echo [*] [4/5] جاري رفع ونشر كافة التحديثات والصفحات الحية إلى GitHub Pages...
git add -A
git commit -m "feat(deploy): update multi-angle landing pages, portal, and seo site"
git push origin main
echo.
echo [*] [5/5] جاري بث المنشورات والتوجيهات السريرية إلى منصات التواصل الاجتماعي (Facebook, Reddit, Blogger)...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode publish
goto end

:opt2
echo.
echo [*] تجهيز حزمة البرومبتات والمصادر السريرية باختيار المنتج...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode notebooklm
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt3
echo.
echo [*] معاينة وتوليد الأصول واللاندنج بيدج بدون نشر فعلي (Dry Run)...
".venv\Scripts\python.exe" antigravity_social_automation.py --dry-run
goto end

:opt4
echo.
echo [*] فتح صندوق الاستقبال manual_inbox وملف البرومبتات...
explorer "media_assets\manual_inbox"
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt5
echo.
echo [*] [1/3] جاري تحديث صفحات الموقع ومقالات السيو...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/3] جاري بناء وتجميع تطبيق البوابة التفاعلية (Clinical Portal App)...
call npm --prefix "portal_app" run build
xcopy /E /Y /I "portal_app\dist\*" "docs\portal\"
echo.
echo [*] [3/3] جاري نشر التغييرات إلى GitHub Pages...
git add -A
git commit -m "feat(deploy): live site & portal sync to GitHub Pages"
git push origin main
echo.
echo [OK] تم التحديث والنشر بنجاح على GitHub Pages!
echo [URL] رابط البوابة المباشر: https://medon90ae.github.io/healing-touch-egypt/portal/
start https://medon90ae.github.io/healing-touch-egypt/portal/
goto end

:opt6
echo.
echo [*] فحص الاتصال بسجل Google Sheet...
".venv\Scripts\python.exe" antigravity_social_automation.py --check-sheet
start https://docs.google.com/spreadsheets/d/12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k/edit?gid=513215731#gid=513215731
goto end

:opt7
echo.
echo [*] ربط وتفويض حساب Reddit...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode auth-reddit
goto end

:opt8
echo.
echo [*] فتح أحدث منشور تم نشره على فيسبوك...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode open-latest
goto end

:end
echo.
echo =====================================================================
echo اكتملت العملية بنجاح!
pause
