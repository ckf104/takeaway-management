#! /usr/bin/python3
from flask import Flask, request, g, session, sessions
from collections import namedtuple
import functools
import random
import os
import flask

goods = namedtuple('goods', ['storename', 'goodsname', 'price', 'sellcount'])
order = namedtuple('order', ['id', 'storename',
                   'goodsname', 'number', 'price', 'status'])
allgoods = [goods(f'store{i + 1}', f'goods{i}', f'{i}', f'{i*10}')
            for i in range(1, 31)]
allorders = [order(f'0x1234597ff{i}', 'store1', 'goods', '2', '30', 'transport')
             for i in range(1, 31)]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd67e5a09-05b8-44e8-804f-90f2e84a4552'
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
    g.username = session['username']
    g.goods = allgoods
    g.orders = allorders
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

@bp.route('/info/orders', methods=['POST'])
def receive_orders():
    print(request.json)
    return 'true'

@bp.route('/info/changesetting', methods=['POST'])
def change_setting():
    print(request.form)
    return 'true'

# teardown functions are called after the context with block exits
app.register_blueprint(bp)
app.run()
