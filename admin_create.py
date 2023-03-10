from getpass import getpass

from webapp import create_app
from webapp.db import db
from webapp.models.user_models import User

app = create_app()

with app.app_context():
    password = 'password'
    password2 = 'password2'
    while not password == password2:
        name = input('Введите имя пользователя: ')

        if User.query.filter(User.name == name).count():
            print("\nПользователь с таким именем уже существует.\n")
            continue

        password = getpass('Введите пароль: ')
        password2 = getpass('Повторите пароль: ')
        if not password == password2:
            print('\nПароли не совпадают\n')

    new_user = User(name=name, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))
