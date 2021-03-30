from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Звание', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])

    submit = SubmitField('Зарегистрироваться')
