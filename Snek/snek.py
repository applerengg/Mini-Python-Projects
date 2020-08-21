import random
#import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"	# do not print message on pygame import
from pygame import *


###
# Configuration Class. Values of the variables
# in this class should be modified instead of 
# the main function. 
###
class CFG():
	CLR_SNEK = (32, 128, 0)			# Snek Color
	CLR_BG = (220, 220, 220)		# Main game Background Color
	CLR_FOOD = (255, 255, 32)		# Food color
	CLR_SCR_TXT = (32, 32, 192)		# Score text color
	CLR_TTL_TXT = (192, 64, 64)		# Title text color
	SIZE_SNEK = 12					# snake size in pixels
	SIZE_WIN = (720, 720)			# Window size (width, height)
	SPD = 30						# snake speed

	# Binary settings
	BRDR_FOOD = True			# draw borders for food
	BRDR_SNEK = False			# draw borders for snek
	PORTAL_WALLS = True			# if set to true, collision with the window borders won't kill.
	ALWYS_SHW_SCR = True 		# if set to true, shows score while playing, otherwise only when game ends.
	ALWYS_SHW_TME = True 		# if set to true, shows time while playing, otherwise only when game ends.

	# Constants
	LCTN_SCR_TXT = (SIZE_SNEK, SIZE_SNEK)	# location on which score will be displayed 
	SIZE_SCR_TXT = SIZE_WIN[0] // 40		# score text size
	SIZE_TTL_TXT = SIZE_WIN[0] // 20		# title text size


###
# Some little utility functions
###
def displayText(disp, text_type, text, msg_location=None):
	color = None
	size = None
	if text_type == "score":
		color = CFG.CLR_SCR_TXT
		size = CFG.SIZE_SCR_TXT
	if text_type == "title":
		color = CFG.CLR_TTL_TXT
		size = CFG.SIZE_TTL_TXT

	font_title = font.SysFont(None, size)
	msg = font_title.render(text, True, color)
	if msg_location == None:
		msg_location = msg.get_rect()
		msg_location.center = (CFG.SIZE_WIN[0]//2, CFG.SIZE_WIN[1]//2)
	disp.blit(msg, msg_location)

def randCoord():
	x = random.randrange(0, CFG.SIZE_WIN[0] - CFG.SIZE_SNEK, CFG.SIZE_SNEK)
	y = random.randrange(0, CFG.SIZE_WIN[1] - CFG.SIZE_SNEK, CFG.SIZE_SNEK)
	return (x, y)

def drawWithBorder(disp, clr, x, y, size, bclr=None):
	if bclr != None:
		draw.rect(disp, bclr, [x, y, size, size], 1)		# draw entity border
		draw.rect(disp, clr, [x+1, y+1, size-2, size-2])	# draw entity itself
	else:
		draw.rect(disp, clr, [x, y, size, size])		# draw entity itself

###
# Main Game Loop Function
###
def gameLoop():
	disp = display.set_mode(CFG.SIZE_WIN)
	display.update()
	display.set_caption("Snek")

	snek = []	# list of coordinate tuples (x,y).
	snek_length = 1

	x, y = randCoord()

	# initially snek is not moving. these
	# values will be updated every time player
	# presses an arrow key.
	move_x, move_y = 0, 0
	prev_move = None	# will be reset everytime key is pressed
	food_x, food_y = randCoord()

	clock = time.Clock()
	border_food = (0,0,0) if CFG.BRDR_FOOD else None
	border_snek = (0,0,0) if CFG.BRDR_SNEK else None

	game_over, quit_game = False, False
	while not quit_game:
		while game_over:
			disp.fill(CFG.CLR_BG)
			displayText(disp, "title", "YU DED MAN! Wanna play again [R] or nah [ESC]?")
			displayText(disp, "score", "SCORE: {}".format(snek_length-1), msg_location=CFG.LCTN_SCR_TXT)	# display score
			display.update()

			for e in event.get():
				#print(e)
				if e.type == KEYDOWN:
					if e.key == K_ESCAPE:
						quit_game = True
						game_over = False	# terminate [while game_over] loop
					if e.key == K_r:
						gameLoop()

		for e in event.get():
			#print(e)
			if e.type == QUIT:
				quit_game = True
			if e.type == KEYDOWN:
				if e.key == K_LEFT and prev_move != K_RIGHT:
					move_x = -CFG.SIZE_SNEK
					move_y = 0
					prev_move = K_LEFT
				elif e.key == K_RIGHT and prev_move != K_LEFT:
					move_x = +CFG.SIZE_SNEK
					move_y = 0
					prev_move = K_RIGHT
				elif e.key == K_UP and prev_move != K_DOWN:
					move_y = -CFG.SIZE_SNEK
					move_x = 0
					prev_move = K_UP
				elif e.key == K_DOWN and prev_move != K_UP:
					move_y = +CFG.SIZE_SNEK
					move_x = 0
					prev_move = K_DOWN

		if x >= CFG.SIZE_WIN[0] or x < 0 or y >= CFG.SIZE_WIN[1] or y < 0:
			if CFG.PORTAL_WALLS:
				x %= CFG.SIZE_WIN[0]
				y %= CFG.SIZE_WIN[1]
			else:	
				game_over = True
		
		x += move_x	
		y += move_y

		disp.fill(CFG.CLR_BG)
		# first create food, after that snek so that when snek eats the food,
		# snek is over the food in display.
		# draw.rect(disp, (0, 0, 0), [food_x, food_y, CFG.SIZE_SNEK, CFG.SIZE_SNEK], 2)	# draw food border
		# draw.rect(disp, CFG.CLR_FOOD, [food_x+1, food_y+1, CFG.SIZE_SNEK-2, CFG.SIZE_SNEK-2])	# draw food
		drawWithBorder(disp, CFG.CLR_FOOD, food_x, food_y, CFG.SIZE_SNEK, bclr=border_food)	# draw food
		head = (x, y)
		snek.append(head)			# first, append new part to snek
		if snek_length < len(snek):	# but if snek hasn't eaten a food,
			del snek[0]				# delete the previous part.
		
		# check if snek has collided with itself:
		for body_part in snek[:-1]:	# exclude real head
			if body_part == head:
				game_over = True

		for body_part in snek:		# draw snek
			drawWithBorder(disp, CFG.CLR_SNEK, body_part[0], body_part[1], CFG.SIZE_SNEK, bclr=border_snek)
			# draw.rect(disp, CFG.CLR_SNEK, 
			# 	[body_part[0], body_part[1], CFG.SIZE_SNEK, CFG.SIZE_SNEK]
			# )

		if CFG.ALWYS_SHW_SCR:
			displayText(disp, "score", "SCORE: {}".format(snek_length-1), msg_location=CFG.LCTN_SCR_TXT)	# display score
		display.update()


		if x == food_x and y == food_y:
			snek_length += 1
			while (food_x, food_y) in snek:		# until food is not inside snek,
				food_x, food_y = randCoord()	# reset food's location
			print("Score =", snek_length-1)


		clock.tick(CFG.SPD)

	quit()


###
# Main Program
###
if __name__ == '__main__':
	init()
	gameLoop()
