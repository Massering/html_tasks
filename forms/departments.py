from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    members = StringField('Участники (ФИ через запятую)', validators=[DataRequired()])
    submit = SubmitField('OK')
