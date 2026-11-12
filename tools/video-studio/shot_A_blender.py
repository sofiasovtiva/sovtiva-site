#!/usr/bin/env python3
"""SOVTIVA V5 — Shot A / zero-cost Blender smoke test.

Original procedural geometry and lighting. Tested: Python syntax only in ChatGPT
runtime (no Blender binary here). Rendering MUST be verified on a machine with
Blender 5.2.x LTS before calling this production-ready.

Run with official Blender 5.2.4 LTS ARM64 / x64:
  blender -b -t 4 --python shot_A_blender.py -- --mode still --out <folder>
  blender -b -t 4 --python shot_A_blender.py -- --mode preview --out <folder>
  blender -b -t 4 --python shot_A_blender.py -- --mode full --out <folder>

All modes generate original scenes with no downloads, external accounts,
AI credits or subscriptions. 'full' can be computationally intensive.
"""
import sys, argparse, math, random, time, json
from pathlib import Path
import bpy
from mathutils import Vector

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['still','preview','full'],default='still')
parser.add_argument('--out',default='sovtiva_v5_shot_A')
parser.add_argument('--engine',choices=['eevee','cycles'],default='eevee')
parser.add_argument('--samples',type=int,default=24)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
DEST=Path(args.out).expanduser().resolve()
DEST.mkdir(parents=True,exist_ok=True)
START=time.monotonic()

# Reset with no external resources. The data file contains only original assets.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass  # Preserve system data blocks; only objects are reset.
sc=bpy.context.scene
sc.frame_start=1;sc.frame_end=72;sc.render.fps=24
sc.render.resolution_x=1080;sc.render.resolution_y=1920
sc.render.resolution_percentage=100 if args.mode in ('still','full') else 40
sc.render.image_settings.file_format='PNG'
sc.render.image_settings.color_mode='RGBA'
sc.render.film_transparent=False
sc.render.use_file_extension=True
sc.render.filepath=str(DEST/'frame_')
try:sc.render.engine='BLENDER_EEVEE_NEXT' if args.engine=='eevee' else 'CYCLES'
except Exception:
    if args.engine=='eevee':
        try:sc.render.engine='BLENDER_EEVEE'
        except Exception:sc.render.engine='CYCLES'
    else:sc.render.engine='CYCLES'
if sc.render.engine=='CYCLES':
    sc.cycles.samples=max(16,args.samples); sc.cycles.device='CPU'
else:
    # The available EEVEE sampling attributes vary across versions.
    if hasattr(sc,'eevee') and hasattr(sc.eevee,'taa_render_samples'):
        sc.eevee.taa_render_samples=max(8,args.samples)
if hasattr(sc.render,'use_motion_blur'):sc.render.use_motion_blur=args.mode=='full'
try:sc.view_settings.view_transform='AgX'
except Exception:sc.view_settings.view_transform='Standard'
sc.view_settings.look='Medium High Contrast' if 'Medium High Contrast' in [x.name for x in sc.view_settings.bl_rna.properties['look'].enum_items] else 'Medium High Contrast' if False else sc.view_settings.look
sc.render.image_settings.color_depth='8'

world=bpy.data.worlds.new('Deep navy studio atmosphere')
sc.world=world;world.use_nodes=True
bg=world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value=(.011,.028,.040,1)
    bg.inputs['Strength'].default_value=.42

NAVY=(.013,.047,.070,1)
TEAL=(.10,.58,.62,1)
BURG=(.22,.035,.093,1)
BRASS=(.75,.39,.105,1)
CREAM=(.86,.82,.67,1)


def material(name, color, metallic=0.0, rough=.45, bump=.0, noise_scale=140):
    m=bpy.data.materials.new(name);m.use_nodes=True
    nt=m.node_tree; bs=nt.nodes.get('Principled BSDF')
    if bs:
        bs.inputs['Base Color'].default_value=color
        bs.inputs['Metallic'].default_value=metallic
        bs.inputs['Roughness'].default_value=rough
        if bump:
            noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=noise_scale
            noise.inputs['Detail'].default_value=2.0
            bumpnode=nt.nodes.new('ShaderNodeBump');bumpnode.inputs['Strength'].default_value=bump
            bumpnode.inputs['Distance'].default_value=.025
            nt.links.new(noise.outputs['Fac'],bumpnode.inputs['Height'])
            nt.links.new(bumpnode.outputs['Normal'],bs.inputs['Normal'])
    return m

mat_body=material('Black ceramic / microscopic variation',NAVY,.40,.23,.10)
mat_screen=material('Glass display / deep jade',(.012,.11,.14,1),.22,.15,.035)
mat_brass=material('Brushed machined brass',BRASS,.87,.22,.13,95)
mat_bright=material('Warm metal edge',(.90,.67,.27,1),.82,.19,.04)
mat_white=material('Ceramic white',CREAM,.06,.5,.06)
mat_ruby=material('Burgundy anodized accent',BURG,.56,.27,.07)
mat_ground=material('Charcoal stage concrete',(.016,.030,.041,1),.14,.33,.2,85)
mat_hardware=material('Smoked metal hardware',(.06,.11,.14,1),.74,.28,.08)


