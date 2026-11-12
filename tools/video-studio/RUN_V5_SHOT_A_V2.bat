@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM SOVTIVA V5 Shot A V2: no subscriptions, cloud GPUs or credits.
REM Automatically locate the installed official Blender version on Windows.
set "BLENDER_EXE="
for %%V in (5.3 5.2 5.4 5.5 5.1) do (
  if not defined BLENDER_EXE if exist "%ProgramFiles%\Blender Foundation\Blender %%V\blender.exe" (
    set "BLENDER_EXE=%ProgramFiles%\Blender Foundation\Blender %%V\blender.exe"
  )
)
if not defined BLENDER_EXE (
  for /d %%G in ("%ProgramFiles%\Blender Foundation\Blender *") do (
    if not defined BLENDER_EXE if exist "%%~fG\blender.exe" set "BLENDER_EXE=%%~fG\blender.exe"
  )
)
if not defined BLENDER_EXE (
  for /f "delims=" %%G in ('where blender.exe 2^>nul') do (
    if not defined BLENDER_EXE set "BLENDER_EXE=%%G"
  )
)
if not defined BLENDER_EXE (
  echo [ERROR] Blender.exe was not found. Blender is not being reinstalled.
  echo If it is installed elsewhere, send the output of: where /r "C:\Program Files" blender.exe
  pause
  exit /b 2
)

echo.
echo ======================================================
echo  SOVTIVA V5 - Cinematic Shot A V2 - 3 second preview
 echo  Blender: %BLENDER_EXE%
echo  Cost: $0 - no account or internet usage
 echo ======================================================
echo.
echo First rendering a native 1080x1920 still and then a
 echo  72-frame low-resolution playable MP4. May take a while.
echo  The BAT window will remain open if an error occurs.
echo.
"%BLENDER_EXE%" -b -t 4 --python "%~dp0shot_A_v2_blender.py" -- --mode preview --out "%~dp0V5_A_V2_output"
set "EXITCODE=%ERRORLEVEL%"
echo.
if not "%EXITCODE%"=="0" (
  echo [FAILED] Blender exited with error %EXITCODE%.
  echo Please send the last lines of this window or any benchmark.json created.
) else (
  echo [DONE] Open V5_A_V2_output next to this BAT file.
  echo Upload the preview MP4, the STILL PNG and benchmark.json.
  echo If there is no MP4, check PNG_frames_if_MP4_fails.
)
echo.
pause
exit /b %EXITCODE%
