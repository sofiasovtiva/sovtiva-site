#!/usr/bin/env python3
"""Sovtiva Cinema Notes V4 - original, rights-cleared procedural 3D video study.

Requires vtk, numpy, Pillow, scipy, ffmpeg. No paid video or external assets.
Writes an original 15.5s social-video concept at a native 720x1280 render resolution.
The illustrative $109 figure assumes 100,000 APPROVED ELIGIBLE views at ~$1.09/1k,
subject to campaign cap, budget, rules and acceptance. It is never a guaranteed payout.
"""
from __future__ import annotations
import argparse, math, subprocess, json, os, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from vtk.util.numpy_support import vtk_to_numpy
import vtk

ROOT=Path(__file__).resolve().parent
W,H,FPS,DURATION=720,1280,24,15.5
N=int(round(FPS*DURATION))
FONTB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FONTR='/usr/share/fonts/opentype/inter/Inter-Regular.otf'
FONTM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
if not Path(FONTR).exists():FONTR='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
if not Path(FONTM).exists():FONTM='/usr/share/fonts/truetype/lato/Lato-Medium.ttf'
INK=(.034,.061,.078); WARM=(.91,.86,.77); JADE=(.29,.61,.57); BRASS=(.72,.54,.32); WINE=(.44,.22,.29)
CAM={}

def clamp(x):return max(0,min(1,x))
def smooth(t):t=clamp(t);return t*t*(3-2*t)
def ease(t):return 1-(1-smooth(t))**3

def phong(actor,color,spec=.55,shine=80,ambient=.12,opacity=1):
 p=actor.GetProperty();p.SetColor(*color);p.SetInterpolationToPhong();p.SetAmbient(ambient);p.SetDiffuse(.68);p.SetSpecular(spec);p.SetSpecularPower(shine);p.SetOpacity(opacity)
 return actor

def geom(src,col,spec=.55,shine=70):
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(src.GetOutputPort())
 a=vtk.vtkActor();a.SetMapper(mapper);return phong(a,col,spec,shine)

def rounded_box(width,height,depth,r,col):
 # True rounded side wall, front and back are polygon surfaces via capping.
 pts=vtk.vtkPoints();n=12
 for cx,cy,start in [(width/2-r,height/2-r,0),(-width/2+r,height/2-r,90),(-width/2+r,-height/2+r,180),(width/2-r,-height/2+r,270)]:
  for i in range(n+1):
   ang=math.radians(start+90*i/n)
   pts.InsertNextPoint(cx+r*math.cos(ang),cy+r*math.sin(ang),-depth/2)
 # polygon must be ordered counterclockwise, our start creates outer polygon CCW? corners go top-right=>top-left=>bottom-left=>bottom-right = CCW reverse; may need rotate orientation but double-sided lights still usable.
 poly=vtk.vtkPolygon();poly.GetPointIds().SetNumberOfIds(pts.GetNumberOfPoints())
 for i in range(pts.GetNumberOfPoints()):poly.GetPointIds().SetId(i,i)
 cells=vtk.vtkCellArray();cells.InsertNextCell(poly)
 pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(cells)
 ext=vtk.vtkLinearExtrusionFilter();ext.SetInputData(pd);ext.SetExtrusionTypeToNormalExtrusion();ext.SetVector(0,0,1);ext.SetScaleFactor(depth);ext.CappingOn()
 norm=vtk.vtkPolyDataNormals();norm.SetInputConnection(ext.GetOutputPort());norm.AutoOrientNormalsOn();norm.ConsistencyOn();norm.SplittingOff()
 return geom(norm,col,.65,80)

def box(x,y,z,c,spec=.3):
 s=vtk.vtkCubeSource();s.SetXLength(x);s.SetYLength(y);s.SetZLength(z);return geom(s,c,spec,48)

def sphere(r,col,spec=.8):
 s=vtk.vtkSphereSource();s.SetRadius(r);s.SetThetaResolution(40);s.SetPhiResolution(28);return geom(s,col,spec,90)

def cylinder(r,h,col):
 s=vtk.vtkCylinderSource();s.SetRadius(r);s.SetHeight(h);s.SetResolution(100);s.CappingOn()
 a=geom(s,col,.75,85);a.RotateX(90);return a

