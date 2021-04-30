from . import db

#followed tutorial from this website for flask models for Users 
#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login 

class UserProfile(db.Model):
    email = db.Column(db.String(120), unique=True, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    pronouns = db.Column(db.String(64), index=True)
    preferences =  db.Column(db.String(64), index=True)
    dob = db.Column(db.Date())
    access_token = db.Column(db.String(300))
    refresh_token = db.Column(db.String(300))
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User {}>'.format(self.first_name) 