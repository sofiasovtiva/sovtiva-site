@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
set "HERE=%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" (
  for /f "delims=" %%P in ('where /r "C:\Program Files\Blender Foundation" blender.exe 2^>nul') do if not exist "%BLENDER%" set "BLENDER=%%P"
)
if not exist "%BLENDER%" (
  echo Blender not found. Please send the error, no reinstall needed yet.
  pause
  exit /b 1
)
if not exist "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" (
  echo ERROR: Original .blend scene is missing. Fully extract the kit.
  pause
  exit /b 1
)
if not exist "%HERE%render_v5_cycles_cpu.py" (
  echo ERROR: CPU render Python script is missing. Fully extract the kit.
  pause
  exit /b 1
)
set "OUT=%HERE%V5_CPU_72_output"
if not exist "%OUT%" mkdir "%OUT%"
echo ============================================================
echo SOVTIVA V5 Shot A - reliable Cycles CPU full preview
echo Blender: %BLENDER%
echo Engine: Cycles CPU only - NO GPU/OpenGL/Vulkan rendering
echo Original scene will not be overwritten. Cost: 0 USD.
echo ============================================================
echo.
"%BLENDER%" --disable-autoexec -b "%HERE%SOVTIVA_V5_SHOT_A_V21.blend" -t 4 --python "%HERE%render_v5_cycles_cpu.py" -- --out "%OUT%" --samples 12 --pct 55 > "%OUT%\blender_console.log" 2>&1
set "RETURN_CODE=%ERRORLEVEL%"
echo Blender exit code: %RETURN_CODE%
if not "%RETURN_CODE%"=="0" echo The CPU render stopped or failed: details in V5_CPU_72_output\blender_console.log
if exist "%OUT%\OPEN_PREVIEW_IN_BROWSER.html" (
  echo.
  echo Animation completed. Open V5_CPU_72_output\OPEN_PREVIEW_IN_BROWSER.html
)
if exist "%HERE%UPLOAD_V5_CPU_72.zip" (
  echo Replacing previous ZIP from this test only.
  del /q "%HERE%UPLOAD_V5_CPU_72.zip" >nul 2>&1
)
echo.
echo Packaging result for visual review...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%OUT%\*' -DestinationPath '%HERE%UPLOAD_V5_CPU_72.zip' -Force"
if exist "%HERE%UPLOAD_V5_CPU_72.zip" (
  echo.
  echo READY: UPLOAD_V5_CPU_72.zip
  echo Upload that ZIP to ChatGPT to inspect every frame and create MP4.
) else (
  echo Packaging failed. Upload benchmark.json and blender_console.log from the output folder.
)
echo This test uses no Runway credits, purchases or subscriptions.
pause
endlocal
