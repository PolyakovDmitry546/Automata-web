from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired(), Length(1, 100)])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(3, 100)])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterFrom(FlaskForm):
    login = StringField(validators=[DataRequired(), Length(1, 100)])
    name = StringField(validators=[DataRequired(), Length(1, 100)])
    surname = StringField(validators=[DataRequired(), Length(1, 100)])
    password = PasswordField("Пароль: ", validators=[DataRequired(),
     Length(3, 100, message="Короткий пароль")])
    password2 = PasswordField("Пароль: ", validators=[DataRequired(),
     Length(3, 100, message="Короткий пароль"),
     EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField("Зарегистрироваться")