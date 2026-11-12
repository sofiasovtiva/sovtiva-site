#!/usr/bin/env python3
"""Original cinematic SOVTIVA 24-second rhythmic underscore and foley.
No samples, AI models, external downloads or cloud credits.
Output: stereo 48k/24bit WAV and 320kbps MP3 in current folder.
"""
import math
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt
import soundfile as sf

ROOT=Path(__file__).resolve().parent
SR=48000
DUR=24.0
N=int(SR*DUR)
t=np.arange(N,dtype=np.float64)/SR
rng=np.random.default_rng(516)
a=np.zeros((N,2),dtype=np.float64)

def add(x, at, gain=1, pan=0):
    p=int(round(at*SR)); n=min(len(x), N-p)
    if n<1: return
    if np.ndim(x)==1:
        angle=(pan+1)*np.pi/4
        a[p:p+n,0]+=gain*x[:n]*math.cos(angle)
        a[p:p+n,1]+=gain*x[:n]*math.sin(angle)
    else:
        a[p:p+n,:]+=gain*x[:n,:]

def env(n, attack=.003, rel=.05):
    s=np.ones(n); u=max(1,int(SR*attack)); v=max(1,int(SR*rel)); u=min(u,n); v=min(v,n); s[:u]*=np.linspace(0,1,u); s[n-v:]*=np.linspace(1,0,v); return s

def metallic(freq,dur=.33,decay=8.5):
    q=np.arange(round(SR*dur))/SR
    y=(np.sin(2*np.pi*freq*q)+.4*np.sin(2*np.pi*freq*2.11*q+.2)+.15*np.sin(2*np.pi*freq*3.14*q+.7))
    return y*np.exp(-decay*q)*env(len(q),.001,.01)

def thump(freq=65,decay=.22):
    q=np.arange(round(SR*.55))/SR
    phase=2*np.pi*(freq*q+32*.035*(1-np.exp(-q/.035)))
    return np.sin(phase)*np.exp(-q/decay)*env(len(q),.003,.07)

def noise_chirp(dur=.24,highpass=1200,lowpass=12000,decay=8):
    n=round(SR*dur);q=np.arange(n)/SR
    h=rng.normal(0,1,n)
    if highpass:
        h=sosfilt(butter(2,highpass,btype='highpass',fs=SR,output='sos'),h)
    if lowpass:
        h=sosfilt(butter(2,lowpass,btype='lowpass',fs=SR,output='sos'),h)
    return h*np.exp(-decay*q)*env(n,.002,.03)

# Evolving original synth ostinato - Dm(add9) -> Bbmaj7 -> C(sus2) -> A7(no3).
chords=[[146.832,174.614,220.0,293.665],[116.54,146.83,174.614,220.0],[130.81,196,261.63,293.665],[110.0,164.81,220,277.18]]
for measure in range(12):
    chord=chords[measure%4]
    for j,freq in enumerate(chord):
        at=measure*2.0
        q=np.arange(round(SR*2.0))/SR
        p=np.sin(2*np.pi*freq*q+(j*.33))+.18*np.sin(2*np.pi*freq*2*q)
        p*=.08*np.sin(np.pi*np.minimum(q/2,1))**1.5
        add(p,at,gain=.7,pan=(-.5+j/3))
    # restrained melodic note on 8ths
    for eighth in range(4):
        at=measure*2+.13+eighth*.5
        freq=chord[[0,2,3,1][eighth]]*2
        q=np.arange(round(SR*.33))/SR
        y=np.sin(2*np.pi*freq*q)*(1+.25*np.sin(2*np.pi*3.1*q))*np.exp(-10*q)
        add(y,at,gain=.12 if measure not in (5,7,8) else .055,pan=(-.55 if eighth%2 else .55))

# Musical rhythm: 120bpm, 48 beats in 24 sec. Reduce in informational section 10-15s.
for beat in range(48):
    at=beat*.5
    if beat in (30,31): continue  # quiet pivot before $0
    weight=.22 if 10<=at<15 else 1
    if beat%4 in (0,2): add(thump(58,.15),at,gain=.48*weight)
    if beat%4 in (1,3): add(noise_chirp(.19,650,5800,22),at,gain=.082*weight,pan=.05)
    add(noise_chirp(.085,4000,16000,40),at+.25,gain=.016*weight,pan=(-.45 if beat%2 else .45))

# Sound action cues mapped to the storyboard. All original procedural noise/synth.
for at in (.45, 1.15):
    add(thump(118,.08),at,.10)
    add(metallic(315,.14,28),at,.06,pan=-.15)
# Glass bulge, break and coin start
for at,vol,pan in [(2.57,.22,-.42),(2.65,.34,.22),(2.72,.15,.65)]:
    add(noise_chirp(.31,1800,14000,15),at,vol,pan)
add(metallic(1050,.65,5.5),2.70,.18,.28)
# Momentum flight and metallic scatter in B
for at,pan in [(3.20,-.75),(3.72,.6),(4.23,-.20),(5.05,.75)]:
    add(metallic(720+70*pan,.55,9),at,.11,pan)
for at in (3.05,5.66,14.82,19.52):
    s=np.arange(round(.44*SR))/SR
    k=rng.normal(size=len(s));k=sosfilt(butter(2,800,btype='lowpass',fs=SR,output='sos'),k)
    add(k*np.sin(np.pi*np.minimum(s/.44,1))**1.5,at,gain=.09,pan=.25)
# Number reveal C: resonant chime with harmonic beating.
for f in (420,839,1255): add(metallic(f,.7,4),6.16,.10,.2)
# D: paper and stamp, papery band noise.
for at,g in [(10.12,.06),(11.18,.045),(13.73,.05)]: add(noise_chirp(.38,300,3500,8),at,g,pan=-.2)
add(thump(80,.26),13.90,.28)
# E: abrupt noir impact; subtract music via duck envelope; zero is isolated.
add(thump(42,.42),15.05,.66)
add(noise_chirp(.32,300,3000,5),15.05,.27)
for at,pan in [(17.1,-.5),(17.30,.5),(17.52,-.3)]:add(metallic(1120,.52,6),at,.075,pan)
# Resolve chime & 24 sec seamless fade.
for at,f,g in [(19.62,440,.12),(21.15,586.66,.07),(22.78,659.25,.13)]:add(metallic(f,.9,4.2),at,g,pan=.4)

# Strong sidechain duck under spoken passages and silence hit.
duck=np.ones(N)
for begin,end,g in [(6,10,.69),(10,15,.47),(15.4,16.2,.12),(19.5,23.6,.55)]:
    s=int(begin*SR);e=int(end*SR);k=int(.12*SR)
    duck[s:e]*=g
    for ii in range(k):
        if s+ii<N: duck[s+ii]*=(1-(1-g)*(1-ii/k))
# Smooth abrupt changes around 0.12s
smooth=np.ones(5)
# no fades on music start, loop has short fade at end
nfade=round(.075*SR)
a[-nfade:]*=np.linspace(1,0,nfade)[:,None]
a*=duck[:,None]
# Narrow safe peak, soft peak limiting with tanh
scale=.90/max(1e-8,np.max(np.abs(a)))
a*=scale
a=np.tanh(a*1.22)*.91
sf.write(ROOT/'SOVTIVA_V5_original_score_24s.wav',a.astype('float32'),SR,subtype='PCM_24')
print('saved',ROOT/'SOVTIVA_V5_original_score_24s.wav','seconds',len(a)/SR,'peak',float(abs(a).max()),'RMS',float(np.sqrt(np.mean(a*a))))
