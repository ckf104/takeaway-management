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

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None :
        db.close()