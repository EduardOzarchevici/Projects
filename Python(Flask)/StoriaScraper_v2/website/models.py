from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    location = db.Column(db.String(500))
    nb_rooms = db.Column(db.Integer)
    surface = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    owner = db.Column(db.String(500))
    price = db.Column(db.String(500))
    link = db.Column(db.String(500))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150))
    favorites = db.relationship('UserFavorite', backref='user', lazy=True)

class UserFavorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    announcement = db.relationship('Announcement', backref=db.backref('favorited_by', lazy=True))