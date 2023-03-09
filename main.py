import pygame
import pgzrun
import math
import random
import os
from enum import Enum
import math
from math import sqrt
from PIL import Image
from bon import InputBox
import numpy as np
HEIGHT=600+100
WIDTH=1200
TITLE="RUZYEF"
class clmo(Enum):
    clic=0
    all=1
    daen=2
    sikaku=3
    line=4
paint_mode=clmo.clic
now_color=(0,0,0)
now_futosa=20
save_txt=""
load_txt=""
class Buttan:
    def __init__(self,color,pos,scope,txt):
        self.txt=txt
        self.color=color
        self.pos=pos
        self.scope=scope
        if 0!=len(self.txt):
            self.txtsize=(((self.scope[0])/len(self.txt))*(90/60))
        else:
            self.txtsize=0
        self.rect=Rect(pos,scope)
    def draw(self):
        screen.draw.filled_rect(self.rect,self.color)
        screen.draw.text(self.txt,self.pos,fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=self.txtsize)
    def collidepoint(self,pos,key):
        if key==mouse.LEFT or key==mouse.RIGHT:
            if(self.pos[0]<=pos[0] and pos[0]<=self.pos[0]+self.scope[0] and self.pos[1]<=pos[1] and pos[1]<=self.pos[1]+self.scope[1]):
                return 1
        return 0
class Smol_Buttan(Buttan):
    def __init__(self,color,pos,scope,txt,mode):
        self.mode=mode
        super().__init__(color,pos,scope,txt)
    def draw(self):
        global paint_mode
        super().draw()
        if paint_mode==self.mode:
            screen.draw.rect(self.rect,(255,0,0))
class Scroll:
    def __init__(self,pos,go_pos,txt,num):
        self.txt=txt+":"
        self.num=num
        self.rect=[pos[0],pos[1],go_pos[0],go_pos[1]]
        self.flg=False
        self.but_rect=Rect((self.rect[2]-10,self.rect[3]-((self.rect[3]-self.rect[1])*(self.num/255))-5),(20,10))
    def draw(self):
        screen.draw.line([self.rect[0],self.rect[1]],[self.rect[2],self.rect[3]],(0,0,0))
        screen.draw.text(str(self.txt)+str(round(self.num)),(self.rect[2]-10,self.rect[3]+3),fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=10)
        screen.draw.filled_rect(self.but_rect,(200,200,200))
        screen.draw.rect(self.but_rect,(0,0,0))
    def collidepoint(self,pos,key):
        if key==mouse.LEFT or key==mouse.RIGHT:
            if(self.but_rect[0]<=pos[0] and pos[0]<=self.but_rect[0]+self.but_rect[2] and self.but_rect[1]<=pos[1] and pos[1]<=self.but_rect[1]+self.but_rect[3]):
                self.flg=True
    def up(self):
        self.flg=False
    def move(self,pos):
        if self.flg==True:
            po=pos[1]
            if po<self.rect[1]:
                po=self.rect[1]
            elif po>self.rect[3]:
                po=self.rect[3]
            self.num=255*(self.rect[3]-po)/(self.rect[3]-self.rect[1])
            self.but_rect=Rect((self.rect[2]-10,self.rect[3]-((self.rect[3]-self.rect[1])*(self.num/255))-5),(20,10))
    def color(self):
        return round(self.num)    
class InputBox:
    def __init__(self,pos,scope):
        self.rect =Rect((pos[0],pos[1]),(scope[0],scope[1]))
        self.butan=Buttan((64,64,64),[pos[0]+scope[0]/2-120,pos[1]+scope[1]*2+60],[240,60],"LOAD")
        self.txt=""
        self.flg=False
    def draw(self):
        global load_txt
        screen.draw.text(self.txt,(self.rect[0],self.rect[1]),fontname='doppioone-regular.ttf',color=(0,0,0),fontsize=90)
        screen.draw.rect(self.rect,(0,0,0))
        screen.draw.filled_rect(Rect((self.rect[0],self.rect[1]+self.rect[3]),(self.rect[2],self.rect[3])),(255,255,255))
        screen.draw.text(load_txt,(self.rect[0],self.rect[1]+self.rect[3]),fontname='doppioone-regular.ttf',color=(0,0,0),fontsize=90)
        self.butan.draw()
        if self.flg==True:
            screen.draw.filled_rect(Rect((self.rect[0],self.rect[1]-self.rect[3]),(self.rect[2],self.rect[3])),(255,0,0))
            screen.draw.text("ロードに失敗しました",((self.rect[0]+self.rect[1])/2-50,self.rect[1]-self.rect[3]),fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=90)
    def handle_event(self, event):
        r = ""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                r = self.txt
                self.txt = ''
            elif event.key == pygame.K_DELETE:
                pass
            elif event.key == pygame.K_BACKSPACE:
                self.txt = self.txt[:-1]
            else:
                self.txt += event.unicode
        return r
    def mouse_down(self,pos,key):
        if 1==self.butan.collidepoint(pos,key):
            return True
        return False
