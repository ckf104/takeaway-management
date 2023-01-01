#! /usr/bin/python3
from flask import Flask, request, g, session, sessions
from collections import namedtuple
import functools
import random
import os
import flask

goods = namedtuple('goods', ['storename', 'goodsname', 'price', 'sellcount'])
order = namedtuple('order', ['id', 'storename',
                   'goodsname', 'number', 'price', 'status', 'address', 'useraddr'])
allgoods = [goods(f'store{i + 1}', f'goods{i}', f'{i}', f'{i*10}')
            for i in range(1, 31)]
allorders = [order(f'0x1234597ff{i}', 'store1', 'goods', '2', '30', str(random.randint(0, 6)), '11111hao', '2222qqq')
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
def customer():
    target = 'user.html'
    g.username = session['username']
    g.goods = allgoods
    g.orders = allorders
    return flask.render_template(target)


@bp.route('/tradesman.html')
def tradesman():
    target = 'tradesman.html'
    g.username = session['username']
    g.goods = allgoods
    g.orders = allorders
    return flask.render_template(target)


@bp.route('/rider.html')
def rider():
    target = 'rider.html'
    g.username = session['username']
    g.waitingOrders = [allorders[i]
                       for i in range(len(allorders)) if i % 2 == 0]
    g.accOrders = [allorders[i] for i in range(len(allorders)) if i % 2 != 0]
    return flask.render_template(target)


@bp.route('/')
def default():
    return flask.redirect('index.html')


@bp.route('/login.html/')
def login():
    if session.get('username'):
        identity = session['identity']
        if identity in ['customer', 'tradesman', 'rider', 'manager']:
            return flask.redirect(flask.url_for(f'.{identity}'))
    return flask.send_from_directory(bp.static_folder, 'login.html')


@bp.route('/auth/login', methods=['POST'])
def auth_login():
    session.clear()
    identity = request.form['identity']
    name = request.form['name']
    password = request.form['password']
    if identity in ['customer', 'tradesman', 'rider', 'manager'] and name == 'ckf104' and password == '123456789':
        session['username'] = name
        session['identity'] = identity
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


@bp.route('/info/orderchange', methods=['POST'])
def order_change():
    print(request.form)
    return 'true'


@bp.route('/info/changesetting', methods=['POST'])
def change_setting():
    print(request.form)
    return 'true'


@bp.route('/info/goodschange', methods=['POST'])
def change_goods():
    print(request.form)
    return 'true'


# teardown functions are called after the context with block exits
app.register_blueprint(bp)
app.run()
