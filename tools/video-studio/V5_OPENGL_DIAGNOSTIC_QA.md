# SOVTIVA V5 — Blender 5.3 Windows ARM GPU diagnostic readback

**Date:** 12 November 2026. **Scope:** Shot A V2.1. **Outcome:** OpenGL EEVEE is promising on six representative frames, but has not passed a full 72-frame animation test. **Total spend:** $0.

## First-party observations

The user supplied a Blender `.blend`, a full V2.1 72-frame PNG animation, a still image and a failure-free diagnostic ZIP. Prior V2.1 animation looked unstable: many black or red/neon frames were encoded directly into original PNG files, before FFmpeg touched them. The diagnostic ZIP contains 7 PNG images with valid ZIP checksums and two complete Blender reports.

- EEVEE launched with the `--gpu-backend opengl` flag: frames **1, 18, 27, 42, 60, 66**, all **594 × 1056** (55% of native 1080 × 1920), visually reviewed and **no obvious black/neon artifacts**. Total elapsed **19.14 sec** (first frame including Blender/GPU startup 11.67 sec; subsequent samples 1.43–1.58 sec). The Python `gpu.platform.backend_type_get()` probe did not initialize in background mode, so the actual active GPU backend was **requested via CLI but not independently queried**.
- Cycles on CPU: frame **42**, **378 × 672** (35%), **8 samples** with denoising, **3.1 sec**, visually clean. These timings **cannot be compared at equal resolution or equal samples**.
- The clean still remains stylistically a development stage; framing, hero-object size, background and audio still require creative approval.

## Decision

Do **not** upgrade Runway, modify drivers, reinstall Blender or spend money. Request a **complete 72-frame serial EEVEE render** under the same `--gpu-backend opengl` launch setting. Use separate `bpy.ops.render.render(write_still=True)` calls for each frame (this mirrors successful diagnostic behavior), collect PNGs, frame-level heuristic QA and Blender logs in a single ZIP. If the full pass is visually clean, assemble 3 seconds at 24fps and proceed with creative shot refinement. If defective frames recur, use the free **Cycles CPU** pipeline for a consistent full-sequence fallback; do not mix engines inside one uninterrupted shot. The GPU driver hypothesis remains unconfirmed.

## Deliverable and required verification

The ZIP `SOVTIVA_V5_OpenGL_72_Free_Render.zip` contains the user-supplied original `.blend`, one-line Windows launcher with auto Blender 5.3 discovery, `render_v5_opengl_72.py`, a local browser playback page and a README. Source is syntax checked, archive CRC passes, but the Blender 72-frame runtime **has not been run within ChatGPT**. The user only needs to extract, double-click `RUN_V5_OPENGL_72.bat` and upload the generated `UPLOAD_V5_OPENGL_72.zip` for proper review.

No external media, licensed tracks, public publishing or new account permissions.
