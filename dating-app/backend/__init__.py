# from flask import Flask
# from .config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# from .backend import app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)


def create_app():

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    return app


# app = Flask(__name__)
# app.config.from_object(Config)
# # db = SQLAlchemy(app)
# # #migrate = Migrate(app, db)

# # migrate = Migrate()
# # migrate.init_app(app, db)


# def create_app():

#     from . import db
#     db.init_app(app)

#     return app


# #from .app import models #removed routes