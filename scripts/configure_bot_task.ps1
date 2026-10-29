# =============================================================================
# 🌿 Healing Touch Egypt - Scheduled Task Advanced Configuration
# =============================================================================
$TaskName = "HealingTouch_TelegramBot_Service"
$BaseDir = "C:\followUPSHEET\healing_touch"
$PythonExe = "$BaseDir\.venv\Scripts\pythonw.exe"
$BotScript = "$BaseDir\scripts\telegram_control_bot.py"

Write-Host "[*] Configuring Scheduled Task: $TaskName"

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$BotScript`"" -WorkingDirectory $BaseDir
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Days 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force | Out-Null

Write-Host "[+] Successfully registered and hardened Scheduled Task: $TaskName"
