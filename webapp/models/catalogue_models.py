from datetime import datetime

from sqlalchemy.orm import relationship

from webapp.db import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text)
    img = db.Column(db.String)
    pictures_dir = db.Column(db.String)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    price = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    img = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='CASCADE'), index=True)
    size = db.Column(db.String, nullable=False)

    artist = relationship('Artist', backref='pictures')

    def __repr__(self):
        return '<Title {} {}>'.format(self.title, self.artist)


class Filter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    artist_id = db.Column(db.Integer)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    pic_id = db.Column(db.Integer, db.ForeignKey('picture.id', ondelete='CASCADE'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)

    product = relationship('Picture', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
