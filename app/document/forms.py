# -*- coding: utf-8 -*-


from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class DocumentForm(Form):
    type = StringField("type", validators=[DataRequired(), Length(1, 64)])
    text = StringField("text", validators=[DataRequired()])
    submit = SubmitField()
