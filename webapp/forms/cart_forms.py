from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    address = StringField(
        "Адрес доставки:",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Оформить", render_kw={"class": "btn btn-primary"})
