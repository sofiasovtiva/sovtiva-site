#!/usr/bin/env python3
"""Sovtiva social-video prototype: rights-gated original editorial story cards.

Generates a silent portrait MP4 plus storyboard images/manifest, using Pillow + FFmpeg.
No paid API, no AI voice, no scraping, no publishing. Human review required.
"""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PALETTE = {
    "navy": "#0B2734", "navy2": "#143E49", "aqua": "#B8E6EC",
    "paper": "#EEECE4", "burgundy": "#672D43", "olive": "#657961",
    "ink": "#0B2734", "muted": "#BDD1D2", "white": "#F7F8F3",
}
FONT_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
FONT_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def font(size, bold=False):
    for candidate in (FONT_BOLD if bold else FONT_REGULAR):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    raise RuntimeError("Install a common system TrueType font (DejaVu or Segoe UI)")


def wrap(text, target_px, drawable, fnt):
    result, line = [], ""
    for word in str(text).split():
        candidate = (line + " " + word).strip()
        if drawable.textbbox((0, 0), candidate, font=fnt)[2] <= target_px or not line:
            line = candidate
        else:
            result.append(line)
            line = word
    if line:
        result.append(line)
    return result


def fitted_lines(draw, text, width_px, max_lines, start_size, min_size):
    for size in range(start_size, min_size-1, -2):
        ft = font(size, True)
        lines = wrap(text, width_px, draw, ft)
        if len(lines) <= max_lines and all(draw.textbbox((0, 0), ln, font=ft)[2] <= width_px for ln in lines):
            return ft, lines, size
    raise ValueError("Headline too long for the safe area. Shorten it; don't silently shrink to illegible text")


def draw_lines(draw, lines, xy, ft, color, gap=1.17):
    x,y=xy
    size=ft.size
    for line in lines:
        draw.text((x,y), line, fill=color, font=ft, stroke_width=0)
        y += int(size*gap)
    return y


def make_card(scene, idx, n, w, h):
    kind = scene.get("theme", ["navy", "paper", "burgundy", "navy2", "olive"][idx % 5])
    if kind not in ("navy", "paper", "burgundy", "navy2", "olive"):
        raise ValueError("Unsupported theme")
    dark = kind != "paper"
    bg=PALETTE[kind]
    fg=PALETTE["white"] if dark else PALETTE["ink"]
    secondary=PALETTE["muted"] if dark else "#4F6D73"
    highlight=PALETTE["aqua"] if dark else PALETTE["burgundy"]
    image=Image.new("RGB", (w,h), bg)
    d=ImageDraw.Draw(image)
    sx=w/1080.0
    def q(v): return max(1,round(v*sx))
    margin=q(84)
    right=w-margin
    # Original abstract editorial geometry, not generated footage.
    d.rounded_rectangle((margin,q(130),right,q(137)), radius=q(4), fill=highlight)
    d.rounded_rectangle((right-q(180), q(175), right+q(100), q(302)), radius=q(35), outline=secondary, width=q(3))
    d.rounded_rectangle((margin-q(190),h-q(550),margin+q(260),h-q(175)),radius=q(48),outline=secondary,width=q(2))
    d.rectangle((margin,q(1340),margin+q(12),q(1480)),fill=highlight)
    d.text((margin,q(56)), "sovtiva.", font=font(q(48),True), fill=fg)
    d.text((right, q(66)), f"STUDIO / {idx+1:02d}", font=font(q(24),True), fill=secondary, anchor="ra")
    kicker=str(scene.get("kicker", "SOVTIVA / EXPLAINED")).upper().strip()
    if len(kicker)>45: raise ValueError("kicker too long")
    d.text((margin,q(325)), kicker, font=font(q(26),True), fill=highlight)
    headline=scene.get("headline","").strip()
    if not headline: raise ValueError("Every scene needs a headline")
    ft, lines, size = fitted_lines(d,headline,right-margin,q(5),q(78),q(48))
    yy=draw_lines(d,lines,(margin,q(430)),ft,fg,1.21)
    body=str(scene.get("body","")).strip()
    if body:
        if len(body)>180: raise ValueError("Scene body too long; use a new scene")
        fbody=font(q(36))
        blines=wrap(body,right-margin-q(10),d,fbody)
        if len(blines)>5: raise ValueError("Body too long for safe area")
        yy=max(yy+q(95),q(890))
        if yy+len(blines)*q(51)>h-q(350): raise ValueError("Content overlaps the footer. Shorten headline/body")
        draw_lines(d,blines,(margin,yy),fbody,fg,1.42)
    source=str(scene.get("source", "")).strip()
    if source:
        if len(source)>110: raise ValueError("Source too long for end card")
        fs=font(q(23))
        sl=wrap(source, right-margin, d, fs)
        if len(sl)>2: raise ValueError("Shorten source note")
        draw_lines(d,sl,(margin,h-q(315)),fs,secondary,1.5)
    # Platform-safe lower area: keep bottom 15% uncluttered.
    progress_top=h-q(210)
    available=right-margin
    step=available/n
    for k in range(n):
        a=margin+round(k*step)
        b=margin+round((k+1)*step-q(10))
        d.rounded_rectangle((a,progress_top,b,progress_top+q(7)),radius=q(4),fill=(highlight if k<=idx else secondary))
    d.text((margin,h-q(150)),"ORIGINAL RESEARCH  /  SOVTIVA",font=font(q(21),True),fill=secondary)
    d.text((right,h-q(151)),f"{idx+1:02d} / {n:02d}",font=font(q(22),True),fill=secondary,anchor="ra")
    return image


