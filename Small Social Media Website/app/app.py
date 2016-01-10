from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
							login_required, current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '192.168.0.207'

app = Flask(__name__)
app.secret_key = 'vn438v7btc238n074nxx3mf983q4&^@NNCJGMRgchmc38470'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # if they are not logged in redirect to login view

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE
	g.db.connect()
	g.user = current_user


@app.after_request
def after_request(response):
	"""Close the database connection after each request."""
	g.db.close()
	return response


@app.route('/register', methods=('GET', 'POST'))
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash("Yay, you registered!", "success")  # method category 'success'
		models.User.create_user(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data
		)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/login', methods=("GET", "POST"))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("Your email or password doesn't match!", "error")
		else:
			if check_password_hash(user.password, form.password.data):
				login_user(user) #Creating a session on the users browser
									# Using a cookie.
									# Can store sessions in the database.
				flash("You've been logged in!", "success")
				return redirect(url_for('index'))
			else:
				flash("Your email or password doesn't match!", "error")
	return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user() # Deletes the cookie created by login_user.
	flash("You've been logged out!", 'success')
	return redirect(url_for('index'))


#might look at using ajax here to have this view load into a part
# of the frame
@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
	form = forms.PostForm()
	if form.validate_on_submit():
		models.Post.create(user=g.user._get_current_object(),
							content=form.content.data.strip())

		flash("Message posted! Thanks!", 'success')
		return redirect(url_for('index'))
	return render_template('post.html', form=form)


@app.route('/')
def index():
	return 'All!'

if __name__ == '__main__':
	models.initialize()
	try:
		models.User.create_user(
				username='andrew1',
				email='spyr1014@gmail.com',
				password='password',
				admin=True
		)
	except ValueError:
		pass
	app.run(debug=DEBUG, host=HOST, port=PORT)