def torus(r,tube,col):
 s=vtk.vtkParametricTorus();s.SetRingRadius(r);s.SetCrossSectionRadius(tube)
 u=vtk.vtkParametricFunctionSource();u.SetParametricFunction(s);u.SetUResolution(128);u.SetVResolution(14)
 return geom(u,col,.65,95)

def texture_plane(im,xw,yh,front=.0):
 im=im.convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 data=im.tobytes(); imp=vtk.vtkImageImport();imp.CopyImportVoidPointer(data,len(data))
 imp.SetDataScalarTypeToUnsignedChar();imp.SetNumberOfScalarComponents(3)
 ww,hh=im.size;imp.SetDataExtent(0,ww-1,0,hh-1,0,0);imp.SetWholeExtent(0,ww-1,0,hh-1,0,0);imp.Update()
 tex=vtk.vtkTexture();tex.SetInputConnection(imp.GetOutputPort());tex.InterpolateOn()
 src=vtk.vtkPlaneSource();src.SetOrigin(-xw/2,-yh/2,front);src.SetPoint1(xw/2,-yh/2,front);src.SetPoint2(-xw/2,yh/2,front);src.Update()
 mp=vtk.vtkPolyDataMapper();mp.SetInputConnection(src.GetOutputPort())
 a=vtk.vtkActor();a.SetMapper(mp);a.SetTexture(tex);a.GetProperty().LightingOff();return a

def text_font(size,bold=False):return ImageFont.truetype(FONTB if bold else FONTR,size)
def center(d,box,text,font,fill):
 b=d.textbbox((0,0),text,font=font);d.text(((box[0]-b[2])/2,box[1]),text,font=font,fill=fill)

def phone_art():
 w,h=720,1310;im=Image.new('RGB',(w,h),(13,26,35));d=ImageDraw.Draw(im)
 for y in range(h):
  k=y/h;d.line((0,y,w,y),fill=(int(15+5*k),int(32+13*k),int(41+14*k)))
 d.rounded_rectangle((45,75,675,128),radius=22,fill=(26,50,57))
 d.text((74,90),'SOVTIVA  /  STUDIO',font=text_font(24,True),fill=(217,224,209))
 d.text((74,197),'VISTAS TOTALES',font=text_font(25,True),fill=(135,169,164))
 d.text((70,245),'100,000',font=text_font(100,True),fill=(238,232,214))
 d.rounded_rectangle((70,418,650,770),radius=34,fill=(22,52,59))
 d.text((99,458),'ALCANCE / ÚLTIMOS 30 DÍAS',font=text_font(21,True),fill=(156,198,184))
 pts=[]
 for i in range(95):
  f=i/94;y=693-180*(.25*f+.20*math.sin(f*8)+.17*math.sin(f*18)+.6*f**3)
  pts.append((107+f*470,y))
 d.line(pts,fill=(104,190,170),width=7,joint='curve')
 for x,y in pts[::20]:d.ellipse((x-5,y-5,x+5,y+5),fill=(196,227,206))
 d.text((75,854),'VISTAS NO SON PAGOS',font=text_font(23,True),fill=(164,186,181))
 d.rounded_rectangle((74,928,650,1070),radius=22,fill=(34,63,66))
 d.text((105,962),'Verifica condiciones y topes',font=text_font(27,True),fill=(237,230,216))
 d.text((105,1008),'antes de calcular ingresos.',font=text_font(22),fill=(181,203,195))
 d.text((74,1220),'sovtiva.com / journal',font=text_font(23),fill=(127,157,154))
 return im

