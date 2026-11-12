# SOVTIVA V5 — Production Bible / Decision Log
**State:** RESEARCHED / PREPRODUCTION ONLY, not filmed, rendered or published. **Creative North Star:** V3's bold kinetic 3D and fun, not V4's softened restrained brochure style. **Version:** 11 Nov 2026. **Cost authorization:** $0. **AI:** ChatGPT and original production scripts; no Claude.

## Why the old renders are insufficient
- V3's true geometry uses VTK, Phong-style lighting and a 540×960 render upscaled to 1080×1920. V4 used 720×1280 geometry then upscale; both lack native-level material/reflection fidelity, voice-led story and a shot-based director/editor workflow.
- V5 must be a miniature film, not a moving slide or rotating product showcase. Preserve V3 energy while adding cinematic physical logic, a singular transformation and real sound.

## Output and scope
- Scripted **24s original vertical short** at 24fps, native 1080×1920 if hardware passes benchmark (576 final cut frames), saved with shot handles.
- 6 story scenes: phone count breaks reality → 3D tokens erupt → $109* coin reveals → paper campaign eligibility → rejection / $0 twist → seamless phone loop. Timings and acceptance are in `v5_shotlist.json`, source of truth for frame-level edits.
- Spoken original Spanish voice. Draft: “¿Cien mil vistas? Suena a fortuna. Pero a una tarifa ilustrativa de uno con cero nueve dólares por cada mil vistas válidas, son unos ciento nueve dólares brutos. Si no te aprueban, puede ser cero. Vistas no son ganancias.” Script is *unapproved* until final duration and financial source QA.
- V5 purpose is to demonstrate creative production and useful research, **not** to suggest creators typically earn $109. Per video figures require campaign terms, caps, verified eligible views, sufficient budget and approval.

