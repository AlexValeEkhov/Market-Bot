from flask import Blueprint, flash, redirect, render_template, url_for

from webapp import db
from webapp.forms.catalogue_forms import ArtistForm, PictureForm
from webapp.functions.decorators import admin_required
from webapp.models.catalogue_models import Artist, Product

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


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
    return render_template("admin/add_artist.html", page_title=title, form=form)


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
        return redirect(url_for("admin.add_artist"))


@blueprint.route("/add_picture")
@admin_required
def add_picture():
    art_list = Artist.query.all()
    form = PictureForm()
    form.artist_id.choices = [(g.id, g.name) for g in art_list]
    title = "Панель админа"
    return render_template("admin/add_picture.html", page_title=title, form=form)


@blueprint.route("/process_add_picture", methods=["POST", "GET"])
def process_add_picture():
    art_list = Artist.query.all()
    form = PictureForm()
    form.artist_id.choices = [(g.id, g.name) for g in art_list]
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
        return redirect(url_for("admin.add_picture"))
