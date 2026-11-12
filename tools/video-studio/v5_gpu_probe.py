#!/usr/bin/env python3
"""SOVTIVA V5 / non-destructive Blender 5.3 ARM GPU QA probe.
Loads the supplied V2.1 .blend before this script runs. Renders only a tiny test
subset and uses original scene materials. No media downloads or paid services.
"""
from __future__ import annotations
import bpy, sys, time, json, traceback, argparse, platform, struct
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--engine',choices=['eevee','cycles'],required=True)
ap.add_argument('--out',required=True)
ap.add_argument('--samples',type=int,default=8)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(a.out).expanduser().resolve()
OUT.mkdir(parents=True, exist_ok=True)
start=time.monotonic()
scene=bpy.context.scene
scene.render.engine='CYCLES' if a.engine=='cycles' else 'BLENDER_EEVEE'
scene.render.fps=24
scene.render.resolution_x=1080
scene.render.resolution_y=1920
scene.render.resolution_percentage=35 if a.engine=='cycles' else 55
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGB'
scene.render.image_settings.color_depth='8'
scene.render.use_file_extension=True
scene.render.film_transparent=False
if a.engine=='cycles':
    scene.cycles.device='CPU'
    scene.cycles.samples=max(4,a.samples)
    if hasattr(scene.cycles,'use_denoising'):
        scene.cycles.use_denoising=True

try:
    import gpu
    backend=gpu.platform.backend_type_get()
except Exception as exc:
    backend='unknown ('+str(exc)+')'

report={
    'purpose':'GPU black/neon frame diagnosis; NOT a finished V5 video',
    'blender':bpy.app.version_string, 'engine':scene.render.engine,
    'requested_gpu_backend':a.engine=='eevee' and 'opengl' or 'not applicable: Cycles CPU',
    'observed_backend':str(backend),'samples':a.samples,
    'render_percentage':scene.render.resolution_percentage,
    'frame_numbers':([1,18,27,42,60,66] if a.engine=='eevee' else [42]),
    'results':[], 'status':'STARTED', 'no_spend':True,
}

def save():
    report['elapsed_seconds']=round(time.monotonic()-start,2)
    (OUT/'benchmark.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')

def png_dimensions(path):
    with open(path,'rb') as f:
        h=f.read(24)
    if h[:8]!=b'\x89PNG\r\n\x1a\n':
        raise RuntimeError('Not a valid PNG signature: '+str(path))
    return list(struct.unpack('>II',h[16:24]))

try:
    for frame in report['frame_numbers']:
        t=time.monotonic()
        scene.frame_set(frame)
        p=OUT/('diagnostic_frame_%04d.png'%frame)
        scene.render.filepath=str(p)
        print('DIAGNOSTIC_BEGIN',a.engine,frame,'backend',backend,flush=True)
        bpy.ops.render.render(write_still=True)
        if not p.exists() or p.stat().st_size<2048:
            raise RuntimeError('Missing or empty PNG '+str(p))
        dimensions=png_dimensions(p)
        expected=[round(1080*scene.render.resolution_percentage/100),
                  round(1920*scene.render.resolution_percentage/100)]
        report['results'].append({
            'frame':frame,'file':p.name,'bytes':p.stat().st_size,
            'dimensions':dimensions,'elapsed_seconds':round(time.monotonic()-t,2)
        })
        save()
        print('DIAGNOSTIC_RENDERED',frame,dimensions,round(time.monotonic()-t,2),'sec',flush=True)
    report['status']='RENDERED_IMAGES_REQUIRE_VISUAL_QA'
    save()
    print('DIAGNOSTIC_FINISHED',OUT,flush=True)
except Exception as exc:
    report['status']='RENDER_ERROR'
    report['error']=repr(exc)
    save()
    traceback.print_exc()
    raise
