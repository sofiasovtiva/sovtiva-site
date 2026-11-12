#!/usr/bin/env python3
"""SOVTIVA V5 — Shot A V2.1 | free, original 3D source for Blender 5.3.

Creates one 3-second, frame-accurate 24fps opening shot: a macro phone count
reaches 100,000 and a dimensional brass token physically breaches the glass.
An angled 3/4 camera flies with the token, amid a few shards and coins.

Run on Windows with included RUN_V5_SHOT_A_V21.bat; no subscriptions, stock
assets, third-party footage, music, downloading, or paid API calls.

**This revised script is syntax-checked; animation rendering must be tested in Blender 5.3.**
User must run it locally in an installed Blender 5.3 and share result for QA.
"""
from __future__ import annotations
import sys, json, math, random, time, traceback
from pathlib import Path
import bpy
from mathutils import Vector

P = __import__('argparse').ArgumentParser()
P.add_argument('--mode', choices=('still', 'preview', 'full'), default='preview')
P.add_argument('--out', default='V5_A_V21_output')
P.add_argument('--engine', choices=('eevee', 'cycles'), default='eevee')
P.add_argument('--samples', type=int, default=24)
args = P.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
OUT = Path(args.out).expanduser().resolve()
OUT.mkdir(parents=True, exist_ok=True)
START = time.monotonic()
FPS, N = 24, 72

# ---- Production manifest and safe reset ----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
s = bpy.context.scene
s.frame_start, s.frame_end = 1, N
s.render.fps = FPS
s.render.resolution_x, s.render.resolution_y = 1080, 1920
s.render.resolution_percentage = 100
s.render.film_transparent = False
s.render.image_settings.color_mode = 'RGBA'
s.render.image_settings.color_depth = '8'
s.render.engine = 'BLENDER_EEVEE' if args.engine == 'eevee' else 'CYCLES'
if s.render.engine == 'CYCLES':
    s.cycles.device = 'CPU'
    s.cycles.samples = max(8, args.samples)
else:
    # EEVEE sampling APIs changed in Blender 5.x; default if unavailable.
    if getattr(s, 'eevee', None) is not None and hasattr(s.eevee, 'taa_render_samples'):
        s.eevee.taa_render_samples = max(8, args.samples)
try:
    s.view_settings.view_transform = 'AgX'
except Exception:
    pass
try:
    s.view_settings.look = 'Medium High Contrast'
except Exception:
    pass
# Keep low-key while preserving the brass highlight rolloff.
try:
    s.view_settings.exposure = -0.65
except Exception:
    pass

