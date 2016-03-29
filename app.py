from flask import Flask

app = Flask(__name__)

from project.home.views import home_blueprint

app.register_blueprint(home_blueprint, url_prefix = '/blue')

@app.route('/')
def home():
	return "Hello!"

if __name__ == '__main__':
    app.run(host = '0.0.0.0')