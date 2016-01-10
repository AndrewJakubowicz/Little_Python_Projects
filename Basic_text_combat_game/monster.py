# functions that belong to a class are called METHODS
# class Monster(object):
	# # double underscore is called "dunder"
	# def __init__(self, hit_points=5, weapon="sword", color="yellow", sound="ropa"):
	# 	self.hit_points = hit_points
	# 	self.weapon = weapon
	# 	self.color = color
	# 	self.sound = sound
	# def __init__(self, **kwargs):
		# Tries to find the arguments and then sets defaults.\
		# initialize Monster like so:
		# bird = Monster(weapon = "axe", sound = "burp")
	# 	self.hit_points = kwargs.get('hit_points', 1)
	# 	self.weapon = kwargs.get('weapon', 'sword')
	# 	self.color = kwargs.get('color', 'yellow')
	# 	self.sound = kwargs.get('sound', 'tweet')
	

	# def battlecry(self):
	# 	return self.sound.upper()

from combat import Combat
import random

COLORS = ['yellow', 'red', 'blue', 'green', 'black', 'brown', 'purple', 'pink']


class Monster(Combat):
	min_hit_points = 1
	max_hit_points = 1
	min_experience = 1
	max_experience = 1
	base_damage = 1
	weapon = 'sword'
	sound = 'roar'

	def __init__(self, **kwargs):
		self.hit_points = random.randint(self.min_hit_points, self.max_hit_points)
		self.experience = random.randint(self.min_experience, self.max_experience)
		self.color = random.choice(COLORS)
		self.damage = self.base_damage

		for key, value in kwargs.items():
			print("THINGS HAPPENED")
			setattr(self, key, value)
			print("self.key = ", key, "value is", value)

	def __str__(self):
		return '{} {}, HP: {}, XP: {}'.format(self.color.title(), 
											self.__class__.__name__, 
											self.hit_points, 
											self.experience)

	def battlecry(self):
		return random.choice(self.sound).upper()



class Goblin(Monster):
	max_hit_points = 3
	max_experience = 2
	sound = [
			'squeak',
			'garble',
			'you are a fool',
			"i'll be back",
			'hrnff',
			'oh noes',
			'fool'
			]

class Troll(Monster):
	base_damage = 2
	attack_limit = 7
	min_hit_points = 3
	max_hit_points = 6
	min_experience = 2
	max_experience = 6
	sound = [
			'there will be blood',
			'grrrrrrr',
			'yawn, my mate will get you',
			'glehhhh',
			"you don't know what lies ahead traveller",
			'hfllllrpd',
			'blerghhhh'
			]

class Dragon(Monster):
	attack_limit = 10
	base_damage = 4
	min_hit_points = 25
	max_hit_points = 40
	min_experience = 30
	max_experience = 40
	sound = 'raaaaaaaaaaaaaaaaaaaaaar'