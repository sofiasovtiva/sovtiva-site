SOVTIVA V5 | SHOT A V2.1 — CORRECTED 3-SECOND ANIMATION
==========================================================

WHY THIS NEW PACKAGE EXISTS
Your Blender 5.3 still DID render, and the screenshot looks dimensional.
The animation was blocked only by this Blender ARM build rejecting:
  image_settings.file_format = 'FFMPEG'
V2.1 does not use that setting. Blender now produces a dependable PNG image
sequence; the included Windows BAT optionally converts it to MP4 using
FFmpeg IF IT IS ALREADY INSTALLED. No more software needs to be purchased.

OTHER REFINEMENTS
- Reduced harsh salmon/red light spilling onto the back wall.
- Reduced excessive white/red reflections and metallic texture noise.
- Preserved the dynamic three-quarter camera, flying coin and glass breach.
- Preserved the original video concept and 24-fps timing; 72 frames = 3 sec.

WHAT TO DO
1. Extract the new ZIP into a new folder.
2. Double-click RUN_V5_SHOT_A_V21.bat.
   It automatically detects your Blender 5.3 installation.
3. After it finishes, open V5_A_V21_output.
4. Double-click OPEN_PREVIEW_IN_BROWSER.html to SEE the animation even if
   the MP4 could not be encoded. The browser preview runs at 24 fps.
5. UPLOAD TO CHATGPT:
   a) benchmark.json
   b) SOVTIVA_V5_SHOT_A_V21_still.png
   c) SOVTIVA_V5_SHOT_A_V21_preview.mp4 if present; OTHERWISE
      UPLOAD_SHOT_A_V21_FRAMES.zip (contains all 72 PNGs).

DO NOT pay for Runway or install anything to make this first animation.
Blender 5.3 already works. No web account or third-party asset is needed.
Do not run 'full' mode yet; this first preview is deliberately 55% render
resolution. The still PNG is rendered at full native 1080x1920 for QA.

If Blender reports an error, the BAT window remains open. Screenshot the
last lines and upload the generated benchmark.json when possible.

FILE STATUS
- Blender 5.3 V2 original still: real render verified by your upload.
- Blender 5.3 V2 original preview: FAILED on unsupported FFMPEG enum.
- V2.1 code: Python parse and compile tested; PNG export paths inspected.
- V2.1 Blender animation: NOT YET RENDERED in this chat; user will run
  the V2.1 BAT and we will inspect the actual image sequence or MP4.

No public posting, subscriptions, spending, or third-party music.
