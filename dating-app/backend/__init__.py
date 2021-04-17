from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .backend import app


app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)
# #migrate = Migrate(app, db)

# migrate = Migrate()
# migrate.init_app(app, db)


def create_app():

    from . import db
    db.init_app(app)

    return app


#from .app import models #removed routes