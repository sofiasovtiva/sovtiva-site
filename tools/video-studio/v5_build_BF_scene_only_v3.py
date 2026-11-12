#!/usr/bin/env python3
"""SOVTIVA V5 - scenes B to F on user's proved Blender 5.3 Cycles CPU.
Uses original shot A .blend provided alongside; modifies *output copy only*.
No network, plugins, subscriptions, stock media or video generation.
Requires Blender 5.3 with bpy; standalone Python syntax checked by producer.
"""
from __future__ import annotations
import argparse, json, math, random, sys, time, traceback
from pathlib import Path
import bpy
from mathutils import Vector

parser=argparse.ArgumentParser()
parser.add_argument('--out',default='V5_FILM_OUTPUT')
parser.add_argument('--mode',choices=('stills','preview','scene'),default='stills')
parser.add_argument('--pct',type=int,default=35)
parser.add_argument('--samples',type=int,default=8)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=Path(args.out).expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
begin=time.monotonic();s=bpy.context.scene
if s is None: raise RuntimeError('Open original SOVTIVA_V5_SHOT_A_V21.blend with -b first')
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=max(4,args.samples)
s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=args.pct
s.render.fps=24;s.frame_start=1;s.frame_end=576
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
try:s.cycles.use_denoising=True
except (AttributeError, TypeError):pass
try:s.view_settings.view_transform='AgX'
except (AttributeError,ValueError):pass
M={
  'ink':bpy.data.materials.get('CERAMIC / midnight titanium'),
  'gold':bpy.data.materials.get('GOLD / milled chamfer'),
  'brass':bpy.data.materials.get('BRASS / satin metal with fine imperfections'),
  'teal':bpy.data.materials.get('GLASS / quiet jade'),
  'ivory':bpy.data.materials.get('CERAMIC / ivory lettering'),
  'wine':bpy.data.materials.get('ACCENT / smoked burgundy'),
  'dark':bpy.data.materials.get('STAGE / matte dark concrete'),
}
if any(v is None for v in M.values()): raise RuntimeError('Required original V2.1 scene materials missing')

def material(name,rgba,metallic=0,rough=.42,emission=0):
 m=bpy.data.materials.new('FILM/'+name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=rgba;p.inputs['Metallic'].default_value=metallic;p.inputs['Roughness'].default_value=rough
 if emission:
  e=p.inputs.get('Emission Color');q=p.inputs.get('Emission Strength')
  if e is not None:e.default_value=rgba
  if q is not None:q.default_value=emission
 return m
M['paper']=material('warm uncoated paper',(.76,.72,.60,1),.0,.76)
M['print']=material('near black ink',(.023,.03,.034,1),.0,.63)
M['muted']=material('smoked graphite',(.09,.13,.15,1),.36,.41)
M['crimson']=material('correctly lit red paint',(.33,.017,.066,1),.25,.37)
M['white']=material('ivory ink',(.86,.86,.74,1),.03,.38)
M['glow']=material('cool monitor glow',(.07,.49,.54,1),.1,.25,emission=.3)

def root(name,location=(0,0,0)):
 p=bpy.data.objects.new('FILM/'+name,None);s.collection.objects.link(p);p.location=location;return p

def box(name,dim,position,mat,parent=None,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=position);o=bpy.context.object;o.name='FILM/'+name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 if bevel:
  mod=o.modifiers.new('soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=3
  o.modifiers.new('weighted face normals','WEIGHTED_NORMAL')
 if parent:o.parent=parent
 return o

def cyl(name,r,depth,position,mat,parent=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=80,radius=r,depth=depth,location=position);o=bpy.context.object;o.name='FILM/'+name;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat)
 mod=o.modifiers.new('milled edge','BEVEL');mod.width=min(.018,depth*.24);mod.segments=3
 if parent:o.parent=parent
 return o

def tor(name,rad,tube,position,mat,parent=None):
 bpy.ops.mesh.primitive_torus_add(major_radius=rad,minor_radius=tube,major_segments=72,minor_segments=10,location=position);o=bpy.context.object;o.name='FILM/'+name;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat)
 if parent:o.parent=parent
 return o