world = bpy.data.worlds.new('STUDIO / deep ink atmosphere')
s.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (.005, .009, .016, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = .13

INK = (.013, .029, .038, 1)
JADE = (.018, .11, .135, 1)
EDGE = (.23, .51, .54, 1)
BRASS = (.58, .295, .075, 1)
GOLD = (.90, .59, .21, 1)
SILVER = (.48, .74, .78, 1)
CREAM = (.88, .90, .83, 1)
WINE = (.26, .033, .096, 1)


def mat(name, color, metallic=0, rough=.45, coat=0, micro=0, scale=120, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    tree = m.node_tree
    bs = tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = color
    bs.inputs['Metallic'].default_value = metallic
    bs.inputs['Roughness'].default_value = rough
    inp = bs.inputs.get('Coat Weight') or bs.inputs.get('Clearcoat')
    if inp is not None:
        inp.default_value = coat
    if emission:
        ei = bs.inputs.get('Emission Color') or bs.inputs.get('Emission')
        es = bs.inputs.get('Emission Strength')
        if ei is not None: ei.default_value = color
        if es is not None: es.default_value = emission
    if micro:
        noise = tree.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = scale
        noise.inputs['Detail'].default_value = 2.0
        bump = tree.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = micro
        bump.inputs['Distance'].default_value = .012
        tree.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        tree.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m

m_ink = mat('CERAMIC / midnight titanium', INK, .48, .27, .35, .018)
m_screen = mat('GLASS / quiet jade', JADE, .13, .23, .45, .002)
m_brass = mat('BRASS / satin metal with fine imperfections', BRASS, .95, .28, .09, .024, 150)
m_gold = mat('GOLD / milled chamfer', GOLD, .91, .25, .13, .010, 120)
m_silver = mat('SHARDS / silvered translucent-edge glass', SILVER, .48, .19, .34)
m_milk = mat('CERAMIC / ivory lettering', CREAM, .04, .41)
m_wine = mat('ACCENT / smoked burgundy', WINE, .68, .25)
m_stage = mat('STAGE / matte dark concrete', (.014, .026, .035, 1), .10, .55, .07, .007)
m_back = mat('WALL / deep charcoal', (.005, .010, .015, 1), .02, .74)
m_rail = mat('PRACTICAL / cyan light', (.09, .38, .41, 1), .33, .28, emission=.6)


def box(name, xyz, dims, surface, bevel=0, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=xyz)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(surface)
    if bevel:
        mod = o.modifiers.new('manufactured rounded edges', 'BEVEL')
        mod.width, mod.segments = bevel, 5
        o.modifiers.new('weighted normals', 'WEIGHTED_NORMAL')
    if parent is not None:
        o.parent = parent
    return o


def cylinder(name, radius, depth, xyz, surface, parent=None, bevel=.016):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=radius, depth=depth, location=xyz)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = (math.pi / 2, 0, 0)
    o.data.materials.append(surface)
    if bevel:
        mod = o.modifiers.new('milled edge', 'BEVEL')
        mod.width = min(bevel, depth * .29)
        mod.segments = 4
        o.modifiers.new('weighted normals', 'WEIGHTED_NORMAL')
    if parent is not None:
        o.parent = parent
    return o


def torus(name, radius, tube, xyz, surface, parent=None):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radius, minor_radius=tube, major_segments=96,
        minor_segments=12, location=xyz)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = (math.pi / 2, 0, 0)
    o.data.materials.append(surface)
    if parent is not None:
        o.parent = parent
    return o


def text(name, message, xyz, size, surface, parent=None, extrude=.002):
    curve = bpy.data.curves.new(name, 'FONT')
    curve.body = message
    curve.align_x, curve.align_y = 'CENTER', 'CENTER'
    curve.size, curve.extrude = size, extrude
    curve.bevel_depth = .001 if extrude else 0
    ob = bpy.data.objects.new(name, curve)
    s.collection.objects.link(ob)
    ob.location = xyz
    ob.rotation_euler = (math.pi / 2, 0, 0)
    ob.data.materials.append(surface)
    if parent is not None:
        ob.parent = parent
    return ob


def root(name, parent=None):
    o = bpy.data.objects.new(name, None)
    s.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def key(o, frame, pos=None, rot=None, scale=None):
    if pos is not None:
        o.location = pos
        o.keyframe_insert(data_path='location', frame=frame)
    if rot is not None:
        o.rotation_euler = rot
        o.keyframe_insert(data_path='rotation_euler', frame=frame)
    if scale is not None:
        o.scale = (scale,) * 3
        o.keyframe_insert(data_path='scale', frame=frame)


def aim(cam, xyz):
    cam.rotation_euler = (Vector(xyz) - cam.location).to_track_quat('-Z', 'Y').to_euler()

# ---- Set: physical, visible depth and deliberate pools of light ----
box('Floor with actual contact shadows', (0, .6, -.18), (23, 22, .30), m_stage, .07)
box('Dark cyclorama rear wall', (0, 4.4, 5.0), (20, .14, 11), m_back)
box('Suspended key-light fixture / left', (-3.7, 2.2, 3.8), (.035, .055, 3.7), m_rail, .012)
box('Suspended fixture / right', (3.8, 3.3, 3.4), (.028, .045, 3.2), m_rail, .012)
# A small riser establishes where the object rests instead of a floating card.
box('Black studio riser', (-.05, .20, .075), (3.15, 1.15, .16), m_ink, .085)
box('Burgundy edging under riser', (-.05, -.31, -.002), (3.13, .038, .026), m_wine, .008)

