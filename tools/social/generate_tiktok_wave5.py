#!/usr/bin/env python3
"""Original Sovtiva Journal vertical microfilms. No external imagery, music or models.
Creates 9 new 1080x1920 H.264 MP4 clips (~16 seconds) and PNG covers.
Generated graphics and copy are original; no customer performance or case study is claimed.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

ROOT=Path("assets/social/tiktok/wave5")
ROOT.mkdir(parents=True,exist_ok=True)
W,H=1080,1920
NAVY=(12,32,39); AQUA=(172,221,221); CREAM=(241,237,225)
BURGUNDY=(131,60,80); OLIVE=(151,159,119)
STORIES=[
("simulon","SIMULON / VIDEO IA",(160,199,180),[
("¿Un mamut que\nte reconoce?","Simulon combina escenas reales con personajes sintéticos.","city"),
("Primero grabas\nla actuación.","Movimiento, voz y entorno alimentan la escena.","inbox"),
("Después se\nregenera el clip.","No es una prueba de render final instantáneo.","layers"),
("La oportunidad:\nun personaje propio.","Licencia, costos y criterio visual. Sovtiva Journal.","proof")]),
("genie4","GOOGLE / MUNDOS IA",(151,181,211),[
("¿Un mundo en\nun solo prompt?","Genie 4 genera entornos interactivos y audio.","city"),
("Puedes cambiar\nel escenario.","Clima, objetos y acciones con instrucciones.","web"),
("Pero aún\nse desordena.","La coherencia cae en sesiones prolongadas.","layers"),
("Simulación,\nno videojuego.","Acceso limitado y fuentes: Sovtiva Journal.","proof")]),
("suncatcher","GOOGLE / IA EN ÓRBITA",(187,196,149),[
("Google envió\nun poema\ndesde el espacio.","Gemma 4 respondió desde un TPU en órbita.","city"),
("La prueba\nsí ocurrió.","Project Suncatcher lanzó un satélite prototipo.","proof"),
("¿Centro de\ndatos espacial?","Faltan energía, comunicaciones y fiabilidad probadas.","stack"),
("Hito real.\nNegocio por probar.","Fuentes oficiales: Sovtiva Journal.","proof")]),
("mischief","TBC / VIDEO IA",(199,146,159),[
("¿Videos hechos\ncon neuronas\nvivas?","El titular es espectacular. El mecanismo, distinto.","voice"),
("Las neuronas\nestán en laboratorio.","El video final corre como software en GPUs.","code"),
("TBC afirma\nque es 5x más rápido.","Es una afirmación del proveedor, no nuestro test.","chart"),
("El costo útil\nes por clip aprobado.","Qué medir: Sovtiva Journal.","proof")]),
("legal","LEGALTECH / IA",(188,157,194),[
("¿Una IA puede\nrevisar contratos?","Anthropic presentó herramientas para equipos legales.","inbox"),
("Puede señalar\ndiferencias.","Con fuentes y un playbook aprobado.","layers"),
("Un abogado\ndebe validar.","Los errores legales no se borran con un prompt.","shield"),
("Automatizar\nsin perder control.","Guía de Sovtiva Journal.","proof")]),
("nemotron","NVIDIA / TRANSCRIPCIÓN",(157,198,165),[
("40 idiomas.\n¿40 resultados\nperfectos?","Nemotron 3.5 Transcribe soporta 40 idiomas.","voice"),
("Identifica voces\ny formatos.","Procesa grabaciones completas, no streaming.","flow"),
("Comprueba cifras\ny nombres propios.","La precisión varía según audio e idioma.","shield"),
("Transcribir no es\nentender sin errores.","Arquitectura: Sovtiva Journal.","proof")]),
("reddit","SEO / AI ANSWERS",(202,162,144),[
("Reddit perdió\n29% en bolsa.","Pero NO perdió 29% de usuarios.","chart"),
("Google envía\nmenos clics.","Las respuestas de IA afectan tráfico referido.","search"),
("Los usuarios\nsemanales crecieron.","Distintas métricas cuentan historias distintas.","chart"),
("No vivas solo\ndel buscador.","Distribución y fuentes: Sovtiva Journal.","proof")]),
("star50","MERCADOS / IA",(182,176,158),[
("¿China perdió\nUS$480,000M?","Reuters reportó una corrección del índice STAR 50.","chart"),
("Caída cercana\nal 40%.","Se trata de valoración bursátil, no de efectivo.","chart"),
("Una acción baja.\nLa tecnología sigue.","La demanda real necesita evidencia propia.","layers"),
("Compra por ROI,\nno por titulares.","Investigación: Sovtiva Journal.","proof")]),
("ram","IA LOCAL / NUBE",(175,183,207),[
("¿La RAM de\ntu PC sobra?","Altman habló de utilización de memoria escasa.","stack"),
("La nube aprovecha\nequipos compartidos.","Pero también añade costos y dependencia.","layers"),
("La IA local\nda más control.","Privacidad, energía y mantenimiento importan.","shield"),
("No elijas bando.\nCalcula el costo.","Criterios: Sovtiva Journal.","proof")])
]
def ff(path,size):
    return ImageFont.truetype(path,size)
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def rect(d,xy,r,fill,outline=None,w=1):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=w)
def illustration(d,kind,accent):
    rect(d,(107,1045,972,1600),35,(22,53,61),(71,103,108),2)
    if kind=="search":
        rect(d,(162,1173,911,1330),22,CREAM)
        d.ellipse((190,1214,245,1269),outline=BURGUNDY,width=7)
        d.line((237,1260,264,1288),fill=BURGUNDY,width=8)
        d.text((280,1230),"¿A QUIÉN RECOMIENDAS?",font=ff(BOLD,31),fill=NAVY)
        for j in range(3):
            rect(d,(186,1380+j*64,854-j*64,1406+j*64),10,accent if j==0 else (90,136,142))
    if kind=="inbox":
        rect(d,(220,1180,857,1480),22,CREAM)
        d.line((230,1194,537,1352,845,1194),fill=BURGUNDY,width=12)
        d.line((230,1468,430,1320),fill=BURGUNDY,width=10)
        d.line((846,1468,640,1320),fill=BURGUNDY,width=10)
        d.ellipse((794,1115,914,1235),fill=(177,60,77))
        d.text((825,1127),"!",font=ff(BOLD,76),fill=CREAM)
    if kind=="flow":
        for j,x in enumerate((164,445,735)):
            if j<2:d.line((x+175,1270,x+272,1270),fill=AQUA,width=8)
            rect(d,(x,1192,x+178,1368),20,(36+j*10,84,93),AQUA,3)
            d.text((x+37,1240),f"0{j+1}",font=ff(BOLD,52),fill=CREAM)
        d.text((191,1460),"CAPTURA     VALIDA      ASIGNA",font=ff(BOLD,29),fill=AQUA)
    if kind=="layers":
        for j in range(3):
            x,y=170+j*60,1183+j*85
            rect(d,(x,y,x+540,y+180),24,(40+j*8,87+j*7,92+j*5),AQUA,2)
        d.text((293,1514),"REPETIR · COMPARAR",font=ff(BOLD,32),fill=CREAM)
    if kind=="chart":
        for j,h in enumerate((215,330,155,390,285)):
            rect(d,(176+j*145,1512-h,268+j*145,1512),9,accent if j==3 else (88,145,150))
        d.line((168,1527,925,1527),fill=AQUA,width=4)
    if kind=="city":
        for j,h in enumerate((185,360,259,421,288,321)):
            x=153+j*135
            d.rectangle((x,1521-h,x+112,1521),fill=(35+j*8,82+j*2,93),outline=AQUA,width=3)
            for k in range(5):
                y=1531-h+k*58
                if y<1498:d.rectangle((x+22,y,x+35,y+21),fill=accent)
        d.line((151,1551,934,1551),fill=OLIVE,width=6)
    if kind=="code":
        for j,t in enumerate(("scene = build_city()","credits = unknown","render(); verify()")):
            rect(d,(173,1170+105*j,900,1240+105*j),11,(15,37,48))
            d.text((204,1186+105*j),t,font=ff(SANS,34),fill=CREAM if j!=1 else (244,179,173))
    if kind=="stack":
        for j,t in enumerate(("TOKENS","CREDITS","RENDERS","REVISIONS")):
            rect(d,(186,1127+97*j,875,1196+97*j),11,(30+j*10,73+j*8,82+j*4))
            d.text((211,1147+97*j),t,font=ff(BOLD,31),fill=CREAM)
            d.line((740,1171+97*j,842,1171+97*j),fill=accent,width=11)
    if kind=="web":
        rect(d,(178,1134,899,1515),20,(237,235,225))
        rect(d,(178,1134,899,1189),19,accent)
        for j in range(3):d.ellipse((203+26*j,1154,217+26*j,1168),fill=(248,240,230))
        rect(d,(224,1232,516,1280),8,(38,78,86))
        rect(d,(224,1310,672,1340),6,(129,154,154))
        rect(d,(224,1365,590,1392),6,(172,191,185))
        rect(d,(224,1430,413,1476),8,(121,62,82))
        rect(d,(693,1225,857,1472),9,(165,192,181))
    if kind=="shield":
        d.polygon([(537,1143),(779,1240),(744,1456),(537,1540),(330,1456),(295,1240)],fill=(26,75,86),outline=accent)
        d.line((423,1336,513,1430,655,1267),fill=CREAM,width=24)
        d.text((375,1560),"PERMISOS",font=ff(BOLD,34),fill=AQUA)
    if kind=="calendar":
        rect(d,(212,1118,870,1532),22,(236,235,228))
        rect(d,(212,1118,870,1218),22,accent)
        for j in range(3):
            for k in range(3):
                x,y=254+k*189,1260+j*77
                rect(d,(x,y,x+128,y+46),9,(123,155,151) if (j+k)%3 else BURGUNDY)
        d.text((280,1483),"IDEA   REVISIÓN   POST",font=ff(BOLD,26),fill=NAVY)
    if kind=="triad":
        for i,(n,t) in enumerate((("01","ENTRADA"),("02","REVISIÓN"),("03","ACCIÓN"))):
            xx=155+270*i
            rect(d,(xx,1216,xx+232,1458),18,(41+i*5,83+i*4,90),AQUA,3)
            d.text((xx+55,1260),n,font=ff(BOLD,60),fill=CREAM)
            d.text((xx+25,1398),t,font=ff(BOLD,22),fill=accent)
            if i<2:d.line((xx+235,1324,xx+269,1324),fill=CREAM,width=6)
    if kind=="clock":
        d.ellipse((363,1143,731,1511),outline=accent,width=16)
        d.ellipse((530,1310,564,1344),fill=CREAM)
        d.line((547,1327,547,1207),fill=CREAM,width=15)
        d.line((547,1327,641,1373),fill=CREAM,width=15)
        d.text((340,1570),"MEDIR ANTES DE COMPRAR",font=ff(BOLD,29),fill=AQUA)
    if kind=="voice":
        for i in range(7):
            x=183+i*108
            hh=[78,160,225,310,186,112,56][i]
            d.line((x,1325-hh//2,x,1325+hh//2),fill=accent if i%2 else AQUA,width=22)
        d.text((300,1510),"ESCUCHA · ACTÚA",font=ff(BOLD,35),fill=CREAM)
    if kind=="proof":
        d.ellipse((351,1120,728,1497),outline=accent,width=12)
        d.line((455,1320,524,1392,653,1215),fill=AQUA,width=25)
        d.text((292,1530),"FUENTES  >  PROMESAS",font=ff(BOLD,28),fill=CREAM)

for slug,topic,accent,slides in STORIES:
    frames=[]
    for n,(headline,detail,kind) in enumerate(slides):
        im=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(im)
        for y in range(H):
            a=y/H
            d.line((0,y,W,y),fill=(int(12+13*a),int(32+12*a),int(39+9*a)))
        for x in range(0,W,90):d.line((x,0,x,H),fill=(27,50,56),width=1)
        for y in range(0,H,90):d.line((0,y,W,y),fill=(27,50,56),width=1)
        d.rectangle((0,0,W,24),fill=accent)
        d.text((86,91),"sovtiva.",font=ff(REG,68),fill=CREAM)
        d.text((86,226),topic,font=ff(BOLD,30),fill=AQUA)
        d.line((85,292,992,292),fill=(67,94,97),width=3)
        size=min(103,int(1050/(max(map(len,headline.split("\n")))*.67)))
        d.multiline_text((81,400),headline,font=ff(SERIF,max(66,size)),fill=CREAM,spacing=20)
        d.multiline_text((85,839),detail,font=ff(SANS,41),fill=(190,216,214),spacing=12)
        illustration(d,kind,accent)
        d.line((88,1710,991,1710),fill=(84,108,109),width=3)
        d.line((88,1710,88+225*(n+1),1710),fill=accent,width=8)
        d.text((85,1771),"SOVTIVA JOURNAL / INVESTIGACIÓN",font=ff(BOLD,27),fill=AQUA)
        d.text((884,1771),f"{n+1:02d} / 04",font=ff(BOLD,29),fill=CREAM)
        path=ROOT/f"{slug}-{n+1}.png";im.save(path,optimize=True)
        frames.append(path)
        if n==0:im.save(ROOT/f"{slug}-cover.png",optimize=True)
    command=["ffmpeg","-hide_banner","-loglevel","error","-y"]
    for p in frames:command+=["-loop","1","-t","4.4","-framerate","24","-i",str(p)]
    filt="".join("[{}:v]scale=1080:1920,format=yuv420p,setpts=PTS-STARTPTS,zoompan=z='min(zoom+0.00012,1.03)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1080x1920:fps=24[v{}];".format(i,i) for i in range(4))
    filt+="[v0][v1]xfade=transition=fade:duration=0.45:offset=3.9[x1];[x1][v2]xfade=transition=fade:duration=0.45:offset=7.8[x2];[x2][v3]xfade=transition=fade:duration=0.45:offset=11.7[vout]"
    command+=["-filter_complex",filt,"-map","[vout]","-t","16.1","-c:v","libx264","-crf","26","-preset","veryfast","-pix_fmt","yuv420p","-movflags","+faststart","-an",str(ROOT/f"{slug}.mp4")]
    subprocess.run(command,check=True)
    print(slug,(ROOT/f"{slug}.mp4").stat().st_size)
