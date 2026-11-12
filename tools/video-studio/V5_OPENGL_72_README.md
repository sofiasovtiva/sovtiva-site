SOVTIVA V5 | 72-FRAME OPENGL TEST | NO COST

The six-frame OpenGL diagnostic looked clean. The old default EEVEE rendering had black and neon corrupted frames. We still need a complete 72-frame test before declaring that the renderer is stable.

QUICK START
1. Extract this ZIP fully into a new folder. Do not run the BAT inside the ZIP.
2. Double-click RUN_V5_OPENGL_72.bat. It automatically finds your installed Blender 5.3.
3. After it finishes, open V5_OPENGL_72_output/OPEN_PREVIEW_IN_BROWSER.html to watch the silent 3-second preview.
4. Upload UPLOAD_V5_OPENGL_72.zip in this same conversation. It includes the 72 PNGs, frame-by-frame QA notes and console log. The data ZIP can be large.

WHAT IT DOES
- Uses the exact 3D .blend scene you uploaded, bundled here for convenience.
- Forces --gpu-backend opengl for this run only (no driver or Blender setting change).
- Renders each frame 1 to 72 separately at 594 x 1056 (55% of 1080 x 1920).
- Runs a conservative automated check for extreme black frames and neon color patches.
- Saves new outputs, never overwrites your original .blend or V2.1 results.
- Uses no paid services, Runway credits, downloads or third-party media.

QUALITY CAUTION
The automated QA is a heuristic. Even if it says 'COMPLETED_REQUIRES_MOTION_REVIEW', you must still share the ZIP so the full animation can be inspected. The OpenGL backend was requested in the command line; a Python backend detection API was unavailable in the preceding headless diagnostic, so do not claim it was independently queried by the app.

If there is an error, upload blender_console.log and benchmark.json from V5_OPENGL_72_output instead. Do not reinstall Blender.

NEXT WHEN THIS PASSES
Encode a proper MP4 from the clean frames, judge pacing, camera travel, coin interaction and screen readability, and only then move to Shot B. The next goal is a complete original 24-second film, not more still images.