# ---- Hero subject: phone with distinct sides, glass, controlled information ----
phone = root('PHONE / physically animated master')
phone.location = (-.12, .15, 2.27)
phone.rotation_euler = (math.radians(3), math.radians(-3), math.radians(15))
box('Phone / actual deep ceramic frame', (0, 0, 0), (1.95, .235, 3.57), m_ink, .155, phone)
box('Phone / narrow machined metal border', (0, -.115, 0), (1.83, .022, 3.45), m_gold, .095, phone)
box('Phone / dark translucent screen', (0, -.130, 0), (1.77, .020, 3.41), m_screen, .077, phone)
box('Phone / earpiece', (0, -.150, 1.52), (.32, .024, .022), m_gold, .008, phone)
box('Phone / physical side key', (.988, -.01, .68), (.036, .12, .23), m_wine, .01, phone)
text('Minimal UI brand', 'sovtiva.', (0, -.159, 1.24), .145, m_milk, phone)
text('Minimal UI label', 'VISTAS', (0, -.161, .56), .107, m_milk, phone)
# Count ticks instead of showing all copy at once.
counts = []
for idx, val in enumerate(('99,998', '99,999', '100,000')):
    o = text('Counter step ' + val, val, (0, -.166, .17), .31, m_milk, phone, .004)
    counts.append(o)
    segments = [(1, 11), (12, 21), (22, N)]
    start, end = segments[idx]
    key(o, 1, scale=(1 if start == 1 else .00001))
    if start > 1:
        key(o, start - 1, scale=.00001)
        key(o, start, scale=1)
    key(o, end, scale=1)
    if end < N:
        key(o, end + 1, scale=.00001)
# Add no large question / $109 / disclaimer in the opening: reserved for later shots.

# ---- Hero token: built as solid metal, physically breaches phone surface ----
def coin(name, r, detail=True):
    pivot = root(name)
    cylinder(name + '/thick minted core', r, .095, (0, 0, 0), m_brass, pivot, .024)
    cylinder(name + '/raised inner face', r * .82, .102, (0, -.004, 0), m_gold, pivot, .012)
    torus(name + '/machined outer rim', r * .90, .013, (0, -.058, 0), m_gold, pivot)
    torus(name + '/etched relief', r * .73, .006, (0, -.064, 0), m_ink, pivot)
    if detail:
        # A physical emblem rather than a prematurely revealed $109 number.
        text(name + '/mint emblem', 'S', (0, -.069, 0), r * .72, m_brass, pivot, .009)
        for j in range(8):
            a = j * 2 * math.pi / 8
            torus(name + '/radial rivet ' + str(j), .022, .006,
                  (math.cos(a) * r * .78, -.068, math.sin(a) * r * .78), m_gold, pivot)
    return pivot

hero = coin('HERO TOKEN / from digital to physical', .48)
hero.parent = phone
for f, position, rotation, size in [
    (1, (0, -.128, .04), (0, 0, 0), .0001),
    (19, (0, -.128, .04), (0, 0, 0), .0001),
    (25, (0, -.158, .04), (.03, .01, 0), .16),
    (34, (.06, -.56, .13), (.12, .26, -.06), .66),
    (45, (.30, -1.17, .32), (.22, -.34, -.13), .95),
    (60, (.63, -1.90, .58), (.34, -.18, -.19), 1.15),
    (72, (.83, -2.60, .74), (.24, .06, .01), 1.28),
]:
    key(hero, f, pos=position, rot=rotation, scale=size)

# Animated embossed glass stress ring visually makes contact with phone plane.
ring = torus('GLASS / radial compression ring', .36, .009, (0, -.166, .04), m_silver, phone)
for f, size in [(1, .001), (20, .001), (30, 1), (38, 1.44), (50, .001), (72, .001)]:
    key(ring, f, scale=size)

