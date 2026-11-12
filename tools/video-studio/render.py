#!/usr/bin/env python3
"""Sovtiva Video Studio: a rights-gated local vertical-video starter. stdlib + FFmpeg."""
import argparse
import hashlib
import json
import shutil
import subprocess
import time
import textwrap
from pathlib import Path


def run(cmd, cwd=None):
    result = subprocess.run([str(part) for part in cmd], cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {cmd[0]}\n{result.stderr[-1800:]}")
    return result.stdout.strip()


def ass_time(seconds):
    n = int(round(float(seconds) * 100))
    return f"{n // 360000}:{(n // 6000) % 60:02}:{(n // 100) % 60:02}.{n % 100:02}"


def escape_ass(s):
    return s.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", r"\N")


def subtitles(segments, duration, destination, w, h):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: %d
PlayResY: %d
WrapStyle: 2
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sovtiva,DejaVu Sans,%d,&H00FFFFFF,&H00FFFFFF,&H0012232A,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,75,75,%d,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" % (w, h, max(23, round(w * .057)), int(h * .16))
    lines = []
    for seg in segments:
        a, b, text = float(seg["start"]), float(seg["end"]), str(seg["text"]).strip()
        if not 0 <= a < b <= duration + .05:
            raise ValueError("Each subtitle must start/end within the selected clip length")
        if not text or len(text) > 120:
            raise ValueError("Subtitle text must have 1–120 characters")
        wrapped = textwrap.wrap(text, width=24, break_long_words=False, break_on_hyphens=False)
        if len(wrapped) > 2 or any(len(line) > 28 for line in wrapped):
            raise ValueError("Caption too long: shorten or split into smaller timed segments")
        lines.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Sovtiva,,0,0,0,,{escape_ass(chr(10).join(wrapped))}")
    destination.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def main(project_path):
    started = time.monotonic()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("Install FFmpeg and ffprobe and add both to PATH")
    project_path = Path(project_path).resolve()
    p = json.loads(project_path.read_text(encoding="utf-8"))
    rights = p.get("rights", {})
    if rights.get("status") != "APPROVED" or not rights.get("owner") or not rights.get("basis"):
        raise PermissionError("Rights gate: set rights.status=APPROVED and document owner + basis first")
    base = project_path.parent
    src = (base / p["source"]).resolve()
    if not src.is_file():
        raise FileNotFoundError("Source file missing. Supply authorized local video in project.source")
    out = (base / p.get("output_dir", "out")).resolve()
    if src == out or out in src.parents:
        raise ValueError("Do not put the input file inside the output directory")
    out.mkdir(parents=True, exist_ok=True)
    stage = out / "_stage"
    stage.mkdir(exist_ok=True)
    clip = p.get("clip", {})
    start, end = float(clip.get("start", 0)), float(clip.get("end", 0))
    duration = round(end - start, 3)
    if start < 0 or duration <= 0 or duration > 180:
        raise ValueError("Specify clip.start and clip.end (up to 180s, start >= 0)")
    w, h = int(p.get("width", 1080)), int(p.get("height", 1920))
    if w < 240 or h < 400 or h <= w or w % 2 or h % 2:
        raise ValueError("Output must be portrait with even dimensions, minimum 240x400")
    caps_file = (base / p.get("captions", "captions.json")).resolve()
    segments = json.loads(caps_file.read_text(encoding="utf-8")) if caps_file.exists() else []
    subtitles(segments, duration, stage / "captions.ass", w, h)
    ffprobe_audio = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", src])
    audio = bool(ffprobe_audio.strip())
    filter_v = (f"[0:v]split=2[bg][fg];[bg]scale={w}:{h}:force_original_aspect_ratio=increase,"
                f"crop={w}:{h},boxblur=20:1[blur];[fg]scale={w}:{h}:force_original_aspect_ratio=decrease[fgfit];"
                f"[blur][fgfit]overlay=(W-w)/2:(H-h)/2" + (",subtitles=captions.ass" if segments else "") + "[v]")
    mp4 = out / "master_vertical.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", start, "-i", src, "-t", duration,
           "-filter_complex", filter_v, "-map", "[v]"]
    if audio:
        cmd += ["-map", "0:a:0", "-af", "loudnorm=I=-16:LRA=11:TP=-1.5", "-c:a", "aac", "-b:a", "160k"]
    else:
        cmd += ["-an"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4]
    run(cmd, cwd=stage)
    thumb = out / "thumbnail.jpg"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", max(.1, min(1.5, duration / 2)), "-i", mp4,
         "-frames:v", "1", "-q:v", "3", thumb])
    sheet = out / "qa_contact_sheet.jpg"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mp4,
         "-vf", "fps=1/3,scale=270:-2,tile=3x2:padding=8:margin=8:color=0x102c36", "-frames:v", "1", "-update", "1", sheet])
    probe = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-show_entries", "format=duration", "-of", "json", mp4]))
    stream = probe["streams"][0]
    if (stream["width"], stream["height"]) != (w, h):
        raise RuntimeError("Rendered dimensions failed QA")
    manifest = {"status": "RENDERED_NEEDS_HUMAN_QA", "published": False, "paid": False,
                "rights_status": rights["status"], "rights_basis": rights["basis"], "rights_owner": rights["owner"],
                "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "duration_s": float(probe["format"]["duration"]),
                "width": w, "height": h, "captions": len(segments), "has_audio": audio,
                "render_seconds": round(time.monotonic() - started, 2),
                "files": [x.name for x in (mp4, thumb, sheet)],
                "editor_review": "PENDING", "publication_approval": "NOT_GRANTED"}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(mp4), "manifest": str(out / "manifest.json"), "status": manifest["status"]}, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local rights-gated SOVTIVA vertical video renderer")
    parser.add_argument("project", help="Project JSON with an authorized source and edit times")
    main(parser.parse_args().project)