def ledger_art(denied=False):
 w,h=840,1120;bg=(233,227,210) if not denied else (215,205,198)
 im=Image.new('RGB',(w,h),bg);d=ImageDraw.Draw(im)
 d.rectangle((58,65,782,72),fill=(151,156,141))
 d.text((64,96),'RESUMEN DE CAMPAÑA',font=text_font(36,True),fill=(38,58,64))
 d.text((66,156),'EJEMPLO / NO ES UN PAGO',font=text_font(23),fill=(103,123,117))
 for x,y,txt,val in [(64,316,'VISTAS ELEGIBLES','100,000'),(64,442,'TARIFA PUBLICADA','~$1.09 / 1K'),(64,569,'ESTADO','APROBADO' if not denied else 'NO APROBADO')]:
  d.text((x,y),txt,font=text_font(25,True),fill=(91,107,106))
  bb=d.textbbox((0,0),val,font=text_font(34,True));d.text((775-bb[2],y-4),val,font=text_font(34,True),fill=(38,57,61) if not denied else (115,56,66))
  d.line((65,y+79,775,y+79),fill=(173,174,162),width=2)
 d.text((64,752),'BRUTO SI SE APRUEBA',font=text_font(29,True),fill=(75,94,93))
 d.text((58,800),'$0' if denied else '$109',font=text_font(115,True),fill=(133,47,70) if denied else (34,92,80))
 d.text((66,1010),'Sujeto a reglas, topes y fondos disponibles.',font=text_font(22),fill=(98,109,100))
 return im

def end_art():
 w,h=900,400;im=Image.new('RGB',(w,h),(24,43,47));d=ImageDraw.Draw(im)
 d.rounded_rectangle((18,18,882,382),radius=16,outline=(102,145,126),width=4)
 d.text((100,112),'sovtiva.',font=text_font(130,True),fill=(238,232,213))
 d.text((111,285),'EL CONTEXTO IMPORTA.',font=text_font(29,True),fill=(164,198,181))
 return im

ren=vtk.vtkRenderer();ren.SetGradientBackground(True);ren.SetBackground(.022,.046,.065);ren.SetBackground2(.048,.087,.099);ren.SetUseFXAA(False)
win=vtk.vtkRenderWindow();win.SetOffScreenRendering(True);win.SetSize(W,H);win.SetMultiSamples(8);win.AddRenderer(ren)
cam=ren.GetActiveCamera();cam.SetViewAngle(34);cam.SetPosition(0,0,12);cam.SetFocalPoint(0,0,0);cam.SetViewUp(0,1,0)
for pos,col,bright in [((-6,7,8),(.73,.91,.82),2.3),((4,-2,6),(1,.62,.49),1.2),((2,3,-5),(.46,.85,.81),2.1)]:
 l=vtk.vtkLight();l.SetPosition(*pos);l.SetFocalPoint(0,0,0);l.SetColor(*col);l.SetIntensity(bright);ren.AddLight(l)
ren.SetAmbient(.12,.12,.12)
# Stage and atmospheric elements
floor=box(24,.10,22,(.026,.047,.057),.32);floor.SetPosition(0,-3.38,-1.7);ren.AddActor(floor)
left=box(.10,9,12,(.043,.081,.091),.16);left.SetPosition(-5.5,0,-3.7);ren.AddActor(left)
rim_a=box(.05,6,.05,JADE,.55);rim_a.SetPosition(-3.45,.2,-4.3);ren.AddActor(rim_a)
rim_b=box(.05,6,.05,BRASS,.55);rim_b.SetPosition(3.45,.2,-4.3);ren.AddActor(rim_b)
# distant sculptural rings
ambient=[]
for k in range(5):
 a=torus(2.5+.25*k,.009,(.12+.02*k,.27+.018*k,.28+.01*k));a.SetPosition((k-2)*1.25,.3,-5.8-k*.4)
 a.SetOrientation(65,20+k*17,10*k);ren.AddActor(a);ambient.append(a)

scenes={x:[] for x in range(5)}
def add(s,a):ren.AddActor(a);scenes[s].append(a);return a

def group(items):
 assembly=vtk.vtkAssembly()
 for item in items: assembly.AddPart(item)
 return assembly

# Scene 0: dimensional glass/metal social analytics device
phonebody=rounded_box(2.45,4.93,.24,.29,(.18,.24,.25))
back=rounded_box(2.54,5.04,.22,.31,(.34,.38,.36))
back.SetPosition(0,0,-.045)
screen=texture_plane(phone_art(),2.30,4.78,.146)
button=box(.09,.42,.16,(.65,.63,.57));button.SetPosition(1.265,.7,0)
camera_ring=torus(.11,.014,(.14,.20,.22));camera_ring.SetPosition(0,2.27,.153)
phone=group([back,phonebody,screen,button,camera_ring]);add(0,phone)
# Small independent physical motifs (true parallax)
phonecoins=[]
for k in range(5):
 a=cylinder(.22+(k%2)*.05,.095,BRASS if k%2 else JADE);add(0,a);phonecoins.append(a)
