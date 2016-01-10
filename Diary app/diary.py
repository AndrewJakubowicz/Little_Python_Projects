from collections import OrderedDict
import datetime
import os #for clearing screen

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
	content = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now) # leave off parenthisis off now() otherwise they'll all overwrite

	class Meta:
		database = db


def initialize():
	"""Create the database and the table if they don't exist."""
	db.connect()
	db.create_tables([Entry], safe=True)


def clear():
	"""Calls cls if on windows, or clear on mac or linux."""
	os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
	"""Show the menu."""
	choice = None

	while choice != 'q':
		clear()
		print("Enter 'q' to quit.")
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__))
		choice = input("Action: ").lower().strip()

		if choice in menu:
			clear()
			menu[choice]()


def add_entry():
	"""Add an entry."""
	print("Enter your entry. Type 'stop' on a new line and hit enter when finished.")
	sentinel = 'stop' #code ends when it reads this
	data = '\n'.join(iter(input, sentinel))

	if data:
		if input('\nSave entry? [Y/N] ').lower() != 'n':
			Entry.create(content=data)
			print("Saved successfully!")


def view_entries(search_query=None):
	"""View previous entries."""
	entries = Entry.select().order_by(Entry.timestamp.desc())
	# Only changes the entries if there is a search_query
	if search_query:
		entries = entries.where(Entry.content.contains(search_query)) # where does filtering

	for entry in entries:
		timestamp = entry.timestamp.strftime('%A %B %d, %Y, %I:%M%p')
		clear()
		print(timestamp)
		print('='*len(timestamp))
		print(entry.content)
		print('\n\n'+'='*len(timestamp))
		print('n) next entry')
		print('d) delete entry')
		print('q) return to main menu')

		next_action = input('Action: [Ndq] ').lower().strip()
		if next_action == 'q':
			break
		elif next_action == 'd':
			delete_entry(entry)
			print("Entry deleted.")
	print("No more entries remain.......")


def search_entries():
	"""Search entries for a string."""
	view_entries(input('Search query: '))

def delete_entry(entry):
	"""Delete and entry."""
	if input("Are you sure? [yN] ").lower() == 'y':
		entry.delete_instance()


menu = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('s', search_entries)
])


if __name__ == '__main__':
	initialize()
	menu_loop()