class Save_InputBox(InputBox):
    def __init__(self,pos,scope):
        self.rect =Rect((pos[0],pos[1]),(scope[0],scope[1]))
        self.txt=""
        self.flg=False
    def draw(self):
        global save_txt
        screen.draw.text(self.txt,(self.rect[0],self.rect[1]),fontname='doppioone-regular.ttf',color=(0,0,0),fontsize=30)
        screen.draw.rect(self.rect,(0,0,0))
        screen.draw.filled_rect(Rect((self.rect[0],self.rect[1]+self.rect[3]),(self.rect[2],self.rect[3])),(255,255,255))
        screen.draw.text(save_txt,(self.rect[0],self.rect[1]+self.rect[3]),fontname='doppioone-regular.ttf',color=(0,0,0),fontsize=30)
class Start:
    def __init__(self):
        self.title_mode=0
        self.start=Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2],[240,60],"START")
        self.conit=Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2+70],[240,60],"IMAGE LOAD")
        self.exp=Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2+140],[240,60],"EXPLANATION")
        self.txt ="\n"
        self.txt+="\n"
        self.txt+="\n"
    def set_start(self,num):
        self.title_mode=num
    def draw(self):
        if self.title_mode==0:
            screen.fill((128, 0, 0))
            screen.draw.text("oEkaKi",(WIDTH/2-200,HEIGHT/3-100),fontname='fugazone_regular.ttf',color=(0,0,0),fontsize=100)
            self.start.draw()
            self.conit.draw()
            self.exp.draw()
        elif self.title_mode==1:
            return
        elif self.title_mode==2:
            screen.fill((255,255,0))
            screen.draw.text("ここにファイル名を入れることで画像をロードすることができます\n名前を入力してEnterをおすと白いボックスに名前が入ります\nその状態で下のloadボタンをおすとその名前のファイルが存在する場合ロードされされます\n日本語は使えません",(0,0),fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=30)
        elif self.title_mode==3:
            screen.fill((255,255,255))
            screen.draw.text(self.txt,(0,0),fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=50)
    def mouse_down(self,pos,key):
        if self.title_mode==0:
            if self.start.collidepoint(pos,key):
                self.title_mode=1
                return 1
            elif self.conit.collidepoint(pos,key):
                self.title_mode=2
            elif self.exp.collidepoint(pos,key):
                self.title_mode=3
        elif self.title_mode==1:
            return 0
        elif self.title_mode==2:
            if key==mouse.LEFT or key==mouse.RIGHT:
                self.title_mode=0
        elif self.title_mode==3:
            if key==mouse.LEFT or key==mouse.RIGHT:
                self.title_mode=0
        return 0
