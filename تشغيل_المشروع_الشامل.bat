@echo off
chcp 1256 >nul
cd /d "C:\followUPSHEET\healing_touch"
cls
echo =====================================================================
echo         ÂÌ·Ì‰Ã  « ‘ „’— - ·ÊÕ… «· Õﬂ„ Ê«·„Õ—ﬂ «·„ÊÕœ «·‘«„·
echo =====================================================================
echo.
echo   [1] «· ‘€Ì· «·‘«„· Ê«·‰‘— «·›Ê—Ì («·„Êﬁ⁄ + ﬂ«‰›« + ›ÌœÌÊ + ›Ì”»Êﬂ)
echo   [2] „⁄«Ì‰… Ê ÃÂÌ“ «·„Õ ÊÏ Ê«· ’„Ì„ Ê«·›ÌœÌÊ (»œÊ‰ ‰‘— - Dry Run)
echo   [3]  ÕœÌÀ Ê‰‘— „ﬁ«·«  Ê„Õ ÊÏ «·„Êﬁ⁄ «·”—Ì—Ì (Zero-Commerce)
echo   [4]  ÕœÌÀ Õ“„… Google NotebookLM Êœ„Ã «·’Ê Ì« 
echo   [5]  ‘€Ì· —«œ«— Ã—Ê»«  ›Ì”»Êﬂ ›ﬁÿ
echo   [6] —»ÿ Ê ›⁄Ì· Õ”«» Reddit  ·ﬁ«∆Ì« (·„—… Ê«Õœ… ›ﬁÿ)
echo.
echo =====================================================================
set /p choice="«Œ — —ﬁ„ «·⁄„·Ì… «·„ÿ·Ê»… («÷€ÿ Enter ·«Œ Ì«— 1 «› —«÷Ì«): "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    echo.
    echo [1/2] Ã«—Ì  ÕœÌÀ «·„Êﬁ⁄ Ê«·„ﬁ«·«  «·”—Ì—Ì… «·„⁄ „œ…...
    ".venv\Scripts\python.exe" github_seo_trend_engine.py --build-site --push-github
    echo.
    echo [2/2] Ã«—Ì  ‘€Ì· «” ÊœÌÊ «· ’„Ì„ Ê«·›ÌœÌÊ Ê«·‰‘— «·‘«„·...
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
echo «ﬂ „·  «·⁄„·Ì… »‰Ã«Õ!
pause