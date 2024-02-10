from core import db
from flask import jsonify
from passlib.hash import pbkdf2_sha256


class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(120),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    location=db.Column(db.String(250),nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, location, **kwargs) -> None:
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.location = location


    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

    @property
    def json(self):
        return {
            "id":self.id,
            "username":self.username,
            "email":self.email,
            "location": self.location
        }
