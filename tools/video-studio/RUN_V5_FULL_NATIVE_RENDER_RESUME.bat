@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
set "BLENDER=%ProgramFiles%\Blender Foundation\Blender 5.3\blender.exe"
set "ROOT=%~dp0V5_FULL_PRODUCTION"
set "A_BLEND=%~dp0SOVTIVA_V5_SHOT_A_V21.blend"
set "BUILD=%~dp0build_BF_scene_only_v3.py"
set "RENDER=%~dp0render_queued_native_frames.py"
set "B_BLEND=%ROOT%\scene_BF\SOVTIVA_V5_FILM_24S_SCENES_A_to_F_COLOR_QA_V3.blend"
if not exist "%BLENDER%" ( echo ERROR: Blender 5.3 Windows ARM not found. & exit /b 2 )
if not exist "%A_BLEND%" ( echo ERROR: Original A blend absent. & exit /b 3 )
if not exist "%BUILD%" ( echo ERROR: B-F scene source absent. & exit /b 4 )
if not exist "%RENDER%" ( echo ERROR: Resumable renderer absent. & exit /b 5 )
if not exist "%ROOT%" mkdir "%ROOT%"
if not exist "%ROOT%\scene_BF" mkdir "%ROOT%\scene_BF"
echo SOVTIVA V5: PRIVATE 24-second 1080x1920 source render / 24fps / Cycles CPU
echo Stage A: 72 frames. Stage B-F: 504 frames. 576 total.
echo Can resume safely by running this file again after interruptions.
echo No network / no publication / no spending.
if not exist "%B_BLEND%" (
 echo Creating original 3D scene B-F (no full render in this step)...
 "%BLENDER%" -b "%A_BLEND%" -t 8 -P "%BUILD%" -- --mode scene --pct 100 --samples 24 --out "%ROOT%\scene_BF"
 if errorlevel 1 ( echo ERROR: Failed to create B-F scene. & exit /b 6 )
)
echo Rendering or resuming native 1080x1920 Shot A frames...
"%BLENDER%" -b "%A_BLEND%" -t 8 -P "%RENDER%" -- --stage a --pct 100 --samples 24 --out "%ROOT%"
if errorlevel 1 ( echo ERROR: A render interrupted. Rerun this .bat to resume. & exit /b 7 )
echo Rendering or resuming native 1080x1920 Shots B-F frames...
"%BLENDER%" -b "%B_BLEND%" -t 8 -P "%RENDER%" -- --stage bf --pct 100 --samples 24 --out "%ROOT%"
if errorlevel 1 ( echo ERROR: B-F render interrupted. Rerun this .bat to resume. & exit /b 8 )
echo All frames rendered. Summarizing output without uploading raw 576 frames.
powershell.exe -NoProfile -NonInteractive -Command "$ErrorActionPreference='Stop'; $r='%ROOT%'; $files=Get-ChildItem -Path (Join-Path $r 'frames') -Filter 'V5_????.png' -File; if($files.Count -ne 576){throw 'Expected 576 frames, found '+$files.Count}; $report=Join-Path $r 'UPLOAD_V5_FINAL_FRAME_REPORT.zip'; if(Test-Path $report){Remove-Item $report}; $wanted=@((Join-Path $r 'progress_shot_A.json'),(Join-Path $r 'progress_shots_BF.json')); foreach($n in 1,72,96,183,299,417,536,576){$wanted+=(Join-Path $r ('frames\V5_{0:D4}.png' -f $n))}; Compress-Archive -Path $wanted -DestinationPath $report; Write-Output ('READY: '+$report)"
if errorlevel 1 ( echo ERROR: Final local frame report packaging failed. Raw frames are safe. & exit /b 9 )
echo SUCCESS: 576 frames. Full-res footage is NOT a final movie. Keep V5_FULL_PRODUCTION folder.
echo The film needs a natural voice and a verified audio mix before public review.
exit /b 0
