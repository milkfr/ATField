from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField


class TaskInfoForm(FlaskForm):
    func_type = StringField("类型", render_kw={"disabled": "disabled"})
    time_type = StringField("时间类型", render_kw={"disabled": "disabled"})
    start_time = DateTimeField("开始时间", render_kw={"disabled": "disabled"})
    end_time = DateTimeField("结束时间", render_kw={"disabled": "disabled"})
    status = StringField("状态", render_kw={"disabled": "disabled"})
    description = StringField("描述", render_kw={"disabled": "disabled"})
    targets = StringField("目标", render_kw={"disabled": "disabled"})
    result = StringField("结果", render_kw={"disabled": "disabled"})

    def __init__(self):
        super(TaskInfoForm, self).__init__()
