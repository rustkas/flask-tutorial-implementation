# pylint: skip-file

from flask import Flask
# from markupsafe import escape
from flask import url_for

app = Flask(__name__)

@app.before_request
def before_request_fuct():
    print('This runs before each request.')

@app.after_request
def after_request_fuct(response):
    print('This runs after each request.')
    return response
@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))