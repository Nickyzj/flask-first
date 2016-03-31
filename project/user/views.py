from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_user, login_required, logout_user

from .forms import LoginForm, RegisterForm
from project import db
from project.models import User, bcrypt

user_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

@user_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			if request.form['username'] == 'admin' and request.form['password'] == 'password':
				return redirect(url_for('home.home'))
		else:
			error = 'Invalid username or password.'
	return render_template('login.html', form = form, error = error)

@user_blueprint.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if form.validate_on_submit():
		user = User(
				name = form.username.data,
				email = form.email.data,
				password = form.password.data
			)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('home.home'))
	return render_template('register.html', form = form)