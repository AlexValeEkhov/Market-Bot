from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship

from db import Base

db = SQLAlchemy()

class User(Base):
    __tablename__ = "Админ/Пользователь"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    phone_number = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"Пользователь {self.id}, {self.username}"

class Customer(Base):
    __tablename__ = "Покупатель"

    id = Column(Integer, primary_key=True)
    user_id = relationship('User')
    phone_number = Column(String)
    email = Column(String)
    bot_id = Column(String)

class Product(Base):
    __tablename__ = "Товар"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    descr = Column(Text)

class Order(Base):
    __tablename__ = "Заказ"

    id = Column(Integer, primary_key=True)
    customer_id = relationship('Customer')
    content = Column(String)
    payment = Column(Integer)
    address = Column(String)
    status = Column(String)

class Picture(Base):
    __tablename__ = "Картинка"

    id = Column(Integer, primary_key=True)
    title = relationship('Product')
    url = Column(String)
