@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
set "HERE=%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" (
 for /f "delims=" %%P in ('where /r "C:\Program Files\Blender Foundation" blender.exe 2^>nul') do if not exist "%BLENDER%" set "BLENDER=%%P"
)
if not exist "%BLENDER%" (echo Blender 5.3 not found&pause&exit /b 1)
if not exist "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" (echo Missing source .blend file. Extract the ZIP fully.&pause&exit /b 1)
set "OUT=%HERE%V5_FIRST_FILM_OUTPUT"
if not exist "%OUT%" mkdir "%OUT%"
echo =========================================================
echo SOVTIVA - FIRST COMPLETE FILM - A-F STORYBOARD 3D
 echo Blender 5.3 / Cycles CPU ONLY. No paid service.
echo Rendering five 3D story stills from shots B, C, D, E, F.
echo Existing approved Shot A remains preserved.
echo LIVE PROGRESS WILL APPEAR BELOW.
echo =========================================================
"%BLENDER%" --disable-autoexec -b "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" -t 4 --python "%HERE%build_v5_scenes_B_F.py" -- --out "%OUT%" --mode stills --pct 35 --samples 8
set "RC=%ERRORLEVEL%"
echo Blender returned exit code %RC%.
if exist "%HERE%UPLOAD_V5_FIRST_FILM_STORYBOARD.zip" del /q "%HERE%UPLOAD_V5_FIRST_FILM_STORYBOARD.zip"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%OUT%\benchmark.json','%OUT%\storyboard\*' -DestinationPath '%HERE%UPLOAD_V5_FIRST_FILM_STORYBOARD.zip' -Force"
if exist "%HERE%UPLOAD_V5_FIRST_FILM_STORYBOARD.zip" (echo READY - Upload UPLOAD_V5_FIRST_FILM_STORYBOARD.zip) else (echo ZIP error - Upload output storyboards as images)
echo. 
echo This is internal storyboard QA, not a publicly ready social video.
pause
endlocal
