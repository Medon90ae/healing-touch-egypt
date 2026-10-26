@echo off
chcp 1256 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo         åíáíäÌ ÊÇÊÔ ãÕÑ - áæÍÉ ÇáÊÍßã æÇáãÍÑß ÇáãæÍÏ ÇáÔÇãá (2026)
echo =====================================================================
echo.
echo   [1] ÇáÊÔÛíá ÇáÔÇãá æÇáäÔÑ ÇáİæÑí (İíÓÈæß + ÅäÓÊÌÑÇã + Êíß Êæß + ÈáæÌÑ + ÑíÏíÊ)
echo   [2] ãÚÇíäÉ æÊÌåíÒ ÇáãÍÊæì æÇáÊÕãíã æÇáİíÏíæ (ÈÏæä äÔÑ - Dry Run)
echo   [3] ÊÍÏíË ÃÓÚÇÑ æãŞÇáÇÊ ÇáãæŞÚ ãä Google Sheet æÇáÑİÚ áÜ GitHub
echo   [4] ÊÍÏíË ÍÒãÉ Google NotebookLM æÌáÈ ÕæÑ pic æÕäÏæŞ manual_inbox
echo   [5] İÊÍ ÕäÏæŞ ÇáæÇÑÏ ÇáãÚÊãÏ (manual_inbox) áÓÍÈ æÅÓŞÇØ äÕæÕ æİíÏíæåÇÊ Çáíæã
echo   [6] ÇÓÊÚÑÇÖ æİÍÕ ÓÌá ÇáÚãáÇÁ æÍÌæÒÇÊ ÇáÇÓÊÔÇÑÇÊ İí Google Sheet
echo   [7] ÑÈØ æÊİÚíá ÍÓÇÈ Reddit ÊáŞÇÆíÇğ (áãÑÉ æÇÍÏÉ İŞØ)
echo   [8] İÊÍ ÃÍÏË ãäÔæÑ Êã äÔÑå Úáì İíÓÈæß İí ÇáãÊÕİÍ
echo.
echo =====================================================================
set /p choice="ÇÎÊÑ ÑŞã ÇáÚãáíÉ ÇáãØáæÈÉ (ÇÖÛØ Enter áÇÎÊíÇÑ 1 ÇİÊÑÇÖíÇğ): "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    echo.
    echo [*] [1/2] ÌÇÑí ãÒÇãäÉ ÇáÃÓÚÇÑ æÊÍÏíË ÇáãæŞÚ Úáì GitHub Pages...
    ".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site --push-github
    echo.
    echo [*] [2/2] ÌÇÑí ÊÔÛíá ÇÓÊæÏíæ ÇáãÍÊæì æÇáÊŞÇØ ÃÕæá manual_inbox æÇáäÔÑ ÇáÔÇãá...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode all
)
if "%choice%"=="2" (
    echo.
    echo [*] ÌÇÑí ÊÔÛíá æÖÚ ÇáãÚÇíäÉ æÊæáíÏ ÇáÊÕÇãíã æÇáİíÏíæ æÇáäÕæÕ ÈÏæä äÔÑ...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --dry-run
)
if "%choice%"=="3" (
    echo.
    echo [*] ÌÇÑí ãÒÇãäÉ ÇáÃÓÚÇÑ ÇáÍíÉ æãŞÇáÇÊ ÇáÓíæ ãä Google Sheet...
    ".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site --push-github
)
if "%choice%"=="4" (
    echo.
    echo [*] ÌÇÑí ÊÍÏíË ÍÒãÉ NotebookLM æÊÌåíÒ ÇáÕæÑ ÇáØÈíÉ æÕäÏæŞ manual_inbox...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode notebooklm
)
if "%choice%"=="5" (
    echo.
    echo [*] ÌÇÑí İÊÍ ãÌáÏ ÇáÇÓÊŞÈÇá manual_inbox...
    explorer "media_assets\manual_inbox"
)
if "%choice%"=="6" (
    echo.
    echo [*] ÌÇÑí İÍÕ ÇáÇÊÕÇá ÈÌÏæá Google Sheet æİÊÍ ÓÌá ÇáÇÓÊÔÇÑÇÊ...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --check-sheet
    start https://docs.google.com/spreadsheets/d/12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k/edit?gid=513215731#gid=513215731
)
if "%choice%"=="7" (
    echo.
    echo [*] ÌÇÑí ÈÏÁ ÊİæíÖ æÑÈØ ÍÓÇÈ Reddit ÇáÏÇÆã...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode auth-reddit
)
if "%choice%"=="8" (
    echo.
    echo [*] ÌÇÑí İÊÍ ÃÍÏË ãäÔæÑ Êã äÔÑå Úáì İíÓÈæß...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode open-latest
)

echo.
echo =====================================================================
echo ÇßÊãáÊ ÇáÚãáíÉ ÈäÌÇÍ!
pause