# Scene 1: physical gold studio token, not a giant text title
coincore=cylinder(1.52,.34,(.66,.48,.24));coinrim=torus(1.43,.065,(.89,.71,.41));coinrim.SetPosition(0,0,.24)
inner=torus(1.08,.018,(.91,.75,.46));inner.SetPosition(0,0,.238)
coinamount=texture_plane(Image.new('RGB',(500,500),(169,123,61)),2.06,2.06,.236)
# use a separate golden inset with precise printing and soft contrast
coinpanel=Image.new('RGB',(640,640),(154,110,55));p=ImageDraw.Draw(coinpanel)
p.ellipse((25,25,615,615),fill=(180,140,75),outline=(225,191,123),width=14)
p.ellipse((84,84,556,556),outline=(224,186,115),width=3)
center(p,(640,245),'$109',text_font(129,True),(245,223,167))
center(p,(640,408),'GROSS*',text_font(32,True),(233,206,152))
coinprinted=texture_plane(coinpanel,2.89,2.89,.196)
# texture is square, would overshoot coin edges; instead inset a circular disk via clipping alpha unsupported; 2.89 square clipped? hide texture with rounded geometry needs circle alpha. use 3D metal coin and typography as separate plane to camera slightly in front
coinface=cylinder(1.31,.03,(.72,.53,.30));coinface.SetPosition(0,0,.207)
coin_group=group([coincore,coinrim,inner,coinface]);add(1,coin_group)
# 3D extruded dollar label, with physical shading in front of coin
vtext=vtk.vtkVectorText();vtext.SetText('109')
extr=vtk.vtkLinearExtrusionFilter();extr.SetInputConnection(vtext.GetOutputPort());extr.SetScaleFactor(.11);extr.CappingOn()
mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(extr.GetOutputPort())
text3=vtk.vtkActor();text3.SetMapper(mapper);phong(text3,(.94,.79,.49),.85,100)
text3.SetScale(.66,.66,.66);text3.SetPosition(-1.05,-.36,.27)
# put 3D lettering inside coin assembly for unified rotation
coin_group.AddPart(text3)
smallcoins=[]
for k in range(7):
 a=cylinder(.20,.07,(.63,.45,.24) if k%2 else (.35,.62,.54));add(1,a);smallcoins.append(a)
# Scene 2: real receipt body and printed image on angled paper
ledgerbody=rounded_box(3.15,4.14,.13,.09,(.87,.83,.73));ledgertex=texture_plane(ledger_art(False),3.04,4.04,.09)
receipt=group([ledgerbody,ledgertex]);receipt.SetScale(.90,.90,.90);add(2,receipt)
receipt_trim=box(3.20,.03,.10,BRASS);receipt_trim.SetPosition(0,2.12,.08)
receipt.AddPart(receipt_trim)
# Scene 3: same object, changed eligibility, uneasy color / no fake payout
ledgerbody2=rounded_box(3.15,4.14,.13,.09,(.75,.70,.64));ledgertex2=texture_plane(ledger_art(True),3.04,4.04,.09)
receipt_fail=group([ledgerbody2,ledgertex2]);receipt_fail.SetScale(.90,.90,.90);add(3,receipt_fail)
redring=torus(2.38,.025,WINE);redring.SetPosition(0,0,-1.3);add(3,redring)
# Scene 4: physical illuminated studio nameplate
plaque=rounded_box(3.95,1.91,.20,.13,(.13,.23,.24));plaque_tex=texture_plane(end_art(),3.78,1.75,.125)
brand=group([plaque,plaque_tex]);add(4,brand)
orb=sphere(.82,(.19,.47,.43));orb.SetPosition(1.6,-1.72,-2.3);add(4,orb)
brandring=torus(1.24,.04,BRASS);brandring.SetPosition(1.6,-1.72,-2.3);add(4,brandring)

