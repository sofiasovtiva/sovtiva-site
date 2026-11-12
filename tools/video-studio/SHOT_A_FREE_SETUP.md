# Sovtiva V5 | Zero-cost true 3D render gate

**Stage:** Free original Blender 5.2.4 LTS source created; Blender runtime output **NOT YET VERIFIED**. The earlier V3 high-energy direction is the target, not V4's quieter aesthetic. This scene is the first **technical shot test**, not a completed V5.

## Requirements

- **Blender 5.2.4 LTS**, free and locally installed. Windows-on-ARM installer is available from Blender's official index: https://download.blender.org/release/Blender5.2/blender-5.2.4-windows-arm64.msi . For Windows x64 use the matching x64 installer. Do not run software from unverified download mirrors.
- No other packages needed: Blender includes the `bpy` runtime, shaders, modeling tools, EEVEE / Cycles renderer and Python runtime.
- Optional: original free `ffmpeg` for assembling final animation to MP4, which is **NOT** performed by Shot A itself.

## Run it locally

Download `shot_A_blender.py` and make sure Blender is installed. From a Windows ARM64 terminal (adjust executable location):

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -t 4 --python "shot_A_blender.py" -- --mode still --out "V5_output"
```

This creates `V5_output/SOVTIVA_V5_SHOT_A.blend`, one native **1080×1920** PNG at frame 37 and a `benchmark.json` with the elapsed time and actual Blender render engine. If headless EEVEE fails on the device, retry with `--engine cycles --samples 16` (slower CPU render, no GPU purchase).

**After checking that still** — it must look physically dimensional, with a clear phone, brushed metal coin, coherent highlights, floor contact and compelling focal point — render a short preview:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -t 4 --python "shot_A_blender.py" -- --mode preview --out "V5_preview"
```

This exports **72 low-resolution PNG frames (3 seconds at 24fps, 40% scale)**. The rest of the six-scene V5 24-second film is planned in `v5_shotlist.json` but not implemented or rendered by this script. Native `--mode full` produces 72 full-size PNG frames and should only be attempted once the still and preview pass.

### Render QA gate

- Read `benchmark.json` and confirm actual Blender version, engine and elapsed time.
- Inspect `shot_A_frame_0037.png`; check real 3D coin visibility, bevels, material roughness, floor shadows and no hidden text.
- Verify that preview frame count = 72 and each image has plausible continuity; no black/blank frame, severe temporal flicker or geometry clipping.
- Do **not** claim the film is rendered or ready to post. Add original narration, carefully mixed original/rights-cleared sound and six-shot production later.
- Performance is unproven on Snapdragon Windows ARM and in the ChatGPT cloud runtime. Blender cannot be installed or run inside the isolated runtime used during source preparation because external installer downloads are blocked.

## Free stack and boundaries

- Blender / EEVEE / Cycles: original 3D camera, geometry, lighting, and motion.
- Original code and own art: $0. No stock assets; no music/audio rights issue in this technical preview (silent frames).
- GitHub: code and scene specs only, not paid GPU compute or automatic render.
- FFmpeg or free DaVinci Resolve later: composition, voice/foley and sound, no subscriptions required.
- Free Runway tier in connected `Sofia` workspace was independently verified to expose **zero video-generation models** on 11 Nov 2026. 500 included credits do not remove the video plan gate; no upgrade or credits were purchased or used.
- vidIQ connection independently verified (150 renewable credits, no credits spent in this verification); unnecessary for 3D rendering. If used later, research only and report actual credit usage.

Production source of truth: https://docs.google.com/document/d/1fKzmufcbti1NUaWrR7cyluzmY6Cahp2uC-tM9BAISgs/edit
