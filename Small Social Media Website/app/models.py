import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=False)

	class Meta:
		database = DATABASE
		# We can't order it like so, order_by = ('joined_at', 'desc')
		# because each member of the order_by tuple is the name of a
		# field. We would be saying, order the joined_at field by the
		# desc field which doesn't exist.
		# Because order_by is a tuple, a trailing comma must be left.
		order_by = ('-joined_at',)
	# Without you need to create a user instance to create a user instance
	# with classmethod. You can create the user model instance when it runs
	# this method and then use it. Calls user.create_user(). Then it refers
	# back to the function itself.

	def get_posts(self):
		return Post.select().where(Post.user == self)

	def get_stream(self):
		return Post.select().where(
				(Post.user == self)
				)

	@classmethod
	def create_user(cls, username, email, password, admin=False):
		try:
			cls.create(
					username=username,
					email=email,
					password=generate_password_hash(password),
					is_admin=admin)
		except IntegrityError:
			raise ValueError("User already exists")

class Post(Model):
	timestamp = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(
			rel_model=User,
			related_name='posts' # What would a user call this. Posts.
			)
	content = TextField()

	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	DATABASE.close()