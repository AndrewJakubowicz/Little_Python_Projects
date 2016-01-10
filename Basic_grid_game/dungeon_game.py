import logging
import random
import time

logging.basicConfig(filename="game.log", level=logging.DEBUG)


CELLS = [(0, 0), (1, 0), (2, 0), 
		(0, 1), (1, 1), (2, 1), 
		(0, 2), (1, 2), (2, 2)]

mini_map = {"(0, 0)": "x", "(1, 0)": "x", "(2, 0)": "x", 
			"(0, 1)": "x", "(1, 1)": "x", "(2, 1)": "x", 
			"(0, 2)": "x", "(1, 2)": "x", "(2, 2)": "x"}

def print_line(s):
	"""Stupid print function that writes each word one at a time. Requires import of time."""
	wait_time = 0.2
	string_list = s.split()
	for word in string_list:
		print word,
		time.sleep(wait_time)
		if wait_time > 0.1:
			wait_time = wait_time * 0.8
	print "\n"

def instruction():
	"""Prints instructions onto the screen."""
	print_line("Type QUIT to exit")
	print_line("Type your move like this: LEFT")
	print_line("You are the P on the map")
	print_line("Win by finding the exit door!")
	print "\n"
	print_line("Turn on cheats with CHEAT")
	print_line("M = monster")
	print_line("D = exit door")

def get_location():
	"""Randomly assigns the game cells."""
	monster = random.choice(CELLS)
	door = random.choice(CELLS)
	player  = random.choice(CELLS)
	if monster == door or door == player or player == monster:
		return get_location()
	return monster, door, player

def move_player(player, move):
	"""Moves the player tuple by the move. Returns new player positions."""
	x, y = player
	if move == "LEFT":
		x -= 1
	elif move == "RIGHT":
		x += 1
	elif move == "UP":
		y -= 1
	elif move == "DOWN":
		y += 1
	return x, y

def get_moves(player):
	"""Looks at the player position and returns valid moves"""
	moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
	if player[1] == 0:
		moves.remove('UP')
	if player[0] == 0:
		moves.remove('LEFT')
	if player[1] == 2:
		moves.remove('DOWN')
	if player[0] == 2:
		moves.remove('RIGHT')
	return moves

monster, door, player = get_location()
logging.info('monster: {}, door: {}, player: {}'.format(
														monster,
														door,
														player
														))
print_line("Welcome to the dungeon!")
print_line("Type HELP for instructions")
while True:
	moves = get_moves(player)
	mini_map[str(player)] = "P"
	print """Map\n{(0, 0)} {(1, 0)} {(2, 0)}
{(0, 1)} {(1, 1)} {(2, 1)}
{(0, 2)} {(1, 2)} {(2, 2)}
""".format(**mini_map)
	mini_map[str(player)] = "."

	print "You can move {}.".format(moves)

	move = raw_input("> ")
	move = move.upper()

	if move == 'QUIT':
		break
	if move == 'HELP':
		instruction()
		continue
	if move == 'CHEAT':
		mini_map[str(door)] = "D"
		mini_map[str(monster)] = "M"
		continue

	if move in moves:
		player = move_player(player, move)
	else:
		print "** Stop walking into walls **"
		continue

	if player == door:
		print "YOU WIN"
		break

	if player == monster:
		print "YOU LOSE"
		break
