# pylint: disable=no-member, too-few-public-methods
"""
Database models
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Username(UserMixin, db.Model):
    """
    Username model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


class Comment(db.Model):
    """
    Comment model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    comment = db.Column(db.String(300), unique=False, nullable=False)
    movie = db.Column(db.Integer, unique=False, nullable=False)
