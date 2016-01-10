import os
import sys

from character import Character
from monster import Dragon
from monster import Goblin
from monster import Troll

LINE = """####################

####################"""

def clear():
	"""Calls cls if on windows, or clear on mac or linux."""
	os.system('cls' if os.name == 'nt' else 'clear')

class Game(object):
	

	def setup(self):
		self.player = Character()
		self.monsters = [
		Goblin(), 
		Goblin(), 
		Goblin(), 
		Troll(), 
		Troll(),
		Goblin(), 
		Troll(),
		Troll(), 
		Dragon()
		]
		self.monster = self.get_next_monster()
		print("An angry {} {} steps forward!".format(self.monster.color.title(),
													self.monster.__class__.__name__))
	def get_next_monster(self):
		try:
			return self.monsters.pop(0)
		except IndexError:
			return None #no monster


	def monster_turn(self):
		if self.monster.attack():
			print("The {} {} prepares its attack!".format(self.monster.color.title(), 
														self.monster.__class__.__name__))
			if input("Dodge? Y/N \n>").lower() == 'y':
				print(LINE)
				if self.player.dodge():
					print("Success!!!")
					print("{} dodges the {}.".format(self.player.name, self.monster.__class__.__name__))
				else:
					self.player.hit_points -= self.monster.damage
					print("Dodge fails.")
					print("{} gets hit for {} health".format(self.player.name, self.monster.damage))
			elif input("Counter-attack? Y/N\n> ").lower() == 'y':
				print(LINE)
				if self.player.counter_attack():
					self.monster.hit_points -= (self.player.lvl*2)
					print("{} pulls of a mighty counter-attack on the {} {} dealing {} damage!".format(
														self.player.name,
														self.monster.color.title(),
														self.monster.__class__.__name__,
														(self.player.lvl*2)
														))
				else:
					self.player.hit_points -= (self.monster.damage*2)
					print("Counter attack fails and you get hit for double!")
					print("{} lose {} hp.".format(self.player.name, (self.monster.damage*2)))
			else:
				self.player.hit_points -= self.monster.damage
				print("You get hit for {} health where you stand!".format(self.monster.damage))
		else:
			print("{} isn't attacking this turn.".format(self.monster.__class__.__name__))


	def player_turn(self):
		# let player attack, rest, quit
		options = ['attack', 'rest', 'quit', "a", "r", "q"]
		user = input("[A]ttack, [R]est, [Q]uit? ").lower()
		clear()
		if user in options:
			print(LINE)
			if user == "attack" or user == "a":
				if self.player.attack():
					if self.monster.dodge():
						print("{} {} dodges your {} attack.".format(self.monster.color.title(), 
																	self.monster.__class__.__name__, 
																	self.player.weapon))
						return
					else:
						self.monster.hit_points -= self.player.lvl
						print("You hit the {} {} for {} dmg.".format(self.monster.color.title(),
																	self.monster.__class__.__name__,
																	self.player.lvl
																	))
				else:
					print("You clumsily miss with your {}.".format(self.player.weapon))
			elif user == "rest" or user == "r":
				print("You take a moment to recover 1 hp.")
				self.player.rest()
			elif user == "quit" or user == "q":
				print("Hope to play again sometime {}!".format(self.player.name))
				sys.exit()
		else:
			print(LINE)
			print("Type 'attack' or 'rest' or 'quit' or the first letter please.")
			self.player_turn()


	def cleanup(self):
		if self.monster.hit_points <= 0:
			print("The {} {} gives one last cry: {}!!!!".format(self.monster.color.title(), 
																self.monster.__class__.__name__, 
																self.monster.battlecry()))
			print("{} {} dies!".format(self.monster.color.title(), self.monster.__class__.__name__))
			self.player.experience += self.monster.experience
			print("Gained {} experience! You have {} total experience.".format(self.monster.experience, self.player.experience))
			while self.player.level_up():
				self.player.lvl += 1
			self.monster = self.get_next_monster()
			if self.monster:
				print("{} monsters remain!".format((len(self.monsters)+1)))
				print("An angry {} {} steps forward!".format(self.monster.color.title(), 
															self.monster.__class__.__name__))
			else:
				print("The monsters stop coming.")
				return
		else:
			print("The {} {} has {} hp remaining.".format(self.monster.color.title(), 
														self.monster.__class__.__name__, 
														self.monster.hit_points))
	

	def __init__(self):
		clear()
		self.setup()
		clear()
		print("{} monsters prepare to battle you!".format(len(self.monsters)))
		while (self.player.hit_points > 0) and (self.monster or self.monsters):
			print(self.player)
			self.monster_turn()
			if self.monster.hit_points > 0 or self.player.hit_points <= 0:
				self.player_turn()
			self.cleanup()
			

		if self.player.hit_points > 0:
			print("You win!")
		elif self.monsters or self.monster:
			print("You were killed by the {} {}. R.I.P {}".format(
												self.monster.color.title(),
												self.monster.__class__.__name__,
												self.player.name
												))
		else:
			print("You drew!")
		
		exit_input = input("Thank you for playing!\n Press enter to quit!")
		clear()
		sys.exit()

