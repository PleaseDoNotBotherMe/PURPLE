from datetime import datetime
import sys
import socket
import threading
import random
import pickle
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import subprocess
import pygame
import tkinter
from tkinter import filedialog
from pypresence import Presence
import pypresence

RPC = Presence(794267714797043793)  # Initialize the client class
RPC.connect() # Start the handshake loop
RPC.update(large_image="logo", large_text="PURPLE")

current_time = datetime.now()

pygame.init()

#host = str(input("Hostname(default:singleplayer):"))
#name = str(input("Your name:"))

connected = False
host = ""

def check():
	global host
	global connected
	global s
	if host != "":
		s = socket.socket()
		s.connect((host, 1094))
		connected = True
		RPC.update(large_image="logo", large_text="PURPLE",
				state="Multyplayer",
				start = datetime.now().timestamp())
	else:
		RPC.update(large_image="logo", large_text="PURPLE",
				state="Singleplayer",
				start = datetime.now().timestamp())
		connected = False

start = 2
try:
	name = sys.argv[1]
	host = sys.argv[2]
	start = 1
except IndexError:
	print("{}:{}:{} [INFO]: Nem adtál meg argumenteket, átdobás főképernyőre".format(current_time.hour, current_time.minute, current_time.second))
	start = 2

pleace = pygame.display.set_mode((700, 700))
pygame.display.set_caption("PURPLE")
pygame.display.set_icon(pygame.image.load("PURPLE32.png"))
playing= True

#players_x = input["players"]["x"]
#players_y = input["players"]["y"]

i2 = 0
i = 0
x = 0
slot = []
y = 0
py = 25
px = 25
pcount = 0
ppleace = 0
key = "-"
got = False
musica = 0
render = False
volume = 0.3
typing = False
host = ""
name = ""
redc = 1
bluec = 1
greenc = 1
pcolor = (0,0,0)
arrows = False
win = -1
i = 0
#           piros         kék           zöld          sárga           fehér        fekete
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 255, 255), (0, 0, 0)]

rgb_scale = 255
cmyk_scale = 100

def rgb_to_cmyk(r : float,g : float,b : float):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale
	
    print(type(r))
	
    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) 
    m = (m - min_cmy) 
    y = (y - min_cmy) 
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

def cmyk_to_rgb(c,m,y,k):
    """
    """
    r = rgb_scale*(1.0-(c+k)/float(cmyk_scale))
    g = rgb_scale*(1.0-(m+k)/float(cmyk_scale))
    b = rgb_scale*(1.0-(y+k)/float(cmyk_scale))
    return (r,g,b)

def ink_add_for_rgb(list_of_colours : list):
    """input: list of rgb, opacity (r,g,b,o) colours to be added, o acts as weights.
    output (r,g,b)
    """
    C = 0
    M = 0
    Y = 0
    K = 0

    for (r,g,b,o) in list_of_colours:
        c,m,y,k = rgb_to_cmyk(r, g, b)
        C+= o*c
        M+=o*m
        Y+=o*y 
        K+=o*k 

    return cmyk_to_rgb(C, M, Y, K)

class Button:
	def __init__(self, x : int, y : int, dx : int, dy : int, color, font : str, fs : int, fc):
		global pleace
		self.s = pleace
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.c = color
		self.f = font
		self.fs = fs
		self.visible = True
		self.fc = fc
		self.click = pygame.mouse.get_pressed()
	def show(self, visible = True):
		self.visible = visible
		if self.visible:
			pygame.draw.rect(self.s, self.c, pygame.Rect(self.x, self.y, self.dx, self.dy))
			self.s.blit(pygame.font.Font("arial.ttf", self.fs).render(self.f, True, self.fc), (self.x, self.y))
	def is_pressed(self, num : int):
		pos = pygame.mouse.get_pos()
		if pos[0] > self.x and pos[1] > self.y and pos[0] < self.dx:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					return True
				if event.type == pygame.MOUSEBUTTONUP:
					return True
		return False

#százalékszámítás: 50 : 100 * 50
#           valamennyinek   százaléka
def set_music():
	global musica
	music_list = ["The Best Clouds.wav", "PURPLE.wav"]
	musica +=1
	if musica >= len(music_list): 
		print("reset!")
		musica = 0 
	#pygame.mixer.music.load(music_list[musica])
	#pygame.mixer.music.set_volume(volume)
	#pygame.mixer.music.play(10000)
def coloring():
	global pcolor
	color = slot[pcount]
	colorline = (pcolor[0], pcolor[1], pcolor[2],0.5)
	if pcolor[0] <= 60 or pcolor[1] <= 60 or pcolor[2] <= 60: colorline = (min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5)
	#(min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5),
	print(color)
	pcolor = ink_add_for_rgb([
					colorline,
					(color[0],color[1],color[2],0.5)
					])
