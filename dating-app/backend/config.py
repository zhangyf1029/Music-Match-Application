import os
from .__init__ import app

#spotify client id 
CLIENT_ID = "7c1f2bab60504b6e91baaf93b7ff0c10"
#spotify client secret 
CLIENT_SECRET = "c27bc4507c8b41a6b3ffed7db05c21d6"

#set up base directory and db paths 
basedir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "UserProfile.db")

class Config(object):
    
    #set up the sqlalchemy uri with track mods as false 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #set database to db.sqlite 
    app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))