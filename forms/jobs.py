from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Название', validators=[DataRequired()])
    work_size = IntegerField('Время на работу (в часах)', validators=[DataRequired()])
    collaborators = StringField('Участники (ФИ через запятую)', validators=[DataRequired()])
    is_finished = BooleanField('Уже выполнена')
    submit = SubmitField('ОК')
