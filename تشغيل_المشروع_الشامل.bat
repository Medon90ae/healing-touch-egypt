@echo off
chcp 1256 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo         åíáíäÌ ÊÇÊÔ ãÕÑ - áæÍÉ ÇáÊÍßã æÇáãÍÑß ÇáãæÍÏ ÇáÔÇãá
echo =====================================================================
echo.
echo   [1] ÇáÊÔÛíá ÇáÔÇãá æÇáäÔÑ ÇáİæÑí (ÇáãæŞÚ + ßÇäİÇ + İíÏíæ + İíÓÈæß)
echo   [2] ãÚÇíäÉ æÊÌåíÒ ÇáãÍÊæì æÇáÊÕãíã æÇáİíÏíæ (ÈÏæä äÔÑ - Dry Run)
echo   [3] ÊÍÏíË ÃÓÚÇÑ ÇáãæŞÚ æÇáãŞÇáÇÊ ãä ÌæÌá ÔíÊ İŞØ
echo   [4] ÊÍÏíË ÍÒãÉ Google NotebookLM æÏãÌ ÇáÕæÊíÇÊ
echo   [5] ÊÔÛíá ÑÇÏÇÑ ÌÑæÈÇÊ İíÓÈæß İŞØ
echo.
echo =====================================================================
set /p choice="ÇÎÊÑ ÑŞã ÇáÚãáíÉ ÇáãØáæÈÉ (ÇÖÛØ Enter áÇÎÊíÇÑ 1 ÇİÊÑÇÖíÇ): "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    echo.
    echo [1/2] ÌÇÑí ÊÍÏíË ÇáãæŞÚ æÇáÃÓÚÇÑ ãä ÌæÌá ÔíÊ...
    ".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site --push-github
    echo.
    echo [2/2] ÌÇÑí ÊÔÛíá ÇÓÊæÏíæ ÇáÊÕãíã æÇáİíÏíæ æÇáäÔÑ ÇáÔÇãá...
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode all
)
if "%choice%"=="2" (
    echo.
    ".venv\Scripts\python.exe" antigravity_social_automation.py --dry-run
)
if "%choice%"=="3" (
    echo.
    ".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site --push-github
)
if "%choice%"=="4" (
    echo.
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode notebooklm
)
if "%choice%"=="5" (
    echo.
    ".venv\Scripts\python.exe" antigravity_social_automation.py --mode groups
)

echo.
echo =====================================================================
echo ÇßÊãáÊ ÇáÚãáíÉ ÈäÌÇÍ!
pause