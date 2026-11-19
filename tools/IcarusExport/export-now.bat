@echo off
rem Exports Icarus now: only what changed since the last export is written.
rem Options are passed on, for example:  export-now.bat --full
setlocal
set "EXE=%~dp0publish\IcarusExport.exe"
if not exist "%EXE%" (
  echo Building IcarusExport first...
  call "%~dp0build.bat"
  if errorlevel 1 goto failed
)
"%EXE%" %*
set "CODE=%ERRORLEVEL%"
echo.
if not "%CODE%"=="0" echo IcarusExport stopped with exit code %CODE%. The log is in "<export folder>\Logs\IcarusExport".
pause
exit /b %CODE%

:failed
echo The build failed. Is the .NET 10 SDK installed?
pause
exit /b 1
