from functools import wraps

from flask import current_app, flash, redirect, request, url_for
from flask_login import config, current_user

from webapp.forms.catalogue_forms import FilterByArtistForm
from webapp.models.catalogue_models import Artist


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash('Эта страница доступна только админам')
            return redirect(url_for('main'))
        return func(*args, **kwargs)
    return decorated_view


def get_artist_names():
    art_list = Artist.query.all()
    form = FilterByArtistForm()
    choices = [(g.id, g.name) for g in art_list]
    choices.insert(0, ("placeholder", "..."))
    return choices, form


def sort_pics_for_slider(pictures_list, pic_id):
    for pic in pictures_list:
        if pic.id == pic_id:
            pictures_list.remove(pic)
            pictures_list.insert(0, pic)
            break
    return pictures_list
