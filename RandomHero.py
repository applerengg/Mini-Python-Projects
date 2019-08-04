
from random import choice, randint
import time 

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
		self.DEFENSE_ABSORB = 7/8
		self.DEFENSE_HP = 0.1
		self.INCORRECT_STAT_ENTRY_HI = printable.translate({ord(i): None for i in "1234567"})
		self.INCORRECT_STAT_ENTRY_LO = printable.translate({ord(i): None for i in "123"})
		self.QUICK_TURN = 20
		self.XP_TO_NEXTLEVEL = 100

cfg = Config()

###
### Hero Class
###

###		attributes:
#	damage		-> amount of harm applied to enemy
#	hp			-> maximum amount of damage player can withstand
#	defense		-> decrase damage taken 
#	speed		-> increase turn frequency and dodge rate
#	bravery		-> (?) delay enemy flee
#	luck 		-> increase crit chance and enemy loot
#	regeneration-> hp increase rate
#	
#	xp			-> required to level up
#	level 		-> player level
#
#	weapon 		-> affects min and max damage
#
class RandomHero():
	def __init__(self, name, damage, hp, defense, speed=1, bravery=0, luck=5, regeneration=0, xp=0, level=1, weapon=None, critmultiplier=1.2, color="green"):
		self.all_attr = dict()
		self.name = name
		self.damage = damage
		self.defense = defense
		self.hp = hp + defense/10	# this one is max hp
		self.curr_hp = self.hp*10 	# this one will be used in fights
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
		self.critmultiplier = critmultiplier + self.damage/20
		self.updateAttrdict()
		self.color = color

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
		self.hp += (hp + defense/10)
		self.defense += defense
		self.speed += speed
		self.bravery += bravery
		self.luck += luck
		self.regeneration += regeneration

		self.curr_hp = self.hp * 10
		self.mindmg += damage
		self.maxdmg += damage
		self.critmultiplier += damage/20

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
		new_stats = new_stats.replace(" ","").replace("\t","")[:10]

		if self.level < 5:
			while any(i in cfg.INCORRECT_STAT_ENTRY_LO for i in new_stats):
				new_stats = input("??> ")
		
			dmg = new_stats.count("1")
			hp = new_stats.count("2")
			defns = new_stats.count("3")
			self.updateAttrs(dmg, hp, defns)
		else:
			while any(i in cfg.INCORRECT_STAT_ENTRY_HI for i in new_stats):
				new_stats = input("??> ")
		
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
class Enemy():
	def __init__(self, level, behaviour=None, boss=None):
		self.level = randint(level-1, level+1)

		behaviours = ["offensive", "defensive", "balanced", None]
		self.behaviour = behaviour if behaviour is not None else choice(behaviours)
		
		boss_options_hilvl = ["boss"]*5 + ["miniboss"]*10 + [None]*85
		boss_options_lowlvl = ["miniboss"]*10 + [None]*90
		if self.level > level:
			self.is_boss = boss if boss is not None else choice(boss_options_hilvl)
		elif self.level >= level:
			self.is_boss = boss if boss is not None else choice(boss_options_lowlvl)

		attr_points = 0
		if level < 5:
			attr_points = cfg.ATTR_POINTS_INITIAL + (level-1) * cfg.ATTR_POINTS_LOWLVL
		else:
			attr_points = cfg.ATTR_POINTS_INITIAL + 3*cfg.ATTR_POINTS_HILVL + (level-4)*cfg.ATTR_POINTS_HILVL	
		if self.is_boss == "miniboss":
			attr_points += cfg.ATTR_POINTS_LOWLVL
			self.color = "cyan"
		if self.is_boss == "boss":
			attr_points += cfg.ATTR_POINTS_HILVL
			self.color = "magenta"

		if behaviour == "offensive":
			self.dmg = randint(attr_points*3//8, attr_points*6//8)
			self.mindmg = randint(0, self.dmg)
			self.maxdmg = 2*self.dmg - self.mindmg
			attr_points -= self.dmg
			self.defense = attr_points // 3
			self.hp = (attr_points//3) + (self.defense/10)
			self.curr_hp = self.hp*10
			attr_points -= self.defense * 2
			self.speed = attr_points // 3
			self.luck = attr_points // 3
			self.regeneration = attr_points // 3
			attr_points -= 3 * (attr_points//3)
			self.speed += attr_points	# spend last points
		if behaviour == "defensive":
			self.defense = randint(attr_points*3//8, attr_points*5//8)
			attr_points -= self.defense
			self.hp = (attr_points//2) + (self.defense/10)
			self.curr_hp = self.hp*10
			attr_points -= attr_points//2
			self.dmg = attr_points // 2
			self.mindmg = randint(self.dmg//2, self.dmg)
			self.maxdmg = 2*self.dmg - self.mindmg
			attr_points -= self.dmg
			self.speed = attr_points // 3
			self.luck = attr_points // 3
			self.regeneration = attr_points // 3
			attr_points -= 3 * (attr_points//3)
			self.speed += attr_points	# spend last points
		if behaviour == "balanced":
			self.defense = attr_points // 5
			self.hp = (attr_points//5) + (defense/10)
			self.curr_hp = self.hp*10
			self.dmg = attr_points // 5
			self.mindmg = randint(0, self.dmg)
			self.maxdmg = 2*self.dmg - self.mindmg 
			attr_points -= 3 * (attr_points//5)
			self.speed = attr_points // 3
			self.luck = attr_points // 3
			self.regeneration = attr_points // 3
			attr_points -= 3 * (attr_points//3)
			self.speed += attr_points	# spend last points
		else:
			self.defense = randint(0, attr_points)
			attr_points -= self.defense
			self.hp = randint(0, attr_points)
			attr_points -= self.hp
			self.hp += self.defense/10
			self.curr_hp = self.hp*10
			self.dmg = randint(0, attr_points)
			self.mindmg = randint(0, self.dmg)
			self.maxdmg = 2*self.dmg - self.mindmg
			attr_points -= self.dmg
			self.speed = randint(0, self.dmg)
			attr_points -= self.speed
			self.luck -= randint(0, self.dmg)
			attr_points -= self.luck
			self.regeneration = randint(0, self.dmg)
			attr_points -= self.regeneration
			self.speed += attr_points	# spend last points
		self.critmultiplier = randint(10,15)/10 + self.dmg/20
		se
			

	def __str__(self):
		return str(sorted(self.updateAttrdict().items()))

	def updateAttrdict(self):
		self.all_attr["name"] = self.name
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

	dodge_rate = opponent.speed - protagonist.speed/2
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
		hero.xp += enemy.xp
		if hero.xp >= cfg.XP_TO_NEXTLEVEL:
			hero.levelUp()
			

	elif winner == enemy:
		cprint("==> {} has won!".format(
			colored(enemy.name, enemy.color) ),
			attrs=["bold"],
			end="\n\n"
		)
	else:
		print("Nobody has won, DEBUG DEBUG DEBUG")


def pprint(entity):
	for k,v in sorted(entity.updateAttrdict().items()):
		print("{: <16}: {}".format(k,v))

if __name__ == '__main__':
	#player = createNewHero()
	#print(player)
	p1 = RandomHero("Ofansif", 15,8,3, color="red")
	p2 = RandomHero("Dengeli", 9,9,8, color="yellow")
	p3 = RandomHero("Defansif", 4,7,15, color="green")
	p4 = RandomHero("Aşırı Ofansif", 23,3,0, color="red")
	p5 = RandomHero("Aşırı Defansif", 1,5,20, color="green")

