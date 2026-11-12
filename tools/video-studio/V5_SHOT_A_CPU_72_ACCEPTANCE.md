# SOVTIVA V5 | Shot A CPU render acceptance

**Evidence date:** 12 November 2026  
**Status:** TECHNICAL ACCEPTANCE — creative revision required; NOT the finished V5 film.

## Original user evidence
- `/mnt/data/UPLOAD_V5_CPU_72.zip`, 75 entries (72 original Blender-rendered PNGs plus `benchmark.json`, console log, HTML preview); ZIP CRC OK.
- Blender `5.3.0`, `CYCLES`, device `CPU`, 12 samples with denoising, original procedural 3D assets; preview 55% of 1080 × 1920 = **594 × 1056**.
- 72 consecutive numbered PNG files `V5A_CPU_0001.png` to `V5A_CPU_0072.png`; identical 594 × 1056 dimensions; each PNG verified readable.
- Blender's terminal log explicitly says `V5_CPU_ALL_FRAMES_RENDERED 72 QA_FLAGS 0`; JSON says `COMPLETE_REQUIRES_HUMAN_REVIEW`; **618.03 seconds**, no paid compute or model credits.

## Independent assistant checks
- Reviewed full 18-panel contact sheet sampled across all 72 frames, including middle and ending; confirms coherent phone, teal studio, 99,998 → 99,999 → 100,000 counter, emergence/forward motion of embossed gold `S` token, accompanying shards and coins. No visible black frames, flat-red frames or neon GPU artifacts in sampled timeline.
- Computer-vision scan across **all 72 original PNGs** (downsampled from actual frames): mean RGB intensity between 55.03 and 81.78 (on 0–255 scale); maximum near-black pixel fraction `0.0001`; no pure-red saturation areas. First-to-last adjacent frame average absolute pixel change max `8.595`, median `2.835`, no abrupt spikes above `20` on the downsampled 99 × 176 pixel comparison. This is a screening metric, not a motion/perceptual quality score.
- Assembled a **silent 3.000 second H.264 MP4, 24 fps, 72 frames, 594 × 1056**, via local FFmpeg with CRF 18. `ffprobe` verified codec, dimensions, duration and frame count. No frame replacement, visual compositing or AI hallucinated footage.
- MP4: `SOVTIVA_V5_Shot_A_Cycles_CPU_3sec.mp4`; contact sheet: `SOVTIVA_V5_CPU_72_contact_sheet.jpg` (both conversation attachments, **not** public website/media releases).

## Creative review / honest limitations
- Technical engine gate **PASS**: reliable Cycles CPU output on the tested hardware at preview size; EEVEE/OpenGL failed prior 72-frame quality gate.
- Film direction gate **NOT PASS YET**: the establishing phone view occupies too much time in a 3-second social opening; the coin covers the important count after appearing, and the bright circular screen reflection competes with focal action. The shape reads as a brand token rather than obviously as valuable earned money; shards look like triangles instead of a convincing break in glass. Phone hovers over platform, which can be deliberate surrealism but needs physical cues. No original narration, foley, edit or sound design yet.
- This is **only Shot A**, not the six-shot 24-second V5. Current test A is 72 frames (3 seconds) whereas the preliminary 24-second shotlist allocates A 48 frames (2 seconds). Before assembly, either edit A to 48 or rebalance the overall timeline. The shotlist is preproduction, not a final locked edit.
- Cycles sampling is 12 at 55% resolution; not yet a native 1080 × 1920 production frame or a final noise/texture grade. Performance at full resolution remains unbenchmarked.

## Production decision and next exact action
1. **Lock CPU Cycles as reliable local render path** for V5 preview. Stop trying EEVEE/Adreno until a separate user-approved driver test is warranted; no payment or new subscriptions.
2. Progress toward Shot B: make the `S`-minted coin fly close enough to fill lens and perform a matched transition into the gold conditional `$109 BRUTOS*` reveal. Build it around motivated speed ramp, original foley, controlled shadows and authentic material highlights.
3. Before final edit, shorten or strengthen opening count, ensure `100,000` visible before occlusion, correct the flat circular reflection and increase clarity of glass-break force. Adjust camera continuity and 24s timings from the V5 shotlist, then render short CPU previews, inspect and correct.
4. Keep documentary disclaimer: $109 is a hypothetical *gross* payout on eligible approved 100,000 views at illustrative $1.09 CPM. No promised earnings. No publishing or paid resources.

**Money spent:** $0. **Third-party creative assets:** none in Shot A. **Social publication:** none.
