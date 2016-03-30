mkvirtualenv flask-first

pip install flask

app.register_blueprint(home_blueprint, url_prefix = '/blue')
http://flask.pocoo.org/docs/0.10/blueprints/

http://discoverflask.com/

'''
By convention templates and static files are stored in subdirectories within the application’s Python source tree, with the names templates and static respectively.
'''

app.run(host='0.0.0.0')

two ways to enable debugging.

app.debug = True
app.run()

app.run(debug=True)

-------------------------

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

--------------------------

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

'''
The following converters exist:

int	    accepts integers
float	like int but for floating point values
path	like the default but also accepts slashes
'''
----------------------------

>>> from flask import Flask, url_for
>>> app = Flask(__name__)
>>> @app.route('/')
... def index(): pass
...
>>> @app.route('/login')
... def login(): pass
...
>>> @app.route('/user/<username>')
... def profile(username): pass
...
>>> with app.test_request_context():
...  print url_for('index')
...  print url_for('login')
...  print url_for('login', next='/')
...  print url_for('profile', username='John Doe')
...
/
/login
/login?next=/
/user/John%20Doe

----------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

------------------------------------

url_for('static', filename='style.css')

'''
The file has to be stored on the filesystem as static/style.css.
'''
-------------------------------------

from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

'''
Case 1: a module:

/application.py
/templates
    /hello.html

Case 2: a package:

/application
    /__init__.py
    /templates
        /hello.html
'''
---------------------------------------

Inside templates you also have access to the request, session and g [1] objects as well as the get_flashed_messages() function.

---------------------------------------

from flask import request

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

-----------------------------------------

searchword = request.args.get('key', '')

------------------------------------------
'''
You can handle uploaded files with Flask easily. Just make sure not to forget to set the enctype="multipart/form-data" attribute on your HTML form, otherwise the browser will not transmit your files at all.
'''
from flask import request

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
    ...


from flask import request
from werkzeug import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
    ...

---------------------------------------------

Reading cookies:

from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.


Storing cookies:

from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp

------------------------------------------------

from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

-------------------------------------------------

from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

--------------------------------------------------
'''
The logic that Flask applies to converting return values into response objects is as follows:

If a response object of the correct type is returned it’s directly returned from the view.
If it’s a string, a response object is created with that data and the default parameters.
If a tuple is returned the items in the tuple can provide extra information. Such tuples have to be in the form (response, status, headers) where at least one item has to be in the tuple. The status value will override the status code and headers can be a list or dictionary of additional header values.
If none of that works, Flask will assume the return value is a valid WSGI application and convert that into a response object.
'''
---------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

----------------------------------------------------
'''
In order to use sessions you have to set a secret key.
'''
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

How to generate good secret keys
>>> import os
>>> os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

-------------------------------------------------------

To flash a message use the flash() method, to get hold of the messages you can use get_flashed_messages() which is also available in the templates.

--------------------------------------------------------

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')

-------------------------------------------------

http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup

-------------------------------------------------

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
'''
That way someone can set an environment variable called FLASKR_SETTINGS to specify a config file to be loaded which will then override the default values. The silent switch just tells Flask to not complain if no such environment key is set.
'''
--------------------------------------------------

'''
Flask allows us to do that with the before_request(), after_request() and teardown_request() decorators:
'''
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

------------------------------------------------

'''
Be sure to use question marks when building SQL statements, as done in the example above. Otherwise, your app will be vulnerable to SQL injection when you use string formatting to build SQL statements.
'''
g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])

------------------------------------------------

session['logged_in'] = True
session.pop('logged_in', None)

------------------------------------------------

Templates 
http://flask.pocoo.org/docs/0.10/tutorial/templates/#tutorial-templates

---------------------------------------------------

Registering Filters

The two following examples work the same and both reverse an object:

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

def reverse_filter(s):
    return s[::-1]
app.jinja_env.filters['reverse'] = reverse_filter

In case of the decorator the argument is optional if you want to use the function name as name of the filter. Once registered, you can use the filter in your templates in the same way as Jinja2’s builtin filters, for example if you have a Python list in context called mylist:

{% for x in mylist | reverse %}
{% endfor %}