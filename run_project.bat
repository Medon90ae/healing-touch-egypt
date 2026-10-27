@echo off
chcp 1256 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo            -      (2026)
echo =====================================================================
echo.
echo   [1]     (  +  +   GitHub + )
echo   [2]       (Clinical Content + Verified Medical Design)
echo   [3]        (Dry Run)
echo   [4]    manual_inbox    
echo   [5]         GitHub Pages
echo   [6]        Google Sheet
echo   [7]    Reddit  (  )
echo   [8]         
echo.
echo =====================================================================
set choice=5
set /p choice="    ( Enter  5    ): "

if "%choice%"=="1" goto opt1
if "%choice%"=="2" goto opt2
if "%choice%"=="3" goto opt3
if "%choice%"=="4" goto opt4
if "%choice%"=="5" goto opt5
if "%choice%"=="6" goto opt6
if "%choice%"=="7" goto opt7
if "%choice%"=="8" goto opt8
goto opt5

:opt1
echo.
echo [*] [1/4]        ...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/4]        (Clinical Guidance Portal App)...
call npm --prefix "portal_app" run build
xcopy /E /Y /I "portal_app\dist\*" "docs\portal\"
echo.
echo [*] [3/4]        GitHub Pages ...
git add docs/ portal_app/ campaign_landing_engine.py github_seo_trend_engine.py products_registry.json promo_config.json PROJECT.md run_project.bat .gitignore
git commit -m "Auto-deploy: full clinical portal and site sync"
git push origin main
echo.
echo [*] [4/4]       manual_inbox  ...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode all
goto end

:opt2
echo.
echo [*]       (Clinical Research & NotebookLM)...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode notebooklm
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt3
echo.
echo [*]           ...
".venv\Scripts\python.exe" antigravity_social_automation.py --dry-run
goto end

:opt4
echo.
echo [*]     manual_inbox  ...
explorer "media_assets\manual_inbox"
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt5
echo.
echo [*] [1/3]        Google Sheet...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/3]       (Clinical Guidance Portal App)...
call npm --prefix "portal_app" run build
xcopy /E /Y /I "portal_app\dist\*" "docs\portal\"
echo.
echo [*] [3/3]      GitHub Pages...
git add docs/ portal_app/ campaign_landing_engine.py github_seo_trend_engine.py products_registry.json promo_config.json PROJECT.md run_project.bat .gitignore
git commit -m "Auto-deploy: latest portal and landing pages to GitHub Pages"
git push origin main
echo.
echo [OK]     GitHub Pages!
echo [URL]       ...
start https://medon90ae.github.io/healing-touch-egypt/portal/
goto end

:opt6
echo.
echo [*]     Google Sheet   ...
".venv\Scripts\python.exe" antigravity_social_automation.py --check-sheet
start https://docs.google.com/spreadsheets/d/12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k/edit?gid=513215731#gid=513215731
goto end

:opt7
echo.
echo [*]      Reddit ...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode auth-reddit
goto end

:opt8
echo.
echo [*]        ...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode open-latest
goto end

:end
echo.
echo =====================================================================
echo   !
pause
