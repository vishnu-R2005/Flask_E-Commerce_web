from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    profile_pic = db.Column(db.String(100), default='default.jpg')  # <-- keep consistent
    is_admin = db.Column(db.Boolean, default=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))  # store only filename
