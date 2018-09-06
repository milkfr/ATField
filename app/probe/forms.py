from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length
from ..models.probe import Host, Service, Domain


class HostForm(FlaskForm):
    ip = StringField("IP", render_kw={"disabled": "disabled"})
    status = StringField("状态", render_kw={"disabled": "disabled"})
    service = SelectMultipleField("服务", coerce=str, render_kw={"disabled": "disabled"})
    domain = SelectMultipleField("域名", coerce=str, render_kw={"disabled": "disabled"})
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 50)])
    submit = SubmitField("提交")

    def __init__(self, host_id):
        super(HostForm, self).__init__()



class ServiceForm(FlaskForm):
    port = IntegerField("端口", render_kw={"disabled": "disabled"})
    tunnel = StringField("通道", render_kw={"disabled": "disabled"})
    protocol = StringField("协议", render_kw={"disabled": "disabled"})
    state = StringField("状态", render_kw={"disabled": "disabled"})
    host = StringField("主机", render_kw={"disabled": "disabled"})
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 50)])

    def __init__(self, service_id):
        super(ServiceForm, self).__init__()



class DomainForm(FlaskForm):
    host = StringField("主机", render_kw={"disabled": "disabled"})
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 50)])

    def __init__(self, domain_id):
        super(DomainForm, self).__init__()
