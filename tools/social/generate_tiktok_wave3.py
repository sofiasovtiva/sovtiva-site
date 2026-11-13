#!/usr/bin/env python3
"""Original Sovtiva Journal vertical microfilms. No external imagery, music or models.
Creates 4 1080x1920, H.264 MP4 clips (16 seconds) and PNG covers for Metricool.
Generated graphics and copy are original; no customer performance or case study is claimed.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

ROOT=Path("assets/social/tiktok/wave3")
ROOT.mkdir(parents=True,exist_ok=True)
W,H=1080,1920
NAVY=(12,32,39); AQUA=(172,221,221); CREAM=(241,237,225)
BURGUNDY=(131,60,80); OLIVE=(151,159,119)
STORIES=[
("ai-search","VISIBILIDAD IA",(126,165,150),[
("Tu empresa no aparece\ncuando preguntan\na una IA.","Eso no prueba que un algoritmo te haya bloqueado.","search"),
("Una respuesta\nNO es un ranking.","Cambian las preguntas. Cambian las fuentes.","layers"),
("Haz una prueba\nrepetible.","Consulta, registra fuentes y repite en otras sesiones.","chart"),
("Menos trucos.\nMás evidencia.","Fuentes y método: Sovtiva Journal.","proof")]),
("crm","PROCESOS / CRM",(180,113,121),[
("El lead llegó.\nNadie respondió.","No siempre es culpa del CRM.","inbox"),
("Formulario.\nHoja. CRM.","Tres herramientas. Ningún responsable claro.","flow"),
("Diseña el\nsiguiente paso.","Validar, asignar y comprobar resultados.","flow"),
("Automatiza\nel handoff.","No automatices el desorden. Sovtiva Journal.","proof")]),
("higgsfield","FACT-CHECK / IA",(158,125,190),[
("«Manhattan en\n15 minutos\ny por $15».","Un prompt no es una factura.","city"),
("La demo\nsí existe.","El costo final no está auditado.","code"),
("Cuenta todo\nel trabajo.","Tokens, créditos, renders y revisiones.","stack"),
("La técnica vale.\nEl hype, menos.","Fact-check y fuentes: Sovtiva Journal.","proof")]),
("outlook","CONTINUIDAD / EMAIL",(126,178,201),[
("¿Qué pasa\nsi Outlook\nse detiene?","No solo se pierde acceso al correo.","inbox"),
("Ventas. Soporte.\nConfirmaciones.","Distintos equipos; una dependencia compartida.","flow"),
("El respaldo\nno es otro logo.","Registra pendientes, usa otro canal y verifica.","flow"),
("Recupera\nel proceso.","Qué confirmó Microsoft y qué no. Sovtiva Journal.","proof")]),
("consultant","COMPRAR IA / CONSULTORÍA",(164,168,122),[
("No compres IA\na ciegas.","Una demo bonita no es un proyecto terminado.","proof"),
("¿Qué proceso\nva a cambiar?","Define una tarea y el resultado esperado.","flow"),
("¿Quién responde\nsi falla?","Responsable, permisos y excepciones.","stack"),
("Primero el alcance.\nDespués la compra.","Siete preguntas en Sovtiva Journal.","proof")]),
("profit","NEGOCIOS DIGITALES",(185,150,111),[
("Vender más\nno es ganar más.","Las ventas no muestran todos los gastos.","chart"),
("Etsy. Shopify.\nGumroad.","Cada plataforma tiene costos distintos.","layers"),
("Suma todos\nlos costos.","Comisiones, devoluciones, publicidad y producción.","stack"),
("Calcula tu\nbeneficio real.","Método y guía en Sovtiva Journal.","proof")])

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
