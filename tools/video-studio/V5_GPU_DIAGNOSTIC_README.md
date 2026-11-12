SOVTIVA V5 / FREE GPU DIAGNOSTIC / BLENDER 5.3 WINDOWS ARM
============================================================

WHY THIS EXISTS
Your 72-frame V2.1 preview completed, but at least 16 of its frames were clearly corrupted (some fully black, others neon/red/green geometry artifacts). Your good still is not proof that the animation is reliable. Possible cause: Qualcomm Adreno graphics/driver/backend instability with Blender 5.3 EEVEE. This is a hypothesis, not yet a diagnosis confirmed on your driver.

WHAT TO DO
1. Extract ALL FOUR files in this kit into a new Windows folder.
2. Double-click RUN_V5_GPU_DIAGNOSTIC.bat.
3. The launcher locates your installed Blender 5.3 automatically and runs:
   A. EEVEE with --gpu-backend opengl at 55% preview resolution: frames 1, 18, 27, 42, 60, 66.
   B. Cycles on CPU at 35% preview resolution: frame 42 only, 8 samples with denoise.
4. When complete, upload UPLOAD_V5_GPU_DIAGNOSTIC.zip here.

PLEASE NOTE
- The diagnostic may take several minutes. No payment, no new tools, no driver installation required.
- If the app crashes at any point, the batch continues and archives available logs.
- No existing V5 outputs or .blend source will be overwritten.
- The produced images are NOT a finished video. We will inspect them to decide whether OpenGL renders reliably enough for the next full 3-second test. If not, use CPU Cycles with appropriate quality/performance trade-offs.
- We are not yet moving on to the other five scenes until Shot A's preview is visually clean.
- Only download official driver updates later if evidence justifies it. No random third-party GPU tweaks.

SUPPORTING EVIDENCE
Blender 5.3 GPU troubleshooting: https://docs.blender.org/manual/en/5.3/troubleshooting/gpu/windows/other.html
Blender 5.3 GPU backend CLI: https://docs.blender.org/manual/es/5.3/advanced/command_line/arguments.html
Documented Qualcomm Adreno Vulkan artifacts: https://projects.blender.org/blender/blender/issues/165862
SOVTIVA video studio record: https://docs.google.com/document/d/1fKzmufcbti1NUaWrR7cyluzmY6Cahp2uC-tM9BAISgs/edit

Status: SOURCE VERIFIED, LOCAL GPU TEST PENDING. No spending.
