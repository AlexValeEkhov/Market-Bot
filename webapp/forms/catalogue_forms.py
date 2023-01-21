from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ArtistForm(FlaskForm):
    name = StringField(
        "Имя художника",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    text = TextAreaField(
        "О художнике",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    photo_url = FileField(
        "Фотография",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class PictureForm(FlaskForm):
    title = StringField(
        "Название картины",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    price = StringField(
        "Цена", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    text = TextAreaField(
        "Описание", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    picture_url = FileField(
        "Файл изображения",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    year = StringField(
        "Год", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    artist_id = SelectField(
        'Художник',
        render_kw={"class": "form-control"},
    )
    size = StringField(
        "Размер", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class FilterByArtistForm(FlaskForm):
    artist_id = SelectField(
        'Выбрать художника',
        render_kw={"class": "form-control"},)
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