class Map:
    def __init__(self):
        global now_futosa,paint_mode
        self.rect=Rect((0,0),(WIDTH,HEIGHT-100))
        self.draw_date=pygame.Surface((self.rect[2],self.rect[3]), flags=0)
        self.draw_date.fill((255,255,255),None, special_flags=0)
        self.i=-1
        self.back_list=[]
        self.yobi_save()
        self.pos=[0,0]
        self.color=(0,0,0)
        self.paint=paint_mode
        self.flg=False
        self.point_flg=False
        self.mode=0#0futhuu1se-bu
    def on_mouse_down(self,pos,key):
        global paint_mode,now_color
        if key==mouse.LEFT:
            if pos[1]<HEIGHT-100:
                if paint_mode==clmo.clic:
                    pygame.draw.circle(self.draw_date,now_color,pos,int(now_futosa/20),width=0)
                    self.pos=pos
                    self.paint=paint_mode
                    self.flg=True
                elif paint_mode==clmo.daen:
                    self.color=self.draw_date.get_at(pos)
                    self.pos=pos
                    self.paint=paint_mode
                    self.point_flg=True
                    self.flg=True
                elif paint_mode==clmo.line:
                    self.color=self.draw_date.get_at(pos)
                    self.pos=pos
                    self.paint=paint_mode
                    self.point_flg=True
                    self.flg=True
                elif paint_mode==clmo.all:
                    self.paint=paint_mode
                    self.draw_date.fill(now_color,None, special_flags=0)
                elif paint_mode==clmo.sikaku:
                    self.color=self.draw_date.get_at(pos)
                    self.pos=pos
                    self.paint=paint_mode
                    self.point_flg=True
                    self.flg=True
    def on_mouse_up(self,pos,key):
        global now_futosa,now_color
        if self.flg==True:
            if key==mouse.LEFT:
                if self.paint==clmo.daen:
                    self.daen(self.pos,pos)
                elif self.paint==clmo.line:
                    self.sen(self.pos,pos,now_futosa/10)
                elif paint_mode==clmo.sikaku:
                    pygame.draw.rect(self.draw_date,now_color, Rect((self.pos[0] if self.pos[0]<pos[0] else pos[0],self.pos[1] if self.pos[1]<pos[1] else pos[1]),(pos[0]-self.pos[0] if pos[0]-self.pos[0]>0 else self.pos[0]-pos[0],pos[1]-self.pos[1] if pos[1]-self.pos[1]>0 else self.pos[1]-pos[1])), width=0)
                self.yobi_save()
                self.point_flg=False
                self.flg=False
    def yobi_save(self):
        self.i+=1
        if len(self.back_list)>self.i:
            self.back_list=self.back_list[:self.i]
        at=pygame.Surface((WIDTH,HEIGHT),flags=0)
        at.blit(self.draw_date,[0,0], area=None, special_flags = 0)
        self.back_list+=[at]
    def on_mouse_move(self,pos):
        global now_futosa
        if self.flg==True:
            if self.paint==clmo.clic:
                #self.sen(self.pos,pos,now_futosa/10)
                pygame.draw.line(self.draw_date,now_color,self.pos,pos, width=int(now_futosa/10))
                pygame.draw.circle(self.draw_date,now_color,pos,int(now_futosa/20),width=0)
                self.pos=pos
    def load(self,name):
        if 0==name.count('.png'):
            name+='.png'
        if os.path.isfile('images/'+name):
            source=pygame.image.load(os.path.join('images',name))
            source=source.convert()
            self.draw_date.blit(source,[0,0], area=None, special_flags = 0)
            self.i=-1
            self.back_list=[]
            self.yobi_save()
            return True
        return False
    def draw(self):
        screen.blit(self.draw_date,(0,0))
        if True==self.point_flg:
            screen.draw.filled_circle(self.pos,2,(0,0,0))
        if self.mode==1:
            screen.draw.filled_rect(Rect((WIDTH/2-120,HEIGHT/2-40),(240,80)),(128,128,0))
            screen.draw.text("save",[WIDTH/2-60,HEIGHT/2-20],fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=50)
    def back(self):
        print(self.i,len(self.back_list))
        if self.i>0:
            self.i-=1
            self.draw_date.blit(self.back_list[self.i],[0,0], area=None, special_flags = 0)
    def move(self):
        print(self.i,len(self.back_list))
        if self.i<len(self.back_list)-1:
            self.i+=1  
            self.draw_date.blit(self.back_list[self.i],[0,0], area=None, special_flags = 0)
    def save(self):
        global save_txt
        lis=[]
        for y in range(self.rect[3]):
            li=[]
            for x in range(self.rect[2]):
                li+=[self.draw_date.get_at((x,y))]
            lis+=[li]
        array=np.array(lis)
        im = Image.fromarray(array)
        im.save("images/"+save_txt+".png")
    def sen(self,pos,go_pos,haba):
        global now_color
        haba/=2
        xsen=(pos[0]-go_pos[0])
        ysen=(pos[1]-go_pos[1])
        if(ysen!=0 and xsen!=0):
            a=ysen/xsen
            b=pos[1]-a*pos[0]
            ap=-1/a
            hyp=(math.sqrt(ysen**2+xsen**2)/xsen)
            haba*=abs(hyp)
            if(pos[1]<go_pos[1]):
                bp=pos[1]-ap*pos[0]
                bgp=go_pos[1]-ap*go_pos[0]
            else:
                bgp=pos[1]-ap*pos[0]
                bp=go_pos[1]-ap*go_pos[0]
            for y in range(self.rect[3]):
                for x in range(self.rect[2]):
                    if(y >= a*x+b -haba and y <= a*x+b +haba):
                        if(y >= ap*x+bp and y <= ap*x+bgp):
                            self.draw_date.set_at((x,y),now_color)
        elif(ysen==0 and xsen==0):
            return
        elif(ysen==0):
            if(pos[0]>go_pos[0]):
                box=pos
                pos=go_pos
                go_pos=box
            haba=int(haba)
            for x in range(pos[0],go_pos[0]):
                for y in range(pos[1]-haba,pos[1]+haba):
                    if(0<y<self.rect[2] and 0<x<self.rect[3]):
                        self.draw_date.set_at((x,y),now_color)
        elif(xsen==0):
            if(pos[1]>go_pos[1]):
                box=pos
                pos=go_pos
                go_pos=box
            haba=int(haba)
            for y in range(pos[1],go_pos[1]):
                for x in range(pos[0]-haba,pos[0]+haba):
                    if(0<y<self.rect[2] and 0<x<self.rect[3]):
                        self.draw_date.set_at((x,y),now_color)
    def daen(self,pos,go_pos):
        global now_color
        pos=list(pos)
        go_pos=list(go_pos)
        xr=(abs(pos[0]-go_pos[0]))/2
        yr=(abs(pos[1]-go_pos[1]))/2
        cen=[(pos[0]+go_pos[0])/2,(pos[1]+go_pos[1])/2]
        if(pos[0]>go_pos[0]):
            box=pos[0]
            pos[0]=go_pos[0]
            go_pos[0]=box
        if(pos[1]>go_pos[1]):
            box=pos[1]
            pos[1]=go_pos[1]
            go_pos[1]=box
        for y in range(pos[1],go_pos[1]):
            for x in range(pos[0],go_pos[0]):
                if(0<y<self.rect[3] and 0<x<self.rect[2]):
                    siki=((x-cen[0])/xr)**2+((y-cen[1])/yr)**2
                    if(siki<=1):
                        self.draw_date.set_at((x,y),now_color)
    def sikaku(self,pos,go_pos,setd):
        for y in range(pos[1] if pos[1]<go_pos[1] else go_pos[1],go_pos[1] if pos[1]<go_pos[1] else pos[1]):
            for x in range(pos[0] if pos[0]<go_pos[0] else go_pos[0],go_pos[0] if pos[0]<go_pos[0] else pos[0]):
                if(0<y<self.rect[2] and 0<x<self.rect[3]):
                    self.date[y][x]=setd
                    self.draw_date.set_at((x,y),setd.value)                          
    def all(self,setd):
        self.draw_date.fill(setd.value,None, special_flags=0)
        self.date= [[setd for i in range(self.rect[2])] for j in range(self.rect[3])] 