def mesh_cube(name,location,dims,mat,bev=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location);o=bpy.context.object;o.name=name
    o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    if bev:
        b=o.modifiers.new('physically rounded corners','BEVEL');b.width=bev;b.segments=4
        o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    return o


def cylinder(name,r,depth,location,mat,parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=depth,location=location)
    o=bpy.context.object;o.name=name;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat)
    b=o.modifiers.new('precision bevel','BEVEL');b.width=min(depth*.3,.026);b.segments=4
    o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    if parent:o.parent=parent
    return o


def torus(name,r,tube,location,mat,parent=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=tube,major_segments=96,minor_segments=12,location=location)
    o=bpy.context.object;o.name=name;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat)
    if parent:o.parent=parent
    return o


def label(name,text,loc,size,mat,parent=None,extrude=.003):
    cr=bpy.data.curves.new(name,'FONT');cr.body=text;cr.align_x='CENTER';cr.align_y='CENTER'
    cr.size=size;cr.extrude=extrude;cr.bevel_depth=.0015 if extrude else 0
    ob=bpy.data.objects.new(name,cr);sc.collection.objects.link(ob)
    ob.location=loc;ob.rotation_euler=(math.pi/2,0,0)
    ob.data.materials.append(mat)
    if parent:ob.parent=parent
    return ob

# A coherent physical environment, not an abstract gradient card.
floor=mesh_cube('Real studio stage / reflective concrete',(0,0,-.13),(40,40,.23),mat_ground,.02)
wall=mesh_cube('Dim studio wall / rear',(0,3.9,6.0),(40,.15,13),mat_ground,.0)
for k in range(-4,5):
    # Receding practical light rails introduce perspective and parallax.
    mesh_cube('Practical wall slit %02d'%k,(k*1.4,3.78,2.0),(.024,.03,4.2),mat_hardware,.006)
mesh_cube('Base for hero device',(0,.35,.085),(3.4,1.3,.16),mat_body,.09)
mesh_cube('Raised brass trim',(0,-.17,.166),(3.32,.045,.014),mat_brass,.004)

# One actual mesh phone, dimensional sides, thin glass, aligned screen details.
phone=bpy.data.objects.new('PHONE / master pivot',None);sc.collection.objects.link(phone)
phone.location=(0,.0,2.13)
body=mesh_cube('ceramic anodized frame',(0,0,0),(1.95,.23,3.72),mat_body,.16);body.parent=phone
screen=mesh_cube('tinted glass screen',(0,-.129,0),(1.76,.018,3.46),mat_screen,.07);screen.parent=phone
mesh_cube('earpiece',(0,-.151,1.55),(.37,.025,.037),mat_hardware,.015).parent=phone
mesh_cube('edge burgundy key',(.987,-.02,.76),(.032,.10,.26),mat_ruby,.012).parent=phone
label('SOVTIVA title','sovtiva.',(0,-.161,1.28),.19,mat_white,phone)
label('counter descriptor','VISTAS',(0,-.165,.46),.21,mat_white,phone)
label('counter display','100,000',(0,-.171,-.04),.49,mat_white,phone,extrude=.005)
label('conditional hint','¿CUÁNTO VALE?',(0,-.168,-.77),.17,mat_bright,phone)
label('internal caveat','EJEMPLO • NO ES UN PAGO',(0,-.171,-1.34),.10,mat_white,phone)

# Independent physically modeled coins, with engraved-style face lettering.
def make_coin(name,r=.43,hero=False):
    root=bpy.data.objects.new(name+' / animation pivot',None);sc.collection.objects.link(root)
    cylinder(name+' / minted brass',r,.11,(0,0,0),mat_brass,root)
    torus(name+' / outer relief',r*.86,.010,(0,-.061,0),mat_bright,root)
    torus(name+' / inner relief',r*.74,.005,(0,-.060,0),mat_hardware,root)
    if hero:
        label(name+' / $109 engraved','$109',(0,-.068,.048),.24,mat_bright,root,.003)
        label(name+' / eligible only','BRUTO*',(0,-.067,-.16),.08,mat_white,root,.002)
    return root

rng=random.Random(29)
hero=make_coin('HERO coin: payout reveal',.50,True)
particles=[make_coin('supporting minted coin %02d'%k,.11+.045*(k%3)) for k in range(11)]

def keyframe(obj,fr,loc=None,scale=None,rotation=None):
    if loc is not None:obj.location=loc;obj.keyframe_insert('location',frame=fr)
    if scale is not None:obj.scale=(scale,)*3;obj.keyframe_insert('scale',frame=fr)
    if rotation is not None:obj.rotation_euler=rotation;obj.keyframe_insert('rotation_euler',frame=fr)

