@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM SOVTIVA V5 SHOT A V2.1 - 100 percent free.
REM The Blender 5.3 Windows ARM build cannot export FFMPEG directly.
REM This launcher renders PNG frames and optionally converts them to MP4
REM ONLY if FFmpeg is already installed; otherwise it zips the frames.
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
  echo [ERROR] Blender.exe not found. Do not reinstall yet.
  echo Find your path with: where /r "C:\Program Files\Blender Foundation" blender.exe
  pause
  exit /b 2
)

set "OUTDIR=%~dp0V5_A_V21_output"
echo.
echo ========================================================
echo SOVTIVA V5 - SHOT A V2.1 - FIXED 3-SECOND ANIMATION
echo ========================================================
echo Blender: "%BLENDER_EXE%"
echo Renders 1 native 1080x1920 still + 72 preview PNG frames.
echo Cost: $0. No purchases, subscriptions or logins.
echo.
"%BLENDER_EXE%" -b -t 4 --python "%~dp0shot_A_v21_blender.py" -- --mode preview --out "%OUTDIR%"
if errorlevel 1 goto BLENDER_FAILED

if not exist "%OUTDIR%\preview_frames\Shot_A_V21_0072.png" goto MISSING_FRAMES

REM Windows free optional: if an FFmpeg binary exists, produce an MP4.
REM No additional software will be downloaded or installed.
where ffmpeg.exe >nul 2>&1
if errorlevel 1 goto NO_FFMPEG

echo.
echo [EXPORT] Existing FFmpeg detected. Encoding preview MP4...
ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 1 -i "%OUTDIR%\preview_frames\Shot_A_V21_%%04d.png" -frames:v 72 -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -movflags +faststart "%OUTDIR%\SOVTIVA_V5_SHOT_A_V21_preview.mp4"
if exist "%OUTDIR%\SOVTIVA_V5_SHOT_A_V21_preview.mp4" echo [OK] MP4 created.
if not exist "%OUTDIR%\SOVTIVA_V5_SHOT_A_V21_preview.mp4" echo [NOTE] MP4 encoder unavailable. Browser preview and frame ZIP remain available.
goto MAKE_ZIP

:NO_FFMPEG
echo.
echo [NOTE] FFmpeg is not installed, so Blender will not make an MP4.
echo This is normal on this Windows ARM build. Use the included HTML preview.
echo A ZIP of the actual 72 frames will be made for ChatGPT review.

:MAKE_ZIP
echo.
echo [ARCHIVE] Packaging the animation frames for upload...
powershell -NoProfile -Command "Compress-Archive -LiteralPath '%OUTDIR%\preview_frames' -DestinationPath '%OUTDIR%\UPLOAD_SHOT_A_V21_FRAMES.zip' -CompressionLevel Fastest -Force"
if errorlevel 1 echo [NOTE] ZIP creation failed; individual rendered frames are still available.
echo.
echo ========================================================
echo [DONE] Open the V5_A_V21_output folder.
echo 1. Double-click OPEN_PREVIEW_IN_BROWSER.html to view animation.
echo 2. Upload the MP4 if present; otherwise upload UPLOAD_SHOT_A_V21_FRAMES.zip.
echo 3. Also upload the still PNG and benchmark.json.
echo ========================================================
echo.
pause
exit /b 0

:MISSING_FRAMES
echo.
echo [ERROR] Blender finished but 72 PNG frames were not found.
echo Send benchmark.json and the last 20 lines of this console.
pause
exit /b 3

:BLENDER_FAILED
echo.
echo [ERROR] Blender failed. Please send the last lines above and
 echo any benchmark.json in V5_A_V21_output.
pause
exit /b 4
