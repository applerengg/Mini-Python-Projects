
from random import choice, randint
import time 
from threading import Thread 	# for ingame day cycle.

import os 
from termcolor import cprint, colored	# colored output on screen

from string import printable	# for attribute point spend checking.

import pickle 	# for saving and loading profiles.
import os 		# for saving and loading profiles.

import sys 		# sys.exit()

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"	# do not print message on pygame import
from pygame import mixer	# background music

os.system("color")		# colored output can be used now
mixer.init()			# initialize for later usage

def clear_screen():
	os.system("cls" if os.name=="nt" else "clear")

###
### Configuration
###
class Config():
	def __init__(self):
		self.ATTR_POINTS_HILVL = 6		# attribute points gained at levelup after level 5
		self.ATTR_POINTS_INITIAL = 10	# attribute points given in the beginning
		self.ATTR_POINTS_LOWLVL = 3		# attribute points gained at levelup before level 5
		self.BRAVERY_CRITDMG = 0.1		# bravery's increase rate of critmultiplier
		self.BRAVERY_FLEEDELAY = 3
		self.DEBUGMDOE = False
		self.DEFENSE_ABSORB = 7/8
		self.DEFENSE_CURRHP_INCREASE = 1
		self.ENEMY_INITIAL_DMG = 3
		self.ENEMY_INITIAL_HP = 1
		self.ENEMY_INITIAL_DEF = 1
		self.ENEMY_INITIAL_SPD = 1
		self.ENEMY_INITIAL_LCK = 1
		self.ENEMY_INITIAL_RGN = 0
		self.ENEMY_MAX_LEVEL = 2
		self.ENEMY_MIN_LEVEL = -2
		self.HP_CURRHP_INCREASE = 10
		self.INCORRECT_STAT_ENTRY_HI = printable.translate({ord(i): None for i in "1234567"})
		self.INCORRECT_STAT_ENTRY_LO = printable.translate({ord(i): None for i in "123"})
		self.MUSIC_BATTLE = "music/RH_test_battle.mp3"
		self.MUSIC_ENEMYENCOUNTER = ""
		self.MUSIC_LEVELUP = "music/RH_test_levelup.mp3"
		self.MUSIC_LOOTENCOUNTER = "music/RH_test_lootencounter.mp3"
		self.MUSIC_MAIN = "music/RH_test_main.mp3"
		self.QUICK_TURN = 20
		self.REGEN_MULTIPLIER = 2/4
		self.TURNLIMIT_MAX = 20
		self.TURNLIMIT_XPHI = 6
		self.TURNLIMIT_XPLOW = 3
		self.XP_TO_NEXTLEVEL = 100

cfg = Config()

class Clock():
	def __init__(self):
		self.clock_thread = Thread(target=self.start)
		self.clock_thread.daemon = True
	def start(self):
		self.clock_thread.start()
	def stop(self):
		pass



###
### Hero Class
###

