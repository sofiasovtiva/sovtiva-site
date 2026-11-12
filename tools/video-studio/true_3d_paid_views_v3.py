#!/usr/bin/env python3
"""SOVTIVA Motion Study V3: true 3D geometry and moving camera, original procedural sound.
Dependencies: VTK, Pillow, NumPy, FFmpeg. No paid API or external media.
"""
import sys, os, math, json, subprocess, argparse, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from pathlib import Path

OUT=Path('/mnt/data/sovtiva_motion_v3');OUT.mkdir(exist_ok=True)
W,H=540,960; FPS=24; DUR=15.; N=int(FPS*DUR)
BLUE=(0.03,0.09,0.135); CREAM=(0.96,0.91,0.78); AQUA=(0.18,0.77,0.76); GOLD=(0.93,0.67,0.30); ROSE=(0.63,0.21,0.35); OLIVE=(0.41,0.53,0.33)
FONT='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
FONTB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FONTS='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'

def smooth(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def easeout(x):return 1-(1-smooth(x))**2
def lerp(a,b,t):return a+(b-a)*t

def vtkmat(actor,col,metal=.0,rough=.4,opacity=1):
 p=actor.GetProperty();p.SetColor(*col);p.SetInterpolationToPhong();p.SetOpacity(opacity)
 p.SetAmbient(.12);p.SetDiffuse(.72);p.SetSpecular(.44);p.SetSpecularPower(65)
 return actor

def actor_from_algorithm(src,col,metal=.0,rough=.4):
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(src.GetOutputPort());a=vtk.vtkActor();a.SetMapper(mapper);vtkmat(a,col,metal,rough);return a

def extruded_text(txt,col=CREAM,depth=.23,size=1.0,metal=.1,rough=.32):
 src=vtk.vtkVectorText();src.SetText(txt)
 ext=vtk.vtkLinearExtrusionFilter();ext.SetInputConnection(src.GetOutputPort());ext.SetExtrusionTypeToNormalExtrusion();ext.SetScaleFactor(depth);ext.CappingOn()
 normals=vtk.vtkPolyDataNormals();normals.SetInputConnection(ext.GetOutputPort());normals.SetFeatureAngle(65);normals.ConsistencyOn()
 normals.Update()
 bounds=normals.GetOutput().GetBounds(); cx=(bounds[0]+bounds[1])/2; cy=(bounds[2]+bounds[3])/2
 transform=vtk.vtkTransform();transform.Translate(-cx,-cy,0)
 shifted=vtk.vtkTransformPolyDataFilter();shifted.SetTransform(transform);shifted.SetInputConnection(normals.GetOutputPort())
 m=vtk.vtkPolyDataMapper();m.SetInputConnection(shifted.GetOutputPort());m.Update()
 a=vtk.vtkActor();a.SetMapper(m);vtkmat(a,col,metal,rough)
 a.SetScale(size,size,size)
 return a

def coin(radius=.66,height=.25,color=GOLD):
 c=vtk.vtkCylinderSource();c.SetRadius(radius);c.SetHeight(height);c.SetResolution(60);c.CappingOn()
 a=actor_from_algorithm(c,color,.82,.22)
 a.RotateX(90)
 return a

def cube(w,h,d,col,metal=.05,rough=.43):
 c=vtk.vtkCubeSource();c.SetXLength(w);c.SetYLength(h);c.SetZLength(d)
 a=actor_from_algorithm(c,col,metal,rough)
 return a

def sphere(rad,color,metal=.2,rough=.25,res=40):
 s=vtk.vtkSphereSource();s.SetRadius(rad);s.SetThetaResolution(res);s.SetPhiResolution(res)
 return actor_from_algorithm(s,color,metal,rough)

def ring(r=1.5,tube=.02,col=AQUA):
 cir=vtk.vtkRegularPolygonSource();cir.SetNumberOfSides(128);cir.SetRadius(r);cir.GeneratePolygonOff()
 tube_f=vtk.vtkTubeFilter();tube_f.SetInputConnection(cir.GetOutputPort());tube_f.SetRadius(tube);tube_f.SetNumberOfSides(10)
 return actor_from_algorithm(tube_f,col,.45,.23)

ren=vtk.vtkRenderer();ren.SetGradientBackground(1);ren.SetBackground(.01,.035,.06);ren.SetBackground2(.035,.10,.14)
ren.SetUseFXAA(False)
w=vtk.vtkRenderWindow();w.SetOffScreenRendering(True);w.SetSize(W,H);w.AddRenderer(ren);w.SetMultiSamples(4)
cam=ren.GetActiveCamera();cam.SetViewAngle(37);cam.SetPosition(0,0,13);cam.SetFocalPoint(0,0,0);cam.SetViewUp(0,1,0)
for pos,color,power in [((-5,6,8),(.50,.90,1.),3.2),((5,-3,4),(1.,.35,.36),1.7),((1,5,-2),(1.,.83,.54),2.0)]:
 l=vtk.vtkLight();l.SetPosition(*pos);l.SetFocalPoint(0,0,0);l.SetColor(*color);l.SetIntensity(power);ren.AddLight(l)
ren.SetAmbient(.18,.18,.18)

# World-space layers have genuine perspective depth, occlusion, lighting and shadows via surfaces.
scene={}
scene[0]=[]
hero=extruded_text('100K',CREAM,depth=.42,size=1.06,metal=.62,rough=.27);ren.AddActor(hero);scene[0].append(hero)
caption3d=extruded_text('VIEWS',AQUA,depth=.10,size=.48,metal=.2,rough=.5);caption3d.SetPosition(0,-1.28,-.32);ren.AddActor(caption3d);scene[0].append(caption3d)
hero_ring=ring(2.38,.026,AQUA);hero_ring.SetPosition(0,.1,-.8);ren.AddActor(hero_ring);scene[0].append(hero_ring)
coins=[]
for j in range(13):
 a=coin(.13+0.055*(j%3==0),.11,GOLD if j%3 else AQUA)
 ren.AddActor(a);scene[0].append(a);coins.append(a)

scene[1]=[]
number=extruded_text('$109',GOLD,depth=.41,size=1.06,metal=.71,rough=.19);ren.AddActor(number);scene[1].append(number)
platform=cube(5.1,.36,2.2,(.11,.22,.28),metal=.36,rough=.3);platform.SetPosition(0,-1.38,-.75);ren.AddActor(platform);scene[1].append(platform)
platform_trim=cube(5.14,.05,2.24,AQUA,metal=.32,rough=.27);platform_trim.SetPosition(0,-1.17,-.75);ren.AddActor(platform_trim);scene[1].append(platform_trim)
stack=[]
for j in range(8):
 a=coin(.26,.09,GOLD);ren.AddActor(a);scene[1].append(a);stack.append(a)

scene[2]=[]
paper=cube(3.30,4.75,.12,CREAM,metal=0,rough=.7);paper.SetPosition(0,0,-.35);ren.AddActor(paper);scene[2].append(paper)
for posx,py,length in [(0,1.05,2.25),(0,.16,2.25),(0,-.70,2.25)]:
 a=cube(length,.09,.13,(.21,.43,.48));a.SetPosition(posx,py,-.17);ren.AddActor(a);scene[2].append(a)
receipt_top=extruded_text('VIEWS 100K',BLUE,depth=.05,size=.29,metal=.12);receipt_top.SetPosition(0,1.67,.08);ren.AddActor(receipt_top);scene[2].append(receipt_top)
receipt_caption=extruded_text('TOTAL $109',ROSE,depth=.07,size=.30,metal=.15);receipt_caption.SetPosition(0,-1.46,.08);ren.AddActor(receipt_caption);scene[2].append(receipt_caption)

scene[3]=[]
zero=extruded_text('$0',CREAM,depth=.5,size=1.38,metal=.25,rough=.27);ren.AddActor(zero);scene[3].append(zero)
zero_ring=ring(2.28,.057,ROSE);zero_ring.SetPosition(0,.2,-.8);ren.AddActor(zero_ring);scene[3].append(zero_ring)
shards=[]
for j in range(24):
 a=cube(.12+(.1*(j%4)),.33+(.24*(j%3)),.11,ROSE if j%2 else GOLD,metal=.6,rough=.3)
 ren.AddActor(a);scene[3].append(a);shards.append(a)

scene[4]=[]
logo=extruded_text('sovtiva.',CREAM,depth=.18,size=.72,metal=.46,rough=.3);ren.AddActor(logo);scene[4].append(logo)
orb=sphere(1.35,AQUA,metal=.72,rough=.18);orb.SetPosition(0,-1.4,-1.5);ren.AddActor(orb);scene[4].append(orb)
rr=[]
for n in range(3):
 a=ring(1.4+n*.27,.027,(.72,.58,.34) if n%2 else AQUA);a.SetPosition(0,-1.4,-1.5);a.RotateY(20+n*40);ren.AddActor(a);scene[4].append(a);rr.append(a)

# Subtle deep 3D background elements visible with camera dolly.
background=[]
for i in range(25):
 x=(i%5-2)*1.7;y=(i//5-2)*2.05
 a=cube(.03,.03,.07,AQUA if i%2 else OLIVE,metal=.55,rough=.2);a.SetPosition(x,y,-4.4);ren.AddActor(a);background.append(a)

for name,acts in scene.items():
 for a in acts:a.SetVisibility(False)

win2img=vtk.vtkWindowToImageFilter();win2img.SetInput(w);win2img.SetInputBufferTypeToRGB();win2img.ReadFrontBufferOff()
fontbig=ImageFont.truetype(FONTB,48)
fontmid=ImageFont.truetype(FONTB,35)
fonttiny=ImageFont.truetype(FONTS,19)
fontsmall=ImageFont.truetype(FONTS,24)

def typog(layer,t,sc):
 d=ImageDraw.Draw(layer)
 ivory=(246,245,232,255); aqua=(141,233,223,255);dim=(154,190,195,255)
 d.text((38,54),'SOVTIVA  /  FIELD NOTES',font=fonttiny,fill=dim,stroke_width=0)
 d.rounded_rectangle((38,90,90,94),radius=2,fill=(158,230,223,255))
 def textcenter(y,txt,font,color=ivory):
  bb=d.textbbox((0,0),txt,font=font);d.text(((W-bb[2])/2,y),txt,font=font,fill=color,stroke_width=0)
 if sc==0:
  textcenter(712,'100,000 VISTAS',fontmid,ivory)
  textcenter(764,'¿CUÁNTO DINERO?',fontsmall,aqua)
 if sc==1:
  textcenter(695,'NO ES UN CHEQUE.',fontmid,ivory)
  textcenter(751,'ES UN CÁLCULO.',fontsmall,aqua)
 if sc==2:
  textcenter(695,'APROBACIÓN · TOPES',fontsmall,ivory)
  textcenter(744,'COSTOS · REGIONES',fontsmall,aqua)
 if sc==3:
  textcenter(691,'CLIP RECHAZADO',fontmid,ivory)
  textcenter(752,'PAGO: CERO.',fontsmall,aqua)
 if sc==4:
  textcenter(643,'NO PERSIGAS VISTAS.',fontmid,ivory)
  textcenter(698,'ENTIENDE LOS NÚMEROS.',fontsmall,aqua)
  textcenter(766,'La investigación en sovtiva.com',fonttiny,dim)
 d.text((38,879),'DATOS ILUSTRATIVOS  ·  SUJETO A CAMPAÑA',font=ImageFont.truetype(FONTS,14),fill=dim)
 # timeline
 d.rounded_rectangle((38,914,W-38,918),radius=2,fill=(80,111,123,255))
 d.rounded_rectangle((38,914,38+(W-76)*(t/DUR),918),radius=2,fill=(151,232,222,255))
 return layer

def scene_at(t):
 return 0 if t<3 else 1 if t<5.7 else 2 if t<8.65 else 3 if t<11.4 else 4

def animate(sc,t):
 # reset visibility; moving camera with measured focal parallax and physical depth (not two-dimensional scale animations).
 for k,group in scene.items():
  for a in group:a.SetVisibility(k==sc)
 ti=[0,3,5.7,8.65,11.4][sc]; u=t-ti
 if sc==0:
  e=smooth(min(1,u/1.3));hero.SetPosition(0,.35,lerp(-3.7,.5,e));hero.RotateY(.7) if u>.07 else None
  caption3d.SetPosition(0,-1.2,-1)
  hero_ring.SetOrientation(25*u,38*u,10*u)
  for j,a in enumerate(coins):
   an=j*2*math.pi/len(coins)+u*(.82+.04*(j%3))
   rad=2.15+.23*math.sin(u*1.8+j)
   a.SetPosition(rad*math.cos(an),.28+rad*.90*math.sin(an),-1.8+.24*math.sin(an*.7+j))
   a.SetOrientation(20+u*70,j*30+u*82,0)
  cam.SetPosition(1.2*math.sin(u*.45),.4*math.cos(u*.7),13-u*.7);cam.SetFocalPoint(0,0,0)
 elif sc==1:
  e=smooth(min(1,u/.7));number.SetPosition(0,.6,lerp(-3.5,.7,e));number.SetOrientation(6*math.sin(u*1.1),-23+18*u,0)
  for j,a in enumerate(stack):
   an=j*2*math.pi/len(stack)+u*.9
   a.SetPosition((1.55+0.19*(j%4))*math.cos(an),-1.7+(.11*(j%4)),-1.5+.25*math.sin(an))
   a.SetOrientation(90,0,22*u+j*40)
  cam.SetPosition(-1.2+u*.6,1.3-u*.35,11.3+u*.55);cam.SetFocalPoint(0,-.1,0)
 elif sc==2:
  paper.SetOrientation(10+u*7,-18+8*u,4*math.sin(u*.7))
  for a in scene[2][1:]:a.SetOrientation(10+u*7,-18+8*u,4*math.sin(u*.7))
  cam.SetPosition(1.5-u*.85,1.6-u*.85,11-u*.1);cam.SetFocalPoint(0,0,-.1)
 elif sc==3:
  e=smooth(min(1,u/.75));zero.SetPosition(0,.32,lerp(-3.8,1.,e));zero.SetOrientation(0,-15+13*u,0)
  zero_ring.SetOrientation(4*u,36*u,4*u)
  for j,a in enumerate(shards):
   ang=j*2.399+u*.58;rad=(.4+u*(.25+(j%4)*.12))*2.0
   a.SetPosition(rad*math.cos(ang),rad*math.sin(ang),-1.0+.5*math.sin(j+u*2))
   a.SetOrientation(u*70+j*23,u*32+j*9,u*49)
  cam.SetPosition(-.2+.65*math.sin(u),.1,12.2-u*.17);cam.SetFocalPoint(0,0,0)
 else:
  logo.SetPosition(0,1.3,lerp(-2.0,.7,smooth(u/.7)));logo.SetOrientation(0,-9+7*math.sin(u),0)
  orb.SetPosition(0,-1.45,-1.6);orb.RotateY(.5)
  for j,a in enumerate(rr):a.SetOrientation(u*(38+j*13),u*(24+j*18),u*(17+j*11))
  cam.SetPosition(2.2*math.cos(.3*u),1.2*math.sin(u*.5),12.8-u*.2);cam.SetFocalPoint(0,-.3,0)
 # BG particles parallax
 for j,a in enumerate(background):a.SetPosition((j%5-2)*1.7+.06*math.sin(t+j),((j//5)-2)*2.05,-4.4+.25*math.sin(t*.6+j))
 cam.SetViewUp(0,1,0)


def frame(t):
 sc=scene_at(t);animate(sc,t);w.Render();win2img.Modified();win2img.Update()
 arr=vtk_to_numpy(win2img.GetOutput().GetPointData().GetScalars())
 out=arr.reshape(H,W,3)[::-1,:,:].copy()
 im=Image.fromarray(out,'RGB').convert('RGBA')
 # atmospheric bloom using sparse overbright highlights only
 if sc!=2:
  gl=im.filter(ImageFilter.GaussianBlur(14));im=Image.blend(im,gl,.055)
 layer=Image.new('RGBA',(W,H),(0,0,0,0));typog(layer,t,sc)
 im=Image.alpha_composite(im,layer)
 return im.convert('RGB')

def audio(path):
 import wave
 sr=44100;secs=DUR
 x=np.arange(int(sr*secs),dtype=np.float64)/sr
 wav=np.zeros(len(x),dtype=np.float64)
 def add(t,freq=155,amp=.32,dec=.26,type='kick'):
  start=int(t*sr)
  if start<0 or start>=len(wav):return
  end=min(len(wav),start+int(sr*dec*4));zz=np.arange(end-start)/sr
  if type=='kick':sig=np.sin(2*np.pi*(freq*zz+60/(2*np.pi*22)*(1-np.exp(-22*zz))))*np.exp(-zz/dec)
  elif type=='chime':sig=(np.sin(2*np.pi*freq*zz)+.34*np.sin(2*np.pi*2.003*freq*zz))*np.exp(-zz/dec)
  elif type=='thunk':sig=(np.sin(2*np.pi*freq*zz)+.22*np.random.default_rng(int(t*10000)).standard_normal(len(zz)))*np.exp(-zz/(dec*.85))
  elif type=='whoosh':sig=np.random.default_rng(int(t*10000)).standard_normal(len(zz))*np.sin(np.pi*np.minimum(1,zz/(dec*4)))**1.2*np.exp(-zz/(dec*1.8))*.46
  else:sig=np.sin(2*np.pi*freq*zz)*np.exp(-zz/dec)
  wav[start:end]+=amp*sig
 for t in np.arange(.1,secs,.48):add(float(t),75,.26,.12)
 for t in np.arange(.37,secs,.96):add(float(t),3000,.07,.03,'thunk')
 for t in [0,.63,1.65,3,3.49,5.7,8.65,11.4]:add(t,90,.48,.28,'kick');add(t,.0,.22,.18,'whoosh')
 for t in [1.05,2.4,4.1,6.8,7.5,10.1,13.1]:add(t,520+90*(t%3),.13,.22,'chime')
 # short original atmospheric bass drone
 wav+=.012*np.sin(2*np.pi*55*x)*(0.7+0.3*np.sin(2*np.pi*.31*x))
 wav*=np.clip(np.minimum(1,x/.13)*np.minimum(1,(secs-x)/.32),0,1)
 wav*=.88/(np.max(np.abs(wav))+1e-9)
 import wave
 with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(wav,-1,1)*32767).astype('<i2').tobytes())

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--fps',type=int,default=24);args=ap.parse_args()
 if args.preview:
  for n,t in enumerate([1.1,4.2,6.6,10.0,12.6]):
   img=frame(t);img.save(OUT/f'preview_{n}.jpg',quality=92)
  print('PREVIEW_READY',[(p.name,p.stat().st_size) for p in sorted(OUT.glob('preview_*.jpg'))]);sys.exit(0)
 start=time.monotonic()
 raw=str(OUT/'silent_3d.mp4');command=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',raw]
 pr=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 for n in range(N):
  img=frame(n/FPS)
  try:pr.stdin.write(img.tobytes())
  except BrokenPipeError:raise RuntimeError(pr.communicate()[1].decode())
  if n%(FPS*3)==0: print('frame',n,'/',N,'elapsed',round(time.monotonic()-start,1),flush=True)
 pr.stdin.close();pr.wait();
 if pr.returncode!=0:raise RuntimeError('FFmpeg render failed')
 snd=OUT/'original_3d_sound.wav';audio(snd)
 final=OUT/'SOVTIVA_3D_motion_study_v3.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-i',str(snd),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(final)],check=True)
 for n,t in enumerate([1.1,4.2,6.6,10.0,12.6]):frame(t).save(OUT/f'preview_{n}.jpg',quality=92)
 print('DONE',final,'seconds',round(time.monotonic()-start,1),'bytes',final.stat().st_size)
