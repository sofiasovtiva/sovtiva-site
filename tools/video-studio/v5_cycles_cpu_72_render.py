#!/usr/bin/env python3
"""SOVTIVA V5 Shot A -- 3-second deterministic CPU Cycles render.

Run with Blender 5.3 on Windows ARM (no paid services, no drivers, no GPU).
Uses the user's original .blend unchanged, renders PNGs with Cycles CPU, and
packages metrics plus a browser-compatible preview. This renderer does NOT
modify the original .blend file or claim to have produced the final V5 film.
"""
import argparse
import json
import struct
import sys
import time
import traceback
from pathlib import Path

import bpy

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--samples', type=int, default=12)
parser.add_argument('--pct', type=int, choices=[35, 55, 100], default=55)
parser.add_argument('--first', type=int, default=1)
parser.add_argument('--last', type=int, default=72)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
if not (1 <= args.first <= args.last <= 72):
    raise ValueError('Frame indices must be in the range 1..72')
if not (4 <= args.samples <= 1024):
    raise ValueError('Invalid samples value: must be 4..1024')

OUT = Path(args.out).expanduser().resolve()
FRAMES = OUT / 'frames'
FRAMES.mkdir(parents=True, exist_ok=True)
t0 = time.monotonic()
s = bpy.context.scene
s.render.engine = 'CYCLES'
s.cycles.device = 'CPU'
s.cycles.samples = args.samples
s.render.resolution_x = 1080
s.render.resolution_y = 1920
s.render.resolution_percentage = args.pct
s.render.fps = 24
s.render.film_transparent = False
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
s.render.image_settings.color_depth = '8'
s.render.use_file_extension = True
# These are conservative CPU settings; material/camera animation is preserved.
for attr, value in [('max_bounces', 5), ('diffuse_bounces', 2),
                    ('glossy_bounces', 3), ('transmission_bounces', 3)]:
    if hasattr(s.cycles, attr):
        setattr(s.cycles, attr, value)
if hasattr(s.cycles, 'use_denoising'):
    s.cycles.use_denoising = True
for layer in s.view_layers:
    if hasattr(layer, 'cycles') and hasattr(layer.cycles, 'use_denoising'):
        layer.cycles.use_denoising = True

try:
    import numpy as np
except ImportError:
    np = None

report = {
    'project': 'SOVTIVA V5 Shot A / free CPU Cycles reliability pass',
    'status': 'STARTED',
    'blender_version': bpy.app.version_string,
    'engine': s.render.engine,
    'device': s.cycles.device,
    'frames_expected': args.last - args.first + 1,
    'fps': 24,
    'native_resolution': [1080, 1920],
    'render_percentage': args.pct,
    'preview_resolution': [round(1080 * args.pct / 100), round(1920 * args.pct / 100)],
    'samples': args.samples,
    'source': 'SOVTIVA_V5_SHOT_A_V21.blend (user-supplied, not overwritten)',
    'cost_usd': 0,
    'completed_frames': [],
    'quality_flags': [],
    'output_files': [],
    'backend_reason': 'Full EEVEE/OpenGL attempt produced 44 quality flags including 35 almost-black frames; clean Cycles CPU diagnostic reference',
}


