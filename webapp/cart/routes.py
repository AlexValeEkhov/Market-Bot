from flask import Blueprint, render_template  # , flash, redirect, url_for

blueprint = Blueprint('cart', __name__, url_prefix='/cart')


@blueprint.route("/cart")
def cart():
    title = "Корзина"
    return render_template('cart/cart.html', page_title=title)
