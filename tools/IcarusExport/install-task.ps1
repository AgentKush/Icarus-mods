<#
.SYNOPSIS
    Registers (or removes) the "Icarus Export" scheduled task.

.DESCRIPTION
    The task runs publish\IcarusExportBackground.exe --scheduled at logon and every few hours.
    Each run reads Icarus's Steam manifest and exits straight away unless Steam has finished
    installing a build that has not been exported yet. It also waits while the game is running.
    After an export it shows a Windows notification with a one-line summary of what changed.
    The background exe has no window, so nothing pops up over the game.

.EXAMPLE
    .\install-task.ps1
.EXAMPLE
    .\install-task.ps1 -ExportRoot 'E:\Icarus Export' -Hours 6
.EXAMPLE
    .\install-task.ps1 -Remove
#>
param(
    [string]$ExportRoot = 'D:\Fmod Exports for Icarus',
    [ValidateRange(1, 24)][int]$Hours = 3,
    [switch]$Remove
)
$ErrorActionPreference = 'Stop'
$name = 'Icarus Export'

if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false
    "Removed the '$name' task."
    return
}

$exe = Join-Path $PSScriptRoot 'publish\IcarusExportBackground.exe'
if (-not (Test-Path $exe)) { throw "Build first: run build.bat, which creates $exe" }

$user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
# A trailing backslash would escape the closing quote ("D:\Export\" -> D:\Export"), so drop it; a drive root
# keeps a dot instead ("E:\.") because "E:" alone means the current folder on that drive.
$out = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ExportRoot).TrimEnd('\')
if ($out -match '^[A-Za-z]:$') { $out += '\.' }
$action = New-ScheduledTaskAction -Execute $exe -Argument "--scheduled --out `"$out`"" -WorkingDirectory (Split-Path $exe)
$atLogon = New-ScheduledTaskTrigger -AtLogOn -User $user
$atLogon.Delay = 'PT10M'   # let Steam start, and finish any update, first
$repeat = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Hours $Hours)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 6)
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $name -Action $action -Trigger $atLogon, $repeat -Settings $settings -Principal $principal -Force `
    -Description "Exports Icarus's paks to $out after each Steam update (Icarus-mods\tools\IcarusExport). Checks every $Hours hours and at logon." |
    Out-Null
"Registered '$name': checks at logon and every $Hours hours, exports to $out."
