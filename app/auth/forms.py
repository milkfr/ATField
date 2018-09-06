from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from ..models.auth import Role, Permission


class LoginForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("密码", validators=[DataRequired(), Length(6, 12)])
    submit = SubmitField("登录")


class UserUpdateForm(FlaskForm):
    name = StringField("用户名", render_kw={"disabled": "disabled"})
    department = StringField("部门", render_kw={"disabled": "disabled"})
    role = SelectMultipleField("角色", coerce=str)
    submit = SubmitField("提交")

    def __init__(self, user):
        super(UserUpdateForm, self).__init__()
        self.role.choices = [(role.id, role.__repr__()) for role in Role.query.filter(or_(
            Role.department == "特权", Role.department == user.department)).order_by(Role.department).all()]

    # def validate_department(self, field):
    #     pass
    #
    # def validate_role_list(self, field):


class RoleUpdateForm(FlaskForm):
    name = StringField("角色名", render_kw={"disabled": "disabled"})
    department = StringField("部门", render_kw={"disabled": "disabled"})
    permission = SelectMultipleField("权限", coerce=str)
    submit = SubmitField("提交")

    def __init__(self):
        super(RoleUpdateForm, self).__init__()
        self.permission.choices = [(permission.id, permission.__repr__()) for permission in Permission.query.all()]
