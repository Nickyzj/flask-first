from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)

app.debug = True
app.secret_key = 'my precious'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\codes\\python\\flask\sandbox\\flask-first\\posts.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from project.home.views import home_blueprint
from project.user.views import user_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(user_blueprint, url_prefix = '/user')

from models import User

login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter(User.id == int(user_id)).first()