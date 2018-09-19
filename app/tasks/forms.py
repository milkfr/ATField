from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, Length
from ..models.tasks import Task


class TaskNewForm(FlaskForm):
    func_type = SelectField("类型", coerce=str)
    command = StringField("命令", validators=[DataRequired(), Length(0, 500)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 500)])
    next = SubmitField("下一步")

    def __init__(self):
        super(TaskNewForm, self).__init__()
        self.func_type.choices = [(func_type, func_type) for func_type in Task.FUNC_TYPES]


class TaskTargetForm(FlaskForm):
    func_type = StringField("类型", render_kw={"readonly": "true"})
    command = StringField("命令", render_kw={"readonly": "true"})
    description = StringField("描述", render_kw={"readonly": "true"})
    targets = SelectMultipleField("目标", coerce=str)
    submit = SubmitField("提交")

    def __init__(self):
        super(TaskTargetForm, self).__init__()


class TaskInfoForm(FlaskForm):
    func_type = StringField("类型", render_kw={"disabled": "disabled"})
    time_type = StringField("时间类型", render_kw={"disabled": "disabled"})
    start_time = DateTimeField("开始时间", render_kw={"disabled": "disabled"})
    end_time = DateTimeField("结束时间", render_kw={"disabled": "disabled"})
    status = StringField("状态", render_kw={"disabled": "disabled"})
    command = StringField("命令", render_kw={"disabled": "disabled"})
    description = StringField("描述", render_kw={"disabled": "disabled"})
    targets = StringField("目标", render_kw={"disabled": "disabled"})
    result = StringField("结果", render_kw={"disabled": "disabled"})

    def __init__(self):
        super(TaskInfoForm, self).__init__()
