@echo off
chcp 1256 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo         ÂÌ·Ì‰Ã  « ‘ „’— - ·ÊÕ… «· Õﬂ„ Ê«·„Õ—ﬂ «·„ÊÕœ «·‘«„· (2026)
echo =====================================================================
echo.
echo   [1] «· ‘€Ì· «·‘«„· Ê«·‰‘— «·›Ê—Ì (»‰«¡ «·„Êﬁ⁄ + «·»Ê«»… + «·‰‘— ·‹ GitHub + «·”Ê‘Ì«·)
echo   [2]  ÃÂÌ“ Õ„·… «·ÌÊ„ Ê«·»—Ê„» «  Ê„’«œ— «·»ÕÀ (Pomelli + Stitch + AI)
echo   [3] „⁄«Ì‰… Ê ÃÂÌ“ «·√’Ê· Ê«··«‰œ‰Ã »ÌœÃ »œÊ‰ ‰‘— (Dry Run)
echo   [4] › Õ ’‰œÊﬁ «·«” ﬁ»«· manual_inbox Ê„·› «·»—Ê„» «  «·Ã«Â“… ··‰”Œ
echo   [5]  ÕœÌÀ «·„Êﬁ⁄ Ê ÿ»Ìﬁ «·»Ê«»… Ê‰‘— «· €ÌÌ—«  „»«‘—… ≈·Ï GitHub Pages
echo   [6] «” ⁄—«÷ Ê›Õ’ ”Ã· «·⁄„·«¡ ÊÕÃÊ“«  «·«” ‘«—«  ›Ì Google Sheet
echo   [7] —»ÿ Ê ›⁄Ì· Õ”«» Reddit  ·ﬁ«∆Ì« (·„—… Ê«Õœ… ›ﬁÿ)
echo   [8] › Õ √ÕœÀ „‰‘Ê—  „ ‰‘—Â ⁄·Ï ›Ì”»Êﬂ ›Ì «·„ ’›Õ
echo.
echo =====================================================================
set choice=5
set /p choice="«Œ — —ﬁ„ «·⁄„·Ì… «·„ÿ·Ê»… («÷€ÿ Enter ·«Œ Ì«— 5 «› —«÷Ì« · ÕœÌÀ Ê‰‘— «·„Êﬁ⁄): "

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
echo [*] [1/4] Ã«—Ì „“«„‰… «·√”⁄«— Ê ÕœÌÀ ’›Õ«  Ê„ﬁ«·«  «·„Êﬁ⁄ «·√”«”Ì...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/4] Ã«—Ì »‰«¡ Ê ÕœÌÀ  ÿ»Ìﬁ «·»Ê«»… «·”—Ì—Ì… «· ›«⁄·Ì… (Stitch AI Portal)...
call npm --prefix "media_assets\manual_inbox\stitch_ai_studio_app" run build
xcopy /E /Y /I "media_assets\manual_inbox\stitch_ai_studio_app\dist\*" "docs\portal\"
echo.
echo [*] [3/4] Ã«—Ì —›⁄ Ê‰‘— √ÕœÀ ﬂÊœ Ê ’„Ì„«  ≈·Ï GitHub Pages  ·ﬁ«∆Ì«...
git add docs/ media_assets/manual_inbox/stitch_ai_studio_app/ campaign_landing_engine.py github_seo_trend_engine.py products_registry.json promo_config.json PROJECT.md run_project.bat .gitignore
git commit -m "Auto-deploy: full clinical portal and site sync"
git push origin main
echo.
echo [*] [4/4] Ã«—Ì »‰«¡ «··«‰œ‰Ã »ÌœÃ Ê«· ﬁ«ÿ √’Ê· manual_inbox Ê«·‰‘— «·‘«„·...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode all
goto end

:opt2
echo.
echo [*] Ã«—Ì ≈⁄œ«œ Ê ÕœÌÀ Õ“„… «·»—Ê„» «  Ê«·„’«œ— (Pomelli + Stitch + Deep Research + NotebookLM)...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode notebooklm
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt3
echo.
echo [*] Ã«—Ì  ‘€Ì· Ê÷⁄ «·„⁄«Ì‰… Ê Ê·Ìœ «··«‰œ‰Ã »ÌœÃ Ê«· ’«„Ì„ Ê«·›ÌœÌÊ »œÊ‰ ‰‘—...
".venv\Scripts\python.exe" antigravity_social_automation.py --dry-run
goto end

:opt4
echo.
echo [*] Ã«—Ì › Õ ’‰œÊﬁ «·«” ﬁ»«· manual_inbox Ê„·› «·»—Ê„» « ...
explorer "media_assets\manual_inbox"
if exist "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt" (
    start notepad "media_assets\manual_inbox\PROMPTS_PACK_TODAY.txt"
)
goto end

:opt5
echo.
echo [*] [1/3] Ã«—Ì „“«„‰… «·√”⁄«— «·ÕÌ… Ê„ﬁ«·«  «·”ÌÊ „‰ Google Sheet...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/3] Ã«—Ì »‰«¡ Ê Ã„Ì⁄  ÿ»Ìﬁ «·»Ê«»… «· ›«⁄·Ì… (Stitch AI Studio)...
call npm --prefix "media_assets\manual_inbox\stitch_ai_studio_app" run build
xcopy /E /Y /I "media_assets\manual_inbox\stitch_ai_studio_app\dist\*" "docs\portal\"
echo.
echo [*] [3/3] Ã«—Ì «·—›⁄ Ê«·‰‘— «·„»«‘— ≈·Ï GitHub Pages...
git add docs/ media_assets/manual_inbox/stitch_ai_studio_app/ campaign_landing_engine.py github_seo_trend_engine.py products_registry.json promo_config.json PROJECT.md run_project.bat .gitignore
git commit -m "Auto-deploy: latest portal and landing pages to GitHub Pages"
git push origin main
echo.
echo [OK]  „ «·‰‘— »‰Ã«Õ ⁄·Ï GitHub Pages!
echo [URL] Ã«—Ì › Õ —«»ÿ «·»Ê«»… «·ÕÌ… ›Ì «·„ ’›Õ...
start https://medon90ae.github.io/healing-touch-egypt/portal/
goto end

:opt6
echo.
echo [*] Ã«—Ì ›Õ’ «·« ’«· »ÃœÊ· Google Sheet Ê› Õ ”Ã· «·«” ‘«—« ...
".venv\Scripts\python.exe" antigravity_social_automation.py --check-sheet
start https://docs.google.com/spreadsheets/d/12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k/edit?gid=513215731#gid=513215731
goto end

:opt7
echo.
echo [*] Ã«—Ì »œ¡  ›ÊÌ÷ Ê—»ÿ Õ”«» Reddit «·œ«∆„...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode auth-reddit
goto end

:opt8
echo.
echo [*] Ã«—Ì › Õ √ÕœÀ „‰‘Ê—  „ ‰‘—Â ⁄·Ï ›Ì”»Êﬂ...
".venv\Scripts\python.exe" antigravity_social_automation.py --mode open-latest
goto end

:end
echo.
echo =====================================================================
echo «ﬂ „·  «·⁄„·Ì… »‰Ã«Õ!
pause