# Physical shards, not random floating titles. Original procedural triangles.
randomizer = random.Random(516)
for j in range(10):
    angle = 2 * math.pi * j / 10 + .16 * randomizer.random()
    mesh = bpy.data.meshes.new('GLASS triangular chip %02d' % j)
    R = .07 + .035 * (j % 3)
    verts = [(-R, 0, -R * .5), (R, 0, -R * .5), (R * .16, 0, R)]
    mesh.from_pydata(verts, [], [(0, 1, 2)])
    mesh.materials.append(m_silver)
    shard = bpy.data.objects.new('GLASS shard %02d' % j, mesh)
    s.collection.objects.link(shard)
    shard.parent = phone
    reach = 1.07 + .23 * (j % 3)
    tx, tz = math.cos(angle) * reach, .05 + math.sin(angle) * reach
    for f, xyz, rot, size in [
        (1, (0, -.165, .04), (0, 0, 0), .001),
        (25, (0, -.165, .04), (0, 0, 0), .001),
        (34, (.23 * tx, -.33, .04 + .23 * tz), (.10 * j, .1, .12 * j), .48),
        (47, (.62 * tx, -.82, .04 + .60 * tz), (.27 * j, .1 * j, .3 * j), .82),
        (72, (tx * 1.55, -1.54, .04 + tz * 1.7), (.41 * j, .31 * j, .44 * j), .65),
    ]:
        key(shard, f, pos=xyz, rot=rot, scale=size)

# Small supporting coins emerge with staggered trajectories. No overlap with
# the 100,000 count until the counter completes.
for j in range(5):
    c = coin('Secondary physical token %02d' % j, .10 + .033 * (j % 3), False)
    c.parent = phone
    ang = math.pi * .25 + j * 2.4
    tx = math.cos(ang) * (1.1 + .24 * (j % 2))
    tz = math.sin(ang) * (1.1 + .13 * (j % 3))
    moment = 34 + 3 * j
    for f, xyz, rot, size in [
        (1, (0, -.14, .04), (0, 0, 0), .0001),
        (moment, (0, -.14, .04), (0, 0, 0), .0001),
        (moment + 13, (tx * .54, -.78, .04 + tz * .54), (.16 * j, .23 * j, .35 * j), .62),
        (72, (tx * 1.42, -2.17, .04 + tz * 1.32), (.4 * j, .15 * j, .42 * j), 1),
    ]:
        key(c, f, pos=xyz, rot=rot, scale=size)

# Phone reacts to the event, then stabilizes. Mostly fixed to keep the set real.
for f, xyz, rot in [
    (1, (-.12, .15, 2.27), (.05, -.052, .262)),
    (19, (-.12, .15, 2.27), (.05, -.052, .262)),
    (25, (-.11, .15, 2.28), (.046, -.048, .269)),
    (30, (-.08, .15, 2.32), (.065, -.042, .284)),
    (37, (-.12, .15, 2.27), (.055, -.055, .255)),
    (72, (-.12, .15, 2.27), (.05, -.052, .262)),
]:
    key(phone, f, pos=xyz, rot=rot)


def area(name, position, target, power, rgb, size, shape='DISK'):
    light = bpy.data.lights.new(name, 'AREA')
    light.energy, light.color, light.size, light.shape = power, rgb, size, shape
    ob = bpy.data.objects.new(name, light)
    s.collection.objects.link(ob)
    ob.location = position
    aim(ob, target)
    return ob

# V2.1 grade correction based on user's actual still: reduce salmon wall wash,
# red/white clipping and micro-bump sparkle while retaining dark cinematic depth.
# Full animation is still unverified until Windows Blender actually renders it.
area('Large cold key / reflection edge', (2.7, -3.5, 5.5), (0, 0, 2.5), 520, (.75, .92, 1), 3.7)
area('Warm brass edge / contained', (-3.1, 1.7, 5.9), (0, -1, 2.8), 435, (1, .78, .55), 2.9)
area('Cyan glass edge', (4.0, .8, 3.2), (0, 0, 2.3), 270, (.28, .73, .78), 2.4)
area('Low neutral bounce', (0, -3.2, .9), (0, -.7, 2.0), 125, (.84, .91, .91), 1.8)

