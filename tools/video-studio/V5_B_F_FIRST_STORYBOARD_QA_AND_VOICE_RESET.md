# SOVTIVA V5 / first five B–F storyboard renders / corrective QA
**Date:** 12 Nov 2026 | **Status:** Technical rendering PASS, creative framing FAIL, voice placeholder REJECTED.

## First-party actual user upload
- Original file `UPLOAD_V5_FIRST_FILM_STORYBOARD.zip`, ZIP CRC verified, 6 members: JSON benchmark + five rendered PNGs.
- Blender 5.3 Cycles CPU, original .blend, 8 samples, 35% resolution (378x672), 24 FPS story timeline 576 frames.
- Five stills at global frames 96,183,299,417,536 all decode correctly, 378x672, no black-out or neon-red glitch visible; 17.09 sec total rendering recorded.
- **DO NOT render all 504 B–F animation frames using V1 camera yet.** Content and captions severely cropped by portrait aspect-ratio camera framing.

| Scene / frame | Technical QA | Creative QA (actual image) | Change |
| --- | --- | --- | --- |
| B / 96 | PASS | Coin centered but small and underwhelming in a mostly empty scene | Slightly tighter early camera; later explosion needs actual animation QA |
| C / 183 | PASS | Coin/value partially cropped, US$ and BRUTOS*/disclaimer illegible | Wider field of view, pull camera back to show full $109 and qualifier |
| D / 299 | PASS | Paper content exceeds screen width; all key eligibility sentences clipped | Camera pulled back substantially for full receipt/terms |
| E / 417 | PASS | NO APROBADO and US$0 cropped hard | Whole rejection card and monetary value must fit |
| F / 536 | PASS | VISTAS and GANANCIAS cropped, logo too small | Center and widen the shot for legible complete takeaway |

## Voice rejection and remediation
CEO explicitly said provisional synthetic narrator "voice is shit". Voice scratch track was an `espeak` placeholder, not human/natural; never reuse or publish. Keep the original, rights-safe synthetic music/foley concept as a separate *unapproved* track.

Preferred final VO: **natural real female Latin American Spanish**, warm, lightly ironic, documentary editorial rather than generic advertising. Recommended zero-spend path is a human performance (e.g. Sofía, if she voluntarily accepts). Record 2–3 takes with iPhone Voice Memos in a soft, quiet room with the music off, about 15–20 cm from microphone, one phrase at a time. Consent is required; don't infer or impersonate Sofía. An alternative free TTS must be sampled/quality-checked before any recording can be called approved. No cloning of a real person's voice.

Revised 24s script:
- 0–3 A: «¿Cien mil vistas?»
- 3–6 B: «Suena a fortuna, ¿no?»
- 6–10 C: «En este ejemplo: ciento nueve dólares brutos.»
- 10–15 D: «Solo si las vistas cuentan, aprueban el contenido y hay presupuesto.»
- 15–19.5 E: «Si no lo aprueban, podrías cobrar cero.»
- 19.5–24 F: «Porque vistas no son ganancias.»

## V2 corrective production kit
`SOVTIVA_V5_B_F_FRAMING_V2_ZERO_COST.zip` has syntax-checked versioned Blender Python source, user-provided source `.blend` preserved, a Windows BAT rendering **15 frames** over B–F, README, voice direction excluding the rejected scratch voice, and first-pass original music-only MP3. Zip CRC verified; new Blender execution NOT YET TESTED on user's machine.

**Next exactly:** User extracts V2 kit and double-clicks `RUN_V5_B_F_FRAMING_V2.bat`, then uploads `UPLOAD_V5_B_F_FRAMING_V2.zip`. Assistant checks all 15 actual 3D frames for complete text, clarity and camera continuity before launching 504 full frames. **No publishing or spend.**
