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

## Sovtiva's own social channels (added 11 November 2026)

This kit is **also the internal production studio for original Sovtiva videos**, not only a client service. Repackage verified Journal research, first-party product demos and rights-cleared video, with one useful insight per post. Never treat views as guaranteed revenue.

- **Research article → silent editorial short:** `social_cards.py` + `social_story.example.json` generates 2–8 portrait panels, a contact sheet, a draft MP4 and a QA manifest using Pillow and FFmpeg. No footage, audio, paid video credits, AI voice or connected accounts are needed.
- **Owned footage → subtitled reel:** use `render.py` with source video, clip times, and manually approved subtitle segments in JSON. Whisper.cpp is only a proposed later transcription layer.
- **Original fictional character:** separate licensed character production, permission gates and transparent synthetic-content labeling.
- **Campaign-funded paid views:** optional, evaluated per live brief; never finance production from assumed clip payouts.

### First-party article-to-video steps

1. Choose a useful source article from `sovtiva.com/journal/`. Note the single claim and original source links.
2. Copy `social_story.example.json` to a private `social_story.json`; write 2–8 scenes, each 1.6–7 seconds, with one clear takeaway. No copied third-party video or unverified metrics.
3. Keep the included rights status `PENDING` until the text, visuals, branding and citations are confirmed as owned/authorized. Record `APPROVED`, owner and usage basis only with evidence.
4. On a local computer with Python 3.10+, Pillow, FFmpeg and ffprobe, run `python social_cards.py social_story.json`. For a quick test choose 540×960; evaluate 1080×1920 separately for delivery.
5. Review every scene in the storyboard contact sheet and play the full silent MP4. The video has **no narration or soundtrack**, and is NOT ready to publish without editorial sign-off.
6. Adapt the script and caption for Instagram, TikTok, YouTube Shorts or Pinterest. Include verified facts, an appropriate CTA and any required sponsorship/AI disclosure.
7. Obtain explicit approval to publish, distribute using an authorized connected account and record platform URL plus actual reach, engagement, qualified traffic and cost.

### Three next original Sovtiva videos (DRAFT / NOT PUBLISHED)

- SV-SOC-001: **Do views pay for the video?** Four visual panels introducing the economics of funded short-form campaigns; article: `/journal/higgsfield-seeded-paid-views-2026/`. A silent local prototype was rendered and inspected; nothing posted.
- SV-SOC-002: **One useful recording, several purposeful clips.** Show the intake/edit/QC loop from a Sovtiva-owned or licensed webinar or interview. Waiting for real footage and consent.
- SV-SOC-003: **What does our video editor actually do?** A restrained 20–30s behind-the-scenes mini-demo of the rights gate, captioned render and QA contact sheet. Clearly separate implemented FFmpeg steps from proposed Remotion, ASR and social integrations.

Style: editorial navy, beige, burgundy, olive, airy typography, no fake UI/metrics, one claim per video, visible sources in native post text. Choose polished original assets, not generic AI-looking stock. Avoid automated posting and paid generation without action-specific approval. Never commit personal footage, clients' media, API keys, tokens, private manifests or contracts to the public repository.

Test evidence: `social_cards.py` produced a four-scene, 13.04s H.264 draft at 540×960 using original Sovtiva copy. Original scene cards and a storyboard sheet were inspected; a decorative shape conflicting with the headline was moved. This validates the small local flow, **not** 1080p throughput, commercial output quality or channel distribution.

### Additional full-HD research video validation (November 11, 2026)

The revised source-led video `examples/SV-SOC-001-paid-views.example.json` was rendered locally with a separate rights-approved copy and 5 original cards. FFprobe verified **1080 × 1920, H.264, 18.08 seconds**. The storyboard was inspected; the output remains **SILENT / DRAFT_NEEDS_HUMAN_QA / NOT PUBLISHED**. This validates original-graphic full-HD export, not the customer-footage renderer, paid platform eligibility or social engagement. Public example remains `rights.status=PENDING` so copying it alone cannot bypass the rights gate.

## TikTok Motion Studio V2 — kinetic editorial short (tested 11 Nov 2026)

The first quiet, static 18s visual became a more energetic 18.17s portrait short in **`kinetic_paid_views_v2.py`**. It uses original graphics (oversized typography, receipt, punchy cards, editable timeline, color shifts, scene-level movement, beat-synced transitions) and programmatically synthesized percussion, bass, chimes and whooshes. It borrows **no copyrighted commercial track** and makes no external API calls.

**Test evidence:** local execution rendered 436 frames at 720×1280/24fps, then exported H.264 MP4 1080×1920/24fps with 44.1kHz AAC audio. FFprobe readback: 18.1667s, 6.15MB. Audio peak ~−1.9dB, mean ~−19.4dB by FFmpeg volumedetect. An eight-panel storyboard was inspected, one illegible header caused by incorrect overlay contrast was corrected, then the entire clip was rendered again. The renderer compiles. Human watch/listen and platform-native placement still need signoff; this is **tested internal content, not published**.

**Run:** Python 3.10+, Pillow, numpy, scipy, system fonts Lato (adjust paths if unavailable), FFmpeg/ffprobe on PATH. From the file's directory: `python kinetic_paid_views_v2.py`. It writes a video, individual storyboard frames, a storyboard grid, original synthesized WAV and temporary MP4 into the script directory. Current implementation assumes a Linux environment and hard-coded aspect/output, so refactor input/config and error handling before client production.

**Content basis:** the independent Sovtiva report about creator-paid views, based on an **illustrative** ~$1.09 CPM. A video reaching 100,000 *eligible approved* views would gross about US$109 **before costs**, assuming the campaign budget and cap allow. An unapproved submission may receive US$0. The short never represents a verified payout or typical creator earnings. Article: `/journal/higgsfield-seeded-paid-views-2026/es/`.

