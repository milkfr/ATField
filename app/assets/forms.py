from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length


class HostUpdateForm(FlaskForm):
    ip = StringField("IP", render_kw={"disabled": "disabled"})
    status = StringField("状态", render_kw={"disabled": "disabled"})
    service = SelectMultipleField("服务", coerce=str, render_kw={"disabled": "disabled"})
    domain = SelectMultipleField("域名", coerce=str, render_kw={"disabled": "disabled"})
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 50)])
    submit = SubmitField("提交")

    def __init__(self, host):
        super(HostUpdateForm, self).__init__()
        self.service.choices = [(service.id, service.__repr__()) for service in host.services]
        self.domain.choices = [(domain.id, domain.__repr__()) for domain in host.domain_list]


class ServiceUpdateForm(FlaskForm):
    port = IntegerField("端口", render_kw={"disabled": "disabled"})
    tunnel = StringField("通道", render_kw={"disabled": "disabled"})
    protocol = StringField("协议", render_kw={"disabled": "disabled"})
    state = StringField("状态", render_kw={"disabled": "disabled"})
    host = StringField("主机", render_kw={"disabled": "disabled"})
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 50)])
    submit = SubmitField("提交")

    def __init__(self):
        super(ServiceUpdateForm, self).__init__()


class DomainUpdateForm(FlaskForm):
    host = SelectMultipleField("主机", coerce=str, render_kw={"disabled": "disabled"})
    name = StringField("名称", validators=[DataRequired(), Length(1, 50)])
    description = StringField("描述", validators=[DataRequired(), Length(0, 50)])
    submit = SubmitField("提交")

    def __init__(self, domain):
        super(DomainUpdateForm, self).__init__()
        self.host.choices = [(host.id, host.__repr__()) for host in domain.host_list]
