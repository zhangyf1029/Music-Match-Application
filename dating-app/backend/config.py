import os
from .__init__ import app

basedir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "User.db")
class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'backend.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))