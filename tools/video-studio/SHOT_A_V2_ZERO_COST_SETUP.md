SOVTIVA V5 | SHOT A V2 — 3-SECOND CINEMATIC TEST
----------------------------------------------------

What changed since your real Blender 5.3 render:
- 3/4 low-angle camera, camera push toward a real 3D coin
- darker studio, dramatic rim light, physically distinct phone sides
- cleaned-up phone interface: counter ONLY, no $109 or big question
- metal token breaks through glass with procedural shards and smaller coins
- 72-frame / 3-second original animation at 24 fps
- one 1080x1920 still for judging genuine material, framing and lighting

WHAT TO DO (Windows):
1. Extract this whole ZIP to its own folder, not just the BAT.
2. Double-click RUN_V5_SHOT_A_V2.bat.
3. The BAT auto-finds your installed Blender 5.3 at
   C:\Program Files\Blender Foundation\Blender 5.3\blender.exe.
4. After Blender finishes, open the V5_A_V2_output folder.
5. Upload the MP4 (may contain 0001-0072 in its name), the STILL PNG,
   and benchmark.json to this ChatGPT conversation.
   If there is an error, send a screenshot of the BAT window instead.

The preview is 55% render resolution on purpose, to validate camera,
composition, motion, physics illusion and pacing before rendering full size.
The included still is native 1080x1920. The preview contains no sound yet;
audio design will follow only after camera and movement pass visual QA.

DO NOT run the full 1080p video until this preview passes. Blender 5.3 is
sufficient; do not reinstall 5.2. No extra downloads, credits or payment.

Fallback if MP4 export fails: Blender saves 72 PNGs in
V5_A_V2_output\PNG_frames_if_MP4_fails. Send a ZIP of those frames plus
benchmark.json, or a screenshot of the error. No additional software needed.

REPRODUCIBLE MANUAL COMMAND (you normally do NOT need it):
"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b -t 4 --python "shot_A_v2_blender.py" -- --mode preview --out "V5_A_V2_output"

EVIDENCE STATUS:
- Your preceding Shot A original Blender EEVEE 5.3 full-res still: verified.
- This V2 source: Python syntax checked, paths and launch flow inspected.
- V2 Blender rendering, material response and performance: NOT yet verified
  in this ChatGPT environment. Your preview will establish actual evidence.

© 2026 Sovtiva. All source geometry/materials/animation are original.
