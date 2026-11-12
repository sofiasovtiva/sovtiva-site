#!/usr/bin/env python3
"""Sovtiva original social-video v2 kinetic typographic renderer. No external assets, audio or paid services."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math, os, functools, json, wave, time, subprocess
from pathlib import Path
W,H,FPS=720,1280,24
BPM=132
BEAT=60/BPM
CUT_BEATS=[0,4,8,12,16,22,28,36,40]
CUTS=[b*BEAT for b in CUT_BEATS]
DUR=CUTS[-1]
N=round(DUR*FPS)
O=Path(__file__).resolve().parent
DARK=(11,31,41); DARK2=(18,57,67); CYAN=(166,226,224); CREAM=(242,235,222); BURG=(127,48,76); OLIVE=(104,124,103); WHITE=(250,250,244); RED=(236,111,124); MUTED=(139,172,178)
FB='/usr/share/fonts/truetype/lato/Lato-Black.ttf'; FS='/usr/share/fonts/truetype/lato/Lato-Semibold.ttf'; FM='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
FONTS={}
def font(n,kind='black'):
 key=(n,kind)
 if key not in FONTS: FONTS[key]=ImageFont.truetype({'black':FB,'semibold':FS,'regular':FM}[kind],n)
 return FONTS[key]
@functools.lru_cache(maxsize=350)
def text_layer(text,size,color,kind='black'):
 f=font(size,kind)
 b=f.getbbox(text,stroke_width=0)
 width=max(1,b[2]-b[0]); height=max(1,b[3]-b[1]); im=Image.new('RGBA',(width+8,height+10),(0,0,0,0))
 d=ImageDraw.Draw(im);d.text((4-b[0],4-b[1]),text,font=f,fill=(*color,255))
 return im

def ease(x):
 x=max(0,min(1,x));return 1-(1-x)**3

def pop(x):
 x=max(0,min(1,x));return 1+math.exp(-8*x)*.16*math.cos(22*x)

def clamp(x,a=0,b=1):return max(a,min(b,x))

def layer(canvas,text,size,col,x,y,align='left',scale=1,alpha=1,kind='black'):
 if alpha<=0:return
 im=text_layer(str(text),int(size),col,kind)
 if abs(scale-1)>.001: im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.Resampling.BICUBIC)
 if alpha<.99: im=im.copy(); im.putalpha(im.getchannel('A').point(lambda p:int(p*alpha)))
 if align=='center': x-=im.width/2
 elif align=='right': x-=im.width
 canvas.paste(im,(int(x),int(y)),im)

def rr(d,box,r,fill,outline=None,width=1):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def bg_for(k):
 bgcols=[DARK,DARK2,CREAM,DARK,DARK2,CREAM,DARK2,DARK]
 a=np.asarray(bgcols[k],dtype=np.float32)
 yy,xx=np.mgrid[0:H,0:W]
 wave=(xx/W*.75+yy/H*.55)
 flare=np.exp(-(((xx/W-.92)**2)/.5+((yy/H-.06)**2)/.4))*20
 dark=(wave*7+flare).astype(np.float32)
 if k in (2,5):dark=-dark*.34
 grad=np.clip(a[None,None,:]+dark[:,:,None]*np.array([.4,.7,.85])[None,None,:],0,255).astype(np.uint8)
 rng=np.random.default_rng(125+k)
 tex=rng.integers(-4,5,size=(H,W,1),dtype=np.int16)
 grad=np.clip(grad.astype(np.int16)+tex,0,255).astype(np.uint8)
 return Image.fromarray(grad,'RGB').convert('RGBA')
BGS=[bg_for(i) for i in range(8)]

def ui(canvas,d,k,t,maincol,back):
 # subtle animated circular line art and native vertical-video frame guides
 X=int(W*.82+math.sin(t*.75)*15); Y=int(H*.27+math.cos(t*.45)*25)
 for r in [180,275,380]:d.arc((X-r,Y-r,X+r,Y+r),-63+int(t*9),50+int(t*9),fill=(*maincol,38),width=2)
 for i in range(8):
  yy=115+i*134
  d.line((0,yy+int(math.sin(t+i)*4),W,yy+int(math.sin(t+i)*4)),fill=(*maincol,12),width=1)
 rr(d,(34,43,686,98),26,(*(CREAM if k in (2,5) else DARK),255),(*maincol,80),2)
 layer(canvas,'SOVTIVA / RESEARCH',19,maincol,57,58,kind='semibold')
 layer(canvas,'ORIGINAL / 001',16,maincol,662,60,align='right',kind='semibold')
 d.line((42,1164,678,1164),fill=(*maincol,145),width=2)
 layer(canvas,'sovtiva.',22,maincol,44,1182)
 layer(canvas,f'{int(k+1):02} / 08',18,maincol,675,1187,align='right',kind='semibold')
 for j in range(40):
  x=44+j*15.3; fill=(*CYAN,220) if j<=(t/DUR)*40 else (*maincol,35)
  d.rectangle((x,1138,x+8,1145),fill=fill)

def fly(canvas,text,size,col,x,y,t,delay=0,offset=105,align='left',kind='black'):
 p=ease((t-delay)/.34)
 layer(canvas,text,size,col,x,y+offset*(1-p),align=align,scale=1.12-.12*p,alpha=p,kind=kind)

def draw_scene(k,t,globalt):
 canvas=BGS[k].copy();d=ImageDraw.Draw(canvas,'RGBA');dark=(k in (2,5));main=DARK if dark else CREAM;soft=DARK2 if dark else CYAN
 ui(canvas,d,k,globalt,main, (255,255,255) if not dark else (0,0,0))
 if k==0:
  fly(canvas,'100,000',176,CREAM,360,322,t,0,.0 if False else 220,'center')
  fly(canvas,'VISTAS',132,CYAN,360,539,t,.13,120,'center')
  layer(canvas,'A VER...',38,MUTED,360,722+22*math.sin(t*3),'center',alpha=clamp((t-.4)*3),kind='semibold')
  # explosive sunburst thin strokes
  for j in range(28):
   a=j*math.tau/28; out=295*ease(t/.45);inner=230*ease(t/.45)
   x,y=360,462
   d.line((x+math.cos(a)*inner,y+math.sin(a)*inner,x+math.cos(a)*out,y+math.sin(a)*out),fill=(*CYAN,int(115*max(0,1-t/1.9))),width=3)
  rr(d,(168,861,555,936),18,(*BURG,240));layer(canvas,'SUENA BRUTAL',35,CREAM,360,875,'center')
 elif k==1:
  fly(canvas,'¿YA ME HICE',77,CREAM,360,292,t,.05,100,'center')
  fly(canvas,'RICO?',157,CYAN,360,425,t,.17,150,'center')
  # playful loading wheel from 0 to 100
  progress=clamp((t-.1)/1.15)
  d.arc((270,685,450,865),0,359,fill=(*CREAM,65),width=15)
  d.arc((270,685,450,865),-90,-90+round(progress*359),fill=(*CYAN,255),width=15)
  layer(canvas,str(int(progress*100))+'%',43,CREAM,360,750,align='center')
  for j in range(17):
   a=j*2.4;py=640+int((j*91+globalt*150)%460);px=70+(j*131)%570
   d.ellipse((px,py,px+7,py+7),fill=(*((CREAM,CYAN,RED)[j%3]),int(170*max(0,1-abs(t-1)/1.5))))
 elif k==2:
  fly(canvas,'EN ALGUNAS',48,DARK,360,229,t,.03,100,'center')
  fly(canvas,'CAMPAÑAS',64,DARK,360,300,t,.12,130,'center')
  # highlighted physical receipt
  p=ease(t/.45); x=92; y=414+int((1-p)*200)
  d.rounded_rectangle((x,y,x+536,y+422),radius=16,fill=(*WHITE,255),outline=(*BURG,160),width=3)
  for n in range(7):
   d.line((122,y+120+n*32,598,y+120+n*32),fill=(*DARK,14),width=1)
  layer(canvas,'PAGO ESTIMADO',27,OLIVE,127,y+38,kind='semibold')
  layer(canvas,'US$'+str(round(109*ease((t-.25)/1.1))),124,BURG,360,y+149,align='center')
  layer(canvas,'BRUTOS*',41,DARK,360,y+295,align='center')
  layer(canvas,'*Si las vistas califican',23,OLIVE,360,y+358,align='center',kind='semibold')
 elif k==3:
  fly(canvas,'LA CUENTA:',49,CYAN,60,218,t,.1,80)
  # math cards animated separately
  boxes=[('100,000',.16),(u'÷ 1,000',.42),('× 1.09',.70)]
  for j,(tx,delay) in enumerate(boxes):
   p=ease((t-delay)/.35); top=318+j*163+int((1-p)*95)
   d.rounded_rectangle((85,top,635,top+124),radius=27,fill=(*(CYAN if j==2 else CREAM),int(235*p)))
   layer(canvas,tx,65,DARK,360,top+18,align='center',alpha=p)
  fly(canvas,'≈ US$109',76,CREAM,360,867,t,1.13,85,'center')
  layer(canvas,'TARIFA ILUSTRATIVA • NO GARANTÍA',19,MUTED,360,1016,align='center',kind='semibold')
 elif k==4:
  fly(canvas,'PERO...',126,CREAM,360,236,t,.04,120,'center')
  fly(canvas,'NO ES',85,CYAN,360,464,t,.19,85,'center')
  fly(canvas,'GANANCIA',112,CREAM,360,580,t,.29,85,'center')
  for j,(tx,fill) in enumerate([('TIEMPO',BURG),('EDICIÓN',OLIVE),('REVISIONES',DARK)]):
   x=72+(j%2)*70;y=825+j*72; p=ease((t-.54-j*.1)/.27)
   d.rounded_rectangle((x+(1-p)*200,y,x+310+(1-p)*200,y+53),radius=14,fill=(*fill,int(240*p)),outline=(*CYAN,int(120*p)),width=2)
   layer(canvas,tx,28,CREAM,x+31+(1-p)*200,y+11,alpha=p)
 elif k==5:
  fly(canvas,'¿Y SI RECHAZAN',65,DARK,360,239,t,.02,100,'center')
  fly(canvas,'EL CLIP?',78,BURG,360,343,t,.16,100,'center')
  layer(canvas,'US$0',208,DARK,360,597,align='center',scale=pop((t-.45)/.5),alpha=clamp((t-.3)*5))
  # angled red approval stamp
  st=text_layer('NO APROBADO',29,CREAM); bg=Image.new('RGBA',(st.width+30,st.height+25),(*BURG,250));bd=ImageDraw.Draw(bg);bd.rounded_rectangle((2,2,bg.width-2,bg.height-2),radius=10,outline=(*DARK,255),width=4);bg.paste(st,(15,10),st);bg=bg.rotate(11,expand=True)
  p=ease((t-.56)/.35)
  if p>0: canvas.paste(bg,(int(345+(1-p)*190),int(830-(1-p)*80)),bg)
 elif k==6:
  fly(canvas,'MEJOR:',56,CYAN,68,223,t,.05,120)
  fly(canvas,'HAZ BUENOS',90,CREAM,68,328,t,.19,125)
  fly(canvas,'VIDEOS.',122,CYAN,65,457,t,.28,125)
  # fake editing timeline with live moving playhead, 3 video crops and sound wave
  rr(d,(47,680,674,1009),23,(*DARK,255),(*CYAN,130),2)
  layer(canvas,'SOVTIVA / TIMELINE',23,MUTED,74,708,kind='semibold')
  for j in range(5):
   x=77+j*111;y=768;fg=(CYAN,BURG,OLIVE,CREAM,CYAN)[j]
   rr(d,(x,y,x+102,y+114),12,(*fg,235));d.rectangle((x+10,y+20,x+92,y+36),fill=(*DARK,60));d.ellipse((x+23,y+47,x+79,y+101),outline=(*DARK,180),width=4)
  yy=929
  for n in range(70):
   xx=83+n*7.7; ampl=12+23*abs(math.sin(n*.44))*abs(math.sin(n*.13+.7))
   d.line((xx,yy-ampl,xx,yy+ampl),fill=(*CYAN,170),width=3)
  xp=74+545*clamp(t/(CUTS[7]-CUTS[6]));d.line((xp,748,xp,996),fill=(*RED,250),width=5)
  layer(canvas,'NO LA SUERTE DEL ALGORITMO.',28,MUTED,360,1043,align='center',kind='semibold')
 else:
  # outro with deliberate simple motion and motion line to differentiate from slide
  for j in range(6):
   a=(j+1)*math.pi/7
   x=360+math.cos(a+globalt*.1)*450; y=520+math.sin(a+globalt*.1)*390
   d.ellipse((x-65,y-65,x+65,y+65),outline=(*CYAN,50),width=3)
  fly(canvas,'MIDE EL',101,CREAM,360,316,t,.05,130,'center')
  fly(canvas,'RESULTADO.',116,CYAN,360,452,t,.16,140,'center')
  d.rounded_rectangle((80,722,638,866),radius=26,fill=(*CREAM,255))
  layer(canvas,'LA INVESTIGACIÓN COMPLETA',25,DARK,359,750,align='center',kind='semibold')
  layer(canvas,'sovtiva.com/journal',36,BURG,360,806,align='center')
  layer(canvas,'CPM: oferta mediana, no pago asegurado.',20,MUTED,360,943,align='center',kind='semibold')
 # quick editorial flash at each cut
 alpha=int(75*max(0,1-t/.07))
 if alpha:d.rectangle((0,0,W,H),fill=(*(CREAM if not dark else DARK),alpha))
 return canvas.convert('RGB')

def write_audio(filename):
 import scipy.signal as sig
 SR=44100; n=round(DUR*SR);audio=np.zeros(n,dtype=np.float32); rng=np.random.default_rng(28)
 def add(start,x,amp=1):
  idx=int(start*SR);end=min(len(audio),idx+len(x));
  if end>idx:audio[idx:end]+=amp*x[:end-idx]
 # pulsing synthetic bass line, percussion and ear candy, no third-party audio
 for b in range(40):
  tm=b*BEAT
  dur=.32;tt=np.arange(int(dur*SR))/SR
  freq=56*np.exp(-tt*16)+44
  kick=np.sin(2*np.pi*np.cumsum(freq)/SR)*np.exp(-tt*13)
  add(tm,kick*.48)
  if b%4 in (1,3):
   st=np.arange(int(.16*SR))/SR;noise=rng.normal(size=len(st));filtered=sig.sosfilt(sig.butter(2,[800,8500],btype='bandpass',fs=SR,output='sos'),noise)
   add(tm,filtered*np.exp(-st*34)*.18)
  for offset in [0,.5]:
   st=np.arange(int(.085*SR))/SR;noise=rng.normal(size=len(st));filtered=sig.sosfilt(sig.butter(2,6500,btype='highpass',fs=SR,output='sos'),noise)
   add(tm+offset*BEAT,filtered*np.exp(-st*50)*.027)
 # bass groove with four-note loop
 tones=[65.41,65.41,87.31,58.27,65.41,73.42,87.31,58.27]
 for j in range(20):
  st=np.arange(int(.41*SR))/SR;freq=tones[j%len(tones)];x=(np.sin(2*np.pi*freq*st)+.25*np.sin(2*np.pi*freq*2*st))*(1-np.exp(-st*60))*np.exp(-st*5.4)
  add(j*2*BEAT,x*.095)
 # bubbles, impacts, whooshes on each scene change
 for k,tm in enumerate(CUTS[1:-1],1):
  st=np.arange(int(.23*SR))/SR; freq=950*np.exp(-st*11)+140;drop=np.sin(2*np.pi*np.cumsum(freq)/SR)*np.exp(-st*18)
  add(tm,drop*.21)
  st=np.arange(int(.26*SR))/SR;noise=rng.normal(size=len(st));env=np.sin(np.pi*st/.26)**1.3;woosh=sig.sosfilt(sig.butter(1,2000,btype='highpass',fs=SR,output='sos'),noise)
  add(max(0,tm-.26),woosh*env*.045)
 # pleasant tiny digital chimes for momentary surprise (original composition)
 for tm in [2.9,4.4,5.9,9.1,13.1,17.2]:
  st=np.arange(int(.3*SR))/SR;add(tm,(np.sin(2*np.pi*659.25*st)+.55*np.sin(2*np.pi*987.8*st))*np.exp(-st*11)*.024)
 peak=max(1e-9,np.max(np.abs(audio)));audio=audio*(.82/peak)
 with wave.open(str(filename),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((audio*32767).astype('<i2').tobytes())

def render_video():
 print('rendering frames...',flush=True)
 args=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',str(O/'silent_temp.mp4')]
 p=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 curr=0;started=time.time()
 for f in range(N):
  t=f/FPS
  while curr<len(CUTS)-2 and t>=CUTS[curr+1]:curr+=1
  image=draw_scene(curr,t-CUTS[curr],t)
  try:p.stdin.write(image.tobytes())
  except BrokenPipeError:print(p.stderr.read().decode());raise
  if f%120==0:print(f,'/',N,round(time.time()-started,1),'s',flush=True)
 p.stdin.close();error=p.stderr.read().decode();rc=p.wait()
 if rc:raise RuntimeError(error)
 print('frames done',time.time()-started,flush=True)

def finish():
 audiofile=O/'original_audio.wav';write_audio(audiofile)
 out=O/'SOVTIVA_paid_views_motion_v2.mp4'
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(O/'silent_temp.mp4'),'-i',str(audiofile),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','19','-c:a','aac','-b:a','192k','-pix_fmt','yuv420p','-movflags','+faststart','-shortest',str(out)]
 subprocess.run(cmd,check=True)
 sheet=[]
 for k in range(8):
  snap=draw_scene(k,CUTS[k+1]-CUTS[k]-.24,CUTS[k+1]-.24)
  snappath=O/f'scene_{k+1:02}.jpg';snap.save(snappath,quality=88)
  sheet.append(snap.resize((270,480)))
 board=Image.new('RGB',(1080,960),CREAM)
 for i,snap in enumerate(sheet):board.paste(snap,((i%4)*270,(i//4)*480))
 board.save(O/'storyboard_v2.jpg',quality=89)
 print(out,os.path.getsize(out))

if __name__=='__main__':
 render_video();finish()