win2=vtk.vtkWindowToImageFilter();win2.SetInput(win);win2.SetInputBufferTypeToRGB();win2.ReadFrontBufferOff()
# UI: restrained type appears only in a lower safe-area editorial subtitle rail.
BG=(5,21,29);PALE=(238,231,217);MUTED=(163,179,176);ACCENT=(148,195,174)
SCENE_TIMES=[0,3.05,5.8,9.65,12.2,DURATION]
TEXT=[('100,000 vistas.','Parece una fortuna.'),('¿Cuánto podría pagar?','~$109 brutos.*'),('La cifra tiene condiciones.','Vistas válidas, topes, revisión.'),('Un clip no aprobado','puede cobrar $0.'),('Más criterio.','Menos promesas.')]

def scene_idx(t):
 for i in range(5):
  if SCENE_TIMES[i]<=t<SCENE_TIMES[i+1]:return i
 return 4

def motion(t,scene):
 for k,objs in scenes.items():
  for obj in objs:obj.SetVisibility(k==scene)
 local=t-SCENE_TIMES[scene]
 if scene==0:
  intro=ease(local/.9)
  phone.SetPosition(-.03, .25+.09*math.sin(local*1.1),-1.7+1.7*intro)
  phone.SetOrientation(-6+2*math.sin(local*.65),-16+8*math.sin(local*.9),-3+2*math.sin(local*.6))
  for k,co in enumerate(phonecoins):
   ang=1.05*k+local*(.35+.06*k);co.SetPosition(2.25*math.cos(ang),1.85*math.sin(ang),-1.5+(.6*math.sin(ang+.5)))
   co.SetOrientation(70,17*k+local*55,0)
  cam.SetPosition(.70-.38*local, .28+local*.05,11.1-.37*local);cam.SetFocalPoint(0,.04,0)
 elif scene==1:
  coin_group.SetPosition(0,.45+.05*math.sin(local*2),-1+.9*ease(local/.7))
  coin_group.SetOrientation(8+3*math.sin(local*.8),-12+19*math.sin(local*.65),-12+3*local)
  for k,co in enumerate(smallcoins):
   ang=k*2.399+local*.7;co.SetPosition((2.45+.18*(k%2))*math.cos(ang),1.1+1.8*math.sin(ang),-1.8-.16*k)
   co.SetOrientation(30+local*33,k*27+local*32,k*25)
  cam.SetPosition(1.15-.24*local, .40+.17*math.sin(local),10.2-.20*local);cam.SetFocalPoint(0,.15,0)
 elif scene==2:
  receipt.SetPosition(0,.35+.08*math.sin(local*.5),-.70+1.20*ease(local/.8));receipt.SetOrientation(-6+3*local,-19+8*local,-2+math.sin(local))
  cam.SetPosition(1.2-.23*local,.5+.02*local,10.5-.18*local);cam.SetFocalPoint(0,0,0)
 elif scene==3:
  receipt_fail.SetPosition(-.05,.35,-.20);receipt_fail.SetOrientation(1.5,-6+2.3*local,3.3)
  redring.SetOrientation(8*local,24*local,9*local)
  cam.SetPosition(.4+.12*local, .25,10.4+.06*local);cam.SetFocalPoint(0,0,0)
 else:
  brand.SetPosition(0,.65+.09*math.sin(local*.8),.05);brand.SetOrientation(-3,-12+3*math.sin(local),0)
  orb.SetPosition(1.6,-1.8,-1.4);orb.RotateY(.28)
  brandring.SetOrientation(30+4*local,42+19*local,10*local)
  cam.SetPosition(-.65+.21*local, .33+.07*local,10.8-.35*local);cam.SetFocalPoint(0,-.35,0)
 cam.SetViewUp(0,1,0)
 for i,a in enumerate(ambient):a.SetOrientation(62+3*math.sin(t*.3+i), 16+i*15+t*2, i*10)

