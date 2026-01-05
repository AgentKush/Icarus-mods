@echo off
REM Script to copy EXMODZ mod files to GitHub folder
REM Run this from the folder where you downloaded the EXMODZ files (likely Downloads)

echo Copying EXMODZ mod files to GitHub folder...

if exist "Agents_Items.EXMODZ" (
    copy /Y "Agents_Items.EXMODZ" "C:\Users\finla\Documents\GitHub\Icarus-mods\Agents_Items\"
    echo Copied Agents_Items.EXMODZ
) else (
    echo WARNING: Agents_Items.EXMODZ not found!
)

if exist "Agents_BioLab.EXMODZ" (
    copy /Y "Agents_BioLab.EXMODZ" "C:\Users\finla\Documents\GitHub\Icarus-mods\Agents_BioLab\"
    echo Copied Agents_BioLab.EXMODZ
) else (
    echo WARNING: Agents_BioLab.EXMODZ not found!
)

if exist "FastProcessing_All_10x.EXMODZ" (
    copy /Y "FastProcessing_All_10x.EXMODZ" "C:\Users\finla\Documents\GitHub\Icarus-mods\FastProcessing_All_10x\"
    echo Copied FastProcessing_All_10x.EXMODZ
) else (
    echo WARNING: FastProcessing_All_10x.EXMODZ not found!
)

if exist "Indestructible_Tools_Weapons.EXMODZ" (
    copy /Y "Indestructible_Tools_Weapons.EXMODZ" "C:\Users\finla\Documents\GitHub\Icarus-mods\Indestructible_Tools_Weapons\"
    echo Copied Indestructible_Tools_Weapons.EXMODZ
) else (
    echo WARNING: Indestructible_Tools_Weapons.EXMODZ not found!
)

if exist "No_Food_Spoilage.EXMODZ" (
    copy /Y "No_Food_Spoilage.EXMODZ" "C:\Users\finla\Documents\GitHub\Icarus-mods\No_Food_Spoilage\"
    echo Copied No_Food_Spoilage.EXMODZ
) else (
    echo WARNING: No_Food_Spoilage.EXMODZ not found!
)

echo.
echo Done! All EXMODZ mod files copied to GitHub folder.
echo.
echo Next steps - commit and push to GitHub:
echo   cd C:\Users\finla\Documents\GitHub\Icarus-mods
echo   git add .
echo   git commit -m "Added all AgentKush mods with EXMODZ files"
echo   git push
echo.
pause
