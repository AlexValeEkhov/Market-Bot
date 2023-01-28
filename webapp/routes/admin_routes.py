from flask import Blueprint, flash, redirect, render_template, url_for

from webapp import db
from webapp.forms.catalogue_forms import (
    ArtistEditForm,
    ArtistForm,
    FilterByArtistForm,
    PictureEditForm,
    PictureForm,
)
from webapp.functions.decorators import admin_required
from webapp.models.catalogue_models import Artist, Picture

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/admin", methods=["POST", "GET"])
@admin_required
def admin():
    artist_list = Artist.query.all()
    form = FilterByArtistForm()
    form.artist_id.choices = [(g.id, g.name) for g in artist_list]
    title = "Панель админа"
    if form.is_submitted():
        artist = Artist.query.filter_by(id=form.artist_id.data).first()
        pictures_list = Picture.query.filter_by(artist_id=artist.id).all()
        form = ArtistEditForm()
        return render_template("admin/edit.html", artist=artist, form=form, pictures_list=pictures_list)
    return render_template("admin/admin.html", page_title=title, artist_list=artist_list, form=form)


@blueprint.route("/add_artist")
@admin_required
def add_artist():
    form = ArtistForm()
    title = "Панель админа"
    return render_template("admin/add_artist.html", page_title=title, form=form)


@blueprint.route("/process_add_artist", methods=["POST", "GET"])
@admin_required
def process_add_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data, text=form.text.data, img=form.img.data, pictures_dir=form.pictures_dir.data
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
@admin_required
def process_add_picture():
    form = PictureForm()
    art_list = Artist.query.all()
    form.artist_id.choices = [(g.id, g.name) for g in art_list]
    if form.validate_on_submit():
        new_picture = Picture(
            title=form.title.data,
            price=form.price.data,
            text=form.text.data,
            img=form.img.data,
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


@blueprint.route("/edit")
def edit():
    artist_list = Artist.query.all()
    form = FilterByArtistForm()
    pictures_list = []
    form.artist_id.choices = [(g.id, g.name) for g in artist_list]
    return render_template("admin/edit.html", artist_list=artist_list, form=form, pictures_list=pictures_list)


@blueprint.route("/artist_editing/<int:artist_id>", methods=["POST", "GET"])
def artist_editing(artist_id):
    form = ArtistEditForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    if form.is_submitted:
        if form.name.data:
            artist.name = form.name.data
        if form.text.data:
            artist.text = form.text.data
        if form.img.data:
            artist.img = form.img.data
        if form.pictures_dir.data:
            artist.pictures_dir = form.pictures_dir.data
        db.session.commit()
        flash("Вы успешно отредактировали данные художника.")
    return redirect(url_for("admin.admin"))


@blueprint.route("/picture_edit/<int:pic_id>", methods=["POST", "GET"])
def picture_edit(pic_id):
    form = PictureEditForm()
    picture = Picture.query.filter_by(id=pic_id).first()
    art_list = Artist.query.all()
    form.artist_id.choices = [(a.id, a.name) for a in art_list]
    if (picture.artist_id, picture.artist.name) in form.artist_id.choices:
        form.artist_id.choices.remove((picture.artist_id, picture.artist.name))
        form.artist_id.choices.insert(0, (picture.artist_id, picture.artist.name))
    return render_template("admin/picture_edit.html", form=form, picture=picture)


@blueprint.route("/picture_editing/<int:pic_id>", methods=["POST", "GET"])
def picture_editing(pic_id):
    form = PictureEditForm()
    picture = Picture.query.filter_by(id=pic_id).first()
    if form.is_submitted:
        if form.title.data:
            picture.title = form.title.data
        if form.text.data:
            picture.text = form.text.data
        if form.img.data:
            picture.img = form.img.data
        if form.year.data:
            picture.year = form.year.data
        if form.artist_id.data != picture.artist_id:
            picture.artist_id = form.artist_id.data
        if form.size.data:
            picture.size = form.size.data
        if form.price.data:
            picture.price = form.price.data
        db.session.commit()
        flash("Вы успешно отредактировали данные картины.")
    return redirect(url_for("admin.admin"))
