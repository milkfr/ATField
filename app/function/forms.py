# -*- coding: utf-8 -*-


from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class FunctionForm(Form):
    part = StringField("Part", validators=[DataRequired(), Length(1, 64)])
    name = StringField("name", validators=[DataRequired(), Length(1, 64)])
    permission = StringField("Permission", validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField("Submit")
