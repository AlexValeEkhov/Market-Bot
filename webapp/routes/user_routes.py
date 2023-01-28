from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from webapp import db
from webapp.email.email import (
    GREETINGS_MESSAGE,
    send_password_reset_email,
    single_email,
)
from webapp.forms.user_forms import (
    AskResetForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
)
from webapp.models.cart_models import Order
from webapp.models.user_models import User

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("main"))
    flash("Неправильное имя пользователя или пароль")
    return redirect(url_for("user.login"))


@blueprint.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('maiin'))
    form = AskResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Пожалуйста, проверьте вашу почту. Мы выслали вам ссылку на сброс пароля.')
        return redirect(url_for('user.login'))
    return render_template("user/ask_reset_password.html", title='Сброс пароля', form=form)


@blueprint.route('/process-reset/<token>', methods=['GET', 'POST'])
def process_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль был успешно изменен.')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main"))


@blueprint.route("/registration")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template("user/registration.html", page_title=title, form=form)


@blueprint.route("/process-reg", methods=["POST"])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data, role="user")
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        title = f"Добро пожаловать, {form.name.data}!"
        body = GREETINGS_MESSAGE
        email = [form.email.data]
        single_email(title, body, email)

        flash("""Вы успешно зарегистрировались! На вашу почту выслано письмо.
        Если вы его не получили, проверьте адрес электронной почты в личном кабинете.""")
        return redirect(url_for("user.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text, error
                    )
                )
        return redirect(url_for("user.register"))


status_dict = {1: "Оформлен", 2: "Оплачен", 3: "Отправлен", 4: "Завершен"}


@blueprint.route("/personal")
def personal():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id).all()
    return render_template('user/personal.html', orders=orders, status_dict=status_dict)


@blueprint.route("/order/<int:order_id>", methods=["GET"])
def order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    content = []
    for one in order.content:
        content.append(one.item)
    return render_template('user/order.html', order=order, content=content, status_dict=status_dict)


@blueprint.route("/order-cancel/<int:order_id>", methods=["GET"])
def order_cancel(order_id):
    order = Order.query.filter_by(id=order_id).first()
    for item in order.content:              # Не понял как работает ondelete CASCADE
        db.session.delete(item)
        db.session.commit()
    db.session.delete(order)
    db.session.commit()
    flash('Заказ был отменён.')
    return redirect(url_for('user.personal'))
