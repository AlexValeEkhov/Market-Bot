from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from webapp import db
from webapp.email.email import ADMIN_EMAIL, ORDER_CONFIRM, single_email
from webapp.forms.cart_forms import OrderForm
from webapp.models.cart_models import Cart, Order, OrderContent

blueprint = Blueprint("cart", __name__, url_prefix="/cart")


@blueprint.route("/cart")
def cart():
    title = "Корзина"
    form = OrderForm()
    cart = Cart.query.filter(Cart.user_id == current_user.id).all()
    content, order_list = [], []
    total = 0
    if cart:
        for one in cart:
            content.append(one.item)
        for pic in set(content):
            order_list.append((pic, content.count(pic)))
            total += pic.price * content.count(pic)
    return render_template(
        "cart/cart.html",
        form=form,
        page_title=title,
        order_list=order_list,
        user=current_user,
        total=total,
    )


@blueprint.route("/cart_add/<int:pic_id>")
def cart_add(pic_id: int):
    new_cart = Cart(user_id=current_user.id, pic_id=pic_id)
    db.session.add(new_cart)
    db.session.commit()
    print(request.form.get('next'))

    # return render_template('cart/cart.html', user=current_user.id, cart=cart.content)
    return redirect(url_for("catalogue.album_filter"))


@blueprint.route("/cart_plus/<int:pic_id>")
def cart_plus(pic_id: int):
    new_cart = Cart(user_id=current_user.id, pic_id=pic_id)
    db.session.add(new_cart)
    db.session.commit()

    return redirect(url_for("cart.cart"))


@blueprint.route("/cart_minus/<int:pic_id>")
def cart_minus(pic_id: int):
    cart = Cart.query.filter(Cart.user_id == current_user.id).filter(Cart.pic_id == pic_id).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for("cart.cart"))


@blueprint.route("/checkout/<int:sum>", methods=["POST"])
def checkout(sum: int):
    form = OrderForm()
    cart = Cart.query.filter(Cart.user_id == current_user.id).all()
    if form.validate_on_submit():
        new_order = Order(
            user_id=current_user.id,
            sum=sum,
            status=1,
            address=form.address.data,
            phone=form.phone.data,
        )
        db.session.add(new_order)
        db.session.commit()
        order = Order.query.filter(Order.user_id == current_user.id).order_by(Order.id.desc()).first()
        for item in cart:
            content = OrderContent(order_id=order.id, pic_id=item.pic_id)
            db.session.add(content)
            db.session.delete(item)
            db.session.commit()
        subject = f"Заказ #{order.id} оформлен."
        body = ORDER_CONFIRM.format(current_user.name, order.id, order.sum)
        email = [ADMIN_EMAIL, current_user.email]
        single_email(subject, body, email)
        flash("Ваш заказ успешно оформлен!")
        return redirect(url_for("cart.cart"))
