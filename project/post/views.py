from flask import Blueprint, render_template, flash, session

from project import db
from project.models import BlogPost, User

post_blueprint = Blueprint(
	'posts', __name__,
	template_folder='templates'
)

@post_blueprint.route('/')
@post_blueprint.route('/<int:user_id>')
def post_list(user_id = None):
	if user_id is not None:
		post_users = db.session.query(BlogPost, User).\
			filter(BlogPost.author_id == User.id).\
			filter(BlogPost.author_id == user_id)
		flash("user_id = {}".format(user_id))
	else:
		post_users = db.session.query(BlogPost, User).filter(BlogPost.author_id == User.id).all()
		flash('All posts are displayed.')
	return render_template('posts.html', post_users = post_users)