def main(config):
    began=time.monotonic()
    config=Path(config).resolve()
    p=json.loads(config.read_text(encoding="utf-8"))
    rights=p.get("rights",{})
    if rights.get("status")!="APPROVED" or not rights.get("owner") or not rights.get("basis"):
        raise PermissionError("Rights gate: approved owned/editorial material and documented basis are required")
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("FFmpeg and ffprobe must be installed and on PATH")
    scenes=p.get("scenes", [])
    if not isinstance(scenes, list) or len(scenes)<2 or len(scenes)>8:
        raise ValueError("Use 2–8 scenes for a short original video")
    w=int(p.get("width",1080));h=int(p.get("height",1920))
    if w<360 or h<640 or w>=h or w%2 or h%2:
        raise ValueError("Use portrait, even dimensions, minimum 360x640")
    output=(config.parent/p.get("output_dir","out_social")).resolve()
    output.mkdir(parents=True,exist_ok=True)
    images=[];duration=0
    for i,scene in enumerate(scenes):
        seconds=float(scene.get("seconds",3.0))
        if seconds<1.6 or seconds>7.0: raise ValueError("Use 1.6–7 seconds per scene")
        duration+=seconds
        slide=make_card(scene,i,len(scenes),w,h)
        path=output/f"scene_{i+1:02d}.png"
        slide.save(path, optimize=True)
        images.append((path,seconds))
    contact_w=min(w,540)
    thumbs=[]
    for path,_ in images:
        im=Image.open(path)
        nw=round(contact_w/2)
        nh=round(h*(nw/w))
        thumbs.append(im.resize((nw,nh)))
    tw=2*thumbs[0].width; th=math.ceil(len(thumbs)/2)*thumbs[0].height
    sheet=Image.new("RGB",(tw,th),"#E7EAE7")
    for i,im in enumerate(thumbs):sheet.paste(im,((i%2)*im.width,(i//2)*im.height))
    sheet.save(output/"storyboard_contact_sheet.jpg",quality=90)
    # Encode scene clips without shell interpolation, then concat in controlled order.
    clips=[]
    for i,(image_path,sec) in enumerate(images):
        clip=output/f"_scene_{i+1:02d}.mp4"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(image_path),"-t",str(sec),"-r","24","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",str(clip)],check=True)
        clips.append(clip)
    concat=output/"_input.ffconcat"
    def quote(p):return str(p.resolve()).replace("\\", "/").replace("'", "'\\''")
    concat.write_text("ffconcat version 1.0\n"+"\n".join("file '"+quote(c)+"'" for c in clips)+"\n",encoding="utf-8")
    result=output/"draft_social_vertical.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",str(concat),"-c","copy","-movflags","+faststart",str(result)],check=True)
    probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height","-of","json",str(result)],capture_output=True,text=True,check=True)
    metadata=json.loads(probe.stdout)
    first=metadata["streams"][0]
    if first["width"]!=w or first["height"]!=h: raise RuntimeError("Output dimensions mismatch")
    manifest={"status":"DRAFT_NEEDS_HUMAN_QA","published":False,"audio":"none","distribution_approved":False,"rights_status":"APPROVED","rights_basis":rights["basis"],"scene_count":len(scenes),"duration_seconds":round(float(metadata["format"]["duration"]),2),"width":w,"height":h,"render_seconds":round(time.monotonic()-began,2),"script_sha256":hashlib.sha256(config.read_bytes()).hexdigest(),"files":["draft_social_vertical.mp4","storyboard_contact_sheet.jpg"],"review":"PENDING","provenance_note":"All visuals and text must originate from Sovtiva or have reuse rights; claims require source checks"}
    (output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"output":str(result),"manifest":str(output/"manifest.json"),"status":manifest["status"]},ensure_ascii=False))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Create original Sovtiva silent portrait social cards")
    parser.add_argument("project",help="Story JSON with owned editorial source rights and 2–8 scenes")
    args=parser.parse_args()
    main(args.project)
