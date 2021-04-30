# from flask import Flask
# from .config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# from .backend import app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models and set up the db 
db = SQLAlchemy()

#set up the app variable to be imported into all other files for later use 
app = Flask(__name__)


def create_app():

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    return app
