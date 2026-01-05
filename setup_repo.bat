@echo off
REM Cleanup and setup script for Icarus-mods repository
REM 1. First download the 3 EXMODZ files from Claude to your Downloads folder
REM 2. Then run this script from your Downloads folder

echo ========================================
echo  Icarus-mods Repository Setup Script
echo ========================================
echo.

set REPO=C:\Users\finla\Documents\GitHub\Icarus-mods

REM Copy EXMODZ files to correct folders
echo Copying EXMODZ files to mod folders...

if exist "Agents_BioLab.EXMODZ" (
    copy /Y "Agents_BioLab.EXMODZ" "%REPO%\Agents_BioLab\"
    echo   [OK] Agents_BioLab.EXMODZ
) else (
    echo   [SKIP] Agents_BioLab.EXMODZ not found
)

if exist "Indestructible_Tools_Weapons.EXMODZ" (
    copy /Y "Indestructible_Tools_Weapons.EXMODZ" "%REPO%\Indestructible_Tools_Weapons\"
    echo   [OK] Indestructible_Tools_Weapons.EXMODZ
) else (
    echo   [SKIP] Indestructible_Tools_Weapons.EXMODZ not found
)

if exist "No_Food_Spoilage.EXMODZ" (
    copy /Y "No_Food_Spoilage.EXMODZ" "%REPO%\No_Food_Spoilage\"
    echo   [OK] No_Food_Spoilage.EXMODZ
) else (
    echo   [SKIP] No_Food_Spoilage.EXMODZ not found
)

echo.
echo Cleaning up old files...

REM Remove empty "Extracted Mods" folders
rmdir /s /q "%REPO%\Agents_BioLab\Extracted Mods" 2>nul
rmdir /s /q "%REPO%\Agents_Items\Extracted Mods" 2>nul
rmdir /s /q "%REPO%\FastProcessing_All_10x\Extracted Mods" 2>nul
rmdir /s /q "%REPO%\Indestructible_Tools_Weapons\Extracted Mods" 2>nul
rmdir /s /q "%REPO%\No_Food_Spoilage\Extracted Mods" 2>nul
echo   [OK] Removed empty Extracted Mods folders

REM Remove old .EXMOD files
del /q "%REPO%\Agents_BioLab\Agents_BioLab.EXMOD" 2>nul
del /q "%REPO%\Indestructible_Tools_Weapons\Indestructible_Tools_Weapons.EXMOD" 2>nul
del /q "%REPO%\No_Food_Spoilage\No_Food_Spoilage.EXMOD" 2>nul
echo   [OK] Removed old .EXMOD files

REM Remove old scripts
del /q "%REPO%\copy_mods.bat" 2>nul
del /q "%REPO%\cleanup.bat" 2>nul
echo   [OK] Removed old scripts

echo.
echo ========================================
echo  Setup complete! Final repository:
echo ========================================
echo.
echo  Icarus-mods/
echo  +-- modinfo.json
echo  +-- README.md
echo  +-- .gitignore
echo  +-- Agents_Items/
echo  ^|   +-- Agents_Items.EXMODZ
echo  ^|   +-- README.md
echo  +-- Agents_BioLab/
echo  ^|   +-- Agents_BioLab.EXMODZ
echo  ^|   +-- README.md
echo  +-- FastProcessing_All_10x/
echo  ^|   +-- FastProcessing_All_10x.EXMODZ
echo  ^|   +-- README.md
echo  +-- Indestructible_Tools_Weapons/
echo  ^|   +-- Indestructible_Tools_Weapons.EXMODZ
echo  ^|   +-- README.md
echo  +-- No_Food_Spoilage/
echo      +-- No_Food_Spoilage.EXMODZ
echo      +-- README.md
echo.
echo ========================================
echo  Now commit and push to GitHub:
echo ========================================
echo.
echo   cd %REPO%
echo   git add .
echo   git commit -m "Reorganized repository with EXMODZ files"
echo   git push
echo.
pause