**Creative test learning:** TikTok's public advertiser guidance emphasizes the first 3 seconds, movement, sound, native portrait format, legible text and variable hook testing. A show-and-reveal sequence is stronger than static fact cards, but no tool can certify actual future views. Creative Center official reference: https://ads.tiktok.com/business/en/guides/video-advertising-guide . Next test: optional human voiceover, a real footage/demonstration element and two hook variations before seeking specific publication approval. No Descript edit was made automatically; the generated local MP4 is not yet imported as a Descript media asset.

## V3: actual 3D geometry and moving camera (11 November 2026)

The user rejected V2 as too two-dimensional. The next prototype uses the actual 3D rendering engine **VTK 9.6.2** with polygon/extruded-text geometry, cylinders, rings, material lighting, perspective camera and occlusion. It is **not** a flat card-animation pass, a prompt-to-video API or a Descript edit.

- **Source:** `true_3d_paid_views_v3.py`. Original Sovtiva-only visual motifs for 100K views, illustrative $109 gross, terms on a 3D paper receipt, rejected $0, and a 3D Sovtiva end card.
- **Output generated:** 15.000-second H.264 MP4, 1080 × 1920 output, 24 fps, original mono AAC at 44.1kHz. Underlying VTK frames are rendered at 540×960 and upscaled on export; do not claim native 1080p ray tracing.
- **Sound:** original Python-generated beat, whooshes, thumps and chimes (no third-party music).
- **Technical verification:** FFprobe confirmed 15s, H.264/AAC, 1080×1920; FFmpeg volumedetect measured about −16.5dB mean and −1.1dB peak. Visual storyboard was inspected. The first render was black due to software PBR shader support; switching to tested Phong lighting fixed it. Extruded text transforms and crowded objects were corrected before final export.
- **Production dependencies:** Python 3.10+, vtk, numpy, Pillow, ffmpeg; Lato/Inter fonts at Linux-specific paths. Output location and dimensions currently use sandbox paths and prototype constants. Portability, performance, external media, human voice, true footage, photographic realism and full social platform testing are **not** solved.
- **Commercial and content limits:** $109 is illustrative gross at approximately $1.09 per thousand *verified eligible* views, conditional on campaign caps and approvals. A rejected clip may earn $0. No commercial spend, platform submissions or social publication. Never put private client media in GitHub.
- **Next creative test:** introduce an owned or licensed physical scene (hands, phone, studio desk) or a generated 3D narrative with realistic props, a distinctive original character, camera whip/transitions, natural voice-over and mixed sound. Compare two creative hooks in native TikTok player after explicit publication approval. More geometry alone won't guarantee attention.

Source copy also stored in SOVTIVA Website Drive folder as `SOVTIVA | True 3D Motion Video Engine V3 | Source.txt`. The rendered MP4 is a conversation artifact, not uploaded to the public GitHub repository.

## V4: Cinema Notes — refined 3D editorial short (11 November 2026)

**Purpose:** replace V3's blunt oversized 3D typography with more cinematic, deliberate visual storytelling for Sovtiva's own TikTok/Reels/Shorts tests. Not a customer case study and not published.

**Actual technical features:** off-screen VTK 3D rendering of a physical phone, metallic coin, two angled campaign statements and a studio nameplate. Independent geometry, real perspective camera positions, rim lighting and original self-generated procedural stereo audio. Spanish in-scene typography, softer palette, coherent visual margins and protected subtitle zone. Source: `tools/video-studio/cinema_notes_v4.py` (Python 3.10+, VTK, numpy, scipy, Pillow, FFmpeg). No Claude, paid model, sampled commercial song or downloaded footage.

**Observed test:** 372 rendered frames, 15.500 seconds at 24 fps. Native 3D scene rasterization 720×1280, exported/upscaled with Lanczos to 1080×1920 H.264 + AAC stereo; FFprobe verified streams, duration and dimensions. FFmpeg audio verification: mean -17.6 dB, peak -7.2 dB after correcting overly quiet first mix. Frame contact sheet generated from the exported video and visually inspected. Render process status=0. No social upload/metrics verified.

**Factual gate:** The example $109 *gross* is conditional on 100,000 campaign-eligible approved views and an illustrative $1.09/1K rate, subject to terms, caps and available budgets. Rejected/unsuccessful clips may earn $0; neither number is a guaranteed payout or verified creator income. On-screen paper explicitly says `EJEMPLO / NO ES UN PAGO`. Underlying editorial research: `/journal/higgsfield-seeded-paid-views-2026/es/`.

**Design changes over V3:** less competing text; a consistent 3D visual metaphor (phone → metallic payout token → campaign statement → rejection → studio mark); quiet camera dolly/orbit instead of hard rotations; softer lighting and color; fewer sound effects with atmospheric music; all explanatory visual text is now in Spanish; receipt size/placement revised to clear the lower caption safe zone.

**Limitations:** still a procedural stylized 3D animation, not filmed product footage or physically-based path-traced cinema. Original audio has no human voiceover. Final video is a local conversation artifact, not committed as a public video to the site or imported to Descript. Code has system-font assumptions and requires local dependencies and approved footage checks for adaptation. Visual mobile review and actual social retention have not been tested.

**Next creative decision:** compare this with one genuine camera-shot or licensed B-roll driven variant with voice, tighter hooks and richer tactile material/lighting, then obtain specific publication approval before release. Do not claim a production economics benchmark from the synthetic demo. No spending or social publication.
