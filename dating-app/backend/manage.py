from flask import Flask
# from venv.Lib.site-packages.flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from .__init__ import app 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    # last_name = db.Column(db.String(64), index=True, unique=True)
    pronouns = db.Column(db.String(64), index=True, unique=True)
    preferences =  db.Column(db.String(64), index=True, unique=True)
    # dob = db.Column(db.Date(), nullable=False)
    # email = db.Column(db.String(120), index=True, unique=True)
    # password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.first_name) 

if __name__ == '__main__':
    manager.run()