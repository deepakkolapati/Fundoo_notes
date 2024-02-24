from core import db
from flask import jsonify
from passlib.hash import pbkdf2_sha256
from .utils import JWT
from datetime import datetime, timedelta,timezone
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy import UniqueConstraint

collaborators = db.Table(
    "collaborators",
    db.metadata,
    db.Column("user_id", db.ForeignKey("users.id",ondelete="CASCADE")),
    db.Column("note_id", db.ForeignKey("notes.id",ondelete="CASCADE")),
    db.Column("access_type", db.String(20), default='read-only'),
    UniqueConstraint("user_id", "note_id", name="unique_user_note")
)

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(120),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    location=db.Column(db.String(250),nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    note = db.relationship('Notes', back_populates='user')
    label=db.relationship('Label', back_populates='user')
    c_notes: Mapped[List['Notes']] = db.relationship(secondary=collaborators, back_populates='c_users')

    def __init__(self, username, email, password, location, **kwargs) -> None:
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.location = location


    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)
    
    def token(self, aud=None, exp=15):
        payload = {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(minutes=exp)}
        if aud:
            payload.update({'aud': aud})
        return JWT.to_encode(payload)
            
    @property
    def json(self):
        return {
            "id":self.id,
            "username":self.username,
            "email":self.email,
            "location": self.location
        }


class Notes(db.Model):
    __tablename__ = 'notes'
    id=db.Column(db.Integer,primary_key=True,nullable=False, autoincrement=True)
    title=db.Column(db.String(50),nullable=True)
    description=db.Column(db.Text,nullable=False)
    color = db.Column(db.String(20))
    reminder = db.Column(db.DateTime, default=None, nullable=True)
    is_archive=db.Column(db.Boolean, default=False)
    is_trash=db.Column(db.Boolean, default=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    user=db.relationship('User',back_populates="note")
    c_users: Mapped[List[User]] =db.relationship(secondary=collaborators,back_populates="c_notes")

    def __init__(self, title, description, color, user_id, reminder=None, **kwargs):
  
        self.title = title
        self.description = description
        self.color = color
        self.user_id = user_id
        self.is_archive = False
        self.is_trash = False

        if reminder:
            self.set_reminder(reminder)

    def set_reminder(self, reminder_time):
        # Set the time zone to 'Asia/Kolkata'
        asia_kolkata_timezone = timezone(timedelta(hours=5, minutes=30))
        reminder_time = reminder_time.replace(tzinfo=asia_kolkata_timezone)

        # Assign the reminder time to the Notes object
        self.reminder = reminder_time

    def __str__(self) -> str:
        return f'{self.title}-{self.id}'
    
    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "reminder": str(self.reminder),
            "is_archive": self.is_archive,
            "is_trash": self.is_trash,
            "user_id": self.user_id
        }
    

class Label(db.Model):
    __tablename__ = 'labels'
    id=db.Column(db.Integer,primary_key=True,nullable=False, autoincrement=True)
    name=db.Column(db.String(50),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',back_populates='label')
    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
        }
