@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "HERE=%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" (
 for /f "delims=" %%P in ('where /r "C:\Program Files\Blender Foundation" blender.exe 2^>nul') do if not exist "%BLENDER%" set "BLENDER=%%P"
)
if not exist "%BLENDER%" (
 echo ERROR: Blender executable was not found. No reinstall needed yet.
 echo Please screenshot this window and send it to ChatGPT.
 pause
 exit /b 1
)
if not exist "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" (
 echo ERROR: The original scene file is missing from this folder.
 pause
 exit /b 1
)
if not exist "%HERE%blender_probe.py" (
 echo ERROR: blender_probe.py is missing from this folder.
 pause
 exit /b 1
)
echo.
echo SOVTIVA V5 free GPU diagnostic -- NO SUBSCRIPTIONS OR PURCHASES
echo Blender: "%BLENDER%"
echo Testing problematic frames using the OpenGL GPU backend.
echo This does not modify your previous render, .blend source, or installed Blender settings.
echo.
if not exist "%HERE%DIAG_OPENGL" mkdir "%HERE%DIAG_OPENGL"
"%BLENDER%" --gpu-backend opengl -b "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" -t 4 --python "%HERE%blender_probe.py" -- --engine eevee --samples 8 --out "%HERE%DIAG_OPENGL" > "%HERE%DIAG_OPENGL\console.log" 2>&1
set "OPENGL_EXIT=%ERRORLEVEL%"
echo OpenGL process return code: %OPENGL_EXIT%
echo.
echo Running ONE low-resolution Cycles CPU reference frame. This can take longer.
echo If this stage crashes, the OpenGL result is still preserved.
if not exist "%HERE%DIAG_CPU" mkdir "%HERE%DIAG_CPU"
"%BLENDER%" -b "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" -t 4 --python "%HERE%blender_probe.py" -- --engine cycles --samples 8 --out "%HERE%DIAG_CPU" > "%HERE%DIAG_CPU\console.log" 2>&1
set "CPU_EXIT=%ERRORLEVEL%"
echo CPU process return code: %CPU_EXIT%
echo.
(
 echo SOVTIVA V5 Diagnostic
 echo Blender: %BLENDER%
 echo OpenGL return code: %OPENGL_EXIT%
 echo Cycles CPU return code: %CPU_EXIT%
 echo The actual images must be inspected to assess GPU stability.
 echo No purchase or subscription used.
) > "%HERE%DIAGNOSTIC_STATUS.txt"
if exist "%HERE%UPLOAD_V5_GPU_DIAGNOSTIC.zip" del /q "%HERE%UPLOAD_V5_GPU_DIAGNOSTIC.zip" >nul 2>&1
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%HERE%DIAG_OPENGL','%HERE%DIAG_CPU','%HERE%DIAGNOSTIC_STATUS.txt' -DestinationPath '%HERE%UPLOAD_V5_GPU_DIAGNOSTIC.zip' -Force"
echo.
echo ==============================================================
echo Please upload UPLOAD_V5_GPU_DIAGNOSTIC.zip to ChatGPT.
echo It includes rendered test frames, timings and console logs.
echo If the ZIP is missing, upload the DIAG_OPENGL and DIAG_CPU benchmark files.
echo ==============================================================
pause
endlocal
