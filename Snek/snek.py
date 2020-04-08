import pygame 
import random
import time


###
# Configuration Class. Values of the variables
# in this class should be modified instead of 
# the main function. 
###
class CFG():
	CLR_SNEK = (240, 64, 64)
	CLR_BG = (128, 128, 128)
	CLR_FOOD = (240, 240, 64)
	CLR_TMSG_BD = (192, 64, 64)
	SIZE_SNEK = 10				# snake size in pixels
	SIZE_WIN = (800, 450)		# Window size (width, height)
	SIZE_FONT = SIZE_WIN[0] // 20
	SPD = 10					# snake speed


###
# Some little utility functions
###
def titleText(disp, text, color, msg_location=None):
	font_style = pygame.font.SysFont(None, CFG.SIZE_FONT)
	msg = font_style.render(text, True, color)
	if msg_location == None:
		msg_location = msg.get_rect()
		msg_location.center = (CFG.SIZE_WIN[0]//2, CFG.SIZE_WIN[1]//2)
	disp.blit(msg, msg_location)

def randCoord():
	x = random.randrange(0, CFG.SIZE_WIN[0] - CFG.SIZE_SNEK, CFG.SIZE_SNEK)
	y = random.randrange(0, CFG.SIZE_WIN[1] - CFG.SIZE_SNEK, CFG.SIZE_SNEK)
	return (x, y)


###
# Main Game Loop Function
###
def gameLoop():
	disp = pygame.display.set_mode(CFG.SIZE_WIN)
	pygame.display.update()
	pygame.display.set_caption("Snek")

	snek = []	# list of coordinate tuples (x,y).
	snek_length = 1

	x, y = randCoord()

	# initially snek is not moving. these
	# values will be updated every time player
	# presses an arrow key.
	move_x, move_y = 0, 0
	prev_move = None	# will be reset everytime key is pressed
	
	food_x, food_y = randCoord()

	clock = pygame.time.Clock()
	
	game_over, quit_game = False, False
	while not quit_game:
		while game_over:
			disp.fill(CFG.CLR_BG)
			titleText(disp, "YU DED MAN! Wanna play again [R] or nah [ESC]?", CFG.CLR_TMSG_BD)
			pygame.display.update()

			for e in pygame.event.get():
				print(e)
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_ESCAPE:
						quit_game = True
						game_over = False	# terminate [while game_over] loop
					if e.key == pygame.K_r:
						gameLoop()

		for e in pygame.event.get():
			print(e)
			if e.type == pygame.QUIT:
				game_over = True
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_LEFT and prev_move != pygame.K_RIGHT:
					move_x = -CFG.SIZE_SNEK
					move_y = 0
					prev_move = pygame.K_LEFT
				elif e.key == pygame.K_RIGHT and prev_move != pygame.K_LEFT:
					move_x = +CFG.SIZE_SNEK
					move_y = 0
					prev_move = pygame.K_RIGHT
				elif e.key == pygame.K_UP and prev_move != pygame.K_DOWN:
					move_y = -CFG.SIZE_SNEK
					move_x = 0
					prev_move = pygame.K_UP
				elif e.key == pygame.K_DOWN and prev_move != pygame.K_UP:
					move_y = +CFG.SIZE_SNEK
					move_x = 0
					prev_move = pygame.K_DOWN

		if x >= CFG.SIZE_WIN[0] or x < 0 or y >= CFG.SIZE_WIN[1] or y < 0:
			game_over = True
		x += move_x	
		y += move_y

		disp.fill(CFG.CLR_BG)
		# first create food, after that snek so that when snek eats the food,
		# snek is over the food in display.
		pygame.draw.rect(disp, CFG.CLR_FOOD, [food_x, food_y, CFG.SIZE_SNEK, CFG.SIZE_SNEK])	# draw food
		head = (x, y)
		snek.append(head)			# first, append new part to snek
		print(head)
		print(snek)
		if snek_length < len(snek):	# but if snek hasn't eaten a food,
			del snek[0]				# delete the previous part.
		print(snek)

		# check if snek has collided with itself:
		for body_part in snek[:-1]:	# exclude real head
			if body_part == head:
				game_over = True

		for body_part in snek:		# draw snek
			pygame.draw.rect(disp, CFG.CLR_SNEK, 
				[body_part[0], body_part[1], CFG.SIZE_SNEK, CFG.SIZE_SNEK]
			)
		pygame.display.update()


		if x == food_x and y == food_y:
			snek_length += 1
			while (food_x, food_y) in snek:		# until food is not inside snek,
				food_x, food_y = randCoord()	# reset food's location
			print("Yummy!!")


		clock.tick(CFG.SPD)

	pygame.quit()


###
# Main Program
###
if __name__ == '__main__':
	pygame.init()
	gameLoop()
