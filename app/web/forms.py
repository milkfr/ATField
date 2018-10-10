from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from ..models.web import Plugin, Application


class ApplicationUpdateForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 500)])
    plugin = SelectMultipleField("需要使用的插件", coerce=str)
    submit = SubmitField("提交")

    def __init__(self):
        super(ApplicationUpdateForm, self).__init__()
        self.plugin.choices = [(plugin.id, plugin.__repr__()) for plugin in Plugin.query.all()]


class PackageUpdateForm(FlaskForm):
    application = StringField("应用", render_kw={"disabled": "disabled"})
    entrance = StringField("入口", render_kw={"disabled": "disabled"})
    path = StringField("路径", render_kw={"disabled": "disabled"})
    method = StringField("方式", render_kw={"disabled": "disabled"})
    status = IntegerField("状态码", validators=[DataRequired()])
    request = StringField("请求", validators=[DataRequired()])
    response = StringField("响应", validators=[DataRequired()])
    remarks = StringField("备注", validators=[DataRequired()])
    submit = SubmitField("提交")

    def __init__(self):
        super(PackageUpdateForm, self).__init__()


class PluginUpdateForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 500)])
    content = StringField("内容", validators=[DataRequired()])
    application = SelectMultipleField("使用的应用", coerce=str)
    submit = SubmitField("提交")

    def __init__(self):
        super(PluginUpdateForm, self).__init__()
        self.application.choices = [(application.id, application.__repr__()) for application in Application.query.all()]
