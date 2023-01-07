import sqlite3
from flask import g, current_app
from flask.cli import with_appcontext
import click

def get_db():
    if 'db' not in g :
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    
    with current_app.open_resource("schema.sql") as f :
        db.executescript(f.read().decode('utf8'))
    
    from initdata import customer_list, tradesman_list, rider_list, goods_list, order_list
    db.executemany('INSERT INTO customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)', customer_list)
    db.executemany('INSERT INTO tradesman VALUES (?, ?, ?, ?, ?)', tradesman_list)
    db.executemany('INSERT INTO rider VALUES (?, ?, ?, ?, ?)', rider_list)
    db.executemany('INSERT INTO goods VALUES (?, ?, ?)', goods_list)
    db.executemany(
        'INSERT INTO orders (order_time, status, customer, rider, storename, goodsname, number, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        order_list,
        )
    db.commit()
    

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None :
        db.close()