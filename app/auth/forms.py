from flask import current_app
from flask_wtf import Form
from wtforms import ValidationError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired(), Email(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 12)])
    submit = SubmitField("Login")

    def validate_username(self, field):
        if field.data != "123@123.com":  # current_app.config["Username"]:
            raise ValidationError("Error username!")

    def validate_password(self, field):
        if field.data != "123456":  # current_app.config["PASSWORD"]:
            raise ValidationError("Error password!")
