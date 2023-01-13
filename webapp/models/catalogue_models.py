from sqlalchemy import ForeignKey

from webapp.db import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text)
    photo_url = db.Column(db.String)

    def __repr__(self):
        return 'Artist name={}>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    price = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    picture_url = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    artist_id = db.Column(db.Integer, ForeignKey(Artist.id))
    size = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Title={} artist={}>'.format(self.title, self.artist_id)
