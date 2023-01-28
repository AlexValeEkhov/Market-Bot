from flask import Blueprint, render_template, request
from flask_login import current_user

from webapp import db
from webapp.forms.catalogue_forms import FilterByArtistForm
from webapp.functions.decorators import get_artist_names, sort_pics_for_slider
from webapp.models.catalogue_models import Artist, Filter, Picture

blueprint = Blueprint("catalogue", __name__, url_prefix="/catalogue")


@blueprint.route("/artist-list")
def artist_list():
    artist_list = Artist.query.all()
    return render_template("catalogue/artists.html", artist_list=artist_list)


@blueprint.route("/artist/<int:artist_id>")
def artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    return render_template("catalogue/artist.html", artist=artist)


@blueprint.route("/album", methods=["POST", "GET"])
def album_filter():
    filter = Filter.query.filter_by(user_id=current_user.id).first()
    if filter:
        db.session.delete(filter)  # сделать фильтр НЕ через БД!
        db.session.commit()
    choices, form = get_artist_names()
    form = FilterByArtistForm(request.args)
    form.artist_id.choices = choices
    pictures_list = Picture.query.all()
    if form.validate():
        if form.artist_id.data == "placeholder":
            pictures_list = Picture.query.all()
        else:
            pictures_list = Picture.query.filter_by(artist_id=form.artist_id.data)
            filter = Filter(user_id=current_user.id, artist_id=form.artist_id.data)
            db.session.add(filter)
            db.session.commit()
    return render_template("catalogue/album.html", form=form, pictures_list=pictures_list)


@blueprint.route("/slider/<int:pic_id>", methods=["POST", "GET"])
def slider(pic_id):
    filter = Filter.query.filter_by(user_id=current_user.id).first()
    if filter:
        pictures_list = Picture.query.filter_by(artist_id=filter.artist_id).all()
        pictures_list = sort_pics_for_slider(pictures_list, pic_id)
    else:
        pictures_list = Picture.query.all()
        pictures_list = sort_pics_for_slider(pictures_list, pic_id)

    return render_template("catalogue/slider_try.html", pictures_list=pictures_list)
