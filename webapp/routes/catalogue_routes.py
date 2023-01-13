from flask import Blueprint, flash, redirect, render_template, url_for

from webapp import db
from webapp.forms.catalogue_forms import ArtistForm, ProductForm
from webapp.models.catalogue_models import Artist, Product

blueprint = Blueprint("catalogue", __name__, url_prefix="/catalogue")

@blueprint.route("/artist")
def artist():
    id = 10
    artist = Artist.query.filter_by(id=id).first()
    name = artist.name
    photo = f"artist/{artist.photo_url}"
    text = artist.text
    return render_template("catalogue/artists.html", name=name, text=text, photo=photo)


@blueprint.route("/album")
def album():
    pictures_list = Product.query.all()
    return render_template("catalogue/album.html", pictures_list=pictures_list)
