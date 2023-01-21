from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp import db
from webapp.forms.cart_forms import OrderForm
from webapp.functions.decorators import check_cart
from webapp.models.cart_models import Order
from webapp.models.catalogue_models import Product

blueprint = Blueprint("cart", __name__, url_prefix="/cart")


@blueprint.route("/cart")
def cart():
    title = "Корзина"
    form = OrderForm()
    cart = check_cart()
    content = cart.content.split()
    order_list = []
    total = 0
    for one in set(content):
        item = Product.query.filter_by(id=int(one)).first()
        if item:
            order_list.append((item, content.count(one)))
            total += item.price * content.count(one)
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
    cart = check_cart()
    cart.content = cart.content + str(pic_id) + " "
    db.session.commit()

    # return render_template('cart/cart.html', user=current_user.id, cart=cart.content)
    return redirect(url_for("catalogue.album"))


@blueprint.route("/cart_plus/<int:pic_id>")
def cart_plus(pic_id: int):
    cart = check_cart()
    cart.content = cart.content + str(pic_id) + " "
    db.session.commit()

    return redirect(url_for("cart.cart"))


@blueprint.route("/cart_minus/<int:pic_id>")
def cart_minus(pic_id: int):
    cart = check_cart()
    content = cart.content.split()
    pic_id = str(pic_id)
    if pic_id in content:
        content.remove(pic_id)
        new_cart = " ".join(content) + " "
        cart.content = new_cart
        db.session.commit()

    return redirect(url_for("cart.cart"))


@blueprint.route("/checkout/<int:sum>", methods=["POST"])
def checkout(sum: int):
    form = OrderForm()
    cart = check_cart()
    if form.validate_on_submit():
        new_order = Order(
            user_id=current_user.id,
            content=cart.content,
            sum=sum,
            status="оформлен",
            address=form.address.data,
        )
        db.session.add(new_order)
        db.session.commit()
        cart.content = ""
        db.session.commit()
        flash("Ваш заказ успешно оформлен!")
        return redirect(url_for("cart.cart"))