def film_overlay(img,t,sc):
 # camera vignette & subtle bloom on bright physical objects; typography in safe areas
 raw=img.convert('RGB');bloom=raw.filter(ImageFilter.GaussianBlur(12))
 raw=Image.blend(raw,bloom,.12)
 from PIL import ImageEnhance
 raw=ImageEnhance.Contrast(raw).enhance(1.04)
 ui=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(ui)
 # top editorial locator
 f12=text_font(18,True);f14=text_font(21,True)
 d.text((52,66),'S O V T I V A    /    N O T A S   D E   C A M P O',font=f12,fill=(185,204,196,230))
 d.line((52,101,130,101),fill=(152,193,171,205),width=2)
 # translucent lower gradient for careful phone safe areas
 grad=Image.new('RGBA',(W,420),(5,18,24,0));pix=grad.load()
 for y in range(420):
  q=y/420;alpha=int(208*(q**1.9))
  ImageDraw.Draw(grad).line((0,y,W,y),fill=(4,16,23,alpha))
 ui.alpha_composite(grad,(0,H-420))
 d=ImageDraw.Draw(ui)
 main,sub=TEXT[sc]
 f1=text_font(49,True);f2=text_font(28)
 d.text((52,1017),main,font=f1,fill=PALE)
 d.text((54,1090),sub,font=f2,fill=(172,209,190))
 if sc==1:
  d.text((54,1140),'*A $1.09 / 1K VISTAS ELEGIBLES',font=text_font(18,True),fill=MUTED)
 if sc==4:
  d.text((54,1140),'LEE EL ANÁLISIS EN SOVTIVA.COM',font=text_font(18,True),fill=MUTED)
 # measured progress, not flashy neon
 d.line((52,1214,W-52,1214),fill=(96,117,116),width=2)
 d.line((52,1214,52+int((W-104)*(t/DURATION)),1214),fill=(179,203,166),width=3)
 # transitions: 5 frames optical dark dip, light touch
 et=t-SCENE_TIMES[sc];rem=SCENE_TIMES[sc+1]-t
 dip=0
 if sc>0 and et<.14:dip=max(dip, int(110*(1-et/.14)))
 if sc<4 and rem<.1:dip=max(dip, int(110*(1-rem/.1)))
 if dip: ImageDraw.Draw(ui).rectangle((0,0,W,H),fill=(2,8,12,dip))
 final=Image.alpha_composite(raw.convert('RGBA'),ui).convert('RGB')
 # subtle fixed film-grain (soft enough not to provoke visual noise)
 return final

def render_frame(t):
 s=scene_idx(t);motion(t,s);win.Render();win2.Modified();win2.Update()
 arr=vtk_to_numpy(win2.GetOutput().GetPointData().GetScalars()).reshape(H,W,3)[::-1].copy()
 return film_overlay(Image.fromarray(arr,'RGB'),t,s)

