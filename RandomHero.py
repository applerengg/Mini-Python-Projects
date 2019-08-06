
from random import choice, randint
import time 
from threading import Thread

import os 
from termcolor import cprint, colored
# ex: cprint("alperen","magenta", attrs=["bold","underline"])

from string import printable

os.system("color")		# colored output can be used now

###
### Configuration
###
class Config():
	def __init__(self):
		self.ATTR_POINTS_HILVL = 6		# attribute points gained at levelup after level 5
		self.ATTR_POINTS_INITIAL = 8	# attribute points given in the beginning
		self.ATTR_POINTS_LOWLVL = 3		# attribute points gained at levelup before level 5
		self.BRAVERY_CRITDMG = 0.1		# bravery increase rate of critmultiplier
		self.BRAVERY_FLEEDELAY = 3
		self.DEFENSE_ABSORB = 7/8
		self.DEFENSE_HP = 0.1
		self.ENEMY_INITIAL_DMG = 3
		self.ENEMY_INITIAL_HP = 1
		self.ENEMY_INITIAL_DEF = 1
		self.ENEMY_INITIAL_SPD = 1
		self.ENEMY_INITIAL_LCK = 1
		self.ENEMY_INITIAL_RGN = 1
		self.ENEMY_MAX_LEVEL = 2
		self.INCORRECT_STAT_ENTRY_HI = printable.translate({ord(i): None for i in "1234567"})
		self.INCORRECT_STAT_ENTRY_LO = printable.translate({ord(i): None for i in "123"})
		self.QUICK_TURN = 20
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




###
### Hero Class
###

###		attributes:
#	damage		-> amount of harm applied to enemy
#	hp			-> maximum amount of damage player can withstand
#	defense		-> decrase damage taken 
#	speed		-> increase turn frequency and dodge rate
#	bravery		-> (?) delay enemy flee and increase critmultiplier
#	luck 		-> increase crit chance and enemy loot
#	regeneration-> hp increase rate
#	
#	xp			-> required to level up
#	level 		-> player level
#
#	weapon 		-> affects min and max damage
#
class RandomHero():
	def __init__(self, name, damage, hp, defense, speed=1, bravery=0, luck=5, regeneration=0, xp=0, level=1, weapon=None, critmultiplier=1.2, color="green", money=0):
		self.all_attr = dict()
		self.name = name
		self.damage = damage
		self.defense = defense
		self.hp = hp 							 # this one is max hp
		self.curr_hp = self.hp*10 + self.defense # this one will be used in fights
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
		self.all_attr["xp"] = self.xp
		self.all_attr["level"] = self.level
		self.all_attr["weapon"] = str(self.weapon)
		self.all_attr["critmultiplier"] = self.critmultiplier
		return self.all_attr

	def updateAttrs(self, damage=0, hp=0, defense=0, speed=0, bravery=0, luck=0, regeneration=0):
		self.damage += damage
		self.hp += hp
		self.defense += defense
		self.speed += speed
		self.bravery += bravery
		self.luck += luck
		self.regeneration += regeneration

		self.curr_hp = self.hp*10 + self.defense
		self.mindmg += damage
		self.maxdmg += damage
		self.critmultiplier += (damage/20) + bravery*cfg.BRAVERY_CRITDMG

	def checkStats(self):
		for k, v in sorted(self.updateAttrdict().items()):
			print("{: <16}: {}".format(k,v))	

	def levelUp(self):
		new_attr_points = 0
		level_earned = self.xp // cfg.XP_TO_NEXTLEVEL
		self.xp -= cfg.XP_TO_NEXTLEVEL * level_earned
		for i in range(1, level_earned+1):
			if self.level + i >= 5:
				new_attr_points += cfg.ATTR_POINTS_HILVL
			else:
				new_attr_points += cfg.ATTR_POINTS_LOWLVL
			
		self.level += level_earned

		levelup_message = """
(1) Damage
(2) HP
(3) Defense{}
You have {} attribute points. Enter {} numbers:
[Be careful! If more than {} numbers entered, the first {} will be applied.]
??> """.format(
		"" if self.level<5 else "\n(4) Speed\n(5) Bravery\n(6) Luck\n(7) Regeneration",
		new_attr_points, new_attr_points, new_attr_points, new_attr_points
	)
	
		new_stats = input(levelup_message)

		if self.level < 5:
			while any(i in cfg.INCORRECT_STAT_ENTRY_LO for i in new_stats):
				new_stats = input("Incorrect entry, try again\n??> ")
		
			new_stats = new_stats.replace(" ","").replace("\t","")[:new_attr_points]
			
			dmg = new_stats.count("1")
			hp = new_stats.count("2")
			defns = new_stats.count("3")
			self.updateAttrs(dmg, hp, defns)
		
		else:
			while any(i in cfg.INCORRECT_STAT_ENTRY_HI for i in new_stats):
				new_stats = input("Incorrect entry, try again\n??> ")
			
			new_stats = new_stats.replace(" ","").replace("\t","")[:new_attr_points]

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
		return "{}: {} - {} damage, {} speed".format(self.name, self.mindmg, self.maxdmg, self.speed)

