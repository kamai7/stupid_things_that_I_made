from kandinsky import *
from ion import *
from time import *
from math import *
from random import *
SCREEN = [320,222]
POS_BAT = [160,0]
POS_COOKIE = [50,50]
POS_UPGRADES = [40,145]
POS_BUTTONS = [40,205]
POS_INFO = [5,5]
ORDERS = ['', 'k', 'm', 'b', 't', 'q', 'Q', 's', 'S', 'o', 'n']
MOVE = [
  KEY_OK,
  KEY_EXE,
  KEY_LEFT,
  KEY_RIGHT,
  KEY_UP,
  KEY_DOWN
]
IN_MENU = False

def num(val, digits=4):
  m = floor(log10(val)) if val >= 1 else 0
  u = min(m//3, len(ORDERS)-1)
  v = val / 10**(m - m%3)
  vret = str(v)[:digits+1] if int(v) != v else str(int(v))
  return vret + ORDERS[u]

def calc_size(x,y,w,h,size):
  scale = size/100
  absx = int(x-(w/2)*scale)
  absy = int(y-(h/2)*scale)
  return absx,absy,int(w*scale),int(h*scale)

def display(object, jeu, y_offset = 0):
  if isinstance(object,Cookie):
    jeu.cookie.display(POS_COOKIE[0],POS_COOKIE[1],jeu,True if jeu.selected == jeu.cookie else False)
  elif isinstance(object,Button):
    display_list(jeu.buttons,POS_BUTTONS[0],POS_BUTTONS[1],80,0,jeu,object=object)
  elif isinstance(object,Bat):
    display_list(jeu.batiments,POS_BAT[0],POS_BAT[1] - y_offset,0,50,jeu,object=object)
  elif isinstance(object,Upgrade):
    display_list(jeu.upgrades,POS_UPGRADES[0],POS_UPGRADES[1],80,0,jeu,object=object)

def display_list(object_list,pos_x,pos_y,x_offset,y_offset,jeu,object=None):
  i = 0
  for obj in object_list:
    selected = True if obj == jeu.selected else False
    if getattr(obj,'show',True):
      if object is None:
        obj.display(pos_x+(i*x_offset),pos_y+(i*y_offset),jeu,selected)
      else:
        if obj == object:
          obj.display(pos_x+(i*x_offset),pos_y+(i*y_offset),jeu,selected)
      i += 1

def calc_color(couleur,offset):
  r,g,b = couleur
  return color(min(max(r+offset,0),255),min(max(g+offset,0),255),min(max(b+offset,0),255))

class Jeu:
  def __init__(self,batiments,buttons,upgrades,cookie,cookies = 0):
    self.cookies = cookies
    self.cps = 0
    self.multiplier = 1
    self.crt_damage = 1.2
    self.crt_chance = 0.02
    self.bat_multiplier = 1
    self.double = 1
    self.bat_multiplier = 1
    self.batiments = batiments
    self.buttons = buttons
    self.upgrades = upgrades
    self.cookie = cookie
    self.selected = self.cookie
    self.y_offset = 0
  def display_info(self):
    if not IN_MENU:
      fill_rect(0,0,160,40,color(255,255,255))
      draw_string("cookies: " + num(self.cookies),POS_INFO[0],POS_INFO[1],color(0,0,0),color(255,255,255))
      draw_string("cps:" + num(self.cps*self.bat_multiplier,digits=2) + "(+" + num((self.cps*self.bat_multiplier)-self.cps,digits=2) + ")" ,POS_INFO[0],POS_INFO[1]+15,color(0,0,0),color(255,255,255))
  def display_all(self):
    fill_rect(0,0,220,380,color(255,255,255))
    self.display_info()
    display(self.cookie,jeu)
    display_list(jeu.buttons,POS_BUTTONS[0],POS_BUTTONS[1],80,0,jeu)
    display_list(jeu.batiments,POS_BAT[0],POS_BAT[1],0,50,jeu)
    display_list(jeu.upgrades,POS_UPGRADES[0],POS_UPGRADES[1],80,0,jeu)
  def update_selected(self,col,row,y_offset = 0):
    col1 = [self.cookie] + [upgrade for upgrade in self.upgrades if upgrade.show] + [button for button in self.buttons if button.show]
    col2 = self.batiments
    map = [col1,col2]
    temp = self.selected
    self.selected = map[col][row]
    display(self.selected,self , y_offset = y_offset)
    display(temp,self, y_offset = y_offset)
    return self.selected, [len(col1),len(col2)]
  def random_upgrade(self):  
    actives_upgrades = [upg for upg in self.upgrades if upg.show]
    if len(actives_upgrades) < 2:
      upgrade = choice(self.upgrades)
      while upgrade.show:
        upgrade = choice(self.upgrades)
      upgrade.show = True
  def actualise_prices(self):
    if not IN_MENU:
      purshaseable = self.batiments + self.upgrades
      for item in purshaseable:
        if item.prix <= self.cookies and item.getable == False:
          item.getable = True
          display(item,jeu)
        elif item.prix > self.cookies and item.getable == True:
          item.getable = False
          display(item,jeu)
  def unlock_upgrade(self):
    for upgrade in self.upgrades:
      if upgrade.show and upgrade.locked:
        upgrade.locked = False
        break

class Item:
  def __init__(self, nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur, modify):
    self.nom = nom
    self.gain = gain
    self.fonc_gain = fonc_gain
    self.prix = prix
    self.fonc_prix = fonc_prix
    self.lvl = 0
    self.couleur = couleur
    self.alt_couleur = alt_couleur
    self.locked = True
    self.modify = modify
    self.getable = False
  def lvl_up(self):
    self.prix = self.fonc_prix(self.prix)
    self.gain = self.fonc_gain(self.lvl)
    self.lvl += 1
  def set_lvl(self,level):
    self.lvl = level
    for i in range(level):
      self.prix = self.fonc_prix(self.prix)
      self.gain = self.fonc_gain(self.lvl)

class Bat(Item):
  def __init__(self, nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur):
    super().__init__(nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur, "cps")
    self.locked = True
  def display(self, x, y, jeu, selected):
    w, h = 160, 50
    outline = color(255,60,60) if selected else color(0,0,0)
    bg = self.couleur if not self.locked else color(180,180,180)
    price = color(255,40,40) if not self.getable else color(20,255,20)
    name = self.alt_couleur if not self.locked else color(0,0,0)
    fill_rect(x,y,w,h,outline)
    fill_rect(x+2,y+2,w-4,h-4,bg)
    fill_rect(319-(w//2),y+6,2,h-12,calc_color(bg,-20))
    draw_string(self.nom,330-w,y+5,name,bg)
    draw_string(num(self.prix),330-(w//2),y+5,price,bg)
    if not self.locked:
      draw_string(num(self.gain),330-(w//2),y+25,color(120,120,120),bg)
      draw_string("lvl:" + str(self.lvl),330-w,y+25,color(0,0,0),bg)
  def action(self,jeu):
    if jeu.cookies >= self.prix:
      jeu.cookies -= self.prix
      self.lvl_up()
      self.locked = False
      cps = 0
      for bat in jeu.batiments:
        if not bat.locked:
          cps += bat.gain
      jeu.cps = cps
      jeu.actualise_prices()
      display(self,jeu,jeu.y_offset)

class Upgrade(Item):
  def __init__(self, nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur, modify):
    super().__init__(nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur, modify)
    self.show = False
    self.global_gain = 0
  def display(self, x, y, jeu, selected):
    bg = self.couleur if not self.locked else color(180,180,180)
    dark_bg = calc_color(bg,-40)
    outline = color(255,60,60) if selected else dark_bg
    absx,absy,w,h = calc_size(x,y,80,80,100)
    fill_rect(absx,absy,w,h,outline)
    absx,absy,w,h = calc_size(x,y,80,80,86 if selected else 92)
    fill_rect(absx,absy,w,h,bg)
    if not self.locked:
      price = color(255,40,40) if not self.getable else color(20,255,20)
      upgrade = '+'+num(self.fonc_gain(self.lvl),digits=3)
      draw_string(self.nom,x-(len(self.nom)*5),absy+5,self.alt_couleur,bg)
      draw_string(upgrade,x-(len(upgrade)*5),y-10,color(30,30,30),dark_bg)
      draw_string(num(self.prix),x-(len(num(self.prix))*5),(absy+h)-20,price,bg)
  def action(self,jeu):
    if jeu.cookies >= self.prix and not self.locked:
      jeu.cookies -= self.prix
      self.show = False
      self.locked = True
      self.lvl_up()
      self.global_gain += self.gain
      setattr(jeu,self.modify,getattr(jeu,self.modify) + self.gain)
      jeu.actualise_prices()
      jeu.random_upgrade()
      display_list(jeu.upgrades,POS_UPGRADES[0],POS_UPGRADES[1],80,0,jeu)

class Button:
  def __init__(self, texte, couleur, action, show):
    self.texte = texte
    self.couleur = couleur
    self.do = action
    self.show = show
  def action(self,jeu):
    self.do(jeu)
  def display(self,x,y,jeu,selected):
    length = len(self.texte)*10
    absx,absy,w,h = calc_size(x,y,length + 25,33,100)
    outline = color(255,160,160) if selected else self.couleur
    border = 6 if selected else 3
    fill_rect(absx,absy,w,h,outline)
    fill_rect(absx+border,absy+border,w-2*border,h-2*border,color(255,255,255))
    draw_string(self.texte,x-(len(self.texte)*5),y-8,self.couleur,color(255,255,255))

class Cookie:
  def __init__(self, base_size):
    self.pressed = 0
    self.base_size = base_size
  def display(self,x_centre,y_centre,jeu,selected):
    x,y,size,size = calc_size(x_centre,y_centre,self.base_size,self.base_size,100 if not selected else 92)
    fill_rect(x-8,y-8,self.base_size*7+20,self.base_size*5+8,color(255,255,255)) # clear 
    fill_rect(x,y+size,size*7,size*3,color(230,142,65))
    fill_rect(x+size,y,size*5,size*5,color(230,142,65))
    fill_rect(x+size,y+size*4,size*5,size,color(214,131,60))
    fill_rect(x,y+size*3,size,size,color(214,131,60))
    fill_rect(x+size*6,y+size*3,size,size,color(214,131,60))
    fill_rect(x+size,y+size,size,size,color(85,46,25))
    fill_rect(x+size*4,y,size,size,color(85,46,25))
    fill_rect(x+size*3,y+size*2,size,size,color(140,75,42))
    fill_rect(x+size*6,y+size*2,size,size,color(85,46,25))
  def action(self,jeu):
    self.pressed += 1
    self.display(POS_COOKIE[0],POS_COOKIE[1],jeu,False)
    for i in range(jeu.double):
      add = jeu.multiplier
      posx = randint(POS_COOKIE[0]-10,POS_COOKIE[0]+20)
      posy = randint(POS_COOKIE[1]-8,POS_COOKIE[1]+12)
      if random() < (jeu.crt_chance/100):
        add *= jeu.crt_damage
        draw_string("+"+num(add,digits=3),posx,posy,color(255,30,30),color(230,150,60))
      else:
        draw_string("+"+num(add,digits=3),posx,posy,color(100,100,100),color(230,150,60))
      jeu.cookies += add

def stats(jeu):
  global IN_MENU
  IN_MENU = True
  outline = color(200,200,200)
  bg = color(240,240,240)
  jeu.buttons[0].show = False
  jeu.buttons[1].show = False
  jeu.buttons[2].show = True
  fill_rect(20,5,270,210,outline)
  fill_rect(25,10,260,200,bg)
  jeu.selected = jeu.buttons[2]
  display(jeu.buttons[2],jeu)
  draw_string("Cookies: "+num(jeu.cookies),35,25,color(100,100,100),bg)
  draw_string("cps: "+num(jeu.cps),35,40,color(100,100,100),bg)
  draw_string("pressed: "+str(jeu.cookie.pressed),35,55,color(100,100,100),bg)
  draw_string("Upgrades",35,80,color(255,170,0),bg)
  draw_string("multiplier: x"+num(jeu.multiplier),35,105,color(100,100,100),bg)
  draw_string("double: "+num(jeu.double),35,120,color(100,100,100),bg)
  draw_string("crt chance: "+num(jeu.crt_chance)+"%",35,135,color(100,100,100),bg)
  draw_string("crt damage: "+num(jeu.crt_damage)+"%",35,150,color(100,100,100),bg)
  draw_string("bat boost: x"+num(jeu.bat_multiplier),35,165,color(100,100,100),bg)
  draw_string("lvl:" + str(jeu.upgrades[0].lvl),220,135,color(100,100,100),bg)
  draw_string("lvl:" + str(jeu.upgrades[2].lvl),220,105,color(100,100,100),bg)
  draw_string("lvl:" + str(jeu.upgrades[5].lvl),220,165,color(100,100,100),bg)
  draw_string("lvl:" + str(jeu.upgrades[1].lvl),220,150,color(100,100,100),bg)
  draw_string("lvl:" + str(jeu.upgrades[4].lvl),220,120,color(100,100,100),bg)

def save(jeu):
  jeu.buttons[0].show = False
  jeu.buttons[1].show = False
  jeu.buttons[2].show = True
  fill_rect(30,80,260,80,color(210,210,210))
  display(jeu.buttons[2],jeu)


def close(jeu):
  print("close")
  global IN_MENU
  IN_MENU = False
  jeu.buttons[0].show = True
  jeu.buttons[1].show = True
  jeu.buttons[2].show = False
  jeu.display_all()

batiments = [ # nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur
  Bat("well", 1, lambda x:(x/2)+1, 50, lambda x:1.05*x+10, color(255,255,210), color(190,190,190)),
  Bat("ruin", 4, lambda x:x+2, 200, lambda x:1.05*x+50, color(255,255,170), color(190,190,190)),
  Bat("chest", 12, lambda x:(x*2)+4, 800, lambda x:1.05*x+200, color(151,106,38), color(50,35,13)),
  Bat("village", 25, lambda x:(x*5)+10, 2500, lambda x:1.05*x+600, color(181,144,91), color(105,83,50)),
  Bat("outpost", 60, lambda x:(x*10)+20, 10000, lambda x:1.05*x+2000, color(71,45,22), color(0,0,0)),
  Bat("portal", 150, lambda x:(x*15)+50, 50000, lambda x:1.07*x+5000, color(112,0,128), color(200,200,255)),
  Bat("strhold", 400, lambda x:(x*20)+100, 200000, lambda x:1.07*x+15000, color(120,120,120), color(255,255,255)),
  Bat("mansion", 1000, lambda x:(x*25)+300, 750000, lambda x:1.08*x+40000, color(80,50,40), color(255,220,180)),
  Bat("bastion", 2500, lambda x:(x*30)+600, 3000000, lambda x:1.08*x+120000, color(50,50,50), color(255,180,150)),
  Bat("nd city", 7000, lambda x:(x*40)+1500, 10000000, lambda x:1.09*x+500000, color(170,140,255), color(255,255,210)),
  Bat("minshft", 20000, lambda x:(x*50)+4000, 50000000, lambda x:1.09*x+2000000, color(20,20,20), color(100,255,255)),
  Bat("fortres", 60000, lambda x:(x*60)+12000, 200000000, lambda x:1.1*x+10000000, color(120,0,0), color(255,150,150)),
  Bat("monumnt", 150000, lambda x:(x*80)+30000, 750000000, lambda x:1.1*x+25000000, color(0,120,120), color(200,255,255)),
  Bat("the end", 500000, lambda x:(x*100)+70000, 3000000000, lambda x:1.12*x+100000000, color(10,10,30), color(255,255,150))
]
buttons = [
  Button("stats",color(155,155,155),stats,True),
  Button("save",color(155,155,155),save,True),
  Button("X",color(255,40,40),close,False)
]
upgrades = [ # nom, gain, fonc_gain, prix, fonc_prix, couleur, alt_couleur, modify
  Upgrade("crt ch", 2, lambda x:2, 200, lambda x:2*x, color(255,100,255), color(255,0,255),"crt_chance"),
  Upgrade("crt dmg", 0.2, lambda x:x/10+0.1, 200, lambda x:2*x, color(255,60,60), color(190,0,0),"crt_damage"),
  Upgrade("x2", 1, lambda x:2**x, 200, lambda x:2*x, color(255,155,25), color(200,115,0),"multiplier"),
  Upgrade("give", 500, lambda x:(2**x)*500, 0, lambda x:0, color(255,100,255), color(0,0,0),"cookies"),
  Upgrade("double", 1, lambda x:1, 200, lambda x:2*x, color(255,100,255), color(0,0,0),"double"),
  Upgrade("bat", 1, lambda x:0.05*x+0.1, 200, lambda x:2*x, color(255,100,255), color(0,0,0),"bat_multiplier")
]
cookie = Cookie(10)

def game(jeu):
  cursor = [0,0] # col, row
  last_tick = monotonic()
  compteur = 0
  pressed = False
  selected,map = jeu.update_selected(cursor[0],cursor[1])
  jeu.random_upgrade()
  jeu.random_upgrade()
  jeu.display_all()
  while True:
    if monotonic() > last_tick + 1:
      compteur += 1
      last_tick = monotonic()
      jeu.cookies += jeu.cps * jeu.bat_multiplier
      jeu.display_info()
      jeu.actualise_prices()
    if compteur % 30 == 0 and not IN_MENU:
      jeu.unlock_upgrade()
      display_list(jeu.upgrades,POS_UPGRADES[0],POS_UPGRADES[1],80,0,jeu)
      compteur += 1
    for key in MOVE:
      if keydown(key):
        if not pressed:
          pressed = True   
          if key == KEY_OK or key == KEY_EXE:
            selected.action(jeu)
            jeu.display_info()
            print("1")
            if not getattr(selected,'show',True):
              cursor = [0,0]
              selected = jeu.cookie
              print("2")
          elif not IN_MENU:
            if key == KEY_UP:
              if cursor[1] > 0:
                cursor[1] -= 1
            elif key == KEY_DOWN:
              if cursor[1] < map[cursor[0]]-1:
                cursor[1] += 1
            elif key == KEY_LEFT:
              if cursor[0] > 0:
                cursor[0] = 0
                cursor[1] = min(cursor[1], map[0] - 1)
                jeu.y_offset = 0
                display_list(jeu.batiments,POS_BAT[0],POS_BAT[1] - jeu.y_offset,0,50,jeu)
            elif key == KEY_RIGHT:
              if cursor[0] < len(map)-1:
                cursor[0] = 1
                cursor[1] = min(cursor[1], map[1] - 1)
                jeu.y_offset = 0
                display_list(jeu.batiments,POS_BAT[0],POS_BAT[1] - jeu.y_offset,0,50,jeu)
            jeu.y_offset = ((cursor[1] - 3)*50) if cursor[1] > 3 and cursor[0] == 1 else 0
            if jeu.y_offset == 0:
              selected,map = jeu.update_selected(cursor[0],cursor[1])
            else:
              fill_rect(POS_BAT[0],POS_BAT[1],160,330,color(255,255,255))
              display_list(jeu.batiments,POS_BAT[0],POS_BAT[1] - jeu.y_offset,0,50,jeu)
              selected,map = jeu.update_selected(cursor[0],cursor[1],y_offset = jeu.y_offset)
        break
    else:
      pressed = False

print("1) new game\n2) load game")
if int(input(": ")) == 1:
  jeu = Jeu(batiments,buttons,upgrades,cookie)
  game(jeu)
else:
  jeu = Jeu(batiments,buttons,upgrades,cookie,cookies=0)
  game(jeu)ggggg