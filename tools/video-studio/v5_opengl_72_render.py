#!/usr/bin/env python3
"""SOVTIVA V5 Shot A: repeatable, 72-frame Blender 5.3 OpenGL EEVEE test.
Runs against the exact uploaded V2.1 .blend. Original assets only; no paid tools.

This is a technical preview, NOT a finished or approved video.
"""
import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

import bpy

ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True)
ap.add_argument('--first', type=int, default=1)
ap.add_argument('--last', type=int, default=72)
ap.add_argument('--pct', type=int, default=55)
opt = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
if not (1 <= opt.first <= opt.last <= 72):
    raise ValueError('Frame range must be within 1..72')
if opt.pct not in (35, 55, 100):
    raise ValueError('Resolution percentage must be 35, 55 or 100')
OUT = Path(opt.out).expanduser().resolve()
FRAMES = OUT / 'frames'
FRAMES.mkdir(parents=True, exist_ok=True)
start = time.monotonic()
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.fps = 24
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = opt.pct
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.color_depth = '8'
scene.render.use_file_extension = True

result = {
    'project': 'SOVTIVA V5 / Shot A V2.1 / OpenGL recovery pass',
    'purpose': 'Detect and eliminate black/neon EEVEE frames; not production acceptance',
    'blender': bpy.app.version_string,
    'engine': scene.render.engine,
    'requested_backend_via_launcher': 'opengl',
    'observed_backend': 'Unverified: backend probe requires initialized GPU context; requested via CLI',
    'source': 'user-provided SOVTIVA_V5_SHOT_A_V21.blend',
    'range': [opt.first, opt.last],
    'fps': 24,
    'resolution': [1080, 1920],
    'render_pct': opt.pct,
    'original_scene_changed': False,
    'estimated_cost_usd': 0,
    'completed_frames': [],
    'quality_flags': [],
    'quality_inspection_method': 'numpy sample of Blender-decoded PNG RGBA, conservative artifact heuristic',
    'status': 'STARTED',
}

try:
    import numpy as np
except ImportError:
    np = None
    result['quality_inspection_method'] = 'NumPy unavailable: visual QA required on every frame'


def save():
    result['elapsed_seconds'] = round(time.monotonic() - start, 2)
    (OUT / 'benchmark.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')


def inspect_png(path):
    """Best-effort heuristic; a pass cannot replace inspection of the moving video."""
    if np is None:
        return {'status': 'NOT_CHECKED', 'reason': 'NumPy unavailable'}
    img = bpy.data.images.load(str(path), check_existing=False)
    try:
        width, height = img.size
        raw = np.empty(width * height * 4, dtype=np.float32)
        img.pixels.foreach_get(raw)
        rgb = raw.reshape(height, width, 4)[::7, ::7, :3]
        extreme_black = float((rgb.max(axis=2) < 0.018).mean())
        hot_red = float(((rgb[:, :, 0] > .55) & (rgb[:, :, 1] < .12) & (rgb[:, :, 2] < .12)).mean())
        hot_green = float(((rgb[:, :, 1] > .70) & (rgb[:, :, 0] < .17) & (rgb[:, :, 2] < .20)).mean())
        hot_blue = float(((rgb[:, :, 2] > .72) & (rgb[:, :, 0] < .16) & (rgb[:, :, 1] < .18)).mean())
        mean_brightness = float(rgb.mean())
        flags = []
        if extreme_black > .79 or mean_brightness < .016:
            flags.append('SUSPECT_NEAR_BLACK')
        if hot_red > .012:
            flags.append('SUSPECT_SATURATED_RED')
        if hot_green > .012:
            flags.append('SUSPECT_SATURATED_GREEN')
        if hot_blue > .012:
            flags.append('SUSPECT_SATURATED_BLUE')
        return {
            'status': 'HEURISTIC_FLAG' if flags else 'HEURISTIC_OK',
            'mean_brightness_linear': round(mean_brightness, 5),
            'fraction_very_black': round(extreme_black, 5),
            'fraction_hot_red': round(hot_red, 5),
            'fraction_hot_green': round(hot_green, 5),
            'fraction_hot_blue': round(hot_blue, 5),
            'flags': flags,
        }
    finally:
        bpy.data.images.remove(img)


try:
    for frame in range(opt.first, opt.last + 1):
        scene.frame_set(frame)
        destination = FRAMES / ('V5A_OpenGL_%04d.png' % frame)
        scene.render.filepath = str(destination)
        t = time.monotonic()
        print('V5_OPENGL_FRAME_START', frame, flush=True)
        bpy.ops.render.render(write_still=True)
        if not destination.exists() or destination.stat().st_size < 2048:
            raise RuntimeError('Missing/empty PNG after render: %s' % destination)
        try:
            image_check = inspect_png(destination)
        except Exception as qa_exc:
            image_check = {'status': 'NOT_CHECKED', 'reason': repr(qa_exc)}
            print('V5_OPENGL_QA_WARNING', frame, repr(qa_exc), flush=True)
        row = {'frame': frame, 'file': destination.name, 'bytes': destination.stat().st_size,
               'seconds': round(time.monotonic() - t, 3), 'quality': image_check}
        result['completed_frames'].append(row)
        if image_check['status'] != 'HEURISTIC_OK':
            result['quality_flags'].append({'frame': frame, 'result': image_check})
        print('V5_OPENGL_FRAME_DONE', frame, 'quality', image_check['status'], flush=True)
        save()
    result['status'] = 'COMPLETED_REQUIRES_MOTION_REVIEW' if not result['quality_flags'] else 'COMPLETED_WITH_QA_FLAGS'
    save()
    print('V5_OPENGL_ALL_FRAMES_RENDERED', len(result['completed_frames']), 'flags',
          len(result['quality_flags']), 'elapsed_seconds', result['elapsed_seconds'], flush=True)
except Exception as exc:
    result['status'] = 'RENDER_FAILED'
    result['error'] = repr(exc)
    save()
    traceback.print_exc()
    raise
