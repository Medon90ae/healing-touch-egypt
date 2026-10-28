' =============================================================================
' 🌿 Healing Touch Egypt - n8n Silent Background Runner
' File: scripts/run_n8n_silent.vbs
' Executes npx n8n start with WindowStyle 0 (completely hidden)
' =============================================================================
Option Explicit

Dim fso, scriptDir, projectDir, WshShell, env, currentPath, runCmd

Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
projectDir = fso.GetParentFolderName(scriptDir)

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = projectDir

Set env = WshShell.Environment("PROCESS")

' Ensure Node.js and npm paths are available in PATH
currentPath = env("PATH")
If InStr(1, currentPath, "C:\Program Files\nodejs", vbTextCompare) = 0 Then
    env("PATH") = currentPath & ";C:\Program Files\nodejs;C:\Users\moga\AppData\Roaming\npm"
End If

' Configure n8n environment variables
env("N8N_PORT") = "5678"
env("N8N_LISTEN_ADDRESS") = "0.0.0.0"
env("GENERIC_TIMEZONE") = "Africa/Cairo"
env("N8N_DEFAULT_BINARY_DATA_MODE") = "filesystem"
env("EXECUTIONS_DATA_PRUNE") = "true"
env("EXECUTIONS_DATA_MAX_AGE") = "168"
env("N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS") = "true"
env("N8N_DIAGNOSTICS_ENABLED") = "false"
env("N8N_VERSION_NOTIFICATIONS_ENABLED") = "false"
env("N8N_RUNNERS_ENABLED") = "false"

' Execute npx n8n start hidden (WindowStyle = 0, WaitOnReturn = False)
runCmd = "cmd.exe /d /s /c npx --prefer-offline --yes n8n start"
WshShell.Run runCmd, 0, False
