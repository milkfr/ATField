# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models.users import User


class RegistrationForm(Form):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("password2", message="密码必须相同")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.get_user_from_email(field.data) is not None:
            raise ValidationError("Email already register")


class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
