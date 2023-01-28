# from threading import Thread

from flask import current_app, render_template
from flask_mail import Mail, Message

# def send_async_email(app, msg, mail):
#     with app.app_context():
#         mail.send(msg)


def single_email(subject, text_body, email):
    mail = Mail(current_app)
    msg = Message(subject, recipients=email)
    msg.body = text_body
    # Thread(target=send_async_email, args=(current_app, msg, mail)).start()
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    single_email(
        "WaterColor Market - Сброс пароля",
        render_template('reset_password.txt', user=user, token=token),
        [user.email],
    )


ADMIN_EMAIL = 'watercolor-market@yandex.ru'

GREETINGS_MESSAGE = "Вы успешно зарегистрировались на сайте WaterColor Market."

ORDER_CONFIRM = """Уважаемый {}. Ваш заказ №{} оформлен.\n Сумма: {}\n
                   С деталями заказа вы можете ознакомиться в личном кабинете."""
