@echo off
REM Script to copy mod files to GitHub folder
REM Run this from the folder where you downloaded the EXMOD files (likely Downloads)

echo Copying mod files to GitHub folder...

if exist "Agents_Items.EXMOD" (
    copy /Y "Agents_Items.EXMOD" "C:\Users\finla\Documents\GitHub\Icarus-mods\Agents_Items\"
    echo Copied Agents_Items.EXMOD
)

if exist "FastProcessing_All_10x.EXMOD" (
    copy /Y "FastProcessing_All_10x.EXMOD" "C:\Users\finla\Documents\GitHub\Icarus-mods\FastProcessing_All_10x\"
    echo Copied FastProcessing_All_10x.EXMOD
)

if exist "Indestructible_Tools_Weapons.EXMOD" (
    copy /Y "Indestructible_Tools_Weapons.EXMOD" "C:\Users\finla\Documents\GitHub\Icarus-mods\Indestructible_Tools_Weapons\"
    echo Copied Indestructible_Tools_Weapons.EXMOD
)

if exist "No_Food_Spoilage.EXMOD" (
    copy /Y "No_Food_Spoilage.EXMOD" "C:\Users\finla\Documents\GitHub\Icarus-mods\No_Food_Spoilage\"
    echo Copied No_Food_Spoilage.EXMOD
)

if exist "Agents_BioLab.EXMOD" (
    copy /Y "Agents_BioLab.EXMOD" "C:\Users\finla\Documents\GitHub\Icarus-mods\Agents_BioLab\"
    echo Copied Agents_BioLab.EXMOD
)

echo.
echo Done! All mod files copied to GitHub folder.
echo.
echo You can now commit and push to GitHub:
echo   cd C:\Users\finla\Documents\GitHub\Icarus-mods
echo   git add .
echo   git commit -m "Added all AgentKush mods"
echo   git push
echo.
pause
