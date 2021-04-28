import os
from .__init__ import app

#Add your client ID
CLIENT_ID = "7c1f2bab60504b6e91baaf93b7ff0c10"
#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "c27bc4507c8b41a6b3ffed7db05c21d6"

basedir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "User.db")

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))