## Core applications: no connector needed
1. Blender **5.2 LTS (5.2.4 as of 2026-11-11)** installed locally, **official Windows ARM installer available** for Snapdragon. Do not install a different architecture blindly. Official: https://www.blender.org/releases/5-2/ and https://code.blender.org/2025/08/blender-for-windows-on-arm/ . Current hardware and drivers must be benchmarked, not assumed adequate.
2. Blender Python `bpy` for one-shot/one-scene project generation. Use EEVEE for layout and 50%-resolution previews; optionally Cycles for selected hero shots. Build versioned .blend scene files and render image sequences (not a single uninterruptible MP4).
3. Assets: original phone, engraved coin, paper + original Sovtiva mark. Optional properly logged CC0 textures/HDRIs from Poly Haven or ambientCG (https://polyhaven.com/license, https://docs.ambientcg.com/license/). Maintain artifact IDs, creator, URL, license, date/rights check.
4. Color, edit, sound: free DaVinci Resolve 21.1 or already-working FFmpeg; Descript optional for source transcript/captions. Do not assume premium Resolve MCP available in free version. No paid Resolve Studio required for our initial cut.
5. GitHub **already connected**; current repo `sofiasovtiva/sovtiva-site` stores scripts, storyboards as non-sensitive source, shotlist, QA notes, manifest template. No GitHub App is required. **GitHub Pages is not a GPU renderer.** Keep large binary masters in private storage. Avoid GitHub Actions rendering until cost/hardware/licensing is known.
6. Research: TikTok public Creative Center for actual creative observations, YouTube Shorts retention dashboard after posting; optional vidIQ connector for reference analysis. Runway/Higgsfield for a difficult scene ONLY after specific permission and credit cost check.
7. Avoid automatic publication, purchased assets, subscribed tools or unlicensed music. Use an original soundtrack or multi-platform rights-cleared license; TikTok Commercial Music Library may not grant Instagram/YouTube use.

## Objective creative rules
- Purposeful motivated camera move every shot. No repetitive orbit/whip-pan just for the sake of motion.
- One focal subject per shot; touchable material imperfections, actual floor contact, edges/bevels, physically plausible inertia. Color direction navy/teal/burgundy/warm brass; strong highlights but no clipped whites.
- Lens work: macro 60–85mm for physical reveal, 28–35mm for chase, focus pulls motivated by object action; DOF must not obscure mandatory figures. Avoid an orthographic 'presentation' camera.
- Every major cut is an object transformation, match move or sound-motivated reveal. A phone-to-coin-to-receipt visual metaphor, not eight separate effects.
- Physical sound: first 2 seconds have a hook; original human narration gets priority in mix; foley and music support the beats. Avoid synthetic repetitive ‘boom’ preset from V2/V3.
- Captions inside platform-safe areas after verifying actual TikTok/IG/YT UI. Never claim universal numerical safe-zone offsets; inspect real preview.

## Ordered execution and gates
**Gate 1: TECH / no paid services.** Confirm Blender 5.2 LTS Windows ARM install; create one still with a physically based brass coin and three area lights. Render 1080×1920 at native res and measure CPU/GPU, RAM, time and errors. Create 5-second EEVEE preview. If render stalls / unacceptable, simplify scene and benchmark EEVEE, then use another authorized machine; do not silently provision a cloud GPU. Record actual timings in Drive.
**Gate 2: STORY.** Produce storyboard of 6–8 original stills plus low-res animatic (with rough human voice) and two alternate first-three-second hooks. Director approves story and 3D transformation before expensive material work.
**Gate 3: 3D.** Build scene scripts for A–F, common camera/material toolkit, physically based shaders (roughness, normals, metal), original device and conditional receipt. No fake payment screen UI. Add per-scene handles, frame logs and resumable renderer, single render at a time to avoid integrated GPU contention.
**Gate 4: EDIT/SOUND.** Compose 24-second cut from individual image sequences, make voice lead with foley synchronized, grade, captions, factual caveats. Create edit decision list and original audio-license manifest.
**Gate 5: QA.** Auto: ffprobe stream properties, correct 576 frames/24fps, no blank frames, no text/missing assets, luminance and color audit, true-peak internal target under -1 dBTP (internal not platform spec), caption overlays; manual: watch full output on phone with sound, judge readability, physics credibility, intrigue, clarity and flow. Repair at shot level and rerender only affected frames.
**Gate 6: REVIEW.** Human signoff for IP/rights, finance wording, fit and final edit; no automatic publish. After *separately authorized* posting, measure hold rate (where available), completions, replays, saves, shares, profile/website visits and qualified inquiries. A/B hooks with same main cut for meaningful comparison.

## Stop criteria for escalation
- If same creative concept fails 2 visual reviews, rewrite story not add particle effects.
- If 1080×1920 preview exceeds acceptable runtime, simplify materials and geometry, reduce viewport samples, use EEVEE first; keep final native-res test as gate.
- If funds/rights unknown, stop media creation; no 'free' footage assumed shareable.
- If optional image-to-video model improves one impossible cinematic shot, price it against the shot and require explicit spend approval. Synthetic generation is not guaranteed coherent between shots.

## Public sources and precedent (not Sovtiva proof)
- Blender LTS https://www.blender.org/releases/5-2/ ; Windows ARM https://code.blender.org/2025/08/blender-for-windows-on-arm/ ; license https://www.blender.org/about/license/
- Case study, independent: https://github.com/Leonxlnx/escapement . Author uses a production bible, shotlist, render queue, GPU lock, exposure QA, sound manifest, and also documents GPU failures. Respect the source's MIT code license and separate third-party media licenses; architecture inspiration only, original V5 scripts/scenes.
- TikTok Creative Center https://ads.tiktok.com/help/article/creative-center?lang=en ; video guide https://ads.tiktok.com/business/en/guides/video-advertising-guide ; commercial music https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/commercial-use-of-music-on-tiktok
- Resolve https://www.blackmagicdesign.com/media/partial/release/20260908-03
- Poly Haven / ambientCG as above.
- Sovtiva public research: https://sovtiva.com/journal/cinematic-3d-video-blender-tiktok-workflow-2026/ and /es/
- Existing SOP: https://docs.google.com/document/d/11lADj2_gvFpnX3sk1ieNyA88zkSut5ZqFe0W5hSqq_s/edit

## Current verified vs not
VERIFIED: V3/V4 source and their described recorded tests; official Blender Windows ARM and 5.2 LTS availability; public original research article; repo files written and read back when completed.
NOT VERIFIED: Blender installed on the target device; native-res Cycles shot; material realism; actual production time; professional finished V5; social posting or view performance; paid tool accounts. Do not mark the pipeline as deployed.
