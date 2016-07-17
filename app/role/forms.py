# -*- coding: utf-8 -*-


from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RoleForm(Form):
    department = StringField("Department", validators=[DataRequired(), Length(1, 64)])
    name = StringField("name", validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField("Submit")