def save_report():
    report['elapsed_seconds'] = round(time.monotonic() - t0, 2)
    (OUT / 'benchmark.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


def png_dims(path):
    with path.open('rb') as fh:
        header = fh.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        raise RuntimeError('Invalid PNG file: %s' % path)
    return list(struct.unpack('>II', header[16:24]))


def image_qa(path):
    """Heuristic cannot replace human motion QA; flags are conservative."""
    if np is None:
        return {'status': 'NOT_CHECKED', 'reason': 'numpy missing'}
    image = bpy.data.images.load(str(path), check_existing=False)
    try:
        w, h = image.size
        arr = np.empty(w * h * 4, dtype=np.float32)
        image.pixels.foreach_get(arr)
        rgb = arr.reshape((h, w, 4))[::8, ::8, :3]
        mx = rgb.max(axis=2)
        black = float((mx < .03).mean())
        r = float(((rgb[:, :, 0] > .65) & (rgb[:, :, 1] < .12) & (rgb[:, :, 2] < .12)).mean())
        g = float(((rgb[:, :, 1] > .72) & (rgb[:, :, 0] < .14)).mean())
        b = float(((rgb[:, :, 2] > .72) & (rgb[:, :, 0] < .14)).mean())
        mean = float(rgb.mean())
        flags = []
        if black > .93 or mean < .018:
            flags.append('NEAR_BLACK_OR_MISSING_LIGHT')
        if r > .15 or g > .15 or b > .15:
            flags.append('ABNORMAL_SATURATED_COLOR_FILL')
        return {'status': 'FLAG' if flags else 'OK',
                'mean_linear_brightness': round(mean, 5),
                'black_fraction': round(black, 5),
                'saturated_fractions': [round(r, 5), round(g, 5), round(b, 5)],
                'flags': flags}
    finally:
        bpy.data.images.remove(image)


def make_html():
    html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sovtiva V5 - CPU Cycles Shot A</title><style>body{background:#091923;color:#dceeed;font:16px system-ui;text-align:center}main{max-width:620px;margin:auto;padding:20px}img{height:75vh;max-width:95%;object-fit:contain}button{background:#234e59;color:#fff;border:1px solid #8caeb5;border-radius:7px;padding:12px}input{width:70%}</style></head><body><main><h2>Sovtiva / V5 Shot A / Cycles CPU</h2><img id="frame" alt="3D animation frame" src="frames/V5A_CPU_0001.png"><p><button id="play">Pause</button> <input id="seek" type="range" min="1" max="72" value="1"><span id="num">1/72</span></p><small>3s at 24 fps, silent original 3D render; not final film.</small></main><script>const im=document.getElementById('frame'),seek=document.getElementById('seek'),num=document.getElementById('num'),btn=document.getElementById('play');let playing=true,t0=performance.now(),last=0;function show(n){if(n===last)return;last=n;im.src='frames/V5A_CPU_'+String(n).padStart(4,'0')+'.png';seek.value=n;num.textContent=n+'/72';}function tick(t){if(playing)show(Math.floor((t-t0)*24/1000)%72+1);requestAnimationFrame(tick);}btn.onclick=()=>{playing=!playing;btn.textContent=playing?'Pause':'Play';if(playing)t0=performance.now()-(+seek.value-1)*1000/24};seek.oninput=()=>{playing=false;btn.textContent='Play';last=0;show(+seek.value)};requestAnimationFrame(tick);</script></body></html>'''
    (OUT / 'OPEN_PREVIEW_IN_BROWSER.html').write_text(html, encoding='utf-8')
    report['output_files'].append('OPEN_PREVIEW_IN_BROWSER.html')


try:
    # Save normal scene data only to output; do not modify/write source .blend.
    for fr in range(args.first, args.last + 1):
        p = FRAMES / ('V5A_CPU_%04d.png' % fr)
        s.frame_set(fr)
        s.render.filepath = str(p)
        begin = time.monotonic()
        print('V5_CPU_FRAME_START', fr, flush=True)
        bpy.ops.render.render(write_still=True)
        if not p.exists() or p.stat().st_size < 2048:
            raise RuntimeError('Missing or empty PNG: %s' % p)
        dim = png_dims(p)
        if dim != report['preview_resolution']:
            raise RuntimeError('Unexpected PNG dimensions for frame %s: %s' % (fr, dim))
        try:
            qa = image_qa(p)
        except Exception as exc:
            qa = {'status': 'NOT_CHECKED', 'reason': repr(exc)}
        elapsed = round(time.monotonic() - begin, 2)
        report['completed_frames'].append({'frame': fr, 'png': p.name, 'elapsed_seconds': elapsed, 'quality': qa})
        if qa['status'] != 'OK':
            report['quality_flags'].append({'frame': fr, 'quality': qa})
        print('V5_CPU_FRAME_FINISHED', fr, 'seconds', elapsed, 'quality', qa['status'], flush=True)
        save_report()
        # Abort severe persistent failures rather than waste a full CPU render.
        flags = report['quality_flags']
        if len(flags) >= 2 and flags[-1]['frame'] == fr and flags[-2]['frame'] == fr-1:
            if all('NEAR_BLACK_OR_MISSING_LIGHT' in x['quality'].get('flags', []) or 'ABNORMAL_SATURATED_COLOR_FILL' in x['quality'].get('flags', []) for x in flags[-2:]):
                raise RuntimeError('Two consecutive severely corrupted frames: %d-%d; aborting to avoid wasted CPU time' % (fr - 1, fr))
    make_html()
    report['status'] = 'COMPLETE_REQUIRES_HUMAN_REVIEW' if not report['quality_flags'] else 'COMPLETE_WITH_QA_FLAGS'
    report['output_files'].append('frames/V5A_CPU_0001.png ... 0072.png')
    save_report()
    print('V5_CPU_ALL_FRAMES_RENDERED', len(report['completed_frames']), 'QA_FLAGS', len(report['quality_flags']), flush=True)
except Exception as exc:
    report['status'] = 'FAILED_OR_STOPPED_FOR_QA'
    report['error'] = repr(exc)
    save_report()
    traceback.print_exc()
    raise