class Sekkei:
    def __init__(self):
        self.rect=Rect((200,HEIGHT-100),(WIDTH-300,100))
        self.cli=Smol_Buttan((255,255,255),[self.rect[0]+10*1+35*0,self.rect[1]+10*1+35*0],[35,35],"CLI",clmo.clic)
        self.all=Smol_Buttan((255,255,255),[self.rect[0]+10*1+35*0,self.rect[1]+10*2+35*1],[35,35],"ALL",clmo.all)
        self.den=Smol_Buttan((255,255,255),[self.rect[0]+10*2+35*1,self.rect[1]+10*1+35*0],[35,35],"DAEN",clmo.daen)
        self.ska=Smol_Buttan((255,255,255),[self.rect[0]+10*2+35*1,self.rect[1]+10*2+35*1],[35,35],"SIKA",clmo.sikaku)
        self.lin=Smol_Buttan((255,255,255),[self.rect[0]+10*3+35*2,self.rect[1]+10*1+35*0],[35,35],"LINE",clmo.line)
        self.futo=Scroll([self.rect[0]+self.rect[2]-25,self.rect[1]+5],[self.rect[0]+self.rect[2]-25,self.rect[1]+self.rect[3]-15],"FU",20)
    clic=0
    en=1
    daen=2
    sikaku=3
    line=4
    def draw(self):
        global now_futosa
        screen.draw.filled_rect(self.rect,(128,128,128))
        self.cli.draw()
        self.all.draw()
        self.den.draw()
        self.ska.draw()
        self.lin.draw()
        self.futo.draw()
        screen.draw.filled_circle([self.rect[0]+self.rect[2]-80,self.rect[1]+self.rect[3]/2],now_futosa/20, (0,0,0))
    def on_mouse_down(self,pos,key):
        global paint_mode
        if self.cli.collidepoint(pos,key):
            paint_mode=clmo.clic
        elif self.all.collidepoint(pos,key):
            paint_mode=clmo.all
        elif self.den.collidepoint(pos,key):
            paint_mode=clmo.daen
        elif self.ska.collidepoint(pos,key):
            paint_mode=clmo.sikaku
        elif self.lin.collidepoint(pos,key):
            paint_mode=clmo.line
        elif key==mouse.LEFT or key==mouse.RIGHT:
                self.futo.collidepoint(pos,key)
    def on_mouse_up(self,key):
        if key==mouse.LEFT or key==mouse.RIGHT:
            self.futo.up()
    def on_mouse_move(self,pos):
        self.futo.move(pos)
        if True==self.futo.flg:
            global now_futosa
            now_futosa=self.futo.num
            if now_futosa==0:
                now_futosa=1
