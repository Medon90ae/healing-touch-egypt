' =============================================================================
' 🌿 Healing Touch Egypt - Telegram Bot Silent Background Runner
' File: scripts/run_bot_silent.vbs
' Executes python scripts/telegram_control_bot.py completely hidden (WindowStyle 0)
' =============================================================================
Option Explicit

Dim fso, scriptDir, projectDir, WshShell, pythonExe, botScript, runCmd

Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
projectDir = fso.GetParentFolderName(scriptDir)

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = projectDir

pythonExe = projectDir & "\.venv\Scripts\python.exe"
botScript = projectDir & "\scripts\telegram_control_bot.py"

If Not fso.FileExists(pythonExe) Then
    WScript.Echo "ERROR: Python virtualenv not found: " & pythonExe
    WScript.Quit 1
End If

If Not fso.FileExists(botScript) Then
    WScript.Echo "ERROR: Telegram bot script not found: " & botScript
    WScript.Quit 1
End If

runCmd = """" & pythonExe & """ """ & botScript & """"
WshShell.Run runCmd, 0, False