# Phone rocks when 100K counts and ejects an impossible physical coin.
for fr,pos,rot in [(1,(0,0,2.13),(0,0,0)),(24,(0,0,2.13),(0,.032,-.015)),(31,(0,0,2.18),(.014,.03,.025)),(38,(0,0,2.13),(-.009,0,-.01)),(72,(0,0,2.13),(0,0,0))]:keyframe(phone,fr,loc=pos,rotation=rot)
for fr,loc,scale,rot in [(1,(0,-.25,2.1),.01,(0,0,0)),(23,(0,-.25,2.1),.02,(0,0,0)),(37,(0,-1.15,2.65),.55,(.0,.18,.08)),(51,(.34,-2.25,3.15),1.15,(.07,.48,.10)),(72,(-.10,-3.35,3.34),1.65,(0,.13,.06))]:keyframe(hero,fr,loc,scale,rot)
for j,ob in enumerate(particles):
    ang=j*2.399
    rad=1.05+(j%4)*.28
    base=27+(j%6)*2
    x=math.sin(ang)*rad;z=2.2+math.cos(ang)*rad*.8
    for fr,loc,scale,rot in [
      (1,(0,-.2,2.3),.01,(0,0,0)),(base,(0,-.2,2.3),.025,(0,0,0)),
      (base+13,(x*.72,-1.55-(j%3)*.12,z),.78,(.2*j,.11*j,.21*j)),
      (72,(x*1.26,-2.4-(j%2)*.32,z-.4),1.0,(.47*j,.31*j,.23*j))]:keyframe(ob,fr,loc,scale,rot)

# Lighting: motivated key/fill/rim + floor contact, not colored flat gradients.
def area(name,pos,target,power,color,size):
    li=bpy.data.lights.new(name,'AREA');li.energy=power;li.color=color;li.shape='DISK';li.size=size
    ob=bpy.data.objects.new(name,li);sc.collection.objects.link(ob);ob.location=pos
    ob.rotation_euler=(Vector(target)-Vector(pos)).to_track_quat('-Z','Y').to_euler()
    return ob
area('Soft 100cm key',(0,-4.0,5.2),(0,0,2.0),950,(.74,.94,1),4.1)
area('Warm metal rim',(-3.2,2.0,5.6),(0,0,2.2),1250,(1.0,.64,.30),3.2)
area('Teal side reflection',(3.0,-.4,2.8),(0,0,2.1),780,(.16,.84,.88),3.0)
area('Floor bounce',(0,-2.8,.65),(0,0,1.7),140,(.90,.53,.29),2.5)

camera_data=bpy.data.cameras.new('CAM-A: physically moving lens')
camera=bpy.data.objects.new('CAM-A: physically moving lens',camera_data)
sc.collection.objects.link(camera);sc.camera=camera
camera_data.type='PERSP';camera_data.lens=52;camera_data.sensor_fit='VERTICAL';camera_data.clip_end=220
camera_data.dof.use_dof=True
camera_data.dof.focus_object=phone
camera_data.dof.aperture_fstop=5.6
for fr,p,target in [(1,(0,-8.0,3.2),(0,0,2.2)),(24,(.2,-7.65,3.0),(0,0,2.2)),(42,(-.8,-7.0,3.35),(0,-.7,2.4)),(72,(-1.0,-6.3,3.65),(-.1,-2.6,3.13))]:
    camera.location=p
    camera.rotation_euler=(Vector(target)-Vector(p)).to_track_quat('-Z','Y').to_euler()
    camera.keyframe_insert('location',frame=fr);camera.keyframe_insert('rotation_euler',frame=fr)

# Smooth keyframes; authored beat timing remains in explicit frame coordinates.
for obj in [phone,hero,camera,*particles]:
    ad=obj.animation_data
    if ad and ad.action:
        try:
            for fc in ad.action.fcurves:
                for kp in fc.keyframe_points:kp.interpolation='BEZIER'
        except AttributeError:
            # Blender 5.x may store layered action channels; interpolation defaults remain Bezier.
            pass

sc.frame_set(37)
sc.camera.data.lens=52
# Preserve .blend for interactive art direction even if only the still is rendered.
bpy.ops.wm.save_as_mainfile(filepath=str(DEST/'SOVTIVA_V5_SHOT_A.blend'))
if args.mode=='still':
    sc.render.resolution_percentage=100
    sc.render.filepath=str(DEST/'shot_A_frame_0037.png')
    bpy.ops.render.render(write_still=True)
else:
    if args.mode=='preview':sc.render.resolution_percentage=40
    sc.render.filepath=str(DEST/'frame_')
    bpy.ops.render.render(animation=True)
with open(DEST/'benchmark.json','w',encoding='utf-8') as f:
    json.dump({'mode':args.mode,'scene':'SOVTIVA V5 A','blender_version':bpy.app.version_string,'engine':sc.render.engine,'samples':args.samples,'render_resolution':[sc.render.resolution_x,sc.render.resolution_y],'percentage':sc.render.resolution_percentage,'frames':72 if args.mode!='still' else 1,'elapsed_seconds':round(time.monotonic()-START,2),'status':'RENDER_FINISHED_IN_THIS_RUNTIME','estimated_cost_usd':0},f,indent=2)
print('SOVTIVA_V5_SHOT_A_FINISHED',str(DEST))
