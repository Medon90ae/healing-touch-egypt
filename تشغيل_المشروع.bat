@echo off
chcp 1256 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo         ÂÌ·Ì‰Ã  « ‘ „’— - ·ÊÕ… «· Õﬂ„ Ê«·„Õ—ﬂ «·„ÊÕœ «·‘«„· (2026)
echo =====================================================================
echo.
echo   [1] «· ‘€Ì· «·‘«„· Ê«·‰‘— «·›Ê—Ì (»‰«¡ «··«‰œ‰Ã »ÌœÃ + ‰‘— ﬂ· «·„‰’« )
echo   [2]  ÃÂÌ“ Õ„·… «·ÌÊ„ Ê«·»—Ê„» «  Ê„’«œ— «·»ÕÀ (Pomelli + Stitch + AI)
echo   [3] „⁄«Ì‰… Ê ÃÂÌ“ «·√’Ê· Ê«··«‰œ‰Ã »ÌœÃ »œÊ‰ ‰‘— (Dry Run)
echo   [4] › Õ ’‰œÊﬁ «·«” ﬁ»«· manual_inbox Ê„·› «·»—Ê„» «  «·Ã«Â“… ··‰”Œ
echo   [5]  ÕœÌÀ √”⁄«— Ê„ﬁ«·«  «·„Êﬁ⁄ „‰ Google Sheet Ê«·—›⁄ ·‹ GitHub
echo   [6] «” ⁄—«÷ Ê›Õ’ ”Ã· «·⁄„·«¡ ÊÕÃÊ“«  «·«” ‘«—«  ›Ì Google Sheet
echo   [7] —»ÿ Ê ›⁄Ì· Õ”«» Reddit  ·ﬁ«∆Ì« (·„—… Ê«Õœ… ›ﬁÿ)
echo   [8] › Õ √ÕœÀ „‰‘Ê—  „ ‰‘—Â ⁄·Ï ›Ì”»Êﬂ ›Ì «·„ ’›Õ
echo.
echo =====================================================================
set choice=1
set /p choice="«Œ — —ﬁ„ «·⁄„·Ì… «·„ÿ·Ê»… («÷€ÿ Enter ·«Œ Ì«— 1 «› —«÷Ì«): "

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
echo [*] [1/2] Ã«—Ì „“«„‰… «·√”⁄«— Ê ÕœÌÀ «·„Êﬁ⁄ «·√”«”Ì...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site
echo.
echo [*] [2/2] Ã«—Ì »‰«¡ «··«‰œ‰Ã »ÌœÃ Ê«· ﬁ«ÿ √’Ê· manual_inbox Ê«·‰‘— «·‘«„·...
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
echo [*] Ã«—Ì „“«„‰… «·√”⁄«— «·ÕÌ… Ê„ﬁ«·«  «·”ÌÊ „‰ Google Sheet Ê«·—›⁄ ·‹ GitHub...
".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site --push-github
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
