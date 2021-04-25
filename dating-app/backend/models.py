from . import db

#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login 

class UserProfile(db.Model):
    email = db.Column(db.String(120), unique=True, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    pronouns = db.Column(db.String(64), index=True)
    preferences =  db.Column(db.String(64), index=True)
    dob = db.Column(db.Date())
    token = db.Column(db.String(300))
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User {}>'.format(self.first_name) 

class DatingProfile(db.Model):
    email = db.Column(db.String(120), unique=True, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    pronouns = db.Column(db.String(64), index=True)
    preferences =  db.Column(db.String(64), index=True)
    dob = db.Column(db.Date())
    token = db.Column(db.String(300))
    image_name = db.Column(db.String(300))
    image_data = db.Column(db.LargeBinary)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User {}>'.format(self.first_name) 

# class ProfileDating(db.Model):
#     email = db.Column(db.String(120), unique=True, primary_key=True)
#     first_name = db.Column(db.String(64), index=True)
#     last_name = db.Column(db.String(64), index=True)
#     pronouns = db.Column(db.String(64), index=True)
#     preferences =  db.Column(db.String(64), index=True)
#     dob = db.Column(db.Date())
#     password = db.Column(db.String(100))

#     def __repr__(self):
#         return '<User {}>'.format(self.first_name) 

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     email = db.Column(db.String(120), unique=True)
#     first_name = db.Column(db.String(64), index=True, unique=True)
#     last_name = db.Column(db.String(64), index=True, unique=True)
#     pronouns = db.Column(db.String(64), index=True, unique=True)
#     preferences =  db.Column(db.String(64), index=True, unique=True)
#     dob = db.Column(db.Date(), nullable=False)
#     password = db.Column(db.String(100))

#     def __repr__(self):
#         return '<User {}>'.format(self.first_name) 

# class Profile_users(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     email = db.Column(db.String(120), unique=True)
#     first_name = db.Column(db.String(64), index=True, unique=True)
#     last_name = db.Column(db.String(64), index=True, unique=True)
#     pronouns = db.Column(db.String(64), index=True, unique=True)
#     preferences =  db.Column(db.String(64), index=True, unique=True)
#     password = db.Column(db.String(100))

#     def __repr__(self):
#         return '<Profile_users {}>'.format(self.first_name) 