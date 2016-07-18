# -*- coding: utf-8 -*-


from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.models.functions import Function
from app.models.roles_functions import RoleFunction


class RoleForm(Form):
    department = StringField("Department", validators=[DataRequired(), Length(1, 64)])
    name = StringField("name", validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField("Submit")


class FunctionAddForm(Form):
    function = SelectField('Function', coerce=int)
    submit = SubmitField("Submit")

    def __init__(self, role_id, *args, **kwargs):
        super(FunctionAddForm, self).__init__(*args, **kwargs)
        self.role_id = role_id
        all_functions = Function.get_published_function()
        except_functions = RoleFunction.get_function_by_role_id(role_id)
        except_functions_id = [func.get('function_id') for func in except_functions]
        functions = [function for function in all_functions if function.id not in except_functions_id]
        self.function.choices = [(function.id, function.part + ' ' + function.name)
                                 for function in functions]

