import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

REMEMBER_COOKIE_DURATION = timedelta(days=5)

SECRET_KEY = "dhgfdhg%^*UU8lLK*^%KDKFs()"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Сигналы приложению об изменениях в БД. Отключаем, чтобы не тратить ресурсы
