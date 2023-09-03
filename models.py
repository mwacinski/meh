from __future__ import annotations
from datetime import datetime
from flask_marshmallow import fields
from . import db, ma


def create_instance_from_json(cls, json_body, **kwargs):
    instance_data = {**json_body, **kwargs}
    return cls(**instance_data)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)


class Movie(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    content = db.Column(db.String(length=5000), nullable=True)
    reviews = db.relationship('Review')

    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

    def update(self, movie: Movie) -> None:
        self.name = movie.name
        self.content = movie.content


class MovieSchema(ma.Schema):
    _id = fields.fields.Integer()
    name = fields.fields.Str()
    content = fields.fields.Str()


class Review(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie._id'))
    content = db.Column(db.String(length=5000), nullable=False)
