@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
set "BLENDER=%ProgramFiles%\Blender Foundation\Blender 5.3\blender.exe"
set "ROOT=%~dp0V5_FULL_PRODUCTION"
set "A_BLEND=%~dp0SOVTIVA_V5_SHOT_A_V21.blend"
set "BUILD=%~dp0build_BF_scene_only_v3.py"
set "RENDER=%~dp0render_queued_native_frames.py"
set "B_BLEND=%ROOT%\scene_BF\SOVTIVA_V5_FILM_24S_SCENES_A_to_F_COLOR_QA_V3.blend"
if not exist "%BLENDER%" ( echo ERROR: Blender 5.3 not found & exit /b 2 )
if not exist "%ROOT%\scene_BF" mkdir "%ROOT%\scene_BF"
if not exist "%B_BLEND%" (
 "%BLENDER%" -b "%A_BLEND%" -t 8 -P "%BUILD%" -- --mode scene --pct 100 --samples 24 --out "%ROOT%\scene_BF"
 if errorlevel 1 exit /b 3
)
echo Testing native full-resolution samples without committing to all 576 frames.
"%BLENDER%" -b "%A_BLEND%" -t 8 -P "%RENDER%" -- --stage a --max-frames 1 --pct 100 --samples 24 --out "%ROOT%"
if errorlevel 1 exit /b 4
"%BLENDER%" -b "%B_BLEND%" -t 8 -P "%RENDER%" -- --stage bf --max-frames 3 --pct 100 --samples 24 --out "%ROOT%"
if errorlevel 1 exit /b 5
echo NATIVE GATE PASS. 4 native frames in V5_FULL_PRODUCTION\frames. Safe to run full render next.
exit /b 0
