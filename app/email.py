from flask import current_app, render_template
from flask_mail import Message
from . import mail, celery
import json


@celery.task
def send_async_email(temp):
    app = current_app._get_current_object()
    subject = temp["body"]
    to = temp["to"]
    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + ' ' + subject,
                  sender=app.config["MAIL_SENDER"], recipients=[to])
    msg.body = temp["body"]
    msg.html = temp["html"]
    mail.send(msg)


def send_email(to, subject, template, **kwargs):
    temp = {
        "to": to,
        "subject": subject,
        "body": render_template(template + ".txt", **kwargs),
        "html": render_template(template + ".html", **kwargs),
    }
    send_async_email.delay(temp)
