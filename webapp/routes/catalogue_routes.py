from flask import Blueprint, redirect, render_template, url_for  # , flash

from webapp.functions.decorators import get_artist_names
from webapp.models.catalogue_models import Artist, Product

blueprint = Blueprint("catalogue", __name__, url_prefix="/catalogue")


@blueprint.route("/artist")
def artist():
    id = 11
    artist = Artist.query.filter_by(id=id).first()
    name = artist.name
    photo = f"artist/{artist.photo_url}"
    text = artist.text
    return render_template("catalogue/artists.html", name=name, text=text, photo=photo)


@blueprint.route("/album")
def album():
    choices, form, names = get_artist_names()
    form.artist_id.choices = choices
    pictures_list = Product.query.all()
    # pictures_list = sorted(pictures_list, key=lambda pic: pic.year) Сортировка по году
    return render_template(
        "catalogue/album.html", form=form, pictures_list=pictures_list, names=names
    )


@blueprint.route("/album_filter", methods=["POST", "GET"])
def album_filter():
    choices, form, names = get_artist_names()
    form.artist_id.choices = choices
    if form.is_submitted():
        print(form.artist_id.data)
        if form.artist_id.data == "placeholder":
            pictures_list = Product.query.all()
        else:
            pictures_list = Product.query.filter_by(artist_id=form.artist_id.data)
    return render_template(
        "catalogue/album.html", form=form, pictures_list=pictures_list, names=names
    )


@blueprint.route("/slider/<int:pic_id>")
def slider(pic_id):
    choices, form, names = get_artist_names()
    picture = Product.query.filter(Product.id == pic_id).first()
    if not picture:
        return redirect(url_for("catalogue.album"))
    return render_template("catalogue/slider.html", pic=picture, names=names)


@blueprint.route("/slider/try")
def slider_try():
    choices, form, names = get_artist_names()
    pictures_list = Product.query.all()
    return render_template(
        "catalogue/slider_try.html", pictures_list=pictures_list, names=names
    )