###		attributes:
#	damage		-> amount of harm applied to enemy
#	hp			-> maximum amount of damage player can withstand
#	defense		-> decrase damage taken 
#	speed		-> increase turn frequency and dodge rate
#	bravery		-> delay enemy flee and increase critmultiplier
#	luck 		-> increase crit chance and enemy loot
#	regeneration-> hp increase rate
#	
#	xp			-> required to level up
#	level 		-> player level
#
#	weapon 		-> affects min-max damage and speed
#
class RandomHero():
	def __init__(self, name, damage, hp, defense, speed=1, bravery=0, luck=5, regeneration=1, xp=0, level=1, weapon=None, critmultiplier=1.2, color="green", money=0):
		self.all_attr = dict()
		self.name = name
		self.damage = damage
		self.defense = defense
		self.hp = hp 							 
		self.max_hp = self.hp*10 + self.defense
		self.curr_hp = self.max_hp 
		self.bravery = bravery
		self.luck = luck
		self.regeneration = regeneration
		self.xp = xp
		self.level = level
		if not weapon:
			self.weapon = Weapon("Fist", -1, 1, 0)
		else:
			self.weapon = weapon
		self.mindmg = self.weapon.mindmg + damage
		self.maxdmg = self.weapon.maxdmg + damage
		self.speed = speed + self.weapon.speed
		self.critmultiplier = critmultiplier + self.damage/20 + self.bravery*cfg.BRAVERY_CRITDMG
		self.updateAttrdict()
		self.color = color
		self.money = money

	def __str__(self):
		return str(sorted(self.updateAttrdict().items()))

	def updateAttrdict(self):
		self.all_attr["name"] = self.name
		self.all_attr["damage"] = self.damage
		self.all_attr["hp"] = self.hp
		self.all_attr["defense"] = self.defense
		self.all_attr["speed"] = self.speed
		self.all_attr["bravery"] = self.bravery
		self.all_attr["luck"] = self.luck
		self.all_attr["regeneration"] = self.regeneration
		self.all_attr["xp"] = round(self.xp, 2)
		self.all_attr["level"] = self.level
		self.all_attr["weapon"] = str(self.weapon)
		self.all_attr["critmultiplier"] = round(self.critmultiplier,2)
		self.all_attr["max hp"] = self.max_hp
		return self.all_attr

	def updateAttrs(self, damage=0, hp=0, defense=0, speed=0, bravery=0, luck=0, regeneration=0):
		self.damage += damage
		self.damage = 1 if self.damage<1 else self.damage
		self.hp += hp
		self.hp = 1 if self.hp<1 else self.hp
		self.defense += defense
		self.defense = 1 if self.defense<1 else self.defense
		self.speed += speed
		self.speed = 1 if self.speed<1 else self.speed
		self.bravery += bravery
		self.bravery = 1 if self.bravery<1 else self.bravery
		self.luck += luck
		self.luck = 1 if self.luck<1 else self.luck
		self.regeneration += regeneration
		self.regeneration = 1 if self.regeneration<1 else self.regeneration

		self.curr_hp = self.hp*10 + self.defense
		self.max_hp = self.curr_hp
		self.mindmg += damage
		self.maxdmg += damage
		self.critmultiplier += (damage/20) + bravery*cfg.BRAVERY_CRITDMG

	def checkStats(self):
		print("\n\t{} Stats:".format(colored(self.name, self.color)))
		for k, v in sorted(self.updateAttrdict().items()):
			print("\t{: <16}: {}".format(k,v))
		print()	# print newline

	def levelUp(self):
		mixer.music.load(cfg.MUSIC_LEVELUP)
		mixer.music.play()

		new_attr_points = 0
		level_earned = int(self.xp // cfg.XP_TO_NEXTLEVEL)
		self.xp -= cfg.XP_TO_NEXTLEVEL * level_earned
		for i in range(1, level_earned+1):
			if self.level + i >= 5:
				new_attr_points += cfg.ATTR_POINTS_HILVL
			else:
				new_attr_points += cfg.ATTR_POINTS_LOWLVL
			
		self.level += level_earned

		levelup_message = """
{0} You are now level {3}
(1) Damage
(2) HP
(3) Defense{1}
You have {2} attribute points. Enter {2} numbers:
[Be careful! If more than {2} numbers entered, the first {2} will be applied.]
??> """.format(
		colored("==> LEVEL UP!","blue",attrs=["bold"]),
		"" if self.level<5 else "\n(4) Speed\n(5) Bravery\n(6) Luck\n(7) Regeneration",
		new_attr_points,
		self.level
	)
	
		new_stats = input(levelup_message)

		new_stats = new_stats.replace(" ","").replace("\t","")[:new_attr_points]
		tooshort = True if len(new_stats) < new_attr_points else False
		
		if self.level < 5:
			while any(i in cfg.INCORRECT_STAT_ENTRY_LO for i in new_stats) or tooshort:
				new_stats = input("Either too short or incorrect entry, try again\n??> ")		
				new_stats = new_stats.replace(" ","").replace("\t","")[:new_attr_points]
				if len(new_stats) < new_attr_points:
					tooshort = True
			
			dmg = new_stats.count("1")
			hp = new_stats.count("2")
			defns = new_stats.count("3")
			self.updateAttrs(dmg, hp, defns)
		
		else:
			while any(i in cfg.INCORRECT_STAT_ENTRY_HI for i in new_stats) or tooshort:
				new_stats = input("Either too short or incorrect entry, try again\n??> ")		
				new_stats = new_stats.replace(" ","").replace("\t","")[:new_attr_points]
				if len(new_stats) < new_attr_points:
					tooshort = True
				else:
					tooshort = False	

			dmg = new_stats.count("1")
			hp = new_stats.count("2")
			defns = new_stats.count("3")
			spd = new_stats.count("4")
			brv = new_stats.count("5")
			lck = new_stats.count("6")
			rgn = new_stats.count("7")
			self.updateAttrs(dmg,hp,defns,spd,brv,lck,rgn)



class Weapon():
	def __init__(self, name, mindmg, maxdmg, speed):
		self.type = name
		self.name = name
		self.mindmg = mindmg
		self.maxdmg = maxdmg
		self.speed = speed
	def changeName(self, newname):
		self.name = newname + "({})".format(self.type)	
	def __str__(self):
		return "{}: {} ~ {} damage, {} speed".format(self.name, self.mindmg, self.maxdmg, self.speed)

###
### Enemy Class
###
class Enemy():
	def __init__(self, level, name=None, behaviour=None, boss=None):
		self.level = level+cfg.ENEMY_MAX_LEVEL if boss else randint(
			level+cfg.ENEMY_MIN_LEVEL, level+cfg.ENEMY_MAX_LEVEL)
		if self.level < 0:
			self.level = 0
		self.color = "red"
		
		# xp will be increased if enemy is boss
		self.xp = 1
		if self.level > level:		# enemy is stronger
			self.xp += cfg.XP_TO_NEXTLEVEL * 3 / 20
		elif self.level < level:	# enemy is weaker
			self.xp += cfg.XP_TO_NEXTLEVEL * 1.5 / 20
		else:						# enemy is same level
			self.xp += cfg.XP_TO_NEXTLEVEL * 2 / 20
		self.xp += randint(-cfg.XP_TO_NEXTLEVEL//30, cfg.XP_TO_NEXTLEVEL//20)	

		names = ["Bandit","Monavar","Mummy","Spicek","Tepelops","Wobbegangsta"]	# add more
		self.name = name if name else choice(names)

		behaviours = ["offensive", "defensive", "balanced"]+[None]*3
		self.behaviour=behaviour if behaviour else choice(behaviours)
		
		boss_options_hilvl = ["boss"]*5 + ["miniboss"]*10 + [None]*85
		boss_options_lowlvl = ["miniboss"]*10 + [None]*90
		if self.level == level + cfg.ENEMY_MAX_LEVEL:
			self.is_boss = boss if boss is not None else choice(boss_options_hilvl)
		elif self.level >= level:
			self.is_boss = boss if boss is not None else choice(boss_options_lowlvl)
		else:
			self.is_boss = boss	

		attr_points = 0
		if self.level < 5:
			attr_points = cfg.ATTR_POINTS_INITIAL//3 + (
				(self.level-1) * cfg.ATTR_POINTS_LOWLVL if self.level>1 else 0
				)
		else:
			attr_points = cfg.ATTR_POINTS_INITIAL//2 + 3*cfg.ATTR_POINTS_LOWLVL + (self.level-4)*cfg.ATTR_POINTS_HILVL	
		if self.is_boss == "miniboss":
			attr_points += cfg.ATTR_POINTS_LOWLVL * 2 
			self.color = "cyan"
			self.xp += cfg.XP_TO_NEXTLEVEL // 3
		if self.is_boss == "boss":
			attr_points += cfg.ATTR_POINTS_HILVL * 2
			self.color = "magenta"
			self.xp += cfg.XP_TO_NEXTLEVEL // 5
		if cfg.DEBUGMDOE == True:	
			print("ATTRPOINTS",attr_points)

		self.loot = 1
		self.loot += randint(round(self.xp/4), round(self.xp*2))

		# DETERMINE ATTRIBUTE DISTRIBUTION
		self.dmg = 0
		self.hp = 0
		self.defense = 0
		self.speed = 0
		self.luck = 0
		self.regeneration = 0
		if behaviour == "offensive":
			self.dmg += randint(attr_points*3//8, attr_points*6//8)
			attr_points -= self.dmg
			self.defense += attr_points // 3
			self.hp += (attr_points//3)
			attr_points -= self.defense * 2
			self.speed += attr_points // 3
			self.luck += attr_points // 3
			self.regeneration += attr_points // 3
			attr_points -= 3 * (attr_points//3)
			self.speed += attr_points if attr_points>0 else 0	# spend last points
		elif behaviour == "defensive":
			self.defense += randint(attr_points*3//8, attr_points*5//8)
			attr_points -= self.defense
			self.hp += (attr_points//2)
			attr_points -= attr_points//2
			self.dmg += attr_points // 2
			attr_points -= self.dmg
			self.speed += attr_points // 3
			self.luck += attr_points // 3
			self.regeneration += attr_points // 3
			attr_points -= 3 * (attr_points//3)
			self.speed += attr_points if attr_points>0 else 0	# spend last points
		elif behaviour == "balanced":
			self.defense += attr_points // 5
			self.hp += (attr_points//5)
			self.dmg += attr_points // 5
			attr_points -= 3 * (attr_points//5)
			self.speed += attr_points // 3
			self.luck += attr_points // 3
			self.regeneration += attr_points // 3
			attr_points -= 3 * (attr_points//3)
			self.speed += attr_points if attr_points>0 else 0	# spend last points
		else:
			self.defense += randint(0, attr_points-1)
			attr_points -= self.defense
			self.hp += randint(0, attr_points) if attr_points>1 else 1
			attr_points -= self.hp
			self.dmg += randint(0, attr_points) if attr_points>1 else 1
			attr_points -= self.dmg
			self.speed += randint(0, attr_points) if attr_points>1 else 1
			attr_points -= self.speed
			self.luck += randint(0, attr_points) if attr_points>1 else 1
			attr_points -= self.luck
			self.regeneration += randint(0, attr_points) if attr_points>1 else 1
			attr_points -= self.regeneration
			self.speed += attr_points if attr_points>0 else 0	# spend last points
		
		self.dmg += cfg.ENEMY_INITIAL_DMG
		self.hp += cfg.ENEMY_INITIAL_HP
		self.defense += cfg.ENEMY_INITIAL_DEF
		self.speed += cfg.ENEMY_INITIAL_SPD
		self.luck += cfg.ENEMY_INITIAL_LCK
		self.regeneration += cfg.ENEMY_INITIAL_RGN

		self.mindmg = randint(0, self.dmg)
		self.maxdmg = 2*self.dmg - self.mindmg
		self.max_hp = self.hp*10 + self.defense
		self.curr_hp = self.max_hp	
		self.critmultiplier = randint(12,15)/10 + self.dmg/20 
		self.all_attr = dict()
		if cfg.DEBUGMDOE == True:
			print("behaviour:",self.behaviour,"dmg:",self.dmg,"hp:",self.hp,"def:",self.defense)
	
	def __str__(self):
		return str(sorted(self.updateAttrdict().items()))

	def updateAttrdict(self):
		self.all_attr["name"] = self.name
		self.all_attr["behaviour"] = self.behaviour if self.behaviour is not None else "Random"
		self.all_attr["mindmg"] = self.mindmg
		self.all_attr["maxdmg"] = self.maxdmg
		self.all_attr["hp"] = self.hp
		self.all_attr["defense"] = self.defense
		self.all_attr["speed"] = self.speed
		self.all_attr["luck"] = self.luck
		self.all_attr["regeneration"] = self.regeneration
		self.all_attr["level"] = self.level
		self.all_attr["critmultiplier"] = round(self.critmultiplier,2)
		self.all_attr["max hp"] = self.max_hp
		return self.all_attr

	def checkStats(self):
		print("\n\t{} Stats:".format(colored(self.name, self.color)))
		for k, v in sorted(self.updateAttrdict().items()):
			print("\t{: <16}: {}".format(k,v))
		print()	# print newline

###
### Gameplay functions
###
def createNewHero():
	clear_screen()
	playername = input("Hero Name: ")
	initial_stats = input("""
Welcome {1}, prepare yourself for a great adventure!
Start by customizing your character.

(1) Damage
(2) HP
(3) Defense
You have {0} attribute points. Enter {0} numbers:
[Be careful! If more than {0} numbers entered, the first {0} will be applied.]
??> """.format(cfg.ATTR_POINTS_INITIAL, colored(playername,"green") ))
	initial_stats = initial_stats.replace(" ","").replace("\t","")[:cfg.ATTR_POINTS_INITIAL]
	tooshort = True if len(initial_stats) < cfg.ATTR_POINTS_INITIAL else False
	while any(i in cfg.INCORRECT_STAT_ENTRY_LO for i in initial_stats) or tooshort:
		initial_stats = input("Either too short or incorrect entry, try again\n??> ")
		initial_stats = initial_stats.replace(" ","").replace("\t","")[:cfg.ATTR_POINTS_INITIAL]
		if len(initial_stats) < cfg.ATTR_POINTS_INITIAL:
			tooshort = True
		else: 
			tooshort = False	
		#print(initial_stats, len(initial_stats), tooshort)	# DEBUG
	
	dmg = initial_stats.count("1")
	hp = initial_stats.count("2") + 1
	defns = initial_stats.count("3")

	player = RandomHero(playername, dmg,hp,defns)
	return player



def attack(protagonist, opponent):
	# return None if fight is not over yet (neither player nor the enemy is defeated), else return the winner
	protagonist.curr_hp += protagonist.regeneration * cfg.REGEN_MULTIPLIER
	if protagonist.curr_hp > protagonist.max_hp:
		protagonist.curr_hp = protagonist.max_hp

	dodge_rate = opponent.speed*2 - protagonist.speed//2
	dodge_rate = 1 if dodge_rate<1 else dodge_rate
	opponent_dodged = choice([1]*dodge_rate + [0]*(100-dodge_rate))
	if opponent_dodged:
		print("xx> {} has missed!".format(
			colored(protagonist.name, protagonist.color) ) 
		)
		time.sleep(2)
		return None

	opponent_blocked = choice([1]*opponent.defense + [0]*(100-opponent.defense))
	if opponent_blocked:
		print("xx> {}'s attack has been blocked!".format(
			colored(protagonist.name, protagonist.color) )
		)
		time.sleep(2)
		return None

	dmg = randint(protagonist.mindmg, protagonist.maxdmg)
	crit = choice([1]*protagonist.luck*2 + [0]*(100-protagonist.luck*2))
	dmg_lowerbound = 1 + protagonist.level/2 
	dmg = dmg_lowerbound if (dmg-opponent.defense*cfg.DEFENSE_ABSORB)<dmg_lowerbound else dmg-opponent.defense*cfg.DEFENSE_ABSORB
	dmg = dmg*protagonist.critmultiplier if crit else dmg
	opponent.curr_hp -= dmg
	print("xx> {} has dealt {}{} damage,\n    {} has {} hp left.".format(
		colored(protagonist.name, protagonist.color), 
		round(dmg,2),
		colored(" critical", attrs=["bold"]) if crit else "",
		colored(opponent.name, opponent.color), 
		round(opponent.curr_hp,2)
		), end="\n" 
	)
	if opponent.curr_hp <= 0:
		time.sleep(2)
		return protagonist
	else:
		time.sleep(2)
		return None


def fight(hero, enemy):
	mixer.music.load(cfg.MUSIC_BATTLE)
	mixer.music.play(loops=-1)

	hturn = 0
	eturn = 0
	winner = None
	turn = 0
	try:
		while True:
			turn += 1
			print("xx> Turn {}".format(turn))
			time.sleep(1)
			hturn += hero.speed
			eturn += enemy.speed
			if hturn >= cfg.QUICK_TURN:
				print("::> Quick Turn for {}!".format(hero.name))
				winner = attack(hero, enemy)
				if winner:
					break
				hturn -= cfg.QUICK_TURN
				turn -= 1
			if eturn >= cfg.QUICK_TURN and not hturn >= cfg.QUICK_TURN:
				print("::> Quick Turn for {}!".format(enemy.name))
				winner = attack(enemy, hero)
				if winner:
					break
				eturn -= cfg.QUICK_TURN
			else:
				winner = attack(hero, enemy)
				if winner:
					break
				winner = attack(enemy, hero)
				if winner:
					break
			# enemy may flee if attacker is the hero
			if isinstance(hero, RandomHero): 
				if turn == cfg.TURNLIMIT_MAX + hero.bravery*cfg.BRAVERY_FLEEDELAY:
					break

			print("{:-<48}".format(""))
			time.sleep(1)
	except KeyboardInterrupt:
		cprint("==> {} has fled!".format(
			colored(hero.name, hero.color) ),
			attrs=["bold"],
			end="\n\n"
		)
		time.sleep(3)
		# restore HPs
		hero.curr_hp = hero.max_hp
		enemy.curr_hp = enemy.max_hp
		return

	# restore HPs
	hero.curr_hp = hero.max_hp
	enemy.curr_hp = enemy.max_hp

	print()	# print newline
	if winner == hero:
		xp_earned = enemy.xp

		loot_multiplier = [2]*(hero.luck//2) + [1.5]*(hero.luck//2) + [1.25]*hero.luck + [1]*(100-(2*(hero.luck//2)+hero.luck))
		money_earned = enemy.loot * choice(loot_multiplier)

		hero.xp += xp_earned
		hero.money += money_earned
		
		cprint("==> {} has won!".format(
			colored(hero.name, hero.color) ),
			attrs=["bold"]
		)
		cprint("==> Earned {} cora and {} xp.".format(
			colored(round(money_earned,2), attrs=["bold"]),
			colored(round(xp_earned,2), attrs=["bold"])	),
			end="\n\n"
		)

		if hero.xp >= cfg.XP_TO_NEXTLEVEL:
			hero.levelUp()
			

	elif winner == enemy:
		xp_earned = enemy.xp / 4
		hero.xp += xp_earned

		cprint("==> {} has won!".format(
			colored(enemy.name, enemy.color) ),
			attrs=["bold"]
		)
		cprint("==> Earned 0 cora and {} xp.".format(
			colored(round(xp_earned,2), attrs=["bold"])	),
			end="\n\n"
		)
	else:			# enemy has fled
		cprint("==> {} has fled!".format(
			colored(enemy.name, enemy.color) ),
			attrs=["bold"],
			end="\n\n"
		)
	time.sleep(1)	


def pprint(entity):
	# Print all attributes of an entity
	for k,v in sorted(entity.__dict__.items()):
		print("{: <16}: {}".format(k,v))

###
### MAIN LOOP FUNCTIONS
###
def enemyEncounter(player):
	try:

		e = Enemy(player.level)
		print("Enemy encounter!\nA {} level {}!".format(
				colored(e.level, attrs=["bold"]),
				colored(e.name, e.color)
			)
		)

		flag_act = True
		while flag_act:
			act = input("""(1) Fight
(2) Check Enemy Stats
(3) Check Your Stats
(4) Runaway
??> """)
			if act == "1":
				print()
				fight(player, e)
				flag_act = False
			elif act == "2":
				e.checkStats()
				input("Press [ENTER] to continue...")
			elif act == "3":
				player.checkStats()
				input("Press [ENTER] to continue...")
			elif act == "4":
				cprint("==> {} has fled!".format(
					colored(player.name, player.color) ),
					attrs=["bold"],
					end="\n\n"
				)
				break
			else:
				continue
	except KeyboardInterrupt:
		return

def lootEncounter(player):
	mixer.music.load(cfg.MUSIC_LOOTENCOUNTER)
	mixer.music.play(loops=-1, start=35)

	print(choice(["You see a box in the middle of the plain.", "You spot a half-buried chest under a tree.", "You notice a bump on the sands. It is a buried crate."]))
	time.sleep(1)
	if player.bravery < (1.1*player.level - 4 + randint(-2, 0)):
		print("You are not brave enough to open it.")
		return

	good = ["You found a shiny piece of armor inside it!",
			"You find a potion, it doesn't seem too suspicious and you decide to drink it.",
			"There is nothing except just a few coras.",
			"There is a decent amount of money in it!"]
	
	bad = [ "As soon as you touch, it triggers an explosion and you get hurt!",
			"You find a potion, it doesn't seem too suspicious and you decide to drink it.", 
			"You find a strange small item inside. While you are trying to figure it out, it releases black gas. You get dizzy and nauseous."]			
	events = [good] + [bad]

	def occur(event):
		print(event)
		if event == good[0]:
			cprint("==> +3 defense", attrs=["bold"])
			exec("player.updateAttrs(defense=2)")
			return 1
		if event == good[1]:
			affected_stat = choice(["damage", "hp", "defense", "bravery", "speed", "regeneration", "luck"])
			cprint("==> +1 {}".format(affected_stat), attrs=["bold"])
			exec("player.updateAttrs("+affected_stat+"=1)")
			return 1
		if event == good[2]:
			loot = randint(5, 9)
			cprint("==> +{} cora".format(loot), attrs=["bold"])
			player.money += loot
			return 1
		if event == good[3]:
			loot = randint(20, 100)
			cprint("==> +{} cora".format(loot), attrs=["bold"])
			player.money += loot
			return 1
		
		if event == bad[0]:
			affected_stat = choice(["hp", "defense"])
			cprint("==> -2 {}".format(affected_stat), attrs=["bold"])
			exec("player.updateAttrs("+affected_stat+"=-2)")
			return -1
		if event == bad[1] or event == bad[2]:
			affected_stat = choice(["damage", "hp", "defense", "bravery", "speed", "regeneration", "luck"])
			cprint("==> -1 {}".format(affected_stat), attrs=["bold"])
			exec("player.updateAttrs("+affected_stat+"=-1)")
			return -1



	locked = randint(0, 1)
	if locked:
		act = input("But it is locked. What do you want to do? \n(1) Try to force open it\n(2) Leave\n??> ")
		if act == "1":
			print("...")
			time.sleep(1)
			if player.damage < 1.5 * player.level or choice([True]*1 + [False]*9):
				affected_stat = choice(["damage", "hp", "defense"])
				print("You are not strong enough, you hurt yourself while trying to open it.")
				cprint("==> -1 {}".format(affected_stat), attrs=["bold"])
				exec("player."+affected_stat+" -= 1")
				exec("player."+affected_stat+" = 1 if player."+affected_stat+"< 1 else player."+affected_stat)
				return -1
			else:
				print("You successfully open it.\n...")
				time.sleep(1)
				event = choice(good)
				occur(event)
		else:
			print("You leave...")
			time.sleep(1)
			return 0		
	
	else:
		act = input("(1) Open it\n(2) Leave\n??> ")
		if act == "1":
			print("...")
			time.sleep(1)
			event = choice(choice(events))
			occur(event)


def store(player):
	print(player.money)
	pass


###
### SAVE & LOAD FUNCTIONS
###
def save(profile):
	# profile is a RandomHero object.
	# Return True if saved, else return False
	while True:		
		save_slot_input = input("Choose a Save Slot (1) (2) (3) to save current profile. Press 'q' to cancel:\n??> ").upper()
		if save_slot_input in ["1", "2", "3"]:
			f = "save_file"+save_slot_input
			if os.path.isfile(f) and os.path.getsize(f) > 0:
				oldprofile = pickle.load(open(f, "rb"))
				confirm = input("Save Slot {} is already occupied.\nHero: {}, level {}.\nPress (1) to confirm overwriting\n??> ".format(save_slot_input, oldprofile.name, oldprofile.level))
				if confirm == "1":
					pickle.dump(profile, open(f, "wb"))
					print("Game Saved to Save Slot {}".format(save_slot_input))
					return True
				else:
					continue
			else:
				pickle.dump(profile, open(f, "wb"))
				print("Game Saved to Save Slot {}".format(save_slot_input))
				return True		
		elif save_slot_input == "Q":
			print("Saving cancelled.")
			return False
		else:
			continue

def load():
	# profile is a RandomHero object.
	# return the saved profile or None depending on the inputs
	while True:		
		save_slot_input = input("Choose a Save Slot (1) (2) (3) to load a profile. Press 'q' to cancel:\n??> ").upper()
		f = "save_file"+save_slot_input 
		if os.path.isfile(f) and os.path.getsize(f) > 0:
			profile = pickle.load(open(f, "rb"))
			confirm = input("Save Slot {} selected.\nHero: {}, level {}. Press (1) to confirm\n??> ".format(save_slot_input, profile.name, profile.level))
			if confirm == "1":
				print("Save Slot {} is loading...".format(save_slot_input))
				return profile
			else: 
				continue
		elif save_slot_input == "Q":
			print("Didn't load profile, creating new profile...")
			time.sleep(1)
			return None
		else:
			print("Selected Save Slot is empty or invalid.")
			continue


if __name__ == '__main__':

	###
	### SET THE PLAYER A PROFILE: LOAD OR CREATE A NEW ONE
	###
	player = None	# initiate player, later will become a RandomHero object by loading or creating a anew one.

	for i in range(1, 4):
		f = "save_file" + str(i)
		if os.path.isfile(f) and os.path.getsize(f) > 0:
			loadable_content = True
			break
	else:
		loadable_content = False

	if loadable_content:
		load_query = input("Saved game(s) available. Press (1) to check/load, any other key otherwise.\n??> ")
		if load_query == "1":
			player = load()
		else:
			print("Creating new profile...")
			time.sleep(1)

	if player == None:	# if a profile is not loaded, create new profile.
		player = createNewHero()
	else:
		clear_screen()
		print("Welcome back {}!\n".format(colored(player.name, player.color)))	
	

	###
	### MAIN LOOP
	###
	while 1:
		if not mixer.music.get_busy():
			mixer.music.load(cfg.MUSIC_MAIN)
			mixer.music.play(loops=-1)

		act = input("""
(1) Explore the wild
(2) Go to the store
(3) Check your stats
(4) Save game
(C) Clear Screen
(Q) Quit game 
??> """).upper()
		if act == "1":
			print()
			for i in range(randint(1, 4)):
				time.sleep(randint(5,20)/10)
				print("...")
			lootEnc_rate = 5 + player.luck	
			func = choice([lootEncounter]*lootEnc_rate + [enemyEncounter]*(100-lootEnc_rate))
			func(player)
			mixer.music.stop()
		elif act == "2":
			store(player)
			time.sleep(1)
		elif act == "3":
			player.checkStats()
			input("Press [ENTER] to continue...")
		elif act == "4":
			save(player)
			time.sleep(1)
		
		elif act == "C":
			clear_screen()
		elif act == "Q":
			confirm = input("""Are you sure you want to quit? Press (1) to confirm.
[Remember that you can save your game before quiting, if you didn't already!]
??> """)
			time.sleep(1)
			if confirm == "1":
				sys.exit()
			else:
				continue
		else:
			continue