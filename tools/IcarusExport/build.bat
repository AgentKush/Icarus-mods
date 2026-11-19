@echo off
rem Builds IcarusExport into the publish folder (needs the .NET 10 SDK).
dotnet publish "%~dp0IcarusExport.csproj" -c Release -o "%~dp0publish" --nologo
