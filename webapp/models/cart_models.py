from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from webapp.db import db
from webapp.models.catalogue_models import Picture
from webapp.models.user_models import User


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), index=True, nullable=False)
    pic_id = db.Column(db.Integer, ForeignKey(Picture.id), index=True, nullable=False)

    item = relationship('Picture', backref='cart')

    def __repr__(self):
        return '<Cart user={} item={}>'.format(self.user_id, self.pic_id)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), index=True, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)  # 1 - оформлен, 2 - оплачен, 3 - отправлен, 4 - завершён
    address = db.Column(db.String)
    phone = db.Column(db.String)

    user = relationship('User', backref='orders')

    def __repr__(self):
        return '<Order {} user {}>'.format(self.id, self.user.name)


class OrderContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey(Order.id, ondelete='CASCADE'), index=True, nullable=False)
    pic_id = db.Column(db.Integer, ForeignKey(Picture.id), index=True, nullable=False)

    order = relationship('Order', backref='content')
    item = relationship('Picture', backref='orders')

    def __repr__(self):
        return '<Order={} item={}>'.format(self.order_id, self.item.title)