class Kara:
    def __init__(self):
        global now_color
        self.rect=Rect((0,HEIGHT-100),(150,100))
        self.r=Scroll([50*0+25,self.rect[1]+5],[50*0+25,self.rect[1]+self.rect[3]-15],"r",0)
        self.g=Scroll([50*1+25,self.rect[1]+5],[50*1+25,self.rect[1]+self.rect[3]-15],"g",0)
        self.b=Scroll([50*2+25,self.rect[1]+5],[50*2+25,self.rect[1]+self.rect[3]-15],"b",0)
    def draw(self):
        global now_color
        screen.draw.filled_rect(self.rect,(255,255,255))
        self.r.draw()
        self.g.draw()
        self.b.draw()
        screen.draw.filled_rect(Rect((self.rect[2],self.rect[1]),(50,self.rect[3])),now_color)
        screen.draw.rect(Rect((self.rect[2],self.rect[1]),(50,self.rect[3])),(128,128,128))
    def on_mouse_down(self,pos,key):
        self.r.collidepoint(pos,key)
        self.g.collidepoint(pos,key)
        self.b.collidepoint(pos,key)
    def on_mouse_up(self,key):
        if key==mouse.LEFT or key==mouse.RIGHT:
            self.r.up()
            self.g.up()
            self.b.up()
    def move(self,pos):
        global now_color
        self.r.move(pos)
        self.g.move(pos)
        self.b.move(pos)
        now_color=(self.r.color(),self.g.color(),self.b.color())
class modo:
    def __init__(self):
        spv=[WIDTH-100,HEIGHT-100]
        self.start=Buttan((64,64,64),[spv[0]+20,spv[1]+10],[60,20],"START")
        self.conit=Buttan((64,64,64),[spv[0]+20,spv[1]+40],[60,20],"SAVE")
        self.bac=Buttan((64,64,64),[spv[0]+10,spv[1]+70],[35,20],"BACK")
        self.mae=Buttan((64,64,64),[spv[0]+10*2+35,spv[1]+70],[35,20],"MOVE")
    def draw(self):
        self.start.draw()
        self.conit.draw()
        self.bac.draw()
        self.mae.draw()
    def on_mouse_down(self,pos,key):
        if self.start.collidepoint(pos,key):
            return 1
        elif self.conit.collidepoint(pos,key):
            return 2
        elif self.bac.collidepoint(pos,key):
            return 3
        elif self.mae.collidepoint(pos,key):
            return 4
        return 0
