# SOVTIVA V5 | OpenGL full 72-frame failure and CPU rendering decision
**12 November 2026 | Original 3D, no spending, internal QA only**

## First-party evidence
User supplied `UPLOAD_V5_OPENGL_72.zip`, `benchmark(3).json`, `blender_console.log`, editable `.blend`, 72 PNG frames and local HTML preview. The ZIP contains 75 entries with valid CRC, including all 72 numbered 594×1056 images (55% of 1080×1920), rendered at 24fps by Blender 5.3.0 EEVEE with `--gpu-backend opengl` requested via CLI (active backend not independently interrogated). Completion status: `COMPLETED_WITH_QA_FLAGS`; 84.84 seconds; 0 USD.

### Actual image inspection
44/72 files triggered heuristic flags. Independent PIL image statistics and visual contact-sheet review confirmed:
- 35 frames with more than 90% of pixels effectively black: frame indices `[20,24,31,33,35,36,37,38,39,41,42,45,46,47,48,49,50,52,53,54,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72]`.
- Frames 34 and 40 have anomalously large saturated-red blocks (>20% of pixels); frame 34 is almost wholly red.
- Frame 57 is mostly white/black, an additional major visual defect not caught by the simple heuristic.
- This is corruption in original PNGs, not video encoding, so no editing or upscaling can repair the root cause.
- The first 12 frames are coherent, but later corruption renders the sequence unusable.

The earlier six-frame OpenGL diagnostic was a misleading *small-sample success*. **Full EEVEE/OpenGL cannot be accepted for this device/scene.** Root cause could be GPU/driver/backend instability; the exact driver-level cause remains unproven, and no driver modification or software purchase is approved.

### Separate CPU evidence
The earlier diagnostic rendered frame 42 with **Cycles CPU, 8 samples, 35% resolution (378×672), approximately 3.1 seconds**. That image was visually clean: correct teal phone, metal coin, real shadows and reflections. Only one Cycles frame was tested; the full sequence has not yet passed.

## Corrective implementation
Created a new ZIP `SOVTIVA_V5_CYCLES_CPU_72_ZERO_COST.zip` containing the original user-owned `.blend`, Blender 5.3 Python source `render_v5_cycles_cpu.py`, Windows `RUN_V5_CYCLES_CPU_72.bat`, and setup instructions. Blender 5.3 is installed on the user's machine.

It renders **all 72 frames** independently using **Cycles CPU** with 12 samples and denoising at 55% preview resolution (594×1056, 3 seconds at 24fps). It validates PNG dimensions, checks for suspicious black/saturated results, and stops early after two consecutive severe failures. On successful completion it provides a local browser preview and always packages available outputs to `UPLOAD_V5_CPU_72.zip`. The original `.blend` is never overwritten and the Windows launcher requires **no paid service, third-party installation, cloud GPU, Runway credits or social publication**. Full CPU runtime/visual quality are still unverified until user executes the ZIP on Windows.

**Next exact action:** User extracts the CPU ZIP, runs `RUN_V5_CYCLES_CPU_72.bat`, returns `UPLOAD_V5_CPU_72.zip`. Assistant inspects every frame, assembles MP4, checks motion/lighting and only then accepts Shot A. If CPU renders reproducibly, use it for V5 production; optimize runtime later without sacrificing reliability. Do not move to shots B–F on a broken engine.