cam_data = bpy.data.cameras.new('CAM-A-V2 / motivated dolly and tracker')
cam = bpy.data.objects.new('CAM-A-V2 / motivated dolly and tracker', cam_data)
s.collection.objects.link(cam)
s.camera = cam
cam_data.type = 'PERSP'
cam_data.sensor_fit = 'VERTICAL'
cam_data.lens = 43
cam_data.clip_end = 150
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 7.1
focus = root('CAM / pull-focus target')
cam_data.dof.focus_object = focus
for fr, xyz, at, foc in [
    (1, (3.65, -9.8, 3.58), (-.15, 0, 2.24), (-.15, .0, 2.24)),
    (21, (3.45, -9.4, 3.53), (-.12, .0, 2.27), (-.12, .0, 2.27)),
    (38, (3.16, -8.45, 3.42), (.03, -.36, 2.4), (.07, -.58, 2.40)),
    (55, (2.80, -7.60, 3.48), (.46, -1.38, 2.61), (.38, -1.45, 2.66)),
    (72, (2.35, -6.95, 3.62), (.70, -1.90, 2.92), (.7, -2.35, 2.93)),
]:
    cam.location = xyz
    aim(cam, at)
    cam.keyframe_insert(data_path='location', frame=fr)
    cam.keyframe_insert(data_path='rotation_euler', frame=fr)
    key(focus, fr, pos=foc)

# Natural ease: avoid the robotic constant rotational speed from V3.
for ob in bpy.data.objects:
    action = ob.animation_data.action if ob.animation_data else None
    if action:
        try:
            for fc in action.fcurves:
                for k in fc.keyframe_points:
                    k.interpolation = 'BEZIER'
                    k.handle_left_type = 'AUTO_CLAMPED'
                    k.handle_right_type = 'AUTO_CLAMPED'
        except (AttributeError, TypeError):
            # Blender 5.3 layered actions can store f-curves in slots.
            # Default interpolation is Bezier; retain it on unsupported APIs.
            pass

# ---- Export strategy V2.1: PNG image sequence (Blender 5.3 portable). ----
# Why not FFMPEG? User's Windows ARM Blender 5.3 returned:
# TypeError enum "FFMPEG" not found in image_settings.file_format.
# PNG is reliably supported; the Windows BAT can use ffmpeg if already present,
# otherwise it creates a ZIP of the frames plus a standalone HTML preview.
# Blender cannot guarantee MP4 output on builds that omit FFmpeg.
scene_path = OUT / 'SOVTIVA_V5_SHOT_A_V21.blend'
s.frame_set(47)
bpy.ops.wm.save_as_mainfile(filepath=str(scene_path))

render_details = {
    'mode': args.mode,
    'scene': 'SOVTIVA V5 / SHOT A V2.1',
    'blender_version': bpy.app.version_string,
    'engine': s.render.engine,
    'fps': FPS,
    'intended_frames': N if args.mode != 'still' else 0,
    'full_frame_size': [1080, 1920],
    'preview_percentage': 55 if args.mode == 'preview' else 100,
    'render_samples_requested': args.samples,
    'stage': 'technical_local_render',
    'estimated_cost_usd': 0,
    'source_rights': '100% original procedural scene, no external assets',
    'export_method': 'native PNG frame sequence, no Blender FFMPEG enum',
    'output_files': [scene_path.name],
}


def write_benchmark(status, error=None):
    render_details['status'] = status
    render_details['elapsed_seconds'] = round(time.monotonic() - START, 2)
    if error:
        render_details['error'] = repr(error)
    (OUT / 'benchmark.json').write_text(
        json.dumps(render_details, indent=2, ensure_ascii=False), encoding='utf-8')


