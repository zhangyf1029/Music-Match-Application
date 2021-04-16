from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

migrate = Migrate()
migrate.init_app(app, db)


#from .app import models #removed routes