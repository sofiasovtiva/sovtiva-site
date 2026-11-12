# Sovtiva Video Studio — local starter v0.1

**Status:** functioning rights-gated FFmpeg proof of concept. Tested with a synthetic video only (6 seconds at 360×640); no real client footage, no social publishing, no paid APIs. Initial research and production SOP live in Sovtiva Drive.

This kit turns a permitted local video into a portrait MP4 using an unfussy centered subject with a blurred background, reviewed timing-based captions, normalized existing audio and a thumbnail. It creates a contact sheet and a machine-readable manifest. It **does not** generate captions from speech, perform automatic jump-cut selection, detect faces or publish video. Those remain later integrations, not production features.

## Requirements

- Python 3.10+ (standard library only)
- FFmpeg and ffprobe on PATH, with libx264 and subtitles/libass filters available
- Rights to process the source video and a human editor to approve the result
- No Claude subscription, external login, paid video generation or cloud hosting required

## First test (no client footage)

1. Open this directory locally. Create a synthetic test recording:

```bash
ffmpeg -hide_banner -y -f lavfi -i testsrc2=size=640x360:rate=30 -f lavfi -i sine=frequency=440:sample_rate=44100 -t 6 -c:v libx264 -preset ultrafast -crf 28 -pix_fmt yuv420p -c:a aac source.mp4
```

2. Copy `project.example.json` to `project.json`. Change `rights.status` to `APPROVED`, `rights.owner` to `Sovtiva synthetic demo`, and `rights.basis` to `Original FFmpeg generated test footage`. Set `width` to 360 and `height` to 640 for a fast test. Keep the original example untouched.
3. Copy `captions.example.json` to `captions.json` and change `captions` in your new `project.json` to `captions.json`.
4. Run `python render.py project.json`. On success, inspect `out/master_vertical.mp4`, `out/thumbnail.jpg`, `out/qa_contact_sheet.jpg`, and `out/manifest.json`.

## For the next authorized Sovtiva video

1. Create a fresh, local production folder with a copy of `render.py`, `project.example.json` and editable captions. Place **only approved** video there; never upload raw private client videos to the public website repository.
2. Record the footage owner, usage permission and approval evidence outside this public repository. Set `rights.status=APPROVED` only when documented.
3. Enter `source`, clip `start` and `end` in seconds (maximum 180), output size 1080×1920 by default, and reviewed `captions.json` segment timings (relative to the clip start).
4. Run the script. Caption segments must be legible and concise; segments longer than two lines are rejected.
5. **Watch and listen to the full export.** Check crop, spelling, hooks, audio, subtitle timing, brand claims, rights and required AI/sponsorship disclosures. A contact sheet is a guide, not a substitute for full playback.
6. Obtain specific publication approval and use your normal approved social posting procedure. This kit cannot publish anywhere. Log timestamps, revision count, time spent, variable costs, audience results and any actual cash collected in the private Drive ledger.

## Workflow responsibility

- **Research / idea:** a current audience need, clear purpose, original hook; source rights.
- **Editorial:** approved shot list / transcripts, trim range, reviewed captions.
- **Production:** render a versioned vertical export with FFmpeg.
- **QA:** editor and brand approval, music/footage rights, disclosures, audio and subtitle inspection.
- **Distribution:** separate, approved action; track real links and performance.
- **Economics:** actual costs, revisions and accepted deliverables; no presumed payouts or CPM guarantees.

## Deliberately not implemented

- **Whisper.cpp / transcription:** install separately and convert corrected text/timings into `captions.json`; automatic ASR output still requires review.
- **Remotion motion graphics:** optional after a real brief and license check. Individual/small organization eligibility differs from a larger company. https://www.remotion.dev/docs/license/pricing
- **MediaPipe speaker tracking:** no facial tracking in this starter; the blurred-background fit avoids unverified face cropping.
- **Higgsfield / Ssemble / Seeded:** independent optional marketplaces, not required for local editing; no subscription or submissions made.
- **Payments, campaigns, automated posting, publishing:** excluded.

## Test evidence

A synthetic 6-second 640×360 video with sine audio was rendered to 360×640 using the same `render.py` code. We verified a 6-second output, caption rendering, MP4 dimensions, a thumbnail and contact sheet, and a manifest containing `RENDERED_NEEDS_HUMAN_QA`. A deliberately unapproved project raised `PermissionError`. One long caption was visually cropped, then automatically wrapped and successfully re-rendered. This does **not** validate 1080p speed or real talking-head footage.

No footage or local manifests should ever be committed to this public repo.

Last internal validation: November 11, 2026 (Mexico City). No expenses incurred.
