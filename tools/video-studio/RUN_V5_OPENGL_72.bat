@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "HERE=%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" (
 for /f "delims=" %%P in ('where /r "C:\Program Files\Blender Foundation" blender.exe 2^>nul') do if not exist "%BLENDER%" set "BLENDER=%%P"
)
if not exist "%BLENDER%" (
 echo ERROR: Blender not found. Upload a screenshot. No reinstall needed yet.
 pause
 exit /b 1
)
if not exist "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" (
 echo ERROR: .blend project missing from extracted folder.
 pause
 exit /b 1
)
if not exist "%HERE%render_v5_opengl_72.py" (
 echo ERROR: renderer script missing from extracted folder.
 pause
 exit /b 1
)
set "OUTPUT=%HERE%V5_OPENGL_72_output"
if not exist "%OUTPUT%" mkdir "%OUTPUT%"
echo SOVTIVA V5 / 72 OpenGL-frame recovery test. Zero cost.
echo Blender: %BLENDER%
echo This test uses an isolated OpenGL launch and never overwrites your existing render.
echo Source: user's own .blend file. Duration: 3 seconds at 24 frames/sec.
echo.
"%BLENDER%" --gpu-backend opengl -b "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" -t 4 --python "%HERE%render_v5_opengl_72.py" -- --out "%OUTPUT%" --first 1 --last 72 --pct 55 > "%OUTPUT%\blender_console.log" 2>&1
set "RETURN_CODE=%ERRORLEVEL%"
echo Blender process return code: %RETURN_CODE%
if not "%RETURN_CODE%"=="0" echo RENDER FAILED: See V5_OPENGL_72_outputlender_console.log
if not exist "%OUTPUT%\frames\V5A_OpenGL_0072.png" echo WARNING: Final PNG missing.

rem A browser player shows the PNG sequence without extra video software.
if exist "%OUTPUT%\frames\V5A_OpenGL_0072.png" copy /Y "%HERE%OPEN_PREVIEW_IN_BROWSER.html" "%OUTPUT%\OPEN_PREVIEW_IN_BROWSER.html" >nul

rem Ship original PNGs and QA log for an independent quality check in ChatGPT.
if exist "%HERE%UPLOAD_V5_OPENGL_72.zip" del /q "%HERE%UPLOAD_V5_OPENGL_72.zip" >nul 2>&1
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%OUTPUT%\*' -DestinationPath '%HERE%UPLOAD_V5_OPENGL_72.zip' -Force" 
if exist "%HERE%UPLOAD_V5_OPENGL_72.zip" (
 echo.
 echo Finished packaging: UPLOAD_V5_OPENGL_72.zip
 echo Please upload that ZIP to ChatGPT. It contains original PNG frames and benchmark.
) else (
 echo Packaging failed: upload V5_OPENGL_72_output folder or screenshot.
)
echo No purchase, credits or additional software used.
pause
endlocal