def sound(path):
 # Fully original procedural score: soft F minor drones, stereo glass plucks, brushed percussion, airy transitions.
 from scipy.signal import butter,sosfilt
 import wave
 sr=44100;n=round(sr*DURATION); tt=np.arange(n,dtype=np.float64)/sr
 rng=np.random.default_rng(2036)
 out=np.zeros((n,2),dtype=np.float64)
 def envelope(x,attack,decay):return (1-np.exp(-x/(attack+.001)))*np.exp(-x/(decay+.001))
 def note(start,freq,amp=.1,dec=.9,pan=.0):
  ix=int(start*sr);end=min(n,ix+int(sr*min(4.5,dec*5)))
  if end<=ix:return
  t=np.arange(end-ix)/sr;sig=(np.sin(2*np.pi*freq*t)+.22*np.sin(2*np.pi*freq*2.01*t))*envelope(t,.01,dec)
  out[ix:end,0]+=amp*(1-pan)/2*sig;out[ix:end,1]+=amp*(1+pan)/2*sig
 # ambient soft synth chords: F minor → Db major → Ab major → Eb major
 chords=[(0,[87.31,130.81,174.61]),(3.05,[69.30,103.83,138.59]),(5.8,[103.83,155.56,207.65]),(9.65,[77.78,116.54,155.56]),(12.2,[87.31,130.81,174.61])]
 for i,(st,fs) in enumerate(chords):
  en=SCENE_TIMES[i+1]-st
  for j,f in enumerate(fs):
   ix=int(st*sr);end=min(n,int((st+en+.18)*sr));t=np.arange(end-ix)/sr
   env=np.minimum(1,t/.42)*np.minimum(1,np.maximum(.0,(en+.18-t)/.44))
   sig=(np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*f*2*t))*.030*env
   out[ix:end,0]+=(.56+.14*j)*sig;out[ix:end,1]+=(.70-.10*j)*sig
 for at in np.arange(.22,DURATION,.63):
  note(float(at),390+(int(at*10)%4)*82,.025,.18,(-1 if int(at*10)%2 else 1)*.22)
 for at in [0,3.05,5.8,9.65,12.2]:
  note(at,60,.15,.28,0)
  ix=int(at*sr);dur=int(.43*sr);end=min(n,ix+dur);t=np.arange(end-ix)/sr
  noise=rng.normal(size=len(t));filtered=sosfilt(butter(3,900,fs=sr,btype='lowpass',output='sos'),noise)
  sig=filtered*.045*np.sin(np.pi*np.minimum(1,t/.43))**2
  out[ix:end,0]+=.65*sig;out[ix:end,1]+=.9*sig
 for at,freq in [(1.4,523),(4.1,659),(6.85,784),(8.6,523),(10.55,349),(13.55,523),(14.5,659)]:note(at,freq,.050,.55,.3)
 # broad warmth and strict headroom
 fade=np.minimum(1,tt/.17)*np.minimum(1,np.maximum(0,(DURATION-tt)/.40))
 out*=fade[:,None];out=sosfilt(butter(4,12000,fs=sr,btype='lowpass',output='sos'),out,axis=0)
 peak=np.max(np.abs(out));out*=min(1,.74/max(.001,peak))
 with wave.open(str(path),'wb') as wf:
  wf.setnchannels(2);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes((out*32767).astype('<i2').tobytes())

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 if args.preview:
  ts=[1.3,3.85,7.0,10.7,13.7]
  ims=[]
  for j,t in enumerate(ts):
   im=render_frame(t);im.save(ROOT/f'v4_preview_{j}.jpg',quality=90)
   ims.append(im.copy().resize((288,512)))
  sheet=Image.new('RGB',(5*288,512),(5,15,19))
  for i,im in enumerate(ims):sheet.paste(im,(i*288,0))
  sheet.save(ROOT/'v4_storyboard.jpg',quality=91)
  print('PREVIEW_READY',str(ROOT/'v4_storyboard.jpg'))
  raise SystemExit(0)
 t0=time.monotonic();outvideo=ROOT/'SOVTIVA_Cinema_Notes_V4.mp4';raw=ROOT/'raw_3d.mp4'
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',raw]
 pr=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
 for frame in range(N):
  im=render_frame(frame/FPS)
  try:pr.stdin.write(im.tobytes())
  except BrokenPipeError:raise RuntimeError('video encode closed early')
  if frame%72==0:print('frame',frame,'/',N,'elapsed',round(time.monotonic()-t0,1),flush=True)
 pr.stdin.close();pr.wait();assert pr.returncode==0
 wav=ROOT/'original_score.wav';sound(wav)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-i',str(wav),'-c:v','libx264','-crf','18','-preset','medium','-c:a','aac','-b:a','192k','-pix_fmt','yuv420p','-movflags','+faststart','-shortest','-af','volume=13.5dB',str(outvideo)],check=True)
 for j,t in enumerate([1.3,3.85,7.0,10.7,13.7]):render_frame(t).save(ROOT/f'v4_preview_{j}.jpg',quality=90)
 sheet=Image.new('RGB',(5*288,512),(5,15,19))
 for j in range(5):sheet.paste(Image.open(ROOT/f'v4_preview_{j}.jpg').resize((288,512)),(j*288,0))
 sheet.save(ROOT/'v4_storyboard.jpg',quality=91)
 probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=codec_name,width,height','-of','json',str(outvideo)])
 print('DONE',str(outvideo),'seconds',round(time.monotonic()-t0,1),'FFPROBE',probe.decode()[:700])
