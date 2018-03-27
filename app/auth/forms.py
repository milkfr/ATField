from flask import current_app
from flask_wtf import Form
from sqlalchemy import or_
from wtforms import ValidationError
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, Length
from ..models.auth import DEPARTMENT, Role, Permission


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


class UserUpdateForm(Form):
    name = StringField("用户名", render_kw={"disabled": "disabled"})
    department = StringField("部门", render_kw={"disabled": "disabled"})
    role = SelectMultipleField("角色", coerce=str)
    submit = SubmitField("提交")

    def __init__(self, user):
        super(UserUpdateForm, self).__init__()
        self.role.choices = [(role.id, role.__repr__()) for role in Role.query.filter(or_(
            Role.department=="特权", Role.department==user.department)).order_by(Role.department).all()]

    # def validate_department(self, field):
    #     pass
    #
    # def validate_role_list(self, field):


class RoleUpdateForm(Form):
    name = StringField("角色名", render_kw={"disabled": "disabled"})
    department = StringField("部门", render_kw={"disabled": "disabled"})
    permission = SelectMultipleField("权限", coerce=str)
    submit = SubmitField("提交")

    def __init__(self, role):
        super(RoleUpdateForm, self).__init__()
        self.permission.choices = [(permission.id, permission.__repr__()) for permission in Permission.query.all()]
