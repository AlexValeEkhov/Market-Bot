from sqlalchemy import ForeignKey

from webapp.db import db
from webapp.models.user_models import User


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), index=True, nullable=False)
    content = db.Column(db.String)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), index=True, nullable=False)
    content = db.Column(db.String)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)  # 1 - оформлен, 2 - оплачен, 3 - отправлен, 4 - завершён
    address = db.Column(db.String)
