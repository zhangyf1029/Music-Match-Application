import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import os
from .config import *


def get_db():
    ''' use this function to get a connection
        to the database when making updates
        inserts, or anything that requires 
        a commit '''
    
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    ''' close the database connection
        by popping it off the stack
        to close it '''
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db.create_all()
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
