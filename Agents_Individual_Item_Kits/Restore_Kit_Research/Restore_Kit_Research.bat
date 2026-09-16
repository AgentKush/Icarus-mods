@echo off
rem Restore Kit Research - Agents Individual Item Kits (Icarus). Made by AgentKush.
rem Double-click to run. Any arguments are passed to Restore_Kit_Research.ps1.
setlocal
set "RKR_NOPAUSE="
for %%A in (%*) do if /I "%%~A"=="-NoPause" set "RKR_NOPAUSE=1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Restore_Kit_Research.ps1" %*
set "RKR_EXIT=%ERRORLEVEL%"
if not defined RKR_NOPAUSE pause
exit /b %RKR_EXIT%
