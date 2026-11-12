# SOVTIVA V5 | Shot A V2.1 | Independent first-party render QA
Date: 12 Nov 2026. **State:** 72-frame local technical render completed; artistic/technical acceptance **FAILED** due to intermittent image corruption. No platform publication, spending, or new paid tools.

## Verified input
- User-supplied original `SOVTIVA_V5_SHOT_A_V21.blend`, `SOVTIVA_V5_SHOT_A_V21_still.png`, `benchmark(2).json`, and `UPLOAD_SHOT_A_V21_FRAMES.zip` (72 full PNGs).
- User benchmark: Blender **5.3.0**, **EEVEE**, 24fps, 72 frames, still at 1080x1920, animation at 55% = **594x1056**, 24 requested samples, **100.29 seconds** measured for pipeline, `RENDER_FINISHED_IN_THIS_RUNTIME`.
- ZIP integrity: 72/72 PNG files present, valid, identical image dimensions **594x1056**, no ZIP CRC errors. The source is original procedural 3D, according to the first-party file manifest; no additional media was mixed.

## MP4 assembly verified
- Made `SOVTIVA_V5_Shot_A_V21_3s_preview.mp4` with FFmpeg, 24fps H.264, 72 frames, **3.000 s**, **594x1056**, video only/silent. Encoding successful. It is a faithful transcription of the *corrupted* original sequence, **not a clean video**.
- 13-frame contact sheet visually inspected at frames 1, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72. The noncorrupt frames show improved brass/teal color grade and physical dimensionality compared with V2.

## Actual blocker
- Frame 18 and 60 are nearly/completely black; frame 42 has extreme blue/green/yellow pixel blocks and dark masses; frame 66 shows red blocks. Numerous additional frames are black or display color corruption. A bounded image-statistics scan flagged at least **16 of 72 frames** as clearly defective under black/red/green thresholds (18,21,23,27,32,35,38,40,44,49,51,55,59,60,64,68). **This is not caused by MP4 encoding:** the PNGs themselves are damaged.
- Suspect Windows ARM Qualcomm Adreno EEVEE graphics backend / driver compatibility; this is a **hypothesis, not confirmed for this machine** because the exact driver and backend have not been measured. Official Blender GPU troubleshooting: https://docs.blender.org/manual/en/5.3/troubleshooting/gpu/windows/other.html . Public Qualcomm Adreno graphics issue reports: https://projects.blender.org/blender/blender/issues/165862 and https://projects.blender.org/blender/blender/issues/146804 .

## Repair strategy, zero dollars
1. Preserve original user scene. Render a **small diagnostic subset** on Blender 5.3 using the **OpenGL GPU backend** to distinguish Vulkan-specific artifacts from scene bugs. Use the supported `--gpu-backend opengl` command-line flag, no driver installation or settings changes; test frames 1,18,27,42,60,66 at 55% resolution.
2. Also render frame 42 using **Cycles CPU at 35% and 8 samples**, testing a GPU-independent control. This may be slower and is not guaranteed to work until run.
3. Inspect the returned test images against original corrupted samples. If OpenGL is clean, rerender 72 frames using OpenGL and automatically validate image frames before assembly; if not, benchmark an efficient CPU Cycles preview, or identify a free supported alternative. Do not disguise corrupted frames as an intentional glitch or waste time rendering other shots.
4. Only once the 3-second preview is visually clean and professionally directed should we advance to Shot B. Preserve V3's high energy, 3D material detail, purposeful camera movement and original audio plan, with no expenditure.

## QA status / next exact task
A small executable diagnostic ZIP is prepared in the active chat: `SOVTIVA_V5_GPU_Diagnostic_No_Cost.zip`, containing the original user .blend, `blender_probe.py`, Windows auto-detect launcher and a README. It will write `UPLOAD_V5_GPU_DIAGNOSTIC.zip` containing OpenGL and CPU images plus runtime/error logs. **Tool code is syntax-checked and ZIP CRC-checked; local Blender run remains unverified.**
