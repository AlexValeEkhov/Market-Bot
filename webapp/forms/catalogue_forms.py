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
    img = FileField(
        "Фотография",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    pictures_dir = StringField(
        "Имя каталога для картин",
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
        "Описание", render_kw={"class": "form-control"}
    )
    img = FileField(
        "Файл изображения",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    year = StringField(
        "Год", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    artist_id = SelectField(
        "Художник",
        render_kw={"class": "form-control"},
    )
    size = StringField(
        "Размер", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class FilterByArtistForm(FlaskForm):
    artist_id = SelectField(
        "Выбрать художника",
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Выбрать", render_kw={"class": "btn btn-primary"})


class ArtistEditForm(FlaskForm):
    name = StringField(
        "Имя художника",
        render_kw={"class": "form-control"},
    )
    text = TextAreaField(
        "О художнике",
        render_kw={"class": "form-control"},
    )
    img = FileField(
        "Фотография",
        render_kw={"class": "form-control"},
    )
    pictures_dir = StringField(
        "Имя каталога для картин",
        render_kw={"class": "form-control"},
    )

    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class PictureEditForm(FlaskForm):
    title = StringField(
        "Название картины",
        render_kw={"class": "form-control"},
    )
    price = StringField(
        "Цена", render_kw={"class": "form-control"}
    )
    text = TextAreaField(
        "Описание", render_kw={"class": "form-control"}
    )
    img = FileField(
        "Файл изображения",
        render_kw={"class": "form-control"},
    )
    year = StringField(
        "Год", render_kw={"class": "form-control"}
    )
    artist_id = SelectField(
        "Художник",
        render_kw={"class": "form-control"},
    )
    size = StringField(
        "Размер", render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