def label(name,body,xyz,size,mat,parent=None,spacing=1,extrude=.0008):
 c=bpy.data.curves.new('FILM/'+name,'FONT');c.body=body;c.align_x='CENTER';c.align_y='CENTER';c.size=size;c.space_character=spacing;c.extrude=extrude
 o=bpy.data.objects.new('FILM/'+name,c);s.collection.objects.link(o);o.location=xyz;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat)
 if parent:o.parent=parent
 return o

def key(obj,frame,pos=None,rot=None,scale=None):
 if pos is not None:obj.location=pos;obj.keyframe_insert('location',frame=frame)
 if rot is not None:obj.rotation_euler=rot;obj.keyframe_insert('rotation_euler',frame=frame)
 if scale is not None:obj.scale=(scale,scale,scale);obj.keyframe_insert('scale',frame=frame)

def aim(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
def cam_key(frame,position,target,lens=42):
 camera=s.camera;camera.location=position;aim(camera,target);camera.keyframe_insert('location',frame=frame);camera.keyframe_insert('rotation_euler',frame=frame);camera.data.lens=lens;camera.data.keyframe_insert('lens',frame=frame)
 # Original Shot A camera uses DOF: avoid out-of-focus shot cuts by updating focus object.
 focus=camera.data.dof.focus_object
 if focus is not None:key(focus,frame,pos=target)

def light(name,xloc,target,power,colour,size):
 data=bpy.data.lights.new('FILM/'+name,'AREA');data.energy=power;data.color=colour;data.shape='DISK';data.size=size;obj=bpy.data.objects.new('FILM/'+name,data);s.collection.objects.link(obj);obj.location=xloc;aim(obj,target)

def studio(name,x):
 box(name+'/stage',(10,12,.20),(x,1,-.19),M['dark'],bevel=.04)
 box(name+'/cyclorama',(10,.18,8),(x,4.2,3.80),M['ink'],bevel=.01)
 light(name+'/cold edge',(x+3,-3,6),(x,0,3),620,(.65,.89,1),3.6)
 light(name+'/warm rim',(x-3,1,5),(x,-1,3),470,(1,.75,.48),2.5)
 light(name+'/teal edge',(x+3,1,3),(x,0,2.6),260,(.25,.73,.78),2.1)

def coin(name,rad,fronttext='S'):
 p=root(name)
 cyl(name+'/bronze rim',rad,.16,(0,0,0),M['brass'],p)
 cyl(name+'/shaped face',rad*.86,.18,(0,-.016,0),M['gold'],p)
 tor(name+'/embossed edging',rad*.78,.014,(0,-.103,0),M['brass'],p)
 tor(name+'/fine inner ring',rad*.64,.008,(0,-.110,0),M['ink'],p)
 label(name+'/minted characters',fronttext,(0,-.124,-.015),rad*.66,M['ink'],p,extrude=.008)
 return p

# SCENE B: kinetic coin chase, frame 73–144, total 3 seconds.
studio('B / kinetic chase',14.0)
b=coin('B / hero token',.65,'S')
for f,pos,rot,sc in [
(73,(14,-.30,2.55),(.0,.02,-.1),.63),
(91,(14.35,-1.25,2.63),(.25,.10,.20),.96),
(113,(14.20,-2.40,2.87),(.12,.42,-.13),1.27),
(139,(13.86,-4.20,3.13),(.43,-.23,.12),1.66),
(144,(13.90,-4.95,3.30),(.63,-.13,-.02),1.85),
]:key(b,f,pos,rot,sc)
for j in range(7):
 c=coin('B / secondary token %02d'%j,.18+(j%3)*.042,'')
 angle=2*math.pi*j/7
 for f,mul,y in [(73,.08,0),(100,.5,-.6),(123,1.1,-1.8),(144,2.0,-3.3)]:
  key(c,f,(14+math.cos(angle)*mul,y,2.7+math.sin(angle)*mul),(.25*j,.33*j,.27*j),.42 if f==73 else .80)
cam_key(73,(16.5,-10,3.77),(14,-.2,2.6),42)
cam_key(102,(16,-8.40,3.66),(14.20,-1.75,2.78),42)
cam_key(123,(15.55,-6.80,3.42),(14.10,-2.45,2.95),36)
cam_key(144,(15.28,-6.21,3.53),(13.90,-4.10,3.23),48)

# SCENE C: conditional $109 gross reveal on engraved object, 145-240, 4 sec.
studio('C / conditional value',28.0)
c=coin('C / value reveal',1.18,'109')
# V3 editorial QA: bright matte text vs brass coin face, retain original metallic rim.
for ob in bpy.data.objects:
 if ob.name.endswith('C / value reveal/minted characters'):
  ob.data.materials.clear();ob.data.materials.append(M['white'])
label('C / currency mark','US$',(-.51,-.145,.47),.31,M['white'],c,extrude=.007)
label('C / gross qualifier','BRUTOS*',(0,-.145,-.62),.28,M['white'],c,extrude=.007)
for f,pos,rot,sc in [
(145,(28,-.2,3.0),(.06,0,-.36),.68),
(161,(28,-.4,3.0),(.15,.06,.10),.95),
(188,(28,-.36,3.0),(.04,-.11,.012),1.0),
(240,(28,-.23,3.0),(.03,.03,-.02),1.02),
]:key(c,f,pos,rot,sc)
label('C / illustrative caveat','EJEMPLO ILUSTRATIVO',(28,-.92,.83),.19,M['white'])
label('C / exact rate','US$1.09 POR MIL VISTAS ELEGIBLES',(28,-.95,.48),.135,M['white'])
cam_key(145,(29.6,-13.4,3.6),(28,-.1,2.90),50)
cam_key(178,(28.85,-13.1,3.35),(28,-.2,2.95),50)
cam_key(240,(28.64,-12.7,3.35),(28,-.2,2.95),52)

# SCENE D: actual conditions, vertical physical receipt, 241-360, 5 sec.
studio('D / terms document',42.0)
d=root('D / paper master',(42,0,3.05))
box('D / thick matte paper',(3.9,.07,5.45),(0,0,0),M['paper'],d,.04)
for n,body,z,size,mat in [
('header','EJEMPLO DE PAGO',2.11,.36,M['print']),
('separator','------------------',1.72,.21,M['muted']),
('rate','US$1.09 / 1,000',1.11,.40,M['print']),
('eligible','VISTAS ELEGIBLES',.61,.24,M['print']),
('approved','CONTENIDO APROBADO',-.08,.26,M['print']),
('budget','PRESUPUESTO Y LIMITES',-.68,.25,M['print']),
('footer','SUJETO A CONDICIONES',-1.73,.22,M['crimson']),
]:label('D / printed '+n,body,(0,-.061,z),size,mat,d)
for f,rot in [(241,(0,.17,-.09)),(281,(.02,-.03,.025)),(327,(-.03,.01,-.020)),(360,(0,-.1,.04))]:key(d,f,rot=rot)
cam_key(241,(43.05,-18.3,3.65),(42,0,3.05),48)
cam_key(299,(42.72,-17.2,3.2),(42,0,3.05),48)
cam_key(360,(42.70,-17.2,3.2),(42,0,3.05),49)

# SCENE E: zero-turn after condition failure, 361-468, 4.5 sec.
studio('E / outcome zero',56.0)
e=root('E / rejected document',(56,0,3.1))
box('E / buckled matte statement',(3.8,.11,5.22),(0,0,0),M['paper'],e,.025)
label('E / big rejection','NO APROBADO',(0,-.067,1.12),.38,M['crimson'],e,extrude=.003)
label('E / payout zero','US$0',(0,-.075,.04),1.10,M['print'],e,extrude=.009)
label('E / outcome caveat','POSIBLE RESULTADO',(0,-.070,-1.47),.22,M['print'],e)
for f,rot in [(361,(0,.14,.03)),(380,(0,-.045,-.055)),(412,(0,.02,.028)),(468,(.03,-.16,-.05))]:key(e,f,rot=rot)
rr=random.Random(599)
for j in range(10):
 piece=coin('E / fractured brass %02d'%j,.10+.03*(j%3),'')
 # Peripheral columns keep all coins clear of headline, US$0 and caveat.
 side=-1 if j%2 else 1
 ring=j//2
 xx=side*(2.4+.14*(ring%3))
 zz=3.10+((ring%5)-2)*.52
 for f,y,down in [(361,.3,0),(393,-.6,.1),(430,-1.45,.6),(468,-2.15,2.2)]:
  key(piece,f,(56+xx,y,zz-down),(.33*j,.21*j,.37*j),.35 if f==361 else .8)
cam_key(361,(57.1,-18.2,3.8),(56,-.1,3.12),46)
cam_key(389,(56.75,-17.5,3.5),(56,-.1,3.10),47)
cam_key(468,(56.62,-17.2,3.24),(56,-.1,2.99),48)

# SCENE F: one clear idea & brief brand, 469-576, 4.5 sec.
studio('F / physical conclusion',70.0)
fl=root('F / massive editorial typography',(70,0,3.1))
box('F / matte display plate',(4.2,.18,4.92),(0,0,0),M['teal'],fl,.15)
for n,body,z,size,mat in [('views','VISTAS',.78,.72,M['white']),('versus','NO SON',.03,.41,M['white']),('money','GANANCIAS',-.7,.55,M['white'])]:
 label('F / '+n,body,(0,-.130,z),size,mat,fl,extrude=.003)
brand=label('F / signed outro','sovtiva.',(0,-.134,-1.64),.30,M['white'],fl)
for f,rot,sc in [(469,(.07,.10,-.10),.81),(512,(0,.00,.006),1.00),(544,(0,0,0),1.00),(575,(0,0,0),1.02)]:key(fl,f,rot=rot,scale=sc)
cam_key(469,(71.10,-18.2,3.65),(70,0,3.1),47)
cam_key(523,(70.76,-17.25,3.4),(70,0,3.1),48)
cam_key(575,(70.72,-17.1,3.37),(70,0,3.1),48)
# End frame intentionally holds F message; editor may use a one-frame hard cut to A on loop.

# V3 repair: typography contrast and peripheral object lanes; wider framing for portrait sensor on C/D/E/F to keep typography and physical props onscreen.
# B only modestly closer; late B may intentionally fill screen for match-cut.
# Save COPY, leave original .blend unchanged.
output_blend=out/'SOVTIVA_V5_FILM_24S_SCENES_A_to_F_COLOR_QA_V3.blend'
s.frame_set(240)
bpy.ops.wm.save_as_mainfile(filepath=str(output_blend))
frames=[86,96,120,151,183,218,255,299,338,375,417,451,482,536,566] if args.mode=='stills' else (list(range(73,577)) if args.mode=='preview' else [])
frdir=out/('storyboard' if args.mode=='stills' else 'frames_B_F')
frdir.mkdir(exist_ok=True)
manifest={'version':'V5_FULL_SCENES_COLOR_QA_V3','stage':'internal 3D framing-check ONLY; not final; voice rejected','engine':'CYCLES CPU','hardware':'Blender 5.3 Windows ARM / Cycles CPU','fps':24,'total_frames':576,'shots':{'A':[1,72],'B':[73,144],'C':[145,240],'D':[241,360],'E':[361,468],'F':[469,576]},'shot_A':'Existing previously verified user clip; NOT rerendered by this script','samples':s.cycles.samples,'pct':args.pct,'mode':args.mode,'frames_completed':[],'status':'STARTED','cost_usd':0,'publish_authorized':False}
def save():
 manifest['elapsed_seconds']=round(time.monotonic()-begin,2)
 (out/'benchmark.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
save()
try:
 for fr in frames:
  s.frame_set(fr)
  destination=frdir/('V5_%04d.png'%fr)
  s.render.filepath=str(destination)
  print('SOVTIVA_FILM_FRAME_START',fr,flush=True)
  bpy.ops.render.render(write_still=True)
  if not destination.exists() or destination.stat().st_size<5000:raise RuntimeError('Missing render output '+str(destination))
  manifest['frames_completed'].append({'frame':fr,'png':str(destination.relative_to(out)),'bytes':destination.stat().st_size})
  save()
  print('SOVTIVA_FILM_FRAME_DONE',fr,flush=True)
 manifest['status']='SCENE_BF_BUILT_READY_FOR_RENDER' if args.mode=='scene' else ('STORYBOARD_REQUIRES_CEO_VISUAL_REVIEW' if args.mode=='stills' else 'FULL_B_F_FRAMES_REQUIRES_QA')
 save()
 print('SOVTIVA_FILM_RENDER_COMPLETED',len(frames),flush=True)
except Exception as exc:
 manifest['status']='RENDER_FAILED';manifest['error']=repr(exc);save();traceback.print_exc();raise
