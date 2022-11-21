#! /usr/bin/python3
from flask import Flask, request, g, session, sessions
import functools
import os
import flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd67e5a09-05b8-44e8-804f-90f2e84a4552'

bp = flask.Blueprint('m', __name__, url_prefix='', static_url_path='/',
                     static_folder='/',
                     template_folder='',
                     root_path=os.path.abspath(f'{__file__}/../../front-end/'))


def checklogin(func):
    @functools.wraps(func)
    def wrap_func(*args, **keys):
        if not session.get('username'):
            return flask.redirect(flask.url_for('.login'))
        return func(*args, **keys)
    return wrap_func


@bp.route('/user.html')
@checklogin
def hello():
    target = 'user.html'
    g.user = {'name': 'ckf104'}
    return flask.render_template(target)


@bp.route('/')
def default():
    return flask.redirect('index.html')


@bp.route('/login.html/')
def login():
    if session.get('username'):
        return flask.redirect(flask.url_for('.hello'))
    return flask.send_from_directory(bp.static_folder, 'login.html')


@bp.route('/auth/login', methods=['POST'])
def auth_login():
    session.clear()
    identity = request.form['identity']
    name = request.form['name']
    password = request.form['password']
    if identity == 'customer' and name == 'ckf104' and password == '123456789':
        session['username'] = name
        return 'true'
    else:
        return 'false'


@bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return 'true'


# teardown functions are called after the context with block exits
app.register_blueprint(bp)
app.run()
