import random

from combat import Combat

class Character(Combat):
	attack_limit = 8
	dodge_limit = 8
	experience = 0
	base_hit_points = 10
	base_lvl = 1

	def attack(self):
		roll = random.randint(1, self.attack_limit)
		if self.weapon == 'sword':
			roll += 1
		elif self.weapon == 'axe':
			roll += 2
		return roll > 4

	def dodge(self):
		roll = random.randint(1, self.dodge_limit)
		if self.weapon == 'bow':
			roll += 2
		roll += (self.lvl - 1)

		return roll > 4

	def get_weapon(self):
		weapon_choice = input("Choose weapon: ([S]word, [A]xe, [B]ow): ").lower()

		if weapon_choice in 'sab':
			if weapon_choice == 's':
				return 'sword'
			if weapon_choice == 'a':
				return 'axe'
			if weapon_choice == 'b':
				return 'bow'
		else:
			return self.get_weapon()


	def __init__(self, **kwargs):
		self.name = input("Name: ")
		self.weapon = self.get_weapon()
		self.hit_points = self.base_hit_points
		self.lvl = self.base_lvl

		for key, value in kwargs.items():
			setattr(self, key, value)

	def __str__(self):
		return "{}, HP: {}, XP: {}, LVL: {}".format(self.name, self.hit_points, self.experience, 
													self.lvl)

	def rest(self):
		if self.hit_points < self.base_hit_points:
			self.hit_points += 1

	def level_up(self):
		if self.experience >= ((self.lvl*2) + 3):
			self.experience -= ((self.lvl*2) + 3)
			print("YOU LEVELED UP. You feel stronger and more nimble!")
			print("Next level in {} experience.".format((((self.lvl+1)*2) + 3)))
			if self.weapon == 'sword':
				if self.attack_limit > 6:
					self.attack_limit += 1
				if self.dodge_limit > 6:
					self.dodge_limit += 1
			elif self.weapon == 'axe':
				if self.attack_limit > 6:
					self.attack_limit += 1
			elif self.weapon == 'bow':
				if self.dodge_limit > 6:
					self.dodge_limit += 1
			else:
				print("YOU MESSED UP THE CODE")
			return True
		return False