mo=modo()
kara=Kara()
sek=Sekkei()
map=Map()
start=Start()
box=InputBox((WIDTH/2-300,HEIGHT/2-40),(600,100))
sebox=Save_InputBox((WIDTH-200-400,HEIGHT-100+10),(400,80/2))
time=0
set_time=-1
def draw():
    global load_txt,save_txt
    start.draw()
    if start.title_mode==1:
        map.draw()
        kara.draw()
        sek.draw()
        mo.draw()
        sebox.draw()
        for event in pygame.event.get():
            txt= sebox.handle_event(event)
            if txt!="":
                save_txt=txt
    elif start.title_mode==2:
        box.draw()
        for event in pygame.event.get():
            txt= box.handle_event(event)
            if txt!="":
                load_txt=txt
    
def update():
    global time,set_time,paint_mode
    time+=1
    if time==set_time:
        map.save()
        map.mode=0
def on_mouse_down(pos,button):
    global map,save_txt,time,set_time,load_txt
    if start.title_mode==1:
        kara.on_mouse_down(pos,button)
        sek.on_mouse_down(pos,button)
        som=mo.on_mouse_down(pos,button)
        if som==1:
            start.set_start(0)
            map=Map()
            save_txt=""
        elif som==2:
            if ""!=save_txt:
                set_time=time+2
                map.mode=1
        elif som==3:
            map.back()
        elif som==4:
            map.move()
        map.on_mouse_down(pos,button)
    elif start.title_mode==2:
        if box.mouse_down(pos,button):
            if ""!=load_txt:
                if map.load(load_txt):
                    start.set_start(1)
                    box.flg=False
                else:
                    box.flg=True
            else:
                box.flg=True
    else:
        start.mouse_down(pos,button)
    
def on_mouse_up(pos,button):
    if start.title_mode==1:
        kara.on_mouse_up(button)
        sek.on_mouse_up(button)
        map.on_mouse_up(pos,button)
def on_mouse_move(pos,rel,buttons):
    if start.title_mode==1:
        kara.move(pos)
        map.on_mouse_move(pos)
        sek.on_mouse_move(pos)
                

pgzrun.go()
"""
(*args, **kwargs)


C:\ProgramData\Anaconda3\Lib\site-packages\pygame
C:\ProgramData\Anaconda3\Lib\site-packages\pgzero


C:/Program Files/Python37/Lib/site-packages/pgzero/__pycache__
C:/Program Files/Python37/Lib/site-packages/pgzero/data

C:/Program Files/Python37/Lib/site-packages/pgzero/__init__.py
C:/Program Files/Python37/Lib/site-packages/pgzero/__main__.py
C:/Program Files/Python37/Lib/site-packages/pgzero/actor.py
C:/Program Files/Python37/Lib/site-packages/pgzero/animation.py
C:/Program Files/Python37/Lib/site-packages/pgzero/builtins.py
C:/Program Files/Python37/Lib/site-packages/pgzero/clock.py
C:/Program Files/Python37/Lib/site-packages/pgzero/constants.py
C:/Program Files/Python37/Lib/site-packages/pgzero/game.py
C:/Program Files/Python37/Lib/site-packages/pgzero/keyboard.py
C:/Program Files/Python37/Lib/site-packages/pgzero/loaders.py
C:/Program Files/Python37/Lib/site-packages/pgzero/music.py
C:/Program Files/Python37/Lib/site-packages/pgzero/ptext.py
C:/Program Files/Python37/Lib/site-packages/pgzero/rect.py
C:/Program Files/Python37/Lib/site-packages/pgzero/runner.py
C:/Program Files/Python37/Lib/site-packages/pgzero/screen.py
C:/Program Files/Python37/Lib/site-packages/pgzero/soundfmt.py
C:/Program Files/Python37/Lib/site-packages/pgzero/spellcheck.py
C:/Program Files/Python37/Lib/site-packages/pgzero/tone.py


https://camp.trainocate.co.jp/magazine/python_machine_learning/

"""

