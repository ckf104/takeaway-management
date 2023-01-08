#! /usr/bin/python3
from flask import Flask, request, g, session, sessions
from collections import namedtuple
import functools
import random
import os
import flask
import sqlite3

goods = namedtuple('goods', ['storename', 'goodsname', 'price', 'sellcount'])
order = namedtuple('order', ['id', 'storename',
                   'goodsname', 'number', 'price', 'status', 'address', 'useraddr'])
rider_order = namedtuple('rider_order', ['id', 'storename', 'goodsname', 'number', 'address', 'useraddr'])
user = namedtuple('user', ['gender', 'realname', 'telephone',
                  'birthday', 'id', 'address', 'username'])
rider_tuple = namedtuple('rider', ['realname', 'address', 'telephone', 'ridername'])
store = namedtuple('store', ['storename', 'telephone', 'address'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd67e5a09-05b8-44e8-804f-90f2e84a4552'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DATABASE'] = f'{os.path.dirname(__file__)}/database.db'

import db
app.teardown_appcontext(db.close_db)
app.cli.add_command(db.init_db_command)

bp = flask.Blueprint('m', __name__, url_prefix='', static_url_path='/',
                     static_folder='/',
                     template_folder='',
                     root_path=os.path.abspath(f'{__file__}/../../front-end/'))


def checklogin(func):
    @functools.wraps(func)
    def wrap_func(*args, **keys):
        if not session.get('username'):
            return flask.redirect('index.html')
        return func(*args, **keys)
    return wrap_func


@bp.route('/user.html')
def customer():
    target = 'user.html'
    username = g.username = session['username']

    allgoods = []
    allorders = []
    
    database = db.get_db()
    goods_fetch = database.execute('SELECT * FROM goods').fetchall()
    for goods_row in goods_fetch :
        storename = goods_row['storename']
        goodsname = goods_row['goodsname']
        price = goods_row['price']
        
        sellcount_fetch = database.execute(
            'SELECT sum(number) AS sum FROM orders WHERE storename = ? AND goodsname = ?',
            (storename, goodsname),
        ).fetchone()
        sellcount = sellcount_fetch['sum']
        
        allgoods.append(goods(storename, goodsname, price, sellcount))
    
    order_fetch = database.execute('SELECT * FROM orders WHERE customer = ? AND status != 6 AND status != 2', (username,)).fetchall()
    for order_row in order_fetch :
        id = order_row['id']
        storename = order_row['storename']
        goodsname = order_row['goodsname']
        number = order_row['number']
        price = order_row['price']
        status = order_row['status']
        
        address_fetch = database.execute('SELECT address FROM tradesman WHERE storename = ?', (storename,)).fetchone()
        address = address_fetch['address']
        useraddr_fetch = database.execute('SELECT address AS useraddr FROM customer WHERE name = ?', (username,)).fetchone()
        useraddr = useraddr_fetch['useraddr']

        allorders.append(order(id, storename, goodsname, number, price, str(status), address, useraddr))
    
    g.goods = allgoods
    g.orders = allorders
    return flask.render_template(target)


@bp.route('/tradesman.html')
@checklogin
def tradesman():
    target = 'tradesman.html'
    username = session['username']
    
    database = db.get_db()
    storename = session['storename']
    g.username = storename
    
    allgoods = []
    allorders = []
    
    goods_fetch = database.execute('SELECT * FROM goods WHERE storename = ?', (storename,)).fetchall()
    for goods_row in goods_fetch :
        goodsname = goods_row['goodsname']
        price = goods_row['price']
        
        sellcount_fetch = database.execute(
            'SELECT sum(number) AS sum FROM orders WHERE storename = ? AND goodsname = ?',
            (storename, goodsname),
        ).fetchone()
        sellcount = sellcount_fetch['sum']
        
        allgoods.append(goods(storename, goodsname, price, sellcount))
    
    order_fetch = database.execute('SELECT * FROM orders WHERE storename = ? AND status = 0', (storename,)).fetchall()
    for order_row in order_fetch :
        id = order_row['id']
        goodsname = order_row['goodsname']
        number = order_row['number']
        price = order_row['price']
        customer = order_row['customer']

        address_fetch = database.execute('SELECT address FROM tradesman WHERE storename = ?', (storename,)).fetchone()
        address = address_fetch['address']
        useraddr_fetch = database.execute('SELECT address AS useraddr FROM customer WHERE name = ?', (customer,)).fetchone()
        useraddr = useraddr_fetch['useraddr']
        
        allorders.append(order(id, storename, goodsname, number, price, 0, address, useraddr))
    
    g.goods = allgoods
    g.orders = allorders
    return flask.render_template(target)


@bp.route('/rider.html')
@checklogin
def rider():
    target = 'rider.html'
    rider = g.username = session['username']
    
    allWaitingOrders = []
    allAccOrders = []
    
    database = db.get_db()
    waitingOrder_fetch = database.execute('SELECT * FROM orders WHERE rider IS NULL AND status = 3').fetchall()
    for waitingOrder_row in waitingOrder_fetch :
        id = waitingOrder_row['id']
        storename = waitingOrder_row['storename']
        goodsname = waitingOrder_row['goodsname']
        number = waitingOrder_row['number']
        customer = waitingOrder_row['customer']
        
        address_fetch = database.execute('SELECT address FROM tradesman WHERE storename = ?', (storename,)).fetchone()
        address = address_fetch['address']
        useraddr_fetch = database.execute('SELECT address AS useraddr FROM customer WHERE name = ?', (customer,)).fetchone()
        useraddr = useraddr_fetch['useraddr']
        
        allWaitingOrders.append(rider_order(id, storename, goodsname, number, address, useraddr))
    
    accOrder_fetch = database.execute('SELECT * FROM orders WHERE rider = ? AND status = 4', (rider,)).fetchall()
    for accOrder_row in accOrder_fetch :
        id = accOrder_row['id']
        storename = accOrder_row['storename']
        goodsname = accOrder_row['goodsname']
        number = accOrder_row['number']
        customer = accOrder_row['customer']
        
        address_fetch = database.execute('SELECT address FROM tradesman WHERE storename = ?', (storename,)).fetchone()
        address = address_fetch['address']
        useraddr_fetch = database.execute('SELECT address AS useraddr FROM customer WHERE name = ?', (customer,)).fetchone()
        useraddr = useraddr_fetch['useraddr']
        
        allAccOrders.append(rider_order(id, storename, goodsname, number, address, useraddr))
    
    g.waitingOrders = allWaitingOrders
    g.accOrders = allAccOrders
    return flask.render_template(target)

@bp.route('/manager.html')
@checklogin
def manager():
    target = 'manager.html'
    g.username = session['username']
    
    allusers = []
    allorders = []
    allriders = []
    allstores = []
    
    database = db.get_db()
    user_fetch = database.execute('SELECT * FROM customer').fetchall()
    for user_row in user_fetch :
        gender = user_row['gender']
        realname = user_row['realname']
        telephone = user_row['telephone']
        birthday = user_row['birthday']
        id = user_row['id']
        address = user_row['address']
        username = user_row['name']
        
        allusers.append(user(gender, realname, telephone, birthday, id, address, username))
    
    order_fetch = database.execute('SELECT * FROM orders WHERE status != 6 AND status != 2').fetchall()
    for order_row in order_fetch :
        id = order_row['id']
        storename = order_row['storename']
        goodsname = order_row['goodsname']
        number = order_row['number']
        price = order_row['price']
        status = order_row['status']
        
        address_fetch = database.execute('SELECT address FROM tradesman WHERE storename = ?', (storename,)).fetchone()
        address = address_fetch['address']
        useraddr_fetch = database.execute('SELECT address AS useraddr FROM customer WHERE name = ?', (username,)).fetchone()
        useraddr = useraddr_fetch['useraddr']
        
        allorders.append(order(id, storename, goodsname, number, price, str(status), address, useraddr))
    
    rider_fetch = database.execute('SELECT * FROM rider').fetchall()
    for rider_row in rider_fetch :
        realname = rider_row['realname']
        address = rider_row['address']
        telephone = rider_row['telephone']
        ridername = rider_row['name']
        
        allriders.append(rider_tuple(realname, address, telephone, ridername))
    
    store_fetch = database.execute('SELECT * FROM tradesman').fetchall()
    for store_row in store_fetch :
        storename = store_row['storename']
        telephone = store_row['telephone']
        address = store_row['address']
        
        allstores.append(store(storename, telephone, address))
    
    g.users = allusers
    g.orders = allorders
    g.riders = allriders
    g.stores = allstores
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
       
    if identity not in ['customer', 'tradesman', 'rider', 'manager'] :
        return 'identity must be customer, tradesman, rider or manager'
    else :
        database = db.get_db()
        
        user = database.execute(
            f'SELECT * FROM {identity} WHERE name = ?', (name,)
        ).fetchone()
        
        if user is None :
            return 'Incorrect name'
        elif user['password'] != password :
            return 'Incorrect password'
        else :
            session['identity'] = identity
            session['username'] = name
            if identity == 'tradesman' :
                session['storename'] = user['storename']
            return 'true'


@bp.route('/auth/signup',methods=['POST'])
def signup():
    database = db.get_db()
    
    identity = request.form['identity']
    name = request.form['name']
    password = request.form['password']
    telephone = request.form['telephone']
    address = request.form['address']
    
    if identity == 'customer' :
        birthday = request.form['birthday']
        gender = request.form['gender']
        realname = request.form['realname']
        id = request.form['id']
        
        try :
            database.execute(
                'INSERT INTO customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (name, password, telephone, birthday, gender, realname, id, address),
            )
            database.commit()
            return 'true'
        except :
            return 'username has already been registered'
        
    elif identity == 'tradesman' :
        storename = request.form['storename']
        
        fetch = database.execute('SELECT * FROM tradesman WHERE name = ?', (name,)).fetchone()
        if fetch is not None :
            return 'username has already been registered'
         
        try:
            database.execute(
                'INSERT INTO tradesman VALUES (?, ?, ?, ?, ?)',
                (name, password, telephone, address, storename),      
            )
            database.commit()
            return 'true'
        except :
            return 'storename has already been registered'
    
    elif identity == 'rider' :
        realname = request.form['realname']
        
        try:
            database.execute(
                'INSERT INTO rider VALUES (?, ?, ?, ?, ?)',
                (name, password, telephone, realname, address),
            )
            database.commit()
            return 'true'
        except :
            return 'username has already been registered'
        
            
@bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return 'true'


@bp.route('/info/orders', methods=['POST'])
def receive_orders():
    database = db.get_db()
    
    status = 0
    customer = session['username']
    
    allorders = request.json
    for order in allorders :
        try :
            database.execute(
                'INSERT INTO orders (status, customer, rider, storename, goodsname, number, price) VALUES (?, ?, NULL, ?, ?, ?, ?)',
                (status, customer, order['storename'], order['goodsname'], order['number'], order['price']),
            )
            database.commit()
        except sqlite3.Error as er :
            response = ' '.join(er.args)
            return response
    
    return 'true'

@bp.route('/info/orderchange', methods=['POST'])
def order_change():
    identity = session['identity']
    name = session['username']
    id = request.form['id']
    previous = request.form['previous']
    next = request.form['next']
    
    database = db.get_db()
    try :
        if identity != 'rider' :
            database.execute(
                'UPDATE orders SET status = ? WHERE id = ? AND status = ?',
                (next, id, previous),
            )
        else :
            database.execute(
                'UPDATE orders SET status = ?, rider = ? WHERE id = ? AND status = ?',
                (next, name, id, previous),
            )
        database.commit()
        return 'true'
    except sqlite3.Error as er :
        response = ' '.join(er.args)
        return response


@bp.route('/info/changesetting', methods=['POST'])
def change_setting():
    identity = session['identity']
    old_name = session['username']
    name = request.form.get('name')
    
    database = db.get_db()
    if name is not None :
        try :
            database.execute(f'UPDATE {identity} SET name = ? WHERE name = ?', (name, old_name))
            database.commit()
        except :
            return 'username has already been registered'
    else :
        name = old_name
    
    for column in ['password', 'telephone', 'address'] :
        new_value = request.form.get(column)
        if new_value is not None :
            try :
                database.execute(f'UPDATE {identity} SET {column} = ? WHERE name = ?', (new_value, name))
                database.commit()
            except sqlite3.Error as er :
                response = ' '.join(er.args)
                return response
    return 'true'
        


@bp.route('/info/goodschange', methods=['POST'])
def change_goods():	
    if session['identity'] == 'tradesman':
        storename = session['storename']
    else:
        storename = request.form.get('storename')
    prevname = request.form.get('prevname')
    newname = request.form.get('newname')
    newprice = request.form.get('newprice')
    
    database = db.get_db()
    if newname is None :
        if newprice is None :
            try :
                database.execute(
                    'DELETE FROM goods WHERE storename = ? AND goodsname = ?',
                    (storename, prevname),
                )
                database.commit()
            except :
                return 'no such goods'
        else :
            try :
                database.execute(
                    'UPDATE goods SET price = ? WHERE storename = ? AND goodsname = ?',
                    (newprice, storename, prevname),
                )
                database.commit()
            except :
                return 'no such goods'
    elif prevname is None :
        try :
            database.execute(
                'INSERT INTO goods VALUES (?, ?, ?)',
                (storename, newname, newprice),
            )
            database.commit()
        except sqlite3.Error as er :
            response = ' '.join(er.args)
            return response
    else :
        if newprice is not None :
            try :
                database.execute(
                    'UPDATE goods SET goodsname = ?, price = ? WHERE storename = ? AND goodsname = ?',
                    (newname, newprice, storename, prevname),
                )
                database.commit()
            except :
                return 'no such goods'
        else :
            try :
                database.execute(
                    'UPDATE goods SET goodsname = ? WHERE storename = ? AND goodsname = ?',
                    (newname, storename, prevname),
                )
                database.commit()
            except :
                return 'no such goods'
    
    return 'true'

@bp.route('/info/goodsinfo', methods=['POST'])
def goodsinfo():
    storename = request.form['storename']
    
    allgoods = []
    
    database = db.get_db()
    goods_fetch = database.execute('SELECT * FROM goods WHERE storename = ?', (storename,)).fetchall()
    for goods_row in goods_fetch :
        goodsname = goods_row['goodsname']
        price = goods_row['price']
        
        sellcount_fetch = database.execute(
            'SELECT sum(number) AS sum FROM orders WHERE storename = ? AND goodsname = ?',
            (storename, goodsname),
        ).fetchone()
        sellcount = sellcount_fetch['sum']
        
        allgoods.append(goods(storename, goodsname, price, sellcount))
        
    import json
    s = json.dumps([g._asdict() for g in allgoods])
    # print(s)
    return s

@bp.route('/info/manager_changeuser', methods=['POST'])
def manager_changeuser():
    database = db.get_db()
    
    prevusername = request.form['prevusername']
    name = request.form.get('name')
    all_none = True
    
    if name is not None :
        all_none = False
        try :
            database.execute('UPDATE customer SET name = ? WHERE name = ?', (name, prevusername))
            database.commit()
        except :
            return 'username has already been registered'
    else :
        name = prevusername
    
    column_list = ['password', 'telephone', 'birthday', 'gender', 'realname', 'id', 'address']
    for column in column_list :
        value = request.form.get(column)
        if value is not None :
            all_none = False
            try :
                database.execute(
                    f'UPDATE customer SET {column} = ? WHERE name = ?',
                    (value, name),
                )
                database.commit()
            except sqlite3.Error as er :
                response = ' '.join(er.args)
                return response
    
    if all_none :
        try :
            database.execute('DELETE FROM customer WHERE name = ?', (name,))
            database.commit()
        except sqlite3.Error as er :
            response = ' '.join(er.args)
            return response
    
    return 'true'
            
@bp.route('/info/manager_changeorder', methods=['POST'])
def manager_changeorder():
    database = db.get_db()
    
    id = request.form['id']
    all_none = True
    
    column_list = ['status', 'storename', 'goodsname', 'number', 'price', 'address']
    for column in column_list :
        value = request.form.get(column)
        if value is not None :
            all_none = False
            try :
                database.execute(
                    f'UPDATE orders SET {column} = ? WHERE id = ?',
                    (value, id),
                )
                database.commit()
            except sqlite3.Error as er :
                response = ' '.join(er.args)
                return response
    
    if all_none :
        try :
            database.execute('DELETE FROM orders WHERE id = ?', (id,))
            database.commit()
        except sqlite3.Error as er :
            response = ' '.join(er.args)
            return response
    
    return 'true'

@bp.route('/info/manager_changerider', methods=['POST'])
def manager_changerider():
    database = db.get_db()
    
    prevridername = request.form['prevridername']
    name = request.form.get('name')
    all_none = True
    
    if name is not None :
        all_none = False
        try :
            database.execute('UPDATE rider SET name = ? WHERE name = ?', (name, prevridername))
            database.commit()
        except :
            return 'username has already been registered'
    else :
        name = prevridername
    
    column_list = ['password', 'telephone', 'realname', 'address']
    for column in column_list :
        value = request.form.get(column)
        if value is not None :
            all_none = False
            try :
                database.execute(
                    f'UPDATE rider SET {column} = ? WHERE name = ?',
                    (value, name),
                )
                database.commit()
            except sqlite3.Error as er :
                response = ' '.join(er.args)
                return response
    
    if all_none :
        try :
            database.execute('DELETE FROM rider WHERE name = ?', (name,))
            database.commit()
        except sqlite3.Error as er :
            response = ' '.join(er.args)
            return response
    return 'true'

@bp.route('/info/manager_changestore', methods=['POST'])
def manager_changestore():
    database = db.get_db()
    
    prevstorename = request.form['prevstorename']
    storename = request.form.get('storename')
    all_none = True
    
    if storename is not None :
        all_none = False
        try :
            database.execute('UPDATE tradesman SET storename = ? WHERE storename = ?', (storename, prevstorename))
            database.commit()
        except :
            return 'storename has already been registered'
    else :
        storename = prevstorename
    
    column_list = ['name', 'password', 'telephone', 'address']
    for column in column_list :
        value = request.form.get(column)
        if value is not None :
            all_none = False
            try :
                database.execute(
                    f'UPDATE tradesman SET {column} = ? WHERE storename = ?',
                    (value, storename),
                )
                database.commit()
            except sqlite3.Error as er :
                response = ' '.join(er.args)
                return response
    
    if all_none :
        try :
            database.execute('DELETE FROM tradesman WHERE storename = ?', (storename,))
            database.commit()
        except sqlite3.Error as er :
            response = ' '.join(er.args)
            return response
    
    return 'true'

# teardown functions are called after the context with block exits
app.register_blueprint(bp)
app.run()
