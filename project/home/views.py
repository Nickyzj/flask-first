from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user

from project import db
from project.models import BlogPost

from .forms import MessageForm


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

@home_blueprint.route('/', methods = ['GET', 'POST'])
def home():
	error = None
	form = MessageForm(request.form)
	if form.validate_on_submit():
		new_message = BlogPost(
				form.title.data,
				form.description.data
			)
		db.session.add(new_message)
		db.session.commit()
		flash('New entry was successfully posted.')
		return redirect(url_for('home.home'))
	posts = db.session.query(BlogPost).all()
	return render_template('index.html', posts = posts, form = form, error = error)

@home_blueprint.route('/welcome')
def welcome():
	return render_template('welcome.html')