def add_color(key):
	global slot
	global pcount
	global ppleace
	global pcolor
	global bluec
	global greenc
	global redc
	global win
	slotr = random.randint(0, 40)
	#if slotr == 1:
	#	slot[pcount] = (-1, -1, -1)
	#elif slotr == 2:
	#	slot[pcount] = (1000, 1000, 1000)
	#	print("ne má")
	#else:
	color = colors[random.randint(0, 5)]
	slot[pcount] = color
	ppleace += 1
	if key == "w":
		pcount -= 7
	elif key == "s":
		pcount += 7
	elif key == "a":
		pcount -= 1
	elif key == "d":
		pcount += 1
	color = slot[pcount]
	#print(str(pcolor))
	#print(win)
	if win == 1:
		coloring()
	if win >= 0:
		win -= 1
	else:
		coloring()
def multyplayer():
	global name
	global px
	global py
	global color
	global win
	global RPC
	
	if key != "-":
		d = {"name":name, "key":key, "character":character}
	else:
		d = {"name":name, "character":character}
	msg = pickle.dumps(d)
	s.send(msg)
	try:
		input = pickle.loads(s.recv(1024))
	except EOFError:
		d = {"name":name, "key":key, "character":character}
		msg = pickle.dumps(d)
		s.send(msg)
		print("Waiting for input...")
	#except:
	#	input = s.recv(1024)
	#	print("The server said:"+str(input))
	print(input)
	got = True
	slot = input["slot"]
	if input["players"] > 0:
		RPC.update(large_image="logo", state="Multyplayer",start = datetime.now().timestamp(),party_id=str(host),join=str(input["code"]), party_size=[input["players"], input["max_players"]])
	count = 0
	i2 = 0
	i = 0
	x = 0
	y = 0
	got = False
	while i2 < 7:
		y = i2*100
		while i < 7:
			x = i*100
			if slot[count] == (1000, 1000, 1000):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 50, 50, 25))
			elif slot[count] == (-1, -1, -1):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 37, y + 23, 25, 50))
			else:
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x, y, 100, 100))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = 0
	i = 0
	for index in input:
		if input[index] != input["slot"]:
			try:
				pygame.draw.rect(pleace, input[index]["color"], pygame.Rect(input[index]["x"], input[index]["y"], 50, 50))
				if input[index]["character"] == 0:pleace.blit(pygame.image.load("character1.png"),[input[index]["x"],input[index]["y"]])
				elif input[index]["character"] == 1:pleace.blit(pygame.image.load("character2.png"),[input[index]["x"],input[index]["y"]])
				elif input[index]["character"] == 2:pleace.blit(pygame.image.load("character3.png"),[input[index]["x"],input[index]["y"]])
				if win == 1:
					pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(input[index]["x"] + 5, input[index]["y"] + 5, 55, 55))
					pleace.blit(pygame.font.Font("arial.ttf", 150).render(str(input[index]["name"]), True, (255, 0, 255)), (0, 400))
				pleace.blit(pygame.font.Font("arial.ttf", 25).render(str(input[index]["name"]), True, (127.5, 127.5, 127.5)), (input[index]["x"], input[index]["y"] - 25))
				pleace.blit(pygame.font.Font("arial.ttf", 35).render(str(input[index]["p-c"]), True, (100, 100, 100)), (input[index]["x"]+ 5, input[index]["y"]+5))
			except:
				pass
		i += 1
	i = 0
	# single player : pygame.draw.rect(pleace, pcolor, pygame.Rect(px, py, 50, 50))
def singleplayer():
	global name
	global pcolor
	global px
	global py
	global colors
	global pleace
	global win
	global name
	global slot
	i2 = 0
	i = 0
	x = 0
	y = 0
	count = 0
	while i2 < 7:
		y = i2*100
		while i < 7:
			x = i*100
			if slot[count] == (1000, 1000, 1000):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
			elif slot[count] == (-1, -1, -1):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 37, y + 23, 25, 50))
			else:
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x, y, 100, 100))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = 0
	print(pcolor)
	#pleace.blit(pygame.font.Font("arial.ttf", 35).render(str(ppleace), True, (100, 100, 100)), (px+ 5, py+5))
	red = pcolor[0]
	green = pcolor[1]
	blue = pcolor[2]
	if pcolor[0] <= 255:
		pygame.draw.rect(pleace,pcolor, pygame.Rect(px, py, 50, 50))
		if red == blue and red > green and green < 127.5 and red > 50 and blue > 50 and red < 255 and blue < 255:
			if win < 1:
				win = 15
		if win > 0:
			pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(px + 5, py + 5, 40, 40))
		if character == 0:pleace.blit(pygame.image.load("character1.png"),[px,py])
		elif character == 1:pleace.blit(pygame.image.load("character2.png"),[px,py])
		elif character == 2:pleace.blit(pygame.image.load("character3.png"),[px,py])
	#elif pcolor[0] > 1000:
	#	pygame
	pleace.blit(pygame.font.Font("arial.ttf", 25).render(name, True, (127.5, 127.5, 127.5)), (px, py - 25))
	#print(pcolor)

