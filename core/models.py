from core import db
from flask import jsonify

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(120),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    location=db.Column(db.String(250),nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    @property
    def json(self):
        return {
            "id":self.id,
            "username":self.username,
            "email":self.email,
            "location": self.location
        }
