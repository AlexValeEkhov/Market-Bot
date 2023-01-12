from flask import Blueprint, render_template, flash, redirect, url_for
from webapp.user.decorators import admin_required
from webapp import db
from webapp.catalogue.forms import ArtistForm, ProductForm
from webapp.catalogue.models import Artist, Product

blueprint = Blueprint("catalogue", __name__, url_prefix="/catalogue")


@blueprint.route("/admin")
@admin_required
def admin():
    title = "Панель админа"
    return render_template("admin/admin.html", page_title=title)


@blueprint.route("/add_artist")
@admin_required
def add_artist():
    form = ArtistForm()
    title = "Панель админа"
    return render_template("catalogue/add_artist.html", page_title=title, form=form)


@blueprint.route("/process_add_artist", methods=["POST", "GET"])
def process_add_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data, text=form.text.data, photo_url=form.photo_url.data
        )
        db.session.add(new_artist)
        db.session.commit()
        flash("Вы успешно добавили художника")
        return redirect(url_for("admin.admin"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text, error
                    )
                )
        return redirect(url_for("catalogue.add_artist"))


@blueprint.route("/add_picture")
@admin_required
def add_product():
    form = ProductForm()
    title = "Панель админа"
    return render_template("catalogue/add_picture.html", page_title=title, form=form)


@blueprint.route("/process_add_picture", methods=["POST", "GET"])
def process_add_picture():
    form = ProductForm()
    if form.validate_on_submit():
        new_picture = Product(
            title=form.title.data,
            price=form.price.data,
            text=form.text.data,
            picture_url=form.picture_url.data,
            year=form.year.data,
            artist_id=form.artist_id.data,
            size=form.size.data,
        )
        db.session.add(new_picture)
        db.session.commit()
        flash("Вы успешно добавили картину")
        return redirect(url_for("admin.admin"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text, error
                    )
                )
        return redirect(url_for("catalogue.add_picture"))
