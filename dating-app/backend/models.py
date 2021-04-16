from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    pronouns = db.Column(db.String(64), index=True, unique=True)
    preferences =  db.Column(db.String(64), index=True, unique=True)
    dob = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.first_name) 