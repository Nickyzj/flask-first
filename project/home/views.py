from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user

from project import db
from project.models import BlogPost, User

from .forms import MessageForm


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

@home_blueprint.route('/index', methods = ['GET', 'POST'])
@login_required
def home():
	error = None
	form = MessageForm(request.form)
	if form.validate_on_submit():
		new_message = BlogPost(
				form.title.data,
				form.description.data,
				current_user.id
			)
		db.session.add(new_message)
		db.session.commit()
		flash('New entry was successfully posted.')
		return redirect(url_for('home.home'))
	posts = db.session.query(BlogPost).all()
	return render_template('index.html', posts = posts, form = form, error = error)

@home_blueprint.route('/')
def welcome():
	print type(current_user)
	if current_user.is_authenticated:
		return redirect(url_for('home.home'))
	return render_template('welcome.html')