character1 = Button(0, 200, 233, 400, (127.5,0,127.5), "Smile", 50, (255,255,255))
character2 = Button(233, 200, 466, 400, (127.5,0,0), "Shur Kers", 50, (255,255,255))
character3 = Button(466, 200, 700, 400, (0,0,127.5), "Ninja", 50, (255,255,255))

while playing:
	#try:
	#	if str(s.recv(1024)).startswith("÷"):
	#		print(str(s.recv(1024)))
	#		d = {"name":name, "y":py, "x":px, "color":pcolor, "level":ppleace}
	#		msg = pickle.dumps(d)
	#		s.send(msg)
	#except:
	#	pass
	if start == 1:
		key = "-"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					if not arrows:
						if py > 75:
							py -= 100
							if not connected: add_color("w")
							else: key = "w"
				elif event.key == pygame.K_s:
					if not arrows:
						if py < 625:
							py += 100
							if not connected:add_color("s")
							else: key = "s"
				elif event.key == pygame.K_d:
					if not arrows:
						if px < 625:
							px += 100
							if not connected:add_color("d")
							else: key = "d"
				elif event.key == pygame.K_a:
					if not arrows:
						if px > 75:
							px -= 100
							if not connected:add_color("a")
							else: key = "a"
				elif event.key == pygame.K_UP:
					if arrows:
						if py > 75:
							py -= 100
							if not connected:add_color("w")
							else: key = "w"
				elif event.key == pygame.K_DOWN:
					if arrows:
						if py < 625:
							py += 100
							if not connected:add_color("s")
							else: key = "s"
				elif event.key == pygame.K_RIGHT:
					if arrows:
						if px < 625:
							px += 100
							if not connected:add_color("d")
							else: key = "d"
				elif event.key == pygame.K_LEFT:
					if arrows:
						if px > 75:
							px -= 100
							if not connected:add_color("a")
							else: key = "a"
				elif event.key == pygame.K_c:
					pcolor = (0, 0, 0)
					ppleace = 0
				elif event.key == pygame.K_ESCAPE:
					playing = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:
					volume -= 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F2:
					volume += 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F3:
					pygame.mixer.music.stop()
					root = tkinter.Tk()
					root.withdraw()
					pygame.mixer.music.load(str(filedialog.askopenfilename()))
					pygame.mixer.music.play(1000000)
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F4:
					if arrows:
						arrows = False
					else:
						arrows = True
				elif event.key == pygame.K_F6:
					pygame.mixer.music.stop()
		if connected:
			multyplayer()
		else:
			if not render:
				render = True
				i2 = 0
				i = 0
				while i2 < 7:
					y = i2*100
					while i < 7:
						x = i*100
						slotr = random.randint(0, 30)
						#if slotr == 1:
						#	slot.append((-1, -1, -1))
						#elif slotr == 2:
						#	slot.append((1000, 1000, 1000))
						#else:
						color = colors[random.randint(0, 5)]
						slot.append(color)
						i += 1
					i = 0
					x = 0
					i2 += 1
				i = 0
				x = 0
				y = 0
				i2 = 0
			singleplayer()
	elif start == 2:
		lol = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if connected:
					s.close()
				playing = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:
					volume -= 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F2:
					volume += 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_RETURN:
					if typing:
						check()
						start = 3
						lol = True
					else:
						typing = True
				elif event.key == pygame.K_DOWN:
					typing = True
				elif event.key == pygame.K_UP:
					typing = False
				elif event.key == pygame.K_BACKSPACE:
					if not typing:
						name = name[:-1]
					else:
						host = host[:-1]
				else:
					if not typing:
						name += event.unicode
					else:
						host += event.unicode

		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 400, 700, 110))
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 540, 700, 110))
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(150, 150, 400, 100))
		pleace.blit(pygame.font.Font("arial.ttf", 100).render("PURPLE", True, (255, 255, 255)), (150, 150))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render("Name:", True, (255, 255, 255)), (0, 400))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render(name , True, (255, 255, 255)), (0, 450))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render("Hostname:", True, (255, 255, 255)), (0, 540))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render(host , True, (255, 255, 255)), (0, 590))
		if lol: pleace.fill((0,0,0))
	elif start == 3:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
		character1.show()
		if character1.is_pressed(0):
			character = 0
			start = 1
			print("nice")
		character2.show()
		if character2.is_pressed(0):
			start = 1
			character = 1
			print("nice")
		character3.show()
		if character3.is_pressed(0):
			start = 1
			character = 2
			print("nice")
	pygame.display.update()
	pygame.time.Clock().tick(60)