###
### Enemy Class
###
# monavar
class Enemy():
	def __init__(self, level, name=None, behaviour=None, boss=None):
		self.level = level+cfg.ENEMY_MAX_LEVEL if boss else randint(level-2, level+cfg.ENEMY_MAX_LEVEL)
		self.color = "red"
		
		# xp will be increased if enemy is boss
		self.xp = 1
		if self.level > level:		# enemy is stronger
			self.xp += cfg.XP_TO_NEXTLEVEL * 3 // 20
		elif self.level < level:	# enemy is weaker
			self.xp += cfg.XP_TO_NEXTLEVEL * 1 // 20
		else:						# enemy is same level
			self.xp += cfg.XP_TO_NEXTLEVEL * 2 // 20
		self.xp += randint(-cfg.XP_TO_NEXTLEVEL//30, cfg.XP_TO_NEXTLEVEL//30)	

		names = ["Monavar"]	# add more
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
			attr_points = cfg.ATTR_POINTS_INITIAL + (self.level-1) * cfg.ATTR_POINTS_LOWLVL
		else:
			attr_points = cfg.ATTR_POINTS_INITIAL + 3*cfg.ATTR_POINTS_LOWLVL + (self.level-4)*cfg.ATTR_POINTS_HILVL	
		if self.is_boss == "miniboss":
			attr_points += cfg.ATTR_POINTS_LOWLVL * 2 
			self.color = "cyan"
			self.xp += cfg.XP_TO_NEXTLEVEL // 3
		if self.is_boss == "boss":
			attr_points += cfg.ATTR_POINTS_HILVL * 2
			self.color = "magenta"
			self.xp += cfg.XP_TO_NEXTLEVEL // 5
		print("ATTRPOINTS",attr_points)

		self.loot = 1
		self.loot += randint(self.xp//4, self.xp*2)

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
		self.curr_hp = self.hp*10 + self.defense	
		self.critmultiplier = randint(12,15)/10 + self.dmg/20 
		self.all_attr = dict()
		print("behaviour:",self.behaviour,"dmg:",self.dmg,"hp:",self.hp,"def:",self.defense)
	
	def __str__(self):
		return str(sorted(self.updateAttrdict().items()))

	def updateAttrdict(self):
		self.all_attr["name"] = self.name
		self.all_attr["behaviour"] = self.behaviour
		self.all_attr["mindmg"] = self.mindmg
		self.all_attr["maxdmg"] = self.maxdmg
		self.all_attr["hp"] = self.hp
		self.all_attr["defense"] = self.defense
		self.all_attr["speed"] = self.speed
		self.all_attr["luck"] = self.luck
		self.all_attr["regeneration"] = self.regeneration
		self.all_attr["level"] = self.level
		self.all_attr["critmultiplier"] = self.critmultiplier
		return self.all_attr

	def checkStats(self):
		for k, v in sorted(self.updateAttrdict().items()):
			print("{: <16}: {}".format(k,v))


###
### Gameplay functions
###
def createNewHero():
	playername = input("hero name: ")
	initial_stats = input("""
(1) Damage
(2) HP
(3) Defense
You have 10 attribute points. Enter 10 numbers:
[Be careful! If more than 10 numbers entered, the first 10 will be applied.]
??> """)
	initial_stats = initial_stats.replace(" ","").replace("\t","")[:10]
	
	dmg = initial_stats.count("1")
	hp = initial_stats.count("2")
	defns = initial_stats.count("3")

	player = RandomHero(playername, dmg,hp,defns)
	return player



def attack(protagonist, opponent):
	# return None if fight is not over yet (neither player nor the enemy is defeated), else return the winner
	protagonist.curr_hp += protagonist.regeneration
	if protagonist.curr_hp > protagonist.hp*10:
		protagonist.curr_hp = protagonist.hp*10

	dodge_rate = opponent.speed - protagonist.speed//2
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
	crit = choice([1]*protagonist.luck + [0]*(100-protagonist.luck))
	dmg = 1 if (dmg-opponent.defense*cfg.DEFENSE_ABSORB)<1 else dmg-opponent.defense*cfg.DEFENSE_ABSORB
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
	hturn = 0
	eturn = 0
	winner = None
	turn = 0
	while True:
		turn += 1
		print("xx> Turn {}".format(turn))
		time.sleep(1)
		hturn += hero.speed
		eturn += enemy.speed
		if hturn == cfg.QUICK_TURN:
			print("::> Quick Turn for {}!".format(hero.name))
			winner = attack(hero, enemy)
			if winner:
				break
			hturn -= cfg.QUICK_TURN
		if eturn == cfg.QUICK_TURN and not hturn == cfg.QUICK_TURN:
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

		print("{:-<32}".format(""))
		time.sleep(1)

	time.sleep(3)
	# restore HPs
	hero.curr_hp = hero.hp*10
	enemy.curr_hp = enemy.hp*10

	if winner == hero:
		cprint("==> {} has won!".format(
			colored(hero.name, hero.color) ),
			attrs=["bold"],
			end="\n\n"
		)
		if turn <= cfg.TURNLIMIT_XPLOW:
			hero.xp += enemy.xp // 4
		elif turn <= cfg.TURNLIMIT_XPHI:
			hero.xp += enemy.xp // 2
		else:
			hero.xp += enemy.xp	

		loot_multiplier = [2]*(hero.luck//2) + [1.5]*(hero.luck//2) + [1.25]*hero.luck + [1]*(100-(2*(hero.luck//2)+hero.luck))
		hero.money += enemy.loot * choice(loot_multiplier)
		
		if hero.xp >= cfg.XP_TO_NEXTLEVEL:
			hero.levelUp()
			

	elif winner == enemy:
		cprint("==> {} has won!".format(
			colored(enemy.name, enemy.color) ),
			attrs=["bold"],
			end="\n\n"
		)
	else:			# enemy has fled
		cprint("==> {} has fled!".format(
			colored(enemy.name, enemy.color) ),
			attrs=["bold"],
			end="\n\n"
		)


def pprint(entity):
	# Print all attributes of an entity
	for k,v in sorted(entity.__dict__.items()):
		print("{: <16}: {}".format(k,v))

if __name__ == '__main__':
	#player = createNewHero()
	#print(player)
	p1 = RandomHero("Ofansif", 15,8,3, color="red")
	p2 = RandomHero("Dengeli", 9,9,8, color="yellow")
	p3 = RandomHero("Defansif", 4,7,15, color="green")
	p4 = RandomHero("Aşırı Ofansif", 23,3,0, color="red")
	p5 = RandomHero("Aşırı Defansif", 1,5,20, color="green")

	e5 = Enemy(5,behaviour="offensive")
	e6 = Enemy(6,behaviour="defensive")
	e7 = Enemy(7,behaviour="balanced")
	e8 = Enemy(8)
	e9 = Enemy(9)