def generate_html_preview():
    # Pure local browser playback. Does not need ffmpeg, internet or libraries.
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Sovtiva V5 Shot A V2.1 | 24fps Preview</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#06151d;color:#e9f4f0;margin:0;font:16px system-ui;text-align:center}
main{max-width:650px;margin:20px auto;padding:0 15px}img{height:min(78vh,850px);max-width:95%;object-fit:contain;
background:#132532;border-radius:8px}button{font:inherit;border:1px solid #648288;border-radius:6px;
background:#183944;color:#f1f5ed;padding:9px 16px;cursor:pointer;margin:10px}
input{width:min(430px,85%)}small{display:block;color:#9ab9b8;line-height:1.6}</style></head><body>
<main><h2>Sovtiva / Shot A V2.1</h2><img id="frame" alt="Scene animation preview"
src="preview_frames/Shot_A_V21_0001.png"><div><button id="play">Pause</button>
<input type="range" id="scrub" min="1" max="72" value="1" step="1">
<span id="counter">01 / 72</span></div>
<small>24 fps · 72 Blender-rendered PNGs · silent, local preview · no extra software.</small></main>
<script>
const image=document.getElementById('frame'),slider=document.getElementById('scrub');
const counter=document.getElementById('counter'),button=document.getElementById('play');
let running=true,first=performance.now(),last=-1;
const path=n=>'preview_frames/Shot_A_V21_'+String(n).padStart(4,'0')+'.png';
function show(n){image.src=path(n);slider.value=n;counter.textContent=String(n).padStart(2,'0')+' / 72';}
function tick(t){if(running){const f=Math.floor((t-first)/1000*24)%72+1;if(f!==last){show(f);last=f;}}
 requestAnimationFrame(tick);}
button.onclick=()=>{running=!running;button.textContent=running?'Pause':'Play';if(running)first=performance.now()-(Number(slider.value)-1)/24*1000;};
slider.oninput=()=>{running=false;button.textContent='Play';show(Number(slider.value));last=Number(slider.value);};
requestAnimationFrame(tick);
</script></body></html>'''
    (OUT / 'OPEN_PREVIEW_IN_BROWSER.html').write_text(html, encoding='utf-8')
    render_details['output_files'].append('OPEN_PREVIEW_IN_BROWSER.html')


try:
    # Always render a new full-resolution still first for creative approval.
    s.render.resolution_percentage = 100
    s.render.image_settings.file_format = 'PNG'
    s.render.image_settings.color_mode = 'RGB'
    s.render.filepath = str(OUT / 'SOVTIVA_V5_SHOT_A_V21_still.png')
    bpy.ops.render.render(write_still=True)
    still = OUT / 'SOVTIVA_V5_SHOT_A_V21_still.png'
    if not still.exists() or still.stat().st_size < 8192:
        raise RuntimeError('Native 1080x1920 still missing or too small')
    render_details['output_files'].append(still.name)

    if args.mode != 'still':
        frames = OUT / 'preview_frames'
        frames.mkdir(parents=True, exist_ok=True)
        s.frame_set(1)
        s.render.resolution_percentage = 55 if args.mode == 'preview' else 100
        s.render.image_settings.file_format = 'PNG'
        s.render.image_settings.color_mode = 'RGB'
        s.render.filepath = str(frames / 'Shot_A_V21_')
        s.render.use_file_extension = True
        bpy.ops.render.render(animation=True)
        actual = sorted(frames.glob('Shot_A_V21_????.png'))
        missing = [f for f in range(1, N+1)
                   if not (frames / ('Shot_A_V21_%04d.png' % f)).exists()]
        if missing:
            raise RuntimeError('Animation PNG sequence incomplete: %s' % missing[:20])
        if len(actual) < N:
            raise RuntimeError('Only %d of %d PNGs produced' % (len(actual), N))
        render_details['rendered_frame_count'] = N
        render_details['output_files'].append('preview_frames/Shot_A_V21_0001.png ... 0072.png')
        generate_html_preview()
    write_benchmark('RENDER_FINISHED_IN_THIS_RUNTIME')
    print('SOVTIVA_V5_SHOT_A_V21_FINISHED:', str(OUT), flush=True)
except Exception as error:
    write_benchmark('RENDER_FAILED_IN_THIS_RUNTIME', error)
    traceback.print_exc()
